import requests
import hashlib
import re
from datetime import datetime

def decode_utf16_hex(hex_string):
    bytes_obj = bytes.fromhex(hex_string)
    return bytes_obj.decode('utf-16-be')

def format_date(date_string):
    parts = date_string.split(',')
    if len(parts) >= 6:
        year = int(parts[0]) + 2000  # Assuming 21 -> 2021
        month, day, hour, minute, second = map(int, parts[1:6])
        return f"{year:04d}-{month:02d}-{day:02d} {hour:02d}:{minute:02d}:{second:02d}"
    return date_string

def extract_messages_from_raw_string(raw):
    # Match each full message dictionary in the "messages" array
    message_blocks = re.findall(r'\{(.*?)\}(?=,\s*\{|\s*\]\s*\})', raw, re.DOTALL)
    formatted_messages = []
    for block in message_blocks:
        # Extract fields using regex
        content_match = re.search(r'"content"\s*:\s*"([^"]+)"', block)
        number_match = re.search(r'"number"\s*:\s*"([^"]+)"', block)
        date_match = re.search(r'"date"\s*:\s*"([^"]+)"', block)
        
        content_hex = content_match.group(1) if content_match else ''
        sender = number_match.group(1) if number_match else 'Unknown'
        raw_date = date_match.group(1) if date_match else 'Unknown'
        
        content = decode_utf16_hex(content_hex)
        formatted_date = format_date(raw_date)
        
        formatted_messages.append({
            "date": formatted_date,
            "number": sender,
            "content": content
        })
    return formatted_messages

def get_auth_cookies(router_ip: str, user_password: str) -> dict:
    r_ld = requests.get(
        f"http://{router_ip}/goform/goform_get_cmd_process?isTest=false&cmd=LD",
        cookies={"stok": ""},
        headers={"referer": f"http://{router_ip}/"},
    )
    m = hashlib.sha256()
    m.update(user_password.encode())
    m2 = hashlib.sha256()
    m2.update(f'{m.hexdigest().upper()}{r_ld.json()["LD"]}'.encode())
    pwd = m2.hexdigest().upper()
    
    r_login = requests.get(
        f"http://{router_ip}/goform/goform_set_cmd_process?isTest=false&goformId=LOGIN&password={pwd}",
        cookies={"stok": ""},
        headers={"referer": f"http://{router_ip}/"},
    )
    
    if "result" not in r_login.json() or r_login.json()["result"] != "0":
        raise Exception("Login failed")
    
    return r_login.cookies.get_dict()

def get_latest_sms_messages(router_ip, auth_cookies, n=19) -> list:
    r_data = requests.get(
        f"http://{router_ip}/goform/goform_get_cmd_process?isTest=false&cmd=sms_data_total&page=0&data_per_page=500&mem_store=2&tags=10&order_by=order+by+id+desc",
        cookies=auth_cookies,
        headers={"referer": f"http://{router_ip}/"},
    )
    
    msgs = []
    try:
        data = r_data.json()
        messages = data.get("messages", [])
        for msg in messages:
            content_hex = msg.get("content", "")
            sender = msg.get("number", "Unknown")
            raw_date = msg.get("date", "Unknown")
            try:
                content = decode_utf16_hex(content_hex)
            except Exception:
                content = "(Failed to decode content)"
            formatted_date = format_date(raw_date)
            msgs.append({
                "date": formatted_date,
                "number": sender,
                "content": content
            })
    except Exception:
        # Fallback: parse from raw response string
        msgs = extract_messages_from_raw_string(r_data.text)
    
    latest = msgs[:n]
    latest.reverse()
    
    return latest



def decode_utf16_hex(hex_string):
    bytes_obj = bytes.fromhex(hex_string)
    return bytes_obj.decode('utf-16-be')

def format_date(date_string):
    parts = date_string.split(',')
    if len(parts) >= 6:
        year = int(parts[0]) + 2000  # Assuming 21 -> 2021
        month, day, hour, minute, second = map(int, parts[1:6])
        return f"{year:04d}-{month:02d}-{day:02d} {hour:02d}:{minute:02d}:{second:02d}"
    return date_string

