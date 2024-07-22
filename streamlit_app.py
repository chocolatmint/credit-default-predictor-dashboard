import streamlit as st

pages = {
    "":[
        st.Page("pages/0_Home.py"),
        st.Page("pages/1_Analisis.py"),
        st.Page("pages/2_Prediksi.py")
    ],
    "About" : [
        st.Page("pages/3_About.py", title="Me"),
        st.Page("pages/4_Project.py", title="This Project")
    ],
}

pg = st.navigation(pages)
pg.run()

