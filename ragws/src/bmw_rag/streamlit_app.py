import requests
import streamlit as st

st.title("PDF and DOCX RAG with Amazon Nova")

question = st.text_input("Ask a question")

if st.button("Ask") and question:
    response = requests.post(
        "http://127.0.0.1:8000/ask",
        json={"question": question},
        timeout=300,
    )

    st.subheader("Answer")
    st.write(response.json()["answer"])