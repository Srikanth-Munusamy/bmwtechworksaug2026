import requests
import streamlit as st

from salesmcp.settings import API_URL


st.set_page_config(
    page_title="Sales MCP Assistant",
    page_icon="📈",
)

st.title("📈 Sales MCP Assistant")

st.caption(
    "Streamlit → FastAPI → Agent → MCP → SQLite"
)

question = st.text_input(
    "Ask a sales question",
    value="List all available products",
)

if st.button("Submit"):

    with st.spinner("Processing..."):

        response = requests.post(
            f"{API_URL}/agent/query",
            json={
                "question": question
            },
            timeout=120,
        )

        if response.status_code == 200:
            result = response.json()

            st.success("Completed")
            st.write(result["answer"])

            with st.expander(
                "MCP tools discovered"
            ):
                st.write(
                    result["available_tools"]
                )

        else:
            st.error(response.text)

    