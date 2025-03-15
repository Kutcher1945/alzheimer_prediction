import streamlit as st
import tensorflow.keras as keras
import numpy as np
from tensorflow.keras.models import load_model
from PIL import Image, ImageOps
import cv2

def eeg_alz():
    image = Image.open('assets/images/image_presentation.jpg')
    st.image(image, caption='МРТ-сканирование мозга')
    
    st.header("Прогнозирование болезни Альцгеймера")
    st.subheader("Прогнозирует диагноз болезни Альцгеймера на основе МРТ-изображения пациента.")
    st.write("Это приложение использует модель CNN.")
    
    #model1 = load_model("alz_model.h5")
    
    # Загрузка модели в Jupyter
    model2 = load_model("model/model_kaggle_alzheimer.h5")
    
    file = st.file_uploader("Пожалуйста, загрузите МРТ-изображение.", type=["jpg", "png"])
    
    def import_and_predict(image_data, model2):
        size = (128, 128) # size = (224,224) для model1
        image = ImageOps.fit(image_data, size, Image.ANTIALIAS)
        image = np.asarray(image)
        img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        img_reshape = img[np.newaxis, ...]
        prediction = model2.predict(img_reshape)
        return prediction
    
    if file is None:
        st.text("Файл изображения не загружен.")
    else:
        image = Image.open(file)
        predictions = import_and_predict(image, model2)
        class_names = ["Лёгкая деменция", "Умеренная деменция", "Без деменции", "Очень лёгкая деменция"]
        string = "Предсказанный диагноз пациента: " + class_names[np.argmax(predictions)]
        st.success(string)
        st.image(image)
