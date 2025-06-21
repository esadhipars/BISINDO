import streamlit as st
import tempfile
import imageio
import cv2
import mediapipe as mp
import numpy as np

st.set_page_config(page_title="Pembaca Bahasa Isyarat", layout="centered")

st.title("📹 Pembaca Video Bahasa Isyarat")
st.write("Unggah video berisi bahasa isyarat, nanti akan ditampilkan dan dideteksi tangan.")

uploaded_file = st.file_uploader("Upload Video", type=["mp4", "mov", "avi"])

if uploaded_file is not None:
    # Simpan video ke file sementara
    tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    tfile.write(uploaded_file.read())

    # Tampilkan video asli
    st.video(tfile.name)

    # Buka video dengan OpenCV
    cap = cv2.VideoCapture(tfile.name)
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2)

    success, frame = cap.read()
    if success:
        # Proses frame pertama
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(image_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # Tampilkan frame dengan deteksi
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        st.image(frame_rgb, caption="Deteksi Tangan pada Frame Pertama")

    cap.release()
    hands.close()