def extract_messages_from_raw_string(raw):
    # Match each full message dictionary in the "messages" array
    message_blocks = re.findall(r'\{(.*?)\}(?=,\s*\{|\s*\]\s*\})', raw, re.DOTALL)

    formatted_messages = []
    for block in message_blocks:
        # Extract fields using regex
        content_match = re.search(r'"content"\s*:\s*"([^"]+)"', block)
        number_match = re.search(r'"number"\s*:\s*"([^"]+)"', block)
        date_match = re.search(r'"date"\s*:\s*"([^"]+)"', block)

        content_hex = content_match.group(1) if content_match else ''
        sender = number_match.group(1) if number_match else 'Unknown'
        raw_date = date_match.group(1) if date_match else 'Unknown'

        content = decode_utf16_hex(content_hex)
        formatted_date = format_date(raw_date)

        formatted_messages.append(
            {"date": formatted_date, "number": sender, "content": content}
        )

    return formatted_messages


def get_auth_cookies(router_ip: str, user_password: str) -> dict:
    r_ld = requests.get(
        f"http://{router_ip}/goform/goform_get_cmd_process?isTest=false&cmd=LD",
        cookies={"stok": ""},
        headers={"referer": f"http://{router_ip}/"},
    )

    m = hashlib.sha256()
    m.update(user_password.encode())
    m2 = hashlib.sha256()
    m2.update(f'{m.hexdigest().upper()}{r_ld.json()["LD"]}'.encode())
    pwd = m2.hexdigest().upper()

    r_login = requests.get(
        f"http://{router_ip}/goform/goform_set_cmd_process?isTest=false&goformId=LOGIN&password={pwd}",
        cookies={"stok": ""},
        headers={"referer": f"http://{router_ip}/"},
    )

    if "result" not in r_login.json() or r_login.json()["result"] != "0":
        raise Exception("Login failed")

    return r_login.cookies.get_dict()


def get_latest_sms_messages(router_ip, auth_cookies, n=19) -> list:
    r_data = requests.get(
        f"http://{router_ip}/goform/goform_get_cmd_process?isTest=false&cmd=sms_data_total&page=0&data_per_page=500&mem_store=2&tags=10&order_by=order+by+id+desc",
        cookies=auth_cookies,
        headers={f"referer": f"http://{router_ip}/"},
    )

    msgs = []
    try:
        data = r_data.json()
        messages = data.get("messages", [])
        for msg in messages:
            content_hex = msg.get("content", "")
            sender = msg.get("number", "Unknown")
            raw_date = msg.get("date", "Unknown")

            try:
                content = decode_utf16_hex(content_hex)
            except Exception:
                content = "(Failed to decode content)"

            formatted_date = format_date(raw_date)
            msgs.append(
                {"date": formatted_date, "number": sender, "content": content}
            )
    except Exception:
        # Fallback: parse from raw response string
        msgs = extract_messages_from_raw_string(r_data.text)

    latest = msgs[:n]
    latest.reverse()
    for m in latest:
        print(f"Date: {m['date']}, From: {m['number']}, Message: {m['content']}")
        print('-' * 50)

    return latest
    
    # json_data = r_data.text
    # messages = json.loads(json_data).get("messages", [])
    

    # if len(messages) > n:
    #     messages = messages[0:n]

    # for msg in messages:
    #     try:
    #         decoded = codecs.decode(msg["content"], "hex").replace(b"\x00", b"")
    #         msg["content"] = decoded.decode("latin-1")
    #     except Exception:
    #         msg["content"] = "(Failed to decode content)"

    # return messages


def main():
    try:
        cookies = get_auth_cookies(ROUTER_IP, ADMIN_PASSWORD)
        sms_list = get_latest_sms_messages(ROUTER_IP, cookies, SMS_COUNT)
        # print(sms_list)

        # print(f"📩 Latest {len(sms_list)} SMS messages:\n")
        # for idx, sms in enumerate(sms_list, 1):
        #     print(f"--- Message {idx} ---")
        #     print(f"📅 Time: {sms.get('date')}")
        #     print(f"📱 From: {sms.get('number')}")
        #     print(f"✉️ Message: {sms.get('content')}\n")

    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
