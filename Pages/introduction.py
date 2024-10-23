import streamlit as st

def show_introduction():
    
    st.title("Portfolio Presentation 🎓")
    
    st.markdown("""
                <h2> 1. Data Visualization Project Introduction </h2>
                <h3>Who I am:</h3>
                <p> I am Willy DU, a <strong> Data Engineering student</strong> at <strong>EFREI PARIS PANTHEON ASSAS UNIVERSITE</strong>.
                This project is part of my acdemic journey, aiming to analyze the <strong> first-round results of the 2017 French Presidential Election</strong>.
                through data analysis and visualization.</p>

                <h3>Project Objective:</h3>
                <p>The main goal of this project is to provide an <strong>overview of the electoral results </strong> at the commune level in France using data visualization tools. The objectives include:</p>
                <ul>
                    <li> Understanding <strong>voter turnout</strong> (abstentions, valid votes, blank and null votes)</li>
                    <li>Analyzing the <strong>distribution of votes</strong> by candidate and by region/department.</li>
                    <li>Highlighting geographical trends through <strong>interactive maps</strong>.</li>
                </ul>

                <p> In this project, I have used <strong>Python</strong> and libraries such as <strong>Pandas</strong>, <strong>Matplotlib</strong>, <strong>Seaborn</strong>, and <strong>Folium</strong> to analyze and visualize the data.</p>

                <h2> 2. Work Approach </h2>
                <h3> Data Exploration and Preparation:</h3>
                <ul> 
                    <li> <strong> Data Sources:</strong>
                        <ul>
                            <li> The electoral results from the frist round of the 2017 French presidential election in a XLS file</li>
                            <li> A CSV file containing information about communes, departments, and regions for the longitude and latitude</li>
                        </ul>
                    </li>
                    <li> <strong> Data Cleaning:</strong> I removed irrelevant columns and merged both datasets to form a complete DataFrame that includes both
                    the electoral results and geographic information of the communes.</li>
                </ul>
                <h3> Data Analysis:</h3>
                <p>The data analysis is divided into several sections, each focusing on a specific aspect of the results:</p>
                <ul>
                    <li><strong>Voter Turnout:</strong> An analysis of the distribution of voter turnout across communes.</li>
                    <li><strong>Vote Distribution:</strong> Exploring the number of votes each candidate received.</li>
                    <li><strong>Geographical Analysis:</strong> Highlighting results by department and region using interactive maps.</li>
                </ul>
                
                <h3> Data Visualization:</h3>
                <p> The data visualization section includes:</p>
                <ul>
                    <li> <strong>Histograms</strong> to show the distribution of voter turnout.</li>
                    <li> <strong>Scatter plots</strong> to explore relationships between different variables.</li>
                    <li> <strong>Bar plots</strong> to compare results between departments.</li>
                    <li> <strong>Interactive maps</strong> to visualize geographical trends.</li>
                </ul>

                <h2> 3. Tools and Technologiuqes Used </h2>
                <ul>
                    <li> <strong> Python:</strong> Programming language used for data analysis and visualization.</li>
                    <li> <strong> Streamlit:</strong> Web application framework used to create the interactive dashboard.</li>
                    <li> <strong> Pandas:</strong> Library used for data manipulation and analysis.</li>
                    <li> <strong> Matplotlib:</strong> Library used for creating static, animated, and interactive visualizations in Python.</li>
                    <li> <strong> Seaborn:</strong> Data visualization library based on Matplotlib that provides a high-level interface for drawing attractive and informative statistical graphics.</li>
                    <li> <strong> Folium:</strong> Library used to create interactive maps in Python.</li>
                </ul>
    """, unsafe_allow_html=True)
