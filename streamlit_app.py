import streamlit as st
import plotly.express as px
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
import numpy as np

# Set the page configuration with modern layout and design
st.set_page_config(page_title="AI-Powered Dashboard", layout="wide", initial_sidebar_state="expanded")

# Add a sleek and modern style to the dashboard
st.markdown("""
    <style>
        body {background-color: #f0f2f6;}
        .css-1d391kg {color: #fff; background-color: #0047AB;}
        .stSelectbox [data-baseweb="select"] {background-color: #1f3b57;}
        .css-12oz5g7 {box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.1);}
        .sidebar .css-1v3fvcr {background-color: #101820FF;}
    </style>
""", unsafe_allow_html=True)

# Sidebar for navigation
with st.sidebar:
    st.title("🔮 AI Dashboard")
    st.markdown("## Navigation")
    nav_option = st.selectbox("Choose Page", ["Home", "Data Analysis", "Model Training", "Model Predictions", "Customize Dashboard"])

# Load the Iris dataset for analysis and model training
data = load_iris()
df = pd.DataFrame(data.data, columns=data.feature_names)
target = pd.Series(data.target)

# Grid layout for responsive design
col1, col2 = st.columns([2, 1])

# Home Page
if nav_option == "Home":
    st.title("Welcome to the AI-Powered Dashboard! 🌟")
    st.write("This is a cutting-edge platform integrating advanced machine learning models and data visualization tools.")
    st.image("https://via.placeholder.com/700x300", use_column_width=True)

# Data Analysis Page
elif nav_option == "Data Analysis":
    st.subheader("📊 Data Analysis")
    with col1:
        fig = px.scatter(df, x="sepal length (cm)", y="sepal width (cm)", color=target, title="Iris Dataset - Sepal Length vs Width")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.write("**Data Preview**")
        st.dataframe(df.head())

# Model Training Page
elif nav_option == "Model Training":
    st.subheader("🤖 Train Your Model")
    X = df
    y = target
    model = RandomForestClassifier(n_estimators=100)
    model.fit(X, y)
    st.success("Model Trained Successfully!")
    
    st.write("### Feature Importance")
    feature_importance = pd.Series(model.feature_importances_, index=X.columns)
    st.bar_chart(feature_importance)

# Model Predictions Page
elif nav_option == "Model Predictions":
    st.subheader("📈 Make Predictions")
    sepal_len = st.slider("Sepal Length", min_value=0.0, max_value=8.0, value=5.0)
    sepal_wid = st.slider("Sepal Width", min_value=0.0, max_value=5.0, value=3.0)
    input_data = np.array([[sepal_len, sepal_wid, 1.4, 0.2]])
    
    prediction = model.predict(input_data)
    st.write(f"The predicted class is: **{prediction[0]}**")

# Customize Dashboard Page
elif nav_option == "Customize Dashboard":
    st.subheader("🎨 Customize Your Dashboard")
    
    # Dark Mode Toggle
    dark_mode = st.checkbox("Enable Dark Mode")
    
    if dark_mode:
        st.markdown("""
            <style>
                body {background-color: #1E1E1E; color: #F5F5F5;}
                .css-1d391kg {color: #fff; background-color: #222;}
                .stSelectbox [data-baseweb="select"] {background-color: #333;}
                .stDataFrame, .stBarChart, .stPlotlyChart, .stSlider {background-color: #333; color: #FFF;}
            </style>
        """, unsafe_allow_html=True)
        st.write("**Dark mode enabled!**")

    # Widget Resizing Options
    st.write("Drag-and-drop layout feature coming soon...")

# Footer with modern branding
st.markdown("""
    <footer style='text-align: center; color: #999; margin-top: 30px;'>
        <p>Built with ❤️ using Streamlit | Powered by AI</p>
    </footer>
""", unsafe_allow_html=True)
