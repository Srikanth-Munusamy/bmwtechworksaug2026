from io import BytesIO

import pandas as pd
import streamlit as st

from parts_agent.agent import (
    PartsProcurementAgent
)
from parts_agent.api_client import (
    BackendAPI
)
from parts_agent.s3_inventory import (
    S3Inventory
)


st.set_page_config(
    page_title=
        "BMW Parts Procurement Agent",
    layout="wide"
)


st.title(
    "BMW Parts Procurement AI Agent"
)


api = BackendAPI()

inventory = S3Inventory()

agent = PartsProcurementAgent()


tab1, tab2, tab3, tab4 = (
    st.tabs(
        [
            "1 Upload Inventory",
            "2 Create Data",
            "3 Run Agent",
            "4 Purchase Requests"
        ]
    )
)


# =================================================
# TAB 1 - Inventory
# =================================================
with tab1:

    st.header(
        "Upload Inventory CSV to AWS S3"
    )

    uploaded = st.file_uploader(
        "Select inventory CSV",
        type=["csv"]
    )

    if uploaded is not None:

        content = (
            uploaded.getvalue()
        )

        df = pd.read_csv(
            BytesIO(content)
        )

        st.dataframe(df)

        required_columns = {
            "part_number",
            "part_name",
            "stock_quantity"
        }

        missing = (
            required_columns
            - set(df.columns)
        )

        if missing:

            st.error(
                f"Missing columns: "
                f"{missing}"
            )

        else:

            if st.button(
                "Upload CSV to S3"
            ):

                result = (
                    inventory
                    .upload_csv(
                        content
                    )
                )

                st.success(
                    "Inventory uploaded "
                    "to S3"
                )

                st.json(result)


# =================================================
# TAB 2 - Create Data
# =================================================
with tab2:

    st.header(
        "Create Service Job"
    )

    with st.form(
        "service_job_form"
    ):

        job_id = st.text_input(
            "Job ID",
            "JOB1001"
        )

        vehicle_model = (
            st.text_input(
                "Vehicle Model",
                "BMW i4"
            )
        )

        issue = st.text_input(
            "Issue",
            "Oil filter replacement"
        )

        part_number = (
            st.text_input(
                "Part Number",
                "OF-2001"
            )
        )

        quantity = st.number_input(
            "Quantity",
            min_value=1,
            value=1
        )

        priority = st.selectbox(
            "Priority",
            [
                "NORMAL",
                "URGENT"
            ]
        )

        submitted = (
            st.form_submit_button(
                "Create Service Job"
            )
        )

    if submitted:

        payload = {
            "job_id":
                job_id,
            "vehicle_model":
                vehicle_model,
            "issue":
                issue,
            "part_number":
                part_number,
            "quantity":
                int(quantity),
            "priority":
                priority,
            "status":
                "OPEN"
        }

        try:

            result = (
                api.create_service_job(
                    payload
                )
            )

            st.success(
                "Service job inserted "
                "through API"
            )

            st.json(result)

        except Exception as e:

            st.error(str(e))


    st.divider()

    st.subheader(
        "Demo Supplier Data"
    )

    if st.button(
        "Load Demo Suppliers"
    ):

        try:

            result = (
                api
                .load_demo_suppliers()
            )

            st.success(
                "Supplier API completed"
            )

            st.json(result)

        except Exception as e:

            st.error(str(e))


# =================================================
# TAB 3 - Agent
# =================================================
with tab3:

    st.header(
        "Run Parts Procurement Agent"
    )

    agent_job_id = (
        st.text_input(
            "Service Job ID",
            "JOB1001",
            key="agent_job"
        )
    )

    authorize = st.checkbox(
        "Authorize purchase request "
        "creation"
    )

    if st.button(
        "Run Agent"
    ):

        try:

            with st.spinner(
                "Agent processing..."
            ):

                result = agent.run(
                    agent_job_id,
                    authorize_purchase=
                        authorize
                )

            st.success(
                "Agent completed"
            )

            st.write(result)

        except Exception as e:

            st.error(str(e))


# =================================================
# TAB 4 - Purchase Requests
# =================================================
with tab4:

    st.header(
        "Purchase Requests"
    )

    if st.button(
        "Refresh Purchase Requests"
    ):

        try:

            rows = (
                api
                .get_purchase_requests()
            )

            st.dataframe(
                pd.DataFrame(rows)
            )

        except Exception as e:

            st.error(str(e))