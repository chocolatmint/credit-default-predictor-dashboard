import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(
    page_title="Credit Default Prediction",
    page_icon="💹",
)

credit_default = st.session_state.data['credit_default']
customer_default = credit_default[credit_default['default payment next month'] == 1]

def formatNumber(number):
    return "{:,}".format(number).replace(",", ".")

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

    if status == 'Gagal Bayar':
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
              color_discrete_map={'Pria': 'blue', 'Wanita': 'pink'})\
        .for_each_annotation(lambda a: a.update(text=a.text.replace("EDUCATION=", "").replace("MARRIAGE=", "")))\
        .update_layout(
            title=f'Customer {status}',
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
    target_counts['Target'] = target_counts['Target'].map({0: 'Tidak Gagal Bayar', 1: 'Gagal Bayar'})

    fig = px.bar(target_counts, x='Target', y='Count', color='Target', labels={'Count': 'Jumlah Customer', 'Target': 'Status'})\
        .update_layout(xaxis_tickformat=',d')\
        .update_layout(title='Customer Berdasarkan Status Gagal Bayar')
        
    return fig

def generateGenderPlot(status):
    credit_default_copy = credit_default.copy()

    if status == 'Gagal Bayar':
        default_customers = credit_default_copy[credit_default_copy['default payment next month'] == 1].copy()
    else:
        default_customers = credit_default_copy[credit_default_copy['default payment next month'] == 0].copy()
    
    default_customers_by_gender = default_customers[['SEX_1', 'SEX_2']].sum()

    data = {'Gender': ['Pria', 'Wanita'], 'Count': default_customers_by_gender.values}
    default_customers_by_gender = pd.DataFrame(data)

    fig = px.bar(default_customers_by_gender, x='Gender', y='Count', color='Gender', labels={'Count': 'Jumlah Customer', 'Gender': 'Jenis Kelamin'})\
        .update_layout(title=f'Berdasarkan Jenis Kelamin')
    
    return fig

def generateAgePlot(status):
    credit_default_copy = credit_default.copy()

    if status == 'Gagal Bayar':
        default_customers = credit_default_copy[credit_default_copy['default payment next month'] == 1].copy()
    else:
        default_customers = credit_default_copy[credit_default_copy['default payment next month'] == 0].copy()

    bin_edges = list(range(20, 101, 10))
    bin_labels = ['{}-an'.format(i) for i in range(20, 100, 10)]
    default_customers['Age_Group'] = pd.cut(default_customers['AGE'], bins=bin_edges, labels=bin_labels, right=False)

    default_customers_by_age_group = default_customers.groupby('Age_Group').size().reset_index(name='Count')

    fig = px.bar(default_customers_by_age_group, x='Age_Group', y='Count', labels={'Count': 'Jumlah Customer', 'Age_Group': 'Kelompok Usia'})\
        .update_layout(title=f'Berdasarkan Kelompok Usia')
    return fig

def generateEducationPlot(status):
    credit_default_copy = credit_default.copy()
    education_mapping = {
        1: 'Lainnya',
        2: 'Sekolah menengah',
        3: 'Universitas',
        4: 'Sekolah pascasarjana'
    }

    if status == 'Gagal Bayar':
        default_customers = credit_default_copy[credit_default_copy['default payment next month'] == 1].copy()
    else:
        default_customers = credit_default_copy[credit_default_copy['default payment next month'] == 0].copy()
    
    default_customers.loc[:, 'EDUCATION'] = default_customers['EDUCATION'].replace(education_mapping)
    default_customers_by_education = default_customers['EDUCATION'].value_counts()

    data = {'Education': default_customers_by_education.index, 'Count': default_customers_by_education.values}
    default_customers_by_education = pd.DataFrame(data)

    fig = px.bar(default_customers_by_education, x='Education', y='Count', labels={'Count': 'Jumlah Customer', 'Education': 'Pendidikan'}) \
        .update_layout(title=f'Berdasarkan Pendidikan')
    
    return fig

def generateMarriagePlot(status):
    credit_default_copy = credit_default.copy()

    if status == 'Gagal Bayar':
        default_customers = credit_default_copy[credit_default_copy['default payment next month'] == 1].copy()
    else:
        default_customers = credit_default_copy[credit_default_copy['default payment next month'] == 0].copy()

    default_customers_by_marriage = default_customers[['MARRIAGE_0', 'MARRIAGE_1', 'MARRIAGE_2', 'MARRIAGE_3']].sum().reset_index()
    default_customers_by_marriage.columns = ['Marriage_Status_Code', 'Count']

    marriage_status_mapping = {
        'MARRIAGE_0': 'Lainnya',
        'MARRIAGE_1': 'Menikah',
        'MARRIAGE_2': 'Lajang',
        'MARRIAGE_3': 'Bercerai'
    }
    default_customers_by_marriage['Marriage_Status'] = default_customers_by_marriage['Marriage_Status_Code'].map(marriage_status_mapping)

    fig = px.bar(default_customers_by_marriage, x='Marriage_Status', y='Count', labels={'Count': 'Jumlah Customer Gagal Bayar', 'Marriage_Status': 'Status Pernikahan'}) \
        .update_layout(title=f'Berdasarkan Status Pernikahan')
    
    return fig

def generateLimitPlot(status):
    credit_default_copy = credit_default.copy()

    if status == 'Gagal Bayar':
        default_customers = credit_default_copy[credit_default_copy['default payment next month'] == 1].copy()
    else:
        default_customers = credit_default_copy[credit_default_copy['default payment next month'] == 0].copy()

    bin_edges = np.arange(0, default_customers['LIMIT_BAL'].max() + 100000, 100000)
    bin_labels = ['{}ribu-{}ribu'.format(i, i + 99) for i in range(0, bin_edges[-1], 100000)]

    default_customers['Limit_Balance_Range'] = pd.cut(default_customers['LIMIT_BAL'], bins=bin_edges, labels=bin_labels, right=False)
    customer_count_by_range = default_customers.groupby('Limit_Balance_Range').size().reset_index(name='Customer_Count')

    fig = px.bar(customer_count_by_range, x='Limit_Balance_Range', y='Customer_Count', labels={'Customer_Count': 'Jumlah Customer', 'Limit_Balance_Range': 'Kredit Limit (per 100ribu)'}) \
        .update_layout(title=f'Berdasarkan Kredit Limit')
    
    return fig

def generateScatterLimitAgePlot(status):
    credit_default_copy = credit_default.copy()

    if status == 'Gagal Bayar':
        default_customers = credit_default_copy[credit_default_copy['default payment next month'] == 1].copy()
    else:
        default_customers = credit_default_copy[credit_default_copy['default payment next month'] == 0].copy()

    fig = px.scatter(default_customers, x='AGE', y='LIMIT_BAL', title='Hubungan Antara Umur dan Batas Kredit')

    return fig

def generatePlots(status):
    area_plot_gender_status = generateGenderPlot(status)
    area_plot_age_status = generateAgePlot(status)
    area_plot_edu_status = generateEducationPlot(status)
    area_plot_marriage_status = generateMarriagePlot(status)
    area_plot_limit_status = generateLimitPlot(status)
    area_plot_scatter_status = generateScatterLimitAgePlot(status)

    return (area_plot_gender_status, area_plot_age_status, area_plot_edu_status,
            area_plot_marriage_status, area_plot_limit_status, area_plot_scatter_status)

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
    left_column, right_column = st.columns([1, 2])
    with st.container(border=True):
        with left_column:
            status_option = st.radio(
                'Pilih Status',
                ("Gagal Bayar", "Tidak Gagal Bayar"))
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

with st.container(border=True):
    status_option1 = "Gagal Bayar"
    status_option1 = st.radio(
    'Pilih Status Customer',
    ("Gagal Bayar", "Tidak Gagal Bayar"))
    
    area_plots = generatePlots(status_option1)
    with st.container():
        if area_plots[0] is not None:
            st.markdown(f'#### Customer {status_option1}')
    
    left_column, right_column = st.columns(2)
    with st.container(border=True):
        
        with left_column:
            if area_plots[0] is not None:
                st.plotly_chart(area_plots[0])

        with right_column:
            if area_plots[1] is not None:
                st.plotly_chart(area_plots[1])

    with st.container(border=True):
        with left_column:
            if area_plots[2] is not None:
                st.plotly_chart(area_plots[2])

        with right_column:
            if area_plots[3] is not None:
                st.plotly_chart(area_plots[3])

    with st.container(border=True):
        with left_column:
            if area_plots[4] is not None:
                st.plotly_chart(area_plots[4])

        with right_column:
            if area_plots[5] is not None:
                st.plotly_chart(area_plots[5])
                
                