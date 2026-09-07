import tomllib
from pathlib import Path

import requests
import streamlit as st


# --------------------------------
# Configuration
# --------------------------------

ROOT_DIR = (
    Path(__file__)
    .resolve()
    .parents[1]
)


with open(
    ROOT_DIR / "config.toml",
    "rb"
) as file:

    CONFIG = tomllib.load(file)


BACKEND_URL = (
    CONFIG["frontend"][
        "backend_url"
    ]
)


# --------------------------------
# Page
# --------------------------------

st.set_page_config(
    page_title=
        "BMW Diagnostic Agent",
    page_icon="🚗"
)


st.title(
    "🚗 BMW Vehicle Diagnostic Agent"
)


st.caption(
    "Streamlit + FastAPI + LLM Agent"
)


# --------------------------------
# User input
# --------------------------------

question = st.text_input(

    "Ask the Agent",

    placeholder=
        "Example: Check BMW1001"

)


# --------------------------------
# Button
# --------------------------------

if st.button(
    "Analyze Vehicle",
    type="primary"
):

    if not question:

        st.warning(
            "Please enter a question."
        )

        st.stop()


    try:

        with st.spinner(
            "Agent is analyzing..."
        ):

            response = requests.post(

                f"{BACKEND_URL}"
                "/agent/query",

                json={
                    "question":
                        question
                },

                timeout=60

            )


        response.raise_for_status()

        data = response.json()


        # -------------------------
        # Agent answer
        # -------------------------

        st.subheader(
            "Agent Response"
        )

        st.success(
            data["answer"]
        )


        # -------------------------
        # Tool activity
        # -------------------------

        with st.expander(
            "Agent Activity"
        ):

            st.write(
                "Iterations:",
                data["iterations"]
            )

            st.write(
                "Tools Used"
            )

            st.json(
                data["tools_used"]
            )


    except requests.exceptions.RequestException as exc:

        st.error(
            f"API Error: {exc}"
        )