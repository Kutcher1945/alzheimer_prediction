import streamlit as st
import requests
import json

# API-ключ и эндпоинт Mistral AI
API_KEY = "QqkMxELY0YVGkCx17Vya04Sq9nGvCahu"
ENDPOINT = "https://api.mistral.ai/v1/chat/completions"
BASE_PROMPT = "Ты полезный и дружелюбный ассистент медицинский ассистент. Отвечай кратко и понятно."

def chat_bot():
    st.title("Чат-бот")
    
    # Хранение сообщений
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "Привет! Чем могу помочь?"}]
    
    # Отображение истории чата
    for message in st.session_state["messages"]:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Функция для отправки запроса к Mistral API
    def generate_response(prompt):
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": "open-mistral-nemo",
            "temperature": 0.3,
            "top_p": 1,
            "max_tokens": 500,
            "messages": [
                {"role": "system", "content": BASE_PROMPT},
                {"role": "user", "content": prompt},
            ],
        }
        response = requests.post(ENDPOINT, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            return response.json().get("choices", [{}])[0].get("message", {}).get("content", "Ошибка при получении ответа")
        return "Ошибка при обращении к API"
    
    # Ввод сообщения пользователем
    if user_input := st.chat_input("Введите сообщение..."):
        st.session_state["messages"].append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)
        
        # Генерация ответа
        with st.chat_message("assistant"):
            with st.spinner("Генерация ответа..."):
                response = generate_response(user_input)
                st.write(response)
        
        # Добавление ответа в историю сообщений
        st.session_state["messages"].append({"role": "assistant", "content": response})

