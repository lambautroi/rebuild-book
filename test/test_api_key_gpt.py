import openai
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key
print("api key : " , api_key)
if not api_key:
    raise ValueError("API key không được tìm thấy. Vui lòng đặt biến môi trường OPENAI_API_KEY.")

try:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Say hello!"}],
        max_tokens=5
    )
    print("API key hoạt động. Phản hồi:", response.choices[0].message.content)
except Exception as e:
    print("Lỗi khi gọi API:", e)