from pathlib import Path

import streamlit as st
import base64
from PIL import Image

# --- FUNCTION ---
def get_base64_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()

# --- PATH SETTINGS ---
current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
css_file = current_dir / "styles" / "main.css"
profile_pic = current_dir /"../images" / "avatar.jpeg"


# --- GENERAL SETTINGS ---
PAGE_TITLE = "About Me | Maudy N Avianti"
PAGE_ICON = ":wave:"
NAME = "Maudy Avianti"
DESCRIPTION = """
A software engineer with an interest in data
"""

linkedin_logo_path = "images/linkedin.png"
github_logo_path = "images/github.png"

linkedin_logo_base64 = get_base64_image(linkedin_logo_path)
github_logo_base64 = get_base64_image(github_logo_path)

linkedin_url = "https://www.linkedin.com/in/maudy-avianti/"
github_url = "https://github.com/chocolatmint"



st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON)


# --- LOAD CSS & PROFIL PIC ---
with open(css_file) as f:
    st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)
profile_pic = Image.open(profile_pic)


# --- HERO SECTION ---
col1, col2 = st.columns(2, gap="small")
with col1:
    st.image(profile_pic, width=230)

with col2:
    st.title(NAME)
    st.markdown(f'{DESCRIPTION}')
    st.markdown(f'Find me on:')

    cols_linkedin, cols_github, cols_other1, cols_other2 = st.columns(4)
    with cols_linkedin:
        st.markdown(
            f"""
                <a href="{['linkedin_url']}" target="_blank">
                    <img src="data:image/png;base64,{linkedin_logo_base64}" style="width:100%; height:20%">
                </a>
            """,
            unsafe_allow_html=True
        )
    
    with cols_github:
        st.markdown(
            f"""
                <a href="{['github_url']}" target="_blank">
                    <img src="data:image/png;base64,{github_logo_base64}" style="width:90%; height:20%">
                </a>
            """,
            unsafe_allow_html=True
        )

    with cols_other1:
        st.markdown(
            f"""
            """,
            unsafe_allow_html=True
        )
    
    with cols_other2:
        st.markdown(
            f"""
            """,
            unsafe_allow_html=True
        )


# --- EXPERIENCE & QUALIFICATIONS ---
st.write('\n')
st.subheader("Experience & Qulifications")
st.write(
    """
- ✔️ 6 years experience as backend developer
- ✔️ Strong hands on experience and knowledge in Java, Golang, Python, and R
- ✔️ Good understanding of statistical principles and their respective applications
- ✔️ Excellent team-player and displaying strong sense of initiative on tasks
"""
)


# --- SKILLS ---
st.write('\n')
st.subheader("Portofolios")
st.write(
    """
- [► Finding the Best Model for Predicting Survival on the Titanic: A Comparison of Logistic Regression and K-nearest neighbor (k-NN)](https://rpubs.com/maudy_avianti/1171557)
- [► Finding the Best Model for Predicting Survival on the Titanic: A Comparison of Naive Bayes, Decision Tree, and Random Forest](https://rpubs.com/maudy_avianti/1171310)
- [► Titanic Survivability Analysis](https://rpubs.com/maudy_avianti/titanic_survivability_analysis)
- [► Amazon Books Analysis](https://rpubs.com/maudy_avianti/amazon_books_analysis)
- [► World forest area dashboard](https://www.shinyapps.io/admin/#/application/11087290)
- [► Spotify daily chart dashboard](https://www.shinyapps.io/admin/#/application/11144834)
- ► SMS spam/ham prediction in Bahasa Indonesia (unpublished)
"""
)



with st.container():
    st.markdown(
        f'<div style="position: fixed; bottom: 10px; right: 10px; background-color: white; padding: 5px; border-radius: 5px; font-size: 12px;">Adapted from <a href="{"https://github.com/Sven-Bo/digital-resume-template-streamlit/tree/master"}" target="_blank">Template Source</a></div>',
        unsafe_allow_html=True
    )