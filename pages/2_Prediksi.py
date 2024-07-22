import streamlit as st
import pickle
import pandas as pd
import numpy as np
import tensorflow as tf
import plotly.express as px
import plotly.graph_objects as go
from streamlit_shap import st_shap
import shap
import pandas as pd


st.set_page_config(
    page_title="Prediksi Kredit Default",
    page_icon="⌛",
    layout="wide",
)

st.title("Prediksi")

# scaler = StandardScaler()

with open('nn_scaled77%.pkl', 'rb') as file:
    nn_scaled = pickle.load(file)

with open('skaler.pkl', 'rb') as file:
    scaler = pickle.load(file)

def predictCustomer(gender_option, limit_text, age_text, education_option, marriage_option, pay1, bill_amt1, pay_amt1, pay2, bill_amt2, 
                    pay_amt2, pay3, bill_amt3, pay_amt3, pay4, bill_amt4, pay_amt4, pay5, bill_amt5, pay_amt5, pay6, bill_amt6, pay_amt6):
    
    sex1 = gender_option == 'Pria'
    sex2 = gender_option == 'Wanita'

    if education_option == "Lainnya":
        education = 0
    elif education_option == "Sekolah Menengah":
        education = 1
    elif education_option == "Universitas":
        education = 2
    elif education_option == "Sekolah Pascasarjana":
        education = 3

    marriage0 = marriage1 = marriage2 = marriage3 = False

    if marriage_option == 'Lainnya':
        marriage0 = True
    elif marriage_option == 'Menikah':
        marriage1 = True
    elif marriage_option == 'Lajang':
        marriage2 = True
    elif marriage_option == 'Bercerai':
        marriage3 = True

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
        "Terlambat pembayaran 8 bulan": 8
    }
    
    pay1 = pay_mapping.get(pay1, 0)
    pay2 = pay_mapping.get(pay2, 0)
    pay3 = pay_mapping.get(pay3, 0)
    pay4 = pay_mapping.get(pay4, 0)
    pay5 = pay_mapping.get(pay5, 0)
    pay6 = pay_mapping.get(pay6, 0)
    
    input_data = np.array([[limit_text, education, age_text, pay1, pay2, pay3, pay4, pay5, pay6, bill_amt1, bill_amt2, bill_amt3, 
                            bill_amt4, bill_amt5, bill_amt6, pay_amt1, pay_amt2, pay_amt3, pay_amt4, pay_amt5, pay_amt6, marriage0,
                            marriage1, marriage2, marriage3, sex1, sex2]], dtype=np.float32)

    input_data2 = pd.DataFrame({
        'LIMIT_BAL': [limit_text],
        'EDUCATION': [education],
        'AGE': [age_text],
        'PAY_1': [pay1],
        'PAY_2': [pay2],
        'PAY_3': [pay3],
        'PAY_4': [pay4],
        'PAY_5': [pay5],
        'PAY_6': [pay6],
        'BILL_AMT1': [bill_amt1],
        'BILL_AMT2': [bill_amt2],
        'BILL_AMT3': [bill_amt3],
        'BILL_AMT4': [bill_amt4],
        'BILL_AMT5': [bill_amt5],
        'BILL_AMT6': [bill_amt6],
        'PAY_AMT1': [pay_amt1],
        'PAY_AMT2': [pay_amt2],
        'PAY_AMT3': [pay_amt3],
        'PAY_AMT4': [pay_amt4],
        'PAY_AMT5': [pay_amt5],
        'PAY_AMT6': [pay_amt6],
        'MARRIAGE_0': [marriage0],
        'MARRIAGE_1': [marriage1],
        'MARRIAGE_2': [marriage2],
        'MARRIAGE_3': [marriage3],
        'SEX_1': [sex1],
        'SEX_2': [sex2],
    }).astype(float)

    scaled_input_data = scaler.transform(input_data2)
    feature_names = list(input_data2.columns)
    
    prediction = nn_scaled.predict(scaled_input_data)
    risk_percentage = prediction[0][0] * 100
    
    explainer = shap.Explainer(nn_scaled, input_data, feature_names=feature_names)
    explanation = explainer(scaled_input_data)

    return risk_percentage, explanation


