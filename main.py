import streamlit as st
from Pages.introduction import show_introduction
from Pages.analysis import show_analysis
from Pages.visualization import show_visualizations

# Sidebar function (kept common across all pages)
def show_sidebar():
    st.sidebar.markdown("""
        <style>
        .img-container {
            display: flex;
            justify-content: center;
        }
        .img-round {
            width: 200px;
            height: 200px;
        }
        </style>
        <div class="img-container">
            <img src="https://media.licdn.com/dms/image/v2/D4E03AQEekGrZuGuVsA/profile-displayphoto-shrink_800_800/profile-displayphoto-shrink_800_800/0/1672338334255?e=1731542400&v=beta&t=DeJAdHRm-lV4ofP6EVyvfJqNY5JYUbsA0qF8T3KBa_Q" class="img-round">
        </div>
        <br>
    """, unsafe_allow_html=True)

    st.sidebar.markdown("""
        <div style="line-height: 1.5; font-size: 20px; padding-bottom: 10px; text-align: center;">
            <u><strong>Author:</strong></u> <br>
            Willy DU <br>
            Willy.du@efrei.net
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.sidebar.columns([1, 4])
    with col1:
        st.image("Images/github.png", width=50)
    with col2:
        st.markdown("<div style='line-height: 3;'><a href='https://github.com/Willy-Du' target='_blank'><strong>GitHub</strong></a></div>", unsafe_allow_html=True)

    col3, col4 = st.sidebar.columns([1, 4])
    with col3:
        st.image("Images/linkedin.png")
    with col4:
        st.markdown("<div style='line-height: 3;'><a href='https://www.linkedin.com/in/willy-du-377037222/' target='_blank'><strong>LinkedIn</strong></a></div>", unsafe_allow_html=True)

# Main function for page navigation
def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Choose a Page:", ["Introduction", "Analysis", "Visualizations"])

    show_sidebar()

    if page == "Introduction":
        show_introduction()
    elif page == "Analysis":
        show_analysis()
    elif page == "Visualizations":
        show_visualizations()

if __name__ == "__main__":
    main()
