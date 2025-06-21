import gradio as gr
import cv2
import mediapipe as mp
import tempfile
import os

# Inisialisasi model deteksi tangan
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

def detect_hands(video_file):
    temp_video_path = video_file.name

    # Buka video
    cap = cv2.VideoCapture(temp_video_path)
    hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2)
    
    frames = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Konversi warna dan deteksi tangan
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(image)

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        frames.append(frame)

    cap.release()
    hands.close()

    # Simpan hasil video dengan tangan ditandai
    output_path = tempfile.mktemp(suffix=".mp4")
    height, width, _ = frames[0].shape
    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), 10, (width, height))
    for f in frames:
        out.write(f)
    out.release()

    return output_path

# Antarmuka Gradio
demo = gr.Interface(
    fn=detect_hands,
    inputs=gr.Video(type="file"),
    outputs=gr.Video()
)

if __name__ == "__main__":
    demo.launch()
