import requests
import streamlit as st


API_URL = "http://127.0.0.1:8000/predictions/v1.0"


st.set_page_config(
    page_title="BMW Parts Demand",
    page_icon="🚗",
    layout="centered",
)

st.title("BMW Spare-Parts Demand Prediction")
st.write(
    "Predict next-month parts demand using an "
    "Amazon SageMaker endpoint."
)

part_names = {
    "Brake system": 0,
    "Battery system": 1,
    "Cooling system": 2,
    "Electrical system": 3,
    "Suspension": 4,
}

part_name = st.selectbox(
    "Part category",
    list(part_names.keys()),
)

current_stock = st.number_input(
    "Current stock",
    min_value=0,
    value=120,
)

previous_demand = st.number_input(
    "Previous-month demand",
    min_value=0,
    value=180,
)

average_demand = st.number_input(
    "Average monthly demand",
    min_value=0,
    value=160,
)

vehicle_sales = st.number_input(
    "Vehicle sales",
    min_value=0,
    value=450,
)

seasonal_index = st.number_input(
    "Seasonal index",
    min_value=0.1,
    value=1.2,
    step=0.1,
)

lead_time_days = st.number_input(
    "Supplier lead time in days",
    min_value=0,
    value=14,
)

if st.button(
    "Predict demand",
    type="primary",
    use_container_width=True,
):
    payload = {
        "part_category": part_names[part_name],
        "current_stock": current_stock,
        "previous_month_demand": previous_demand,
        "average_monthly_demand": average_demand,
        "vehicle_sales": vehicle_sales,
        "seasonal_index": seasonal_index,
        "lead_time_days": lead_time_days,
    }

    try:
        response = requests.post(
            API_URL,
            json=payload,
            timeout=30,
        )
        response.raise_for_status()

        result = response.json()

        st.metric(
            "Predicted demand",
            result["predicted_demand"],
        )

        st.metric(
            "Recommended order quantity",
            result["recommended_order_quantity"],
        )

        if result["reorder_required"]:
            st.warning("Reorder is required.")
        else:
            st.success("Current stock is sufficient.")

    except requests.RequestException as error:
        st.error(f"API request failed: {error}")