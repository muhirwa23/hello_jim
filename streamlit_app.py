import streamlit as st
import numpy as np
import pandas as pd
import streamlit as st

# Set page configuration for a better first impression
st.set_page_config(page_title="HACK THE FUTURE", layout="wide", page_icon=":sparkles:")

# Customize the background color and text
st.markdown("""
    <style>
        .main {
            background-color: #f0f2f6;
        }
        .title h1 {
            font-size: 3em;
            font-weight: bold;
            color: #4B6587;
        }
        .header-text {
            font-size: 1.2em;
            color: #333;
        }
    </style>
    """, unsafe_allow_html=True)

# Create a stylish header
st.markdown("<div class='title'><h1>Welcome to My Beautiful App</h1></div>", unsafe_allow_html=True)

# Sidebar for user interaction
st.sidebar.header("Navigation")
st.sidebar.markdown("Use the following options to interact:")
page = st.sidebar.selectbox("Choose a page:", ["Home", "Analytics", "About"])

st.sidebar.markdown("## Other Settings")
if st.sidebar.checkbox("Show tips"):
    st.sidebar.markdown("Here are some tips on how to use the app...")

# Main layout
if page == "Home":
    st.markdown("<div class='header-text'><p>Explore the key features of our app below.</p></div>", unsafe_allow_html=True)
    
    # Create three columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.image("https://source.unsplash.com/400x300/?nature", use_column_width=True)
        st.markdown("### Feature 1")
        st.write("Lorem ipsum dolor sit amet, consectetur adipiscing elit.")
    
    with col2:
        st.image("https://source.unsplash.com/400x300/?tech", use_column_width=True)
        st.markdown("### Feature 2")
        st.write("Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.")
    
    with col3:
        st.image("https://source.unsplash.com/400x300/?business", use_column_width=True)
        st.markdown("### Feature 3")
        st.write("Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris.")
    
    # Create a section with a different layout
    st.markdown("---")
    st.markdown("### Detailed Analytics")
    col4, col5 = st.columns([1, 2])
    
    with col4:
        st.markdown("##### Key Metrics")
        st.metric(label="Visitors", value="1000", delta="5%")
        st.metric(label="Conversion Rate", value="4.5%", delta="0.3%")
        st.metric(label="Revenue", value="$1500", delta="10%")
    
    with col5:
        st.line_chart({"Sales": [100, 120, 150, 170, 200], "Expenses": [50, 60, 70, 90, 100]})
    
elif page == "Analytics":
    st.markdown("<div class='header-text'><p>Analyze key performance metrics in real-time.</p></div>", unsafe_allow_html=True)
    st.area_chart({"Data": [1, 3, 2, 4, 7, 6, 8]})
    
    st.bar_chart({"Category A": [5, 3, 8], "Category B": [6, 7, 3], "Category C": [4, 6, 5]})
    
elif page == "About":
    st.markdown("<div class='header-text'><p>Learn more about our project and its creators.</p></div>", unsafe_allow_html=True)
    st.write("""
        This app was built using [Streamlit](https://streamlit.io), a simple and powerful framework for building data apps.
        Our team is dedicated to creating intuitive and interactive user experiences with the latest technologies.
    """)

# Footer section
st.markdown("---")
st.markdown("<h5 style='text-align:center; color:gray;'>Made with ❤️ by [Your Name]</h5>", unsafe_allow_html=True)


