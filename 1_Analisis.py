import streamlit as st
import pickle
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(
    page_title="Analisis Dataset Kredit Default",
    page_icon="💹",
    layout="wide",
)

with open('credit_default_datasets.pkl', 'rb') as file:
    credit_default = pickle.load(file)['credit_default']

st.title("Analisis")
customer_default = credit_default[credit_default['default payment next month'] == 1]

month_mapping = {
    'PAY_1': 'April 2005',
    'PAY_2': 'Mei 2005',
    'PAY_3': 'Juni 2005',
    'PAY_4': 'Juli 2005',
    'PAY_5': 'Agustus 2005',
    'PAY_6': 'September 2005'
}

color_map = {'Default': '#5a9bd4', 
            'Tidak Default': '#104e8b'}

def formatNumber(number):
    return "{:,}".format(number).replace(",", ".")

# INFOBOX FUNCTIONS
def totalCustomerBox():
    return formatNumber(credit_default.shape[0])

def totalCustomerDefaultBox():
    return formatNumber(customer_default.shape[0])

def totalOutstandingAmountBox():
    bill_amt_columns = ["BILL_AMT1", "BILL_AMT2", "BILL_AMT3", "BILL_AMT4", "BILL_AMT5", "BILL_AMT6"]
    bill_amt_sum = credit_default[bill_amt_columns].sum().sum()
    
    pay_amt_columns = ["PAY_AMT1", "PAY_AMT2", "PAY_AMT3", "PAY_AMT4", "PAY_AMT5", "PAY_AMT6"]
    pay_amt_sum = credit_default[pay_amt_columns].sum().sum()

    return formatNumber(bill_amt_sum - pay_amt_sum)

def totalDefaultOutstandingAmountBox():
    bill_amt_columns = ["BILL_AMT1", "BILL_AMT2", "BILL_AMT3", "BILL_AMT4", "BILL_AMT5", "BILL_AMT6"]
    bill_amt_sum = customer_default[bill_amt_columns].sum().sum()
    
    pay_amt_columns = ["PAY_AMT1", "PAY_AMT2", "PAY_AMT3", "PAY_AMT4", "PAY_AMT5", "PAY_AMT6"]
    pay_amt_sum = customer_default[pay_amt_columns].sum().sum()

    return formatNumber(bill_amt_sum - pay_amt_sum)

# PLOT FUNCTIONS

def generatePlot(status, education, marriage):
    credit_default_copy = credit_default.copy()
    credit_default_copy['MARRIAGE'] = credit_default_copy[['MARRIAGE_1', 'MARRIAGE_2']].idxmax(axis=1)
    credit_default_copy['SEX'] = credit_default_copy[['SEX_1', 'SEX_2']].idxmax(axis=1)

    credit_default_copy['SEX'] = credit_default_copy['SEX'].replace({
        'SEX_1': 'Pria',
        'SEX_2': 'Wanita'
    })

    credit_default_copy['MARRIAGE'] = credit_default_copy['MARRIAGE'].replace({
    'MARRIAGE_1': 'Menikah',
    'MARRIAGE_2': 'Lajang'
    })

    if status == 'Default':
        customers = credit_default_copy[credit_default_copy['default payment next month'] == 1].copy()
    else:
        customers = credit_default_copy[credit_default_copy['default payment next month'] == 0].copy()
    
    customers['EDUCATION'] = customers['EDUCATION'].replace({
        1: 'Lainnya',
        2: 'Sekolah Menengah',
        3: 'Universitas',
        4: 'Sekolah Pascasarjana'
    })
    
    customers = customers[customers['EDUCATION'] == education]
    customers = customers[customers['MARRIAGE'] == marriage]

    age_sex_education_marriage_counts = customers.groupby(['AGE', 'SEX', 'EDUCATION', 'MARRIAGE']).size().reset_index(name='Count')

    fig = px.area(age_sex_education_marriage_counts, x='AGE', y='Count', color='SEX', line_group='SEX',
              labels={
                  'AGE': 'Usia', 'Count': 'Jumlah Customer',
                  'SEX': 'Jenis Kelamin', 'EDUCATION': 'Pendidikan', 'MARRIAGE' : 'Status Pernikahan'
              },
              color_discrete_map={'Pria': '#1f77b4', 'Wanita': '#ff85c0'})\
        .for_each_annotation(lambda a: a.update(text=a.text.replace("EDUCATION=", "").replace("MARRIAGE=", "")))\
        .update_layout(
            title=f'Persona Customer {status}',
            legend_title_text=None,
            legend=dict(orientation="h", yanchor="bottom", y=0.9, xanchor="right", x=1),
            margin=dict(l=20, r=20, t=40, b=20),
            height=400,
            width=1300
        )
    return fig

