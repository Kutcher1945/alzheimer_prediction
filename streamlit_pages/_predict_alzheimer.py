import time
import joblib
import pandas as pd
from config import *
import streamlit as st

def prediction_page():
    def convert_to_one_hot(selected_category, all_categories):
            one_hot = [True if category == selected_category else False for category in all_categories]
            for value in one_hot:
                user_input.append(value)

    def predict_alzheimer(input_data):
        loaded_model = joblib.load('model/alzheimer_model.pkl')
        predictions = loaded_model.predict(input_data)

        return predictions

    st.title("Информация о пациенте")

    age = st.number_input("Возраст", min_value=0, max_value=122, step=1, value=65)
    gender = st.selectbox("Пол", ("Мужской", "Женский"))
    education = st.number_input("Годы образования", min_value=0, value=12)

    st.write("<br>", unsafe_allow_html=True)

    st.header("Демографические данные")
    ethnicity = st.radio("Этническая принадлежность", ("Испано-/Латиноамериканец", "Не испано-/Латиноамериканец", "Неизвестно"))
    race_cat = st.radio("Расовая категория", ("Белый", "Черный", "Азиат"))

    st.write("<br>", unsafe_allow_html=True)

    st.header("Генетическая информация")
    apoe_allele_type = st.selectbox("Тип аллеля APOE", ["APOE4_0", "APOE4_1", "APOE4_2"])
    apoe_genotype = st.selectbox("Генотип APOE4", ("2,2", "2,3", "2,4", "3,3", "3,4", "4,4"))
    imputed_genotype = st.radio("Импутированный генотип", ("Истина", "Ложь"))

    st.header("Когнитивная оценка")
    mmse = st.number_input("Оценка MMSE", min_value=0, max_value=30, step=1)

    st.write("<br>", unsafe_allow_html=True)
    predict_button = st.button("Сделать прогноз")
    st.write("")

    loading_bar = st.empty()
    if age and education and mmse and apoe_genotype and race_cat and gender and apoe_allele_type and imputed_genotype and ethnicity and predict_button:
        loading_bar.write("Спасибо за ввод информации о пациенте.")
        progress_text = "Пожалуйста, подождите, идёт прогнозирование клинического состояния..."
        my_bar = loading_bar.progress(0, text=progress_text)

        for percent_complete in range(100):
            time.sleep(0.02)
            my_bar.progress(percent_complete + 1, text=progress_text)

        user_input = [age, education, mmse]

        convert_to_one_hot("PTRACCAT_" + race_cat, PTRACCAT_CATEGORIES)
        convert_to_one_hot("APOE Genotype_" + apoe_genotype, APOE_CATEGORIES)
        convert_to_one_hot("PTETHCAT_" + ethnicity, PTHETHCAT_CATEGORIES)
        convert_to_one_hot(apoe_allele_type, APOE4_CATEGORIES)
        convert_to_one_hot("PTGENDER_" + gender, PTGENDER_CATEGORIES)
        convert_to_one_hot("imputed_genotype_" + imputed_genotype, IMPUTED_CATEGORIES)

        data = pd.DataFrame([user_input])
        predicted_condition = predict_alzheimer(data)
        
        loading_bar.empty()

        st.write("")
        st.write("")
        st.write("### Прогнозируемое клиническое состояние:", unsafe_allow_html=True)
        st.write(f"## <b>{ABBREVIATION[predicted_condition[0]]}</b> ({predicted_condition[0]})", unsafe_allow_html=True)
        st.write(f"{CONDITION_DESCRIPTION[predicted_condition[0]]}", unsafe_allow_html=True)