with st.expander('Klik di sini untuk mengetahui cara mengisi formulir di bawah:'):
    st.info("""
        **Cara Pengisian Formulir:**

        1. **Pilih Jenis Kelamin**: Pilih "Pria" atau "Wanita".
        2. **Masukkan Kredit Limit**: Isi dengan nilai kredit limit (maksimal 999999).
        3. **Masukkan Usia**: Isi dengan usia Anda (antara 20 hingga 99 tahun).
        4. **Pilih Tingkat Pendidikan**: Pilih salah satu dari "Lainnya", "Sekolah Menengah", "Universitas", atau "Sekolah Pascasarjana".
        5. **Pilih Status Pernikahan**: Pilih salah satu dari "Lainnya", "Menikah", "Lajang", atau "Bercerai".
        6. **Isi Status Pembayaran dan Jumlah**: Untuk setiap kolom, pilih status pembayaran dan isi jumlah tagihan serta jumlah pembayaran dalam $NT.
        7. **Klik Tombol 'Prediksi'**: Setelah mengisi semua data, klik tombol "Prediksi" untuk melihat kemungkinan default customer.
    """)

with st.container(border=True):
    st.markdown(f'##### Isi informasi di bawah untuk memprediksi kemungkinan default customer:')
    gender_col, limit_col, age_col, edu_col, marriage_col = st.columns(5)
    with gender_col:
        gender_option = st.radio(
            'Pilih Jenis Kelamin',
            ("Pria", "Wanita"))
             
    with limit_col:
        limit_text = st.number_input("Kredit Limit (dalam $NT)", min_value=0, max_value=999999)
    
    with age_col:
        age_text = st.number_input("Usia", min_value=20, max_value=99)

    with edu_col:
        education_option = st.selectbox(
        "Pilih Tingkat Pendidikan",
        ("Lainnya", "Sekolah Menengah", "Universitas", "Sekolah Pascasarjana"))
    
    with marriage_col:
        marriage_option = st.selectbox("Pilih Status Pernikahan",
        ('Lainnya', 'Menikah', 'Lajang', 'Bercerai'))

    with st.container(border=True):
        col1, col2 = st.columns(2)
        
        with col1:
            pay1 = st.selectbox(
            'Pilih Status Pembayaran 1',
            ("Tidak ada transaksi", "Lunas", "Penggunaan revolving credit", "Terlambat pembayaran 1 bulan", 
             "Terlambat pembayaran 2 bulan", "Terlambat pembayaran 3 bulan", "Terlambat pembayaran 4 bulan", 
             "Terlambat pembayaran 5 bulan", "Terlambat pembayaran 6 bulan", "Terlambat pembayaran 7 bulan",
             "Terlambat pembayaran 8 bulan"))
            bill_amt1 = st.number_input("Jumlah Tagihan 1 (dalam $NT)", min_value=None, max_value=None)
            pay_amt1 = st.number_input("Jumlah Pembayaran 1 (dalam $NT)", min_value=None, max_value=None)
        
        with col2:
            pay2 = st.selectbox(
            'Pilih Status Pembayaran 2',
            ("Tidak ada transaksi", "Lunas", "Penggunaan revolving credit", "Terlambat pembayaran 1 bulan", 
             "Terlambat pembayaran 2 bulan", "Terlambat pembayaran 3 bulan", "Terlambat pembayaran 4 bulan", 
             "Terlambat pembayaran 5 bulan", "Terlambat pembayaran 6 bulan", "Terlambat pembayaran 7 bulan",
             "Terlambat pembayaran 8 bulan"))
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
             "Terlambat pembayaran 8 bulan"))
            bill_amt3 = st.number_input("Jumlah Tagihan 3 (dalam $NT)", min_value=None, max_value=None)
            pay_amt3 = st.number_input("Jumlah Pembayaran 3 (dalam $NT)", min_value=None, max_value=None)
        
        with col4:
            pay4 = st.selectbox(
            'Pilih Status Pembayaran 4',
            ("Tidak ada transaksi", "Lunas", "Penggunaan revolving credit", "Terlambat pembayaran 1 bulan", 
             "Terlambat pembayaran 2 bulan", "Terlambat pembayaran 3 bulan", "Terlambat pembayaran 4 bulan", 
             "Terlambat pembayaran 5 bulan", "Terlambat pembayaran 6 bulan", "Terlambat pembayaran 7 bulan",
             "Terlambat pembayaran 8 bulan"))
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
             "Terlambat pembayaran 8 bulan"))
            bill_amt5 = st.number_input("Jumlah Tagihan 5 (dalam $NT)", min_value=None, max_value=None)
            pay_amt5 = st.number_input("Jumlah Pembayaran 5 (dalam $NT)", min_value=None, max_value=None)
        
        with col6:
            pay6 = st.selectbox(
            'Pilih Status Pembayaran 6',
            ("Tidak ada transaksi", "Lunas", "Penggunaan revolving credit", "Terlambat pembayaran 1 bulan", 
             "Terlambat pembayaran 2 bulan", "Terlambat pembayaran 3 bulan", "Terlambat pembayaran 4 bulan", 
             "Terlambat pembayaran 5 bulan", "Terlambat pembayaran 6 bulan", "Terlambat pembayaran 7 bulan",
             "Terlambat pembayaran 8 bulan"))
            bill_amt6 = st.number_input("Jumlah Tagihan 6 (dalam $NT)", min_value=None, max_value=None)
            pay_amt6 = st.number_input("Jumlah Pembayaran 6 (dalam $NT)", min_value=None, max_value=None)
                
if st.button('Prediksi'):
    risk_percentage, explanation = predictCustomer(gender_option, limit_text, age_text, education_option, marriage_option, pay1, bill_amt1, pay_amt1, pay2, bill_amt2, 
                                                    pay_amt2, pay3, bill_amt3, pay_amt3, pay4, bill_amt4, pay_amt4, pay5, bill_amt5, pay_amt5, pay6, bill_amt6, pay_amt6)
        
    st.markdown('<h4 style="text-align: center;">Kemungkinan Default</h4>', unsafe_allow_html=True)
    st.write(f"<h3 style='text-align: center;'>{risk_percentage:.2f}%</h3>", unsafe_allow_html=True)

    if risk_percentage >= 50:
        gauge_color = 'red'
        text = "Customer kemungkinan besar gagal bayar di bulan berikutnya"
    else:
        gauge_color = 'green'
        text = "Customer kemungkinan besar tidak gagal bayar di bulan berikutnya"

    fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = risk_percentage,
            domain = {'x': [0, 1], 'y': [0, 1]},
            gauge=dict(
                axis=dict(range=[None, 100], tickwidth=1, tickcolor="darkblue",),
                bar=dict(color=gauge_color),
                bgcolor="white",
                borderwidth=2,
                bordercolor="gray"
            )))
    
    st.plotly_chart(fig)
    st.write(f"<h5 style='text-align: center;'>{text}</h5>", unsafe_allow_html=True)
        
    st.markdown('<h4 style="text-align: center;">Penjelasan</h4>', unsafe_allow_html=True)
    with st.expander("Lihat Penjelasan Lengkap"):
        st.markdown('<div style="display: flex; justify-content: center;">', unsafe_allow_html=True)
        st_shap(shap.plots.waterfall(explanation[0]), width=1200, height=500)
        st.markdown('</div>', unsafe_allow_html=True)