def generateGenericPlot():
    target_counts = credit_default['default payment next month'].value_counts()

    data = {'Target': target_counts.index, 'Count': target_counts.values}
    target_counts = pd.DataFrame(data)
    target_counts['Target'] = target_counts['Target'].map({0: 'Tidak Default', 1: 'Default'})

    fig = px.bar(target_counts, x='Target', y='Count', color='Target', 
                labels={'Count': 'Jumlah Customer', 'Target': 'Status'},color_discrete_map=color_map,)\
        .update_layout(xaxis_tickformat=',d')\
        .update_layout(title='Customer Berdasarkan Status Pembayaran Bulan Depan')
        
    return fig

def generateGenderPlot():
    credit_default_copy = credit_default.copy()
    credit_default_copy['SEX'] = credit_default_copy[['SEX_1', 'SEX_2']].idxmax(axis=1)
    
    credit_default_copy['SEX'] = credit_default_copy['SEX'].replace({
        'SEX_1': 'Pria',
        'SEX_2': 'Wanita'
    })

    for i in range(1, 7):
        credit_default_copy[f'OUTSTANDING_AMT{i}'] = credit_default[f'BILL_AMT{i}'] - credit_default[f'PAY_AMT{i}']
    
    average_outstanding_by_gender = credit_default_copy.groupby('SEX')[['OUTSTANDING_AMT1', 'OUTSTANDING_AMT2', 'OUTSTANDING_AMT3', 'OUTSTANDING_AMT4', 'OUTSTANDING_AMT5', 'OUTSTANDING_AMT6']].mean()
    sum_of_averages = average_outstanding_by_gender.mean(axis=1).reset_index(name='Sum_Average_Outstanding_Amount')
    
    fig = px.bar(sum_of_averages, x='SEX', y='Sum_Average_Outstanding_Amount', color='SEX',
                 labels={'SEX': 'Jenis Kelamin', 'Sum_Average_Outstanding_Amount': 'Rata-rata Outstanding Amount'},
                 title='Berdasarkan Jenis Kelamin')

    return fig

def generateAgePlot():
    credit_default_copy = credit_default.copy()

    age_bins = [20, 30, 40, 50, 60, 70, 80, 90]
    age_labels = ['20-29 tahun', '30-39 tahun', '40-49 tahun', '50-59 tahun', '60-69 tahun', '70-79 tahun', '80-89 tahun']
    credit_default_copy['AGE_GROUP'] = pd.cut(credit_default_copy['AGE'], bins=age_bins, labels=age_labels)

    for i in range(1, 7):
        credit_default_copy[f'OUTSTANDING_AMT{i}'] = credit_default[f'BILL_AMT{i}'] - credit_default[f'PAY_AMT{i}']
    
    average_outstanding_by_age = credit_default_copy.groupby('AGE_GROUP')[['OUTSTANDING_AMT1', 'OUTSTANDING_AMT2', 'OUTSTANDING_AMT3', 'OUTSTANDING_AMT4', 'OUTSTANDING_AMT5', 'OUTSTANDING_AMT6']].mean()
    sum_of_averages = average_outstanding_by_age.mean(axis=1).reset_index(name='Sum_Average_Outstanding_Amount')
    
    fig = px.bar(sum_of_averages, x='AGE_GROUP', y='Sum_Average_Outstanding_Amount',
                 labels={'AGE_GROUP': 'Kelompok Usia', 'Sum_Average_Outstanding_Amount': 'Rata-rata Outstanding Amount'},
                 title='Berdasarkan Kelompok Usia (per 10 tahun)')

    return fig

