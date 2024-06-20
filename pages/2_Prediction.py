import streamlit as st

st.set_page_config(
    page_title="Credit Default Prediction",
    page_icon="⌛",
)

def formatNumber(number):
    return "{:,}".format(number).replace(",", ".")

def predictCustomer(gender_col, limit_col, age_col, edu_col, pay1, bill_amt1, pay_amt1, pay2, bill_amt2, pay_amt2,
                    pay3, bill_amt3, pay_amt3, pay4, bill_amt4, pay_amt4, pay5, bill_amt5, pay_amt5,
                    pay6, bill_amt6, pay_amt6,):
  

    return "MAUDY"


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
        st.write(predictCustomer(gender_col, limit_col, age_col, edu_col, pay1, bill_amt1, pay_amt1, pay2, bill_amt2, pay_amt2,
                                pay3, bill_amt3, pay_amt3, pay4, bill_amt4, pay_amt4, pay5, bill_amt5, pay_amt5,
                                pay6, bill_amt6, pay_amt6))