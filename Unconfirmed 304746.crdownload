import streamlit as st
import tempfile
import imageio

st.set_page_config(page_title="Pembaca Bahasa Isyarat", layout="centered")

st.title("📹 Pembaca Video Bahasa Isyarat")
st.write("Unggah video berisi bahasa isyarat, nanti akan ditampilkan.")

uploaded_file = st.file_uploader("Upload Video", type=["mp4", "mov", "avi"])

if uploaded_file is not None:
    # Simpan video ke file sementara
    tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    tfile.write(uploaded_file.read())

    # Tampilkan video
    st.video(tfile.name)

    # Ekstrak frame pertama (tanpa cv2)
    try:
        reader = imageio.get_reader(tfile.name)
        frame1 = reader.get_data(0)
        st.image(frame1, caption="Frame Pertama dari Video")
        reader.close()
    except Exception as e:
        st.warning("Gagal membaca frame video: " + str(e))
