import requests
import streamlit as st


API_URL = (
    "http://127.0.0.1:8000/inventory"
)


st.title(
    "Inventory LangGraph Agent"
)


question = st.text_input(
    "Enter inventory question",
    placeholder=
        "Check stock for battery_pack"
)


if st.button("Ask Agent"):

    response = requests.post(
        API_URL,
        json={
            "question": question
        }
    )

    result = response.json()

    st.subheader(
        "Inventory Response"
    )

    st.write(
        result["answer"]
    )