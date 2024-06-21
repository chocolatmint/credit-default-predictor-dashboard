import streamlit as st
import pickle
import numpy as np
import tensorflow as tf
import plotly.express as px
from streamlit_shap import st_shap
import shap

st.set_page_config(
    page_title="Credit Default Prediction",
    page_icon="⌛",
)

with open('nn_unscaled.pkl', 'rb') as file:
    nn_unscaled = pickle.load(file)

def predictCustomer(gender_option, limit_text, age_text, education_option, pay1, bill_amt1, pay_amt1, pay2, bill_amt2, pay_amt2,
                    pay3, bill_amt3, pay_amt3, pay4, bill_amt4, pay_amt4, pay5, bill_amt5, pay_amt5, pay6, bill_amt6, pay_amt6):
    try:
        limit = float(limit_text.replace(",", "").replace(".", "")) if limit_text else 0
    except ValueError:
        limit = 0
    
    education_mapping = {
        "Lainnya": 0,
        "Sekolah Menengah": 1,
        "Universitas": 2,
        "Sekolah Pascasarjana": 3
    }
    
    pay_mapping = {
        "Tidak ada transaksi": -2,
        "Lunas": -1,
        "Penggunaan revolving credit": 0,
        "Terlambat pembayaran 1 bulan": 1,
        "Terlambat pembayaran 2 bulan": 2,
        "Terlambat pembayaran 3 bulan": 3,
        "Terlambat pembayaran 4 bulan": 4,
        "Terlambat pembayaran 5 bulan": 5,
        "Terlambat pembayaran 6 bulan": 6,
        "Terlambat pembayaran 7 bulan": 7,
        "Terlambat pembayaran 8 bulan": 8,
        "Terlambat pembayaran >= 9 bulan": 9
    }
    
    pay1 = pay_mapping.get(pay1, 0)
    pay2 = pay_mapping.get(pay2, 0)
    pay3 = pay_mapping.get(pay3, 0)
    pay4 = pay_mapping.get(pay4, 0)
    pay5 = pay_mapping.get(pay5, 0)
    pay6 = pay_mapping.get(pay6, 0)
    
    input_data = np.array([[pay6, pay5, pay4, pay3, pay2, pay1, limit, pay_amt6, pay_amt5, pay_amt4]])
    
    prediction = nn_unscaled.predict(input_data)
    risk_percentage = prediction[0][0] * 100
    
    explainer = shap.Explainer(nn_unscaled, input_data)
    explanation = explainer(input_data)

    return risk_percentage, explanation


