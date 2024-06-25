import streamlit as st

def main():
    st.title("Hi!")
    st.markdown("Nice to meet you, I'm Maudy.")
    st.markdown("I am a software engineer with an interest in data. "
                "I enjoy building applications that leverage data to solve problems "
                "and improve decision-making processes.")

    st.header("Skills")
    st.markdown("- **Programming**: Java, Golang, Python, R")
    st.markdown("- **Data Analysis**: Manipulating and visualizing data")
    st.markdown("- **Software Development**: Building scalable applications")

    st.header("Data Science Projects")
    st.markdown("Here are a few projects I've worked on:")
    st.markdown("- [Finding the Best Model for Predicting Survival on the Titanic: A Comparison of Logistic Regression and K-nearest neighbor (k-NN)](https://rpubs.com/maudy_avianti/1171557)")
    st.markdown("- [Finding the Best Model for Predicting Survival on the Titanic: A Comparison of Naive Bayes, Decision Tree, and Random Forest](https://rpubs.com/maudy_avianti/1171310)")
    st.markdown("- [Titanic Survivability Analysis](https://rpubs.com/maudy_avianti/titanic_survivability_analysis)")
    st.markdown("- [Amazon Books Analysis](https://rpubs.com/maudy_avianti/amazon_books_analysis)")   
    st.markdown("- [World forest area dashboard](https://www.shinyapps.io/admin/#/application/11087290)")
    st.markdown("- [Spotify daily chart dashboard](https://www.shinyapps.io/admin/#/application/11144834)")
    st.markdown("- SMS spam/ham prediction in Bahasa Indonesia")


    st.header("Interests")
    st.markdown("I am passionate about exploring new technologies and methodologies "
                "to enhance data-driven applications and contribute to meaningful projects.")

    st.header("Contact Me")
    st.markdown("Connect with me on [LinkedIn](https://www.linkedin.com/in/maudy-avianti/) or explore my projects on [GitHub](https://github.com/chocolatmint)")

if __name__ == '__main__':
    main()
