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
    st.markdown("- Predictive modeling for customer churn using machine learning techniques")
    st.markdown("- Exploratory data analysis on retail sales data to identify trends and insights")
    st.markdown("- Building a recommendation system using collaborative filtering")


    st.header("Interests")
    st.markdown("I am passionate about exploring new technologies and methodologies "
                "to enhance data-driven applications and contribute to meaningful projects.")

    st.header("Contact Me")
    st.markdown("Connect with me on [LinkedIn](https://www.linkedin.com/in/maudy-avianti/) or explore my projects on [GitHub](https://github.com/chocolatmint)")

if __name__ == '__main__':
    main()