with st.container(border=True):
    gender_col, limit_col, age_col, edu_col = st.columns(4)
    with gender_col:
        gender_option = st.radio(
            'Pilih Jenis Kelamin',
            ("Pria", "Wanita"))
             
    with limit_col:
        limit_text = st.text_input("Kredit Limit", "dalam $NT")
    
    with age_col:
        age_text = st.text_input("Usia", "tahun")

    with edu_col:
        education_option = st.selectbox(
        "Pilih Tingkat Pendidikan",
        ("Lainnya", "Sekolah Menengah", "Universitas", "Sekolah Pascasarjana"))

    with st.container(border=True):
        col1, col2 = st.columns(2)
        
        with col1:
            pay1 = st.selectbox(
            'Pilih Status Pembayaran 1',
            ("Tidak ada transaksi", "Lunas", "Penggunaan revolving credit", "Terlambat pembayaran 1 bulan", 
             "Terlambat pembayaran 2 bulan", "Terlambat pembayaran 3 bulan", "Terlambat pembayaran 4 bulan", 
             "Terlambat pembayaran 5 bulan", "Terlambat pembayaran 6 bulan", "Terlambat pembayaran 7 bulan",
             "Terlambat pembayaran 8 bulan", "Terlambat pembayaran >= 9 bulan"))
            bill_amt1 = st.number_input("Jumlah Tagihan 1 (dalam $NT)", min_value=None, max_value=None)
            pay_amt1 = st.number_input("Jumlah Pembayaran 1 (dalam $NT)", min_value=None, max_value=None)
        
        with col2:
            pay2 = st.selectbox(
            'Pilih Status Pembayaran 2',
            ("Tidak ada transaksi", "Lunas", "Penggunaan revolving credit", "Terlambat pembayaran 1 bulan", 
             "Terlambat pembayaran 2 bulan", "Terlambat pembayaran 3 bulan", "Terlambat pembayaran 4 bulan", 
             "Terlambat pembayaran 5 bulan", "Terlambat pembayaran 6 bulan", "Terlambat pembayaran 7 bulan",
             "Terlambat pembayaran 8 bulan", "Terlambat pembayaran >= 9 bulan"))
            bill_amt2 = st.number_input("Jumlah Tagihan 2 (dalam $NT)", min_value=None, max_value=None)
            pay_amt2 = st.number_input("Jumlah Pembayaran 2 (dalam $NT)", min_value=None, max_value=None)

    
    with st.container(border=True):
        col3, col4 = st.columns(2)
        with col3:
            pay3 = st.selectbox(
            'Pilih Status Pembayaran 3',
            ("Tidak ada transaksi", "Lunas", "Penggunaan revolving credit", "Terlambat pembayaran 1 bulan", 
             "Terlambat pembayaran 2 bulan", "Terlambat pembayaran 3 bulan", "Terlambat pembayaran 4 bulan", 
             "Terlambat pembayaran 5 bulan", "Terlambat pembayaran 6 bulan", "Terlambat pembayaran 7 bulan",
             "Terlambat pembayaran 8 bulan", "Terlambat pembayaran >= 9 bulan"))
            bill_amt3 = st.number_input("Jumlah Tagihan 3 (dalam $NT)", min_value=None, max_value=None)
            pay_amt3 = st.number_input("Jumlah Pembayaran 3 (dalam $NT)", min_value=None, max_value=None)
        
        with col4:
            pay4 = st.selectbox(
            'Pilih Status Pembayaran 4',
            ("Tidak ada transaksi", "Lunas", "Penggunaan revolving credit", "Terlambat pembayaran 1 bulan", 
             "Terlambat pembayaran 2 bulan", "Terlambat pembayaran 3 bulan", "Terlambat pembayaran 4 bulan", 
             "Terlambat pembayaran 5 bulan", "Terlambat pembayaran 6 bulan", "Terlambat pembayaran 7 bulan",
             "Terlambat pembayaran 8 bulan", "Terlambat pembayaran >= 9 bulan"))
            bill_amt4 = st.number_input("Jumlah Tagihan 4 (dalam $NT)", min_value=None, max_value=None)
            pay_amt4 = st.number_input("Jumlah Pembayaran 4 (dalam $NT)", min_value=None, max_value=None)

    with st.container(border=True):
        col5, col6 = st.columns(2)
        with col5:
            pay5 = st.selectbox(
            'Pilih Status Pembayaran 5',
            ("Tidak ada transaksi", "Lunas", "Penggunaan revolving credit", "Terlambat pembayaran 1 bulan", 
             "Terlambat pembayaran 2 bulan", "Terlambat pembayaran 3 bulan", "Terlambat pembayaran 4 bulan", 
             "Terlambat pembayaran 5 bulan", "Terlambat pembayaran 6 bulan", "Terlambat pembayaran 7 bulan",
             "Terlambat pembayaran 8 bulan", "Terlambat pembayaran >= 9 bulan"))
            bill_amt5 = st.number_input("Jumlah Tagihan 5 (dalam $NT)", min_value=None, max_value=None)
            pay_amt5 = st.number_input("Jumlah Pembayaran 5 (dalam $NT)", min_value=None, max_value=None)
        
        with col6:
            pay6 = st.selectbox(
            'Pilih Status Pembayaran 6',
            ("Tidak ada transaksi", "Lunas", "Penggunaan revolving credit", "Terlambat pembayaran 1 bulan", 
             "Terlambat pembayaran 2 bulan", "Terlambat pembayaran 3 bulan", "Terlambat pembayaran 4 bulan", 
             "Terlambat pembayaran 5 bulan", "Terlambat pembayaran 6 bulan", "Terlambat pembayaran 7 bulan",
             "Terlambat pembayaran 8 bulan", "Terlambat pembayaran >= 9 bulan"))
            bill_amt6 = st.number_input("Jumlah Tagihan 6 (dalam $NT)", min_value=None, max_value=None)
            pay_amt6 = st.number_input("Jumlah Pembayaran 6 (dalam $NT)", min_value=None, max_value=None)
                
    if st.button('Predict'):
        risk_percentage, explanation = predictCustomer(gender_option, limit_text, age_text, education_option, pay1, bill_amt1, pay_amt1, pay2, bill_amt2, pay_amt2,
                                                       pay3, bill_amt3, pay_amt3, pay4, bill_amt4, pay_amt4, pay5, bill_amt5, pay_amt5, pay6, bill_amt6, pay_amt6)
        
        fig = px.pie(
            values=[risk_percentage, 100 - risk_percentage],
            names=['Risk', 'No Risk'],
            title='Credit Default Prediction Risk Percentage',
            hole=0.3
        )
        st.plotly_chart(fig)
        
        st.subheader("Risk Percentage")
        st.write(f"{risk_percentage:.2f}%")
        
        st.subheader("Explanation")
        st_shap(shap.plots.beeswarm(explanation), height=300)
        st_shap(shap.plots.waterfall(explanation[0]), height=300)
