import base64
import streamlit as st

st.set_page_config(
    page_title="About This Project",
    page_icon=":wave:",
    layout="wide",
)

def get_base64_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()

st.title("Prediksi Default Kartu Kredit")

st.markdown(
    f"""
    <div style="justify-content: center;">
        <a href="{['github_url']}" target="_blank">
            <img src="data:image/png;base64,{get_base64_image("images/cc.png")}" style="width:30%; height:20%">
        </a>
    </div>
    """,
    unsafe_allow_html=True
)

html_content = """
<div style="text-align: justify;">
    Kartu kredit memudahkan pembayaran dengan skema cicilan, membantu pembelian barang mahal atau mendesak. Namun, jika risiko gagal bayar meningkat dapat merugikan lembaga keuangan. Analisis manual kredit analis terhadap data customer untuk menilai risiko memiliki keterbatasan, rentan <i>human error</i>, dan memakan waktu. Diperlukan cara lain dalam melakukan analisis; salah satunya dengan menggunakan machine learning.
</div>
"""
st.markdown(html_content, unsafe_allow_html=True)

st.markdown(f'#### Sumber Data')
html_content2 = """
<div style="text-align: justify;">
    Dataset diambil dari <a href="https://archive.ics.uci.edu/dataset/350/default+of+credit+card+clients">UCI</a>, berasal dari lembaga keuangan di Taiwan pada 2005.
</div>
"""
st.markdown(html_content2, unsafe_allow_html=True)

st.markdown(f'#### Disclaimer')
html_content3 = """
<div style="text-align: justify;">
    Hasil prediksi mungkin kurang relevan karena dataset lama dan kondisi sosial-ekonomi berbeda, sehingga perlu analisis lebih lanjut untuk data kondisi Indonesia saat ini.
</div>
"""
st.markdown(html_content3, unsafe_allow_html=True)
