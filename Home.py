import streamlit as st

st.set_page_config(
    page_title="Credit Default Prediction",
    page_icon="🏠",
)

def main():
    st.title("Prediksi Default Kartu Kredit")

    st.image('images/cc.png', caption='Ilustrasi', width=int(0.25 * 1000))

    st.markdown(f'#### Latar Belakang')
    html_content = """
    <div style="text-align: justify;">
        Kartu kredit adalah alat bayar yang populer digunakan oleh masyarakat di Indonesia. Keuntungan utama yang ditawarkan dari penggunaan kartu kredit adalah pembayaran yang dapat dilakukan secara dicicil, sehingga pengguna kartu kredit lebih mudah membeli barang tanpa harus membayar sekaligus.  Hal ini sangat membantu bagi mereka yang ingin membeli barang dengan harga yang lebih tinggi atau melakukan pembelian yang <i>urgent</i> namun tidak memiliki dana yang cukup. Dengan adanya kartu kredit, masyarakat dapat memperoleh barang-barang dengan cepat dan membayarnya secara bertahap.
    </div>
    <div></div>
    <div style="text-align: justify;">
        Seiring dengan meningkatnya penggunaan kartu kredit, kemungkinan risiko gagal bayar (default) juga semakin meningkat. Hal ini menjadi perhatian serius bagi lembaga keuangan penyedia kartu kredit. Ketika seorang customer gagal membayar tagihan kartu kreditnya secara tepat waktu, tidak hanya merusak reputasi yang bersangkutan, hal ini juga mengakibatkan kerugian finansial bagi lembaga keuangan pemberi pinjaman.
    </div>
    <div></div>
    <div style="text-align: justify;">
        Proses existing untuk memantau dan mengelola risiko gagal bayar sudah dimiliki oleh lembaga keuangan. Proses tersebut biasanya dilakukan oleh seorang kredit analis, dengan melakukan analisis manual terhadap data customer, seperti riwayat pembayaran, jumlah tagihan, dan faktor lainnya, untuk menilai risiko kredit secara langsung berdasarkan pengalaman dan pengetahuan mereka. Akan tetapi, analisis manual sering kali memiliki keterbatasan dalam menangani data yang banyak dan kompleksitas yang semakin meningkat. Analisis manual dapat menjadi proses yang memakan waktu dan rentan terhadap <i>human error</i>, terutama saat harus mengolah jumlah data yang besar dengan cepat. Analisis manual juga memerlukan waktu yang cukup lama karena dilakukan oleh manusia, berbeda dengan pemrosesan secara otomatis yang bisa dilakukan dengan cepat oleh komputer.
    </div>
    """
    st.markdown(html_content, unsafe_allow_html=True)

    st.markdown(f'#### Sumber Data')
    html_content2 = """
    <div style="text-align: justify;">
        Projek ini akan menggunakan dataset yang diambil dari situs UCI dengan judul "<a href="https://archive.ics.uci.edu/dataset/350/default+of+credit+card+clients">Default of Credit Card Clients</a>". Dataset ini berasal dari sebuah lembaga keuangan di negara Taiwan pada tahun 2005.
    </div>
    <div></div>
    """
    st.markdown(html_content2, unsafe_allow_html=True)

    st.markdown(f'#### Disclaimer')
    html_content3 = """
    <div style="text-align: justify;">
        Kemungkinan terjadinya ketidak-relevanan hasil prediksi dapat terjadi dikarenakan dataset yang digunakan terlalu *outdated* dan berbeda dengan kondisi sosial-ekonomi yang ada di Indonesia, sehingga diperlukan analisis lebih lanjut jika pemodelan ini ingin diimplementasikan pada data kondisi masa kini di Indonesia.
    </div>
    <div></div>
    """
    st.markdown(html_content3, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
