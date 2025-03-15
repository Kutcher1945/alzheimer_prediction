import streamlit as st
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from PIL import Image, ImageOps
import cv2
import os

# Отключаем GPU, если он не поддерживается
try:
    tf.config.experimental.set_visible_devices([], "GPU")
except:
    pass

def eeg_alz():
    st.title("🧠 Прогнозирование болезни Альцгеймера")
    
    # Загрузка и отображение изображения
    image_path = 'assets/images/image_presentation.jpg'
    if os.path.exists(image_path):
        image = Image.open(image_path)
        st.image(image, caption='МРТ-сканирование мозга')

    st.subheader("🔍 Определение диагноза на основе МРТ-изображения пациента")
    st.write("Это приложение использует модель **CNN** для анализа изображений.")

    # Пути к моделям
    model_paths = ["model/model_kaggle_alzheimer.h5", "model/model_kaggle_alzheimer.keras"]

    # Проверка наличия модели и загрузка
    model = None
    for path in model_paths:
        if os.path.exists(path):
            try:
                model = load_model(path)
                st.success(f"✅ Загружена модель: `{path}`")
                break
            except Exception as e:
                st.warning(f"⚠ Ошибка загрузки модели `{path}`: {e}")

    if model is None:
        st.error("❌ Файл модели не найден. Убедитесь, что модель загружена в папку `model/`.")
        return

    # Загрузка файла изображения
    file = st.file_uploader("📂 Пожалуйста, загрузите МРТ-изображение.", type=["jpg", "png"])

    def import_and_predict(image_data, model):
        try:
            size = (128, 128)  # Размер входного изображения
            image = ImageOps.fit(image_data, size, Image.Resampling.LANCZOS)  # Улучшенное масштабирование
            image = np.asarray(image)

            # Преобразование изображения в RGB (на случай ч/б изображений)
            if len(image.shape) == 2:
                image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
            elif image.shape[-1] == 4:  # Если изображение в формате RGBA, удаляем альфа-канал
                image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)

            img_reshape = image[np.newaxis, ...]  # Добавляем размерность batch
            prediction = model.predict(img_reshape)
            return prediction
        except Exception as e:
            st.error(f"❌ Ошибка обработки изображения: {e}")
            return None

    if file:
        image = Image.open(file)
        predictions = import_and_predict(image, model)

        if predictions is not None:
            class_names = ["Лёгкая деменция", "Умеренная деменция", "Без деменции", "Очень лёгкая деменция"]
            predicted_class = class_names[np.argmax(predictions)]
            st.success(f"🧠 **Предсказанный диагноз пациента:** {predicted_class}")
            st.image(image, caption="📷 Загруженное изображение")