def generateEducationPlot():
    credit_default_copy = credit_default.copy()
    education_mapping = {
        1: 'Lainnya',
        2: 'Sekolah menengah',
        3: 'Universitas',
        4: 'Sekolah pascasarjana'
    }

    credit_default_copy['EDUCATION'] = credit_default_copy['EDUCATION'].map(education_mapping)
    
    for i in range(1, 7):
        credit_default_copy[f'OUTSTANDING_AMT{i}'] = credit_default[f'BILL_AMT{i}'] - credit_default[f'PAY_AMT{i}']
    
    average_outstanding_by_education = credit_default_copy.groupby('EDUCATION')[['OUTSTANDING_AMT1', 'OUTSTANDING_AMT2', 'OUTSTANDING_AMT3', 'OUTSTANDING_AMT4', 'OUTSTANDING_AMT5', 'OUTSTANDING_AMT6']].mean()
    
    sum_of_averages = average_outstanding_by_education.mean(axis=1).reset_index(name='Sum_Average_Outstanding_Amount')
    
    fig = px.bar(sum_of_averages, x='EDUCATION', y='Sum_Average_Outstanding_Amount',
                 labels={'EDUCATION': 'Tingkat Pendidikan', 'Sum_Average_Outstanding_Amount': 'Rata-rata Outstanding Amount'},
                 title='Berdasarkan Tingkat Pendidikan',
                 category_orders={'MARRIAGE': ['Lainnya', 'Sekolah menengah', 'Universitas', 'Sekolah pascasarjana']})
    return fig

def generateMarriagePlot():
    credit_default_copy = credit_default.copy()

    marriage_status_mapping = {
        'MARRIAGE_0': 'Lainnya',
        'MARRIAGE_1': 'Menikah',
        'MARRIAGE_2': 'Lajang',
        'MARRIAGE_3': 'Bercerai'
    }
    credit_default_copy['MARRIAGE'] = credit_default_copy[['MARRIAGE_0', 'MARRIAGE_1', 'MARRIAGE_2', 'MARRIAGE_3']].idxmax(axis=1)
    credit_default_copy['MARRIAGE'] = credit_default_copy['MARRIAGE'].replace(marriage_status_mapping)

    for i in range(1, 7):
        credit_default_copy[f'OUTSTANDING_AMT{i}'] = credit_default[f'BILL_AMT{i}'] - credit_default[f'PAY_AMT{i}']
    
    average_outstanding_by_marriage = credit_default_copy.groupby('MARRIAGE')[['OUTSTANDING_AMT1', 'OUTSTANDING_AMT2', 'OUTSTANDING_AMT3', 'OUTSTANDING_AMT4', 'OUTSTANDING_AMT5', 'OUTSTANDING_AMT6']].mean()
    
    sum_of_averages = average_outstanding_by_marriage.mean(axis=1).reset_index(name='Sum_Average_Outstanding_Amount')
    
    fig = px.bar(sum_of_averages, x='MARRIAGE', y='Sum_Average_Outstanding_Amount',
                 labels={'MARRIAGE': 'Status Pernikahan', 'Sum_Average_Outstanding_Amount': 'Rata-rata Outstanding Amount'},
                 title='Berdasarkan Status Pernikahan',
                 category_orders={'MARRIAGE': ['Lainnya', 'Lajang', 'Menikah', 'Bercerai']})

    return fig

def generateLimitPlot():
    credit_default_copy = credit_default.copy()

    bins = np.arange(0, credit_default['LIMIT_BAL'].max() + 100000, 100000)
    labels = [f'{int(bins[i])}-{int(bins[i+1]-1)}' for i in range(len(bins)-1)]
    credit_default_copy['LIMIT_BAL_BIN'] = pd.cut(credit_default_copy['LIMIT_BAL'], bins=bins, labels=labels, right=False)

    for i in range(1, 7):
        credit_default_copy[f'OUTSTANDING_AMT{i}'] = credit_default_copy[f'BILL_AMT{i}'] - credit_default_copy[f'PAY_AMT{i}']

    average_outstanding_by_limit_bin = credit_default_copy.groupby('LIMIT_BAL_BIN')[['OUTSTANDING_AMT1', 'OUTSTANDING_AMT2', 'OUTSTANDING_AMT3', 'OUTSTANDING_AMT4', 'OUTSTANDING_AMT5', 'OUTSTANDING_AMT6']].mean()

    sum_of_averages = average_outstanding_by_limit_bin.mean(axis=1).reset_index(name='Sum_Average_Outstanding_Amount')

    fig = px.bar(sum_of_averages, x='LIMIT_BAL_BIN', y='Sum_Average_Outstanding_Amount',
                labels={'LIMIT_BAL_BIN': 'Kredit Limit', 'Sum_Average_Outstanding_Amount': 'Rata-rata Outstanding Amount'},
                title='Berdasarkan Kredit Limit (per 100k)')

    return fig

