import requests
import difflib

JSON_URL = "https://raw.githubusercontent.com/pan756/bypass-linkday.xyz/refs/heads/main/keywords.json"

def normalize_text(text):
    replacements = (
        ("áàảãạăắằẳẵặâấầẩẫậ", "a"),
        ("éèẻẽẹêếềểễệ", "e"),
        ("íìỉĩị", "i"),
        ("óòỏõọôốồổỗộơớờởỡợ", "o"),
        ("úùủũụưứừửữự", "u"),
        ("ýỳỷỹỵ", "y"),
        ("đ", "d"),
        (".", ""), (",", ""), ("?", ""), ("!", ""), (":", ""), (" ", "")
    )
    text = text.lower()
    for chars, rep in replacements[:7]:
        for ch in chars:
            text = text.replace(ch, rep)
    for char, rep in replacements[7:]:
        text = text.replace(char, rep)
    return text

def load_keywords(url):
    response = requests.get(url)
    response.raise_for_status()
    raw_data = response.json()

    data = {}
    display_map = {}
    for original_key, code in raw_data.items():
        norm_key = normalize_text(original_key)
        data[norm_key] = code
        display_map[norm_key] = original_key
    return data, display_map

def find_code(keyword_input, data, display_map):
    norm_input = normalize_text(keyword_input)

    if norm_input in data:
        print(f"Mã code: {data[norm_input]}")
    else:
        suggestion = difflib.get_close_matches(norm_input, data.keys(), n=1, cutoff=0.6)
        if suggestion:
            matched_key = suggestion[0]
            print(f"Ko tìm thấy từ khóa chính xác, có phải m muốn tìm: \"{display_map[matched_key]}\"?")
            print(f"Mã code: {data[matched_key]}")
        else:
            print("Không tìm thấy mã code cho từ khóa m đã nhập. Chắc do danh sách keywords thiếu đấy đổi từ khóa khác đi. Để update sau 🤡")
def main():
    try:
        data, display_map = load_keywords(JSON_URL)
        keyword_input = input("Vui lòng sao chép và dán từ khóa cần tìm vào đây: ").strip()
        find_code(keyword_input, data, display_map)
    except requests.exceptions.RequestException:
        print("Lỗi kết nối: Không thể tải danh sách từ khóa.")
    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")

if __name__ == "__main__":
    main()
