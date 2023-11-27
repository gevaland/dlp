import streamlit as st
import requests


def send_video_to_fastapi(video_file):
    url = "http://localhost:8600/upload_video/"
    files = {"video": video_file}
    response = requests.post(url, files=files)
    return response


def main():
    st.title("Загрузка и обработка видео, содержащего дорожные знаки")

    video_file = st.file_uploader("Выберите видео-файл", type=["mp4", "avi"])

    if video_file is not None:
        st.success(
            "Видео-файл успешно отправлен на FastAPI! Ожидайте обработки!"
        )
        response = send_video_to_fastapi(video_file)
        if response.status_code == 200:
            st.success("Видео обработано!")
            st.subheader("Processed Video:")
            st.video(response.content)
        else:
            st.error("Произошла ошибка при отправке видео-файла на FastAPI.")


if __name__ == "__main__":
    main()