def generateOutstandingAmountMonthPlot():
    outstanding_amounts = {
        "April 2005": (credit_default["BILL_AMT1"] - credit_default["PAY_AMT1"]).sum(),
        "Mei 2005": (credit_default["BILL_AMT2"] - credit_default["PAY_AMT2"]).sum(),
        "Juni 2005": (credit_default["BILL_AMT3"] - credit_default["PAY_AMT3"]).sum(),
        "Juli 2005": (credit_default["BILL_AMT4"] - credit_default["PAY_AMT4"]).sum(),
        "Agustus 2005": (credit_default["BILL_AMT5"] - credit_default["PAY_AMT5"]).sum(),
        "September 2005": (credit_default["BILL_AMT6"] - credit_default["PAY_AMT6"]).sum(),
    }

    fig = px.line(
        x=list(outstanding_amounts.keys()),
        y=list(outstanding_amounts.values()),
        title='Outstanding Amount Berdasarkan Bulan',
        labels={'x': 'Bulan', 'y': 'Outstanding Amount ($NT)'},
        markers=True
    ).update_layout(title='Outstanding Amount Berdasarkan Bulan')

    return fig

def generateOutstandingCountMonthPlot():
    outstanding_amt_apr = (credit_default["BILL_AMT1"] - credit_default["PAY_AMT1"] > 0).sum()
    outstanding_amt_may = (credit_default["BILL_AMT2"] - credit_default["PAY_AMT2"] > 0).sum()
    outstanding_amt_jun = (credit_default["BILL_AMT3"] - credit_default["PAY_AMT3"] > 0).sum()
    outstanding_amt_jul = (credit_default["BILL_AMT4"] - credit_default["PAY_AMT4"] > 0).sum()
    outstanding_amt_aug = (credit_default["BILL_AMT5"] - credit_default["PAY_AMT5"] > 0).sum()
    outstanding_amt_sep = (credit_default["BILL_AMT6"] - credit_default["PAY_AMT6"] > 0).sum()

    months = ["April 2005", "Mei 2005", "Juni 2005", "Juli 2005", "Agustus 2005", "September 2005"]
    df_outstanding = pd.DataFrame({
        "Bulan": months,
        "Jumlah Customer": [
            outstanding_amt_apr, outstanding_amt_may, outstanding_amt_jun,
            outstanding_amt_jul, outstanding_amt_aug, outstanding_amt_sep
        ]
    })

    fig = px.line(
        data_frame=df_outstanding,
        x='Bulan',
        y='Jumlah Customer',
        title='Jumlah Customer Berdasarkan Outstanding Amount',
        labels={'Jumlah Customer Berdasarkan Outstanding Amount': 'Jumlah Customer'},
        markers=True,
    ).update_layout(title=f'Jumlah Customer Berdasarkan Outstanding Amount')

    return fig

def generateStatusPerMonth(data, selected_month):
    pay_mapping = {
        -2: "Tidak ada transaksi",
        -1: "Lunas",
        0: "Penggunaan revolving credit",
        1: "Terlambat pembayaran 1 bulan",
        2: "Terlambat pembayaran 2 bulan",
        3: "Terlambat pembayaran 3 bulan",
        4: "Terlambat pembayaran 4 bulan",
        5: "Terlambat pembayaran 5 bulan",
        6: "Terlambat pembayaran 6 bulan",
        7: "Terlambat pembayaran 7 bulan",
        8: "Terlambat pembayaran 8 bulan",
        9: "Terlambat pembayaran >= 9 bulan"
    }
    selected_payment_status = f'PAY_{list(month_mapping.keys()).index(selected_month) + 1}' 
    payment_status_counts = data[selected_payment_status].value_counts().sort_index()  
    payment_status_counts.index = payment_status_counts.index.map(pay_mapping)
    
    data_long = payment_status_counts.reset_index()
    data_long.columns = ['Status Pembayaran', 'Jumlah'] 
    
    fig = px.bar(data_long, x='Status Pembayaran', y='Jumlah',
                title=f'Status Pembayaran di Bulan {month_mapping[selected_month]}',
                labels={'Status Pembayaran': 'Status Pembayaran', 'Jumlah': 'Jumlah'},
                color_discrete_sequence=['blue'])

    return fig

def generatePlots():
    area_plot_gender_status = generateGenderPlot()
    area_plot_age_status = generateAgePlot()
    area_plot_edu_status = generateEducationPlot()
    area_plot_marriage_status = generateMarriagePlot()
    area_plot_limit_status = generateLimitPlot()

    return (area_plot_gender_status, area_plot_age_status, area_plot_edu_status,
            area_plot_marriage_status, area_plot_limit_status)

