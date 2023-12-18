import streamlit as st
import requests

def send_text_matching(uploaded_file, option):
    url = f"http://localhost:8600/matching/{option}"
    files = {"file": uploaded_file}
    response = requests.post(url, files=files)
    return response


def main():
    st.title("Матчинг вакансий и резюме")

    option = st.radio("Что Вы хотите загрузить?", ("Resume", "Job"))

    uploaded_file = st.file_uploader(
        f"Загрузите {option.lower()}", type=["txt"]
    )

    if uploaded_file is not None:
        response = send_text_matching(uploaded_file, option)

        files = response.json()["files"]
        for file in files:
            with open(file, "r") as f:
                file_name = file.split("/")[-1]
                file_name = file_name[: file_name.rfind(".")]
                st.markdown(f"{file_name}")
                content = f.read()
                st.code(content)


if __name__ == "__main__":
    main()
