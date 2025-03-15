import base64
import streamlit as st
from config import *
from streamlit_pages._home_page import home_page
from streamlit_pages._predict_alzheimer import prediction_page
# from streamlit_pages._latest_news import news_page
# from streamlit_pages._team_members import team_members  
from streamlit_pages._chat_page import chat_bot
from streamlit_pages._eeg_alz import eeg_alz

# НАСТРОЙКА КОНФИГУРАЦИИ СТРАНИЦЫ
st.set_page_config(
    page_title="Система прогнозирования болезни Альцгеймера",
    page_icon=":brain:",
)

st.markdown(f"<style>{CSS}</style>", unsafe_allow_html=True)

def set_page_background(png_file):
    @st.cache_data()
    def get_base64_of_bin_file(bin_file):
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = f'''
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{bin_str}");
            }}
        </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)

# set_page_background(BACKGROUND) 

# ОСНОВНОЕ ПРИЛОЖЕНИЕ STREAMLIT
st.sidebar.image(SIDE_BANNER)

st.sidebar.title("Система прогнозирования болезни Альцгеймера")
app_mode = st.sidebar.selectbox(
    "Пожалуйста, выберите раздел нашего веб-сайта:",
    ["Главная", "Прогнозирование Альцгеймера", "Чат-бот", "Прогнозирование по МРТ - ЭЭГ"],
)

st.sidebar.write("""
# Отказ от ответственности
Прогнозы, предоставляемые этой системой, носят исключительно информационный характер. Для точного диагноза и рекомендаций обратитесь к врачу.

# Контакт
По вопросам обращайтесь по [почте](mailto:adilan.akhramovich@gmail.com).
""")


def main():
    if app_mode == "Главная":
        home_page()
    if app_mode == "Прогнозирование Альцгеймера":
        prediction_page()
    if app_mode == "Чат-бот":
        chat_bot()
    # if app_mode == "Последние новости":
    #     news_page()
    # if app_mode == "Члены команды":
    #     team_members()
    if app_mode == "Прогнозирование по МРТ - ЭЭГ":
        eeg_alz()


if __name__ == "__main__":
    main()