# STREAMLIT

with st.container(border=True):
    infobox1, infobox2 = st.columns(2)
    with infobox1:
        st.metric(label="Jumlah Customer", value=totalCustomerBox()) 
    with infobox2:
        st.metric(label="Jumlah Customer Default", value=totalCustomerDefaultBox())

    infobox3, infobox4 = st.columns(2)
    with infobox3:
        st.metric(label="Total Outstanding Amount", value=totalOutstandingAmountBox(), help = 'dalam NTD$')
    with infobox4:
        st.metric(label="Total Default Outstanding Amount", value=totalDefaultOutstandingAmountBox(), help = 'dalam NTD$')

with st.container(border=True):
    st.plotly_chart(generateGenericPlot())
    
with st.container(border=True):
    st.markdown(f'##### Pilih pilihan di bawah untuk melihat persona customer:')
    left_column, right_column = st.columns([1, 2])
    with st.container(border=True):
        with left_column:
            status_option = st.radio(
                'Pilih Status',
                ("Default", "Tidak Default"))
            education_option = st.selectbox(
            "Pilih Tingkat Pendidikan",
            ("Lainnya", "Sekolah Menengah", "Universitas", "Sekolah Pascasarjana"))
            marriage_option = st.selectbox(
            "Pilih Status Pernikahan",
            ("Menikah", "Lajang"))
            
            area_plot_fig = generatePlot(status_option, education_option, marriage_option)

    with st.container(border=True):            
        with right_column:
            if area_plot_fig is not None:
                st.plotly_chart(area_plot_fig)

plot_options = [
    'Jenis Kelamin', 
    'Kelompok Usia', 
    'Tingkat Pendidikan', 
    'Status Pernikahan', 
    'Kredit Limit'
]

with st.container(border=True):
    st.markdown(f'##### Pilih kategori di bawah untuk melihat informasi outstanding amount:')
    selected_plot = st.selectbox('Pilih Kategori:', plot_options)
    selected_index = plot_options.index(selected_plot)

    st.plotly_chart(generatePlots()[selected_index])
                
with st.container(border=True):
    st.plotly_chart(generateOutstandingAmountMonthPlot())
    
with st.container(border=True):
    st.plotly_chart(generateOutstandingCountMonthPlot())

with st.container(border=True):
    st.markdown(f'## Perbandingan Kredit Limit Berdasarkan Status Pembayaran')

    st.markdown(f'#### Tidak Default')
    with st.container(border=True):
        infobox1, infobox2, infobox3, infobox4, infobox5 = st.columns(5)
        with infobox1:
            st.metric(label="Min", value=formatNumber(10000), help = 'dalam NTD$') 
        with infobox2:
            st.metric(label="Max", value=formatNumber(1000000), help = 'dalam NTD$')
        with infobox3:
            st.metric(label="Q1", value=formatNumber(70000), help = 'dalam NTD$')
        with infobox4:
            st.metric(label="Median/Q2", value=formatNumber(150000), help = 'dalam NTD$')
        with infobox5:
            st.metric(label="Q3", value=formatNumber(250000), help = 'dalam NTD$')

    st.markdown(f'#### Default')
    with st.container(border=True):
        infobox1, infobox2, infobox3, infobox4, infobox5 = st.columns(5)
        with infobox1:
            st.metric(label="Min", value=formatNumber(10000), help = 'dalam NTD$') 
        with infobox2:
            st.metric(label="Max", value=formatNumber(740000), help = 'dalam NTD$')
        with infobox3:
            st.metric(label="Q1", value=formatNumber(50000), help = 'dalam NTD$')
        with infobox4:
            st.metric(label="Median/Q2", value=formatNumber(90000), help = 'dalam NTD$')
        with infobox5:
            st.metric(label="Q3", value=formatNumber(200000), help = 'dalam NTD$')

with st.container(border=True):
    st.markdown(f'##### Pilih pilihan bulan di bawah untuk melihat statistik status pembayaran:')
    selected_month = st.selectbox('Pilih Bulan', options=list(month_mapping.keys()), format_func=lambda x: month_mapping[x])
    
    statusPlot = generateStatusPerMonth(credit_default, selected_month)
    if statusPlot is not None:
            st.plotly_chart(statusPlot)
