import openai

def generate_summary(text: str, max_tokens: int = 500) -> str:
    """
    Tạo tóm tắt ngắn gọn cho một đoạn văn bản.
    :param text: Văn bản cần tóm tắt
    :param max_tokens: Số token tối đa của tóm tắt
    :return: Chuỗi tóm tắt
    """
    if not text.strip():
        return "(Không có nội dung để tóm tắt)"

    prompt = f"Write a concise summary of the following text:\n\n{text}"
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=0.3,
        )
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        return f"(Lỗi khi tạo tóm tắt: {e})"
