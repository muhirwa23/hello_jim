import streamlit as st
import pandas as pd
import plotly.express as px

# Set page configuration
st.set_page_config(page_title="Creative Streamlit App", layout="wide", page_icon=":sparkles:")

# Custom CSS for attractive design
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #6e8efb, #a777e3);
        color: white;
    }
    h1 {
        font-family: 'Verdana', sans-serif;
        font-size: 3em;
        font-weight: bold;
        color: #fff;
    }
    .sidebar .sidebar-content {
        background: linear-gradient(135deg, #a777e3, #6e8efb);
    }
    .css-1d391kg {
        background-color: rgba(0, 0, 0, 0.5);
    }
    </style>
    """, unsafe_allow_html=True)

# Header
st.markdown("<h1 style='text-align: center;'>Welcome to the Creative App 🌟</h1>", unsafe_allow_html=True)

# Sidebar for navigation
st.sidebar.markdown("## Explore the App")
options = st.sidebar.radio("Go to", ['Home', 'Interactive Data', 'About'])

# Home Page
if options == 'Home':
    st.markdown("<h3 style='text-align: center;'>A New Way to Experience Data 🎨</h3>", unsafe_allow_html=True)
    
    # Two Columns Layout for an Introduction
    col1, col2 = st.columns(2)
    with col1:
        st.image("https://source.unsplash.com/500x300/?creative,design", use_column_width=True)
        st.markdown("### Why Choose Us?")
        st.write("""
            - Interactive Data Visualizations
            - Dynamic User Input
            - Beautiful, Responsive Design
        """)
        
    with col2:
        st.image("https://source.unsplash.com/500x300/?innovation,tech", use_column_width=True)
        st.markdown("### Our Key Features")
        st.write("""
            - Real-time Analytics
            - Engaging User Experience
            - Intuitive Interface
        """)

# Interactive Data Page
elif options == 'Interactive Data':
    st.markdown("<h3>Analyze with Beautiful Visuals 📊</h3>", unsafe_allow_html=True)
    
    # Sample DataFrame
    df = pd.DataFrame({
        'Category': ['A', 'B', 'C', 'D'],
        'Values': [300, 150, 400, 250]
    })
    
    # Display DataFrame and Chart
    st.markdown("#### Data Overview:")
    st.dataframe(df)
    
    # Create interactive chart with Plotly
    fig = px.bar(df, x='Category', y='Values', title='Category vs Values', color='Category', text='Values')
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='white')
    
    st.plotly_chart(fig, use_container_width=True)

# About Page
elif options == 'About':
    st.markdown("<h3>About Us 💡</h3>", unsafe_allow_html=True)
    st.write("""
        This app is built to showcase a beautiful, functional interface while keeping the user experience simple.
        Created with [Streamlit](https://streamlit.io).
    """)
    st.video("https://www.youtube.com/watch?v=B2iAodr0fOo")

# Footer
st.markdown("---")
st.markdown("<h5 style='text-align: center;'>Made with ❤️ by Muhirwa Jean Bosco</h5>", unsafe_allow_html=True)
