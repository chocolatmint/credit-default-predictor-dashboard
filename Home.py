import streamlit as st

st.set_page_config(
    page_title="Credit Default Prediction",
    page_icon="🏠",
)

def main():
    st.title("Credit Default Prediction")
    st.write(
        "Welcome! This dashboard provides insights "
        "into credit default predictions based on historical data."
    )

    st.markdown("### Dashboard Summary")
    st.write(
        "This dashboard allows you to explore and analyze credit default predictions. "
        "It includes visualizations and summary statistics based on the dataset."
    )


    st.markdown("### Data Source")
    st.write(
        "The data used in this dashboard was taken from [Default of Credit Card Clients - UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/350/default+of+credit+card+clients). "
        "It includes anonymized data related to borrowers' demographics, credit history, and loan details."
    )

if __name__ == "__main__":
    main()
