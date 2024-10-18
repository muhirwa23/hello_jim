import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer  # Hugging Face imports
# Set up Streamlit Page Configuration
st.set_page_config(
    page_title="Unemployment in Youth - Rwanda",
    page_icon="📊",
    layout="wide"
)
# Load Hugging Face Text-Generation Model
@st.cache(allow_output_mutation=True)
def load_hugging_face_model():
    # Load pre-trained GPT-2 model and tokenizer
    model = AutoModelForCausalLM.from_pretrained("gpt2")  # Use gpt2 for Causal LM
    tokenizer = AutoTokenizer.from_pretrained("gpt2")
    pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)
    return pipe
# Load the model for the app
hugging_face_model = load_hugging_face_model()

# Custom CSS for UI
st.markdown("""
    <style>
    .main { background-color: #1c1e21; color: white; }
    h1 { color: #F0F8FF; font-size: 2.5em; font-weight: bold; text-align: center; }
    .footer { text-align: center; padding: 10px; color: white; font-size: 0.9em; }
    </style>
    """, unsafe_allow_html=True)

# Simulated Dataset for Unemployment
np.random.seed(42)
regions = ['North', 'South', 'East', 'West', 'Central']
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

simulated_data = pd.DataFrame({
    'Month': np.random.choice(months, 100),
    'Region': np.random.choice(regions, 100),
    'Youth Employed': np.random.randint(300, 1000, size=100),
    'Unemployed': np.random.randint(50, 200, size=100),
    'Success Rate': np.random.uniform(60, 90, size=100),
    'Failure Rate': np.random.uniform(10, 40, size=100)
})

# Sidebar Navigation
st.sidebar.title("🔍 Unemployment Dashboard")
st.sidebar.subheader("Navigation")
page = st.sidebar.radio("Select a Page", ["Home", "Data Analysis", "Statistics", "Dynamic Charts", "Model Training", "AI-Powered Insights"])

# Home Page with AI-Suggested Insights
if page == "Home":
    st.markdown("## 🏠 Welcome to the **Unemployment in Youth - Rwanda Dashboard**")
    
    st.markdown("### AI-Powered Insights for the Latest Trends")
    
    # User can ask AI questions
    user_query = st.text_input("Ask AI any questions about unemployment data, trends, or predictions:")
    
    if user_query:
        with st.spinner('CognitivessAI is thinking...'):
            # Use Hugging Face pipeline to generate response
            ai_response = hugging_face_model(user_query, max_length=100)[0]['generated_text']
            st.markdown(f"**AI Response:** {ai_response}")
    
    # Tabs for Multiple Charts
    tab1, tab2, tab3 = st.tabs(["📊 KPI Metrics", "📈 Employment Trends", "🗺️ Regional Insights"])

    # Tab 1: KPI Metrics
    with tab1:
        st.markdown("<div class='metric-container'>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("""
                <div class="metric-box">
                    <img src="https://img.icons8.com/ios-filled/50/FFFFFF/employment.png" class="icon"/>
                    <h3>Total Employed</h3>
                    <p>85%</p>
                </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
                <div class="metric-box">
                    <img src="https://img.icons8.com/ios-filled/50/FFFFFF/exchange.png" class="icon"/>
                    <h3>Total Exchange</h3>
                    <p>45%</p>
                </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown("""
                <div class="metric-box">
                    <img src="https://img.icons8.com/ios-filled/50/FFFFFF/error.png" class="icon"/>
                    <h3>Total Failures</h3>
                    <p>15%</p>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # Tab 2: Employment Trends with Line Charts
    with tab2:
        st.markdown("### Monthly Success and Failure Rates")
        num_months = st.slider("Select number of months to display", min_value=3, max_value=12, value=6)
        displayed_data = simulated_data[simulated_data['Month'].isin(months[:num_months])]

        fig = px.line(displayed_data, x='Month', y=['Success Rate', 'Failure Rate'], markers=True)
        fig.update_layout(
            title="Success & Failure Rates Over Time",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            title_font_color="white"
        )
        st.plotly_chart(fig, use_container_width=True)

    # Tab 3: Regional Insights with Map
    with tab3:
        st.markdown("### Map of Unemployment by Region")
        region_coordinates = {
            'North': [1.9403, 29.8739],
            'South': [2.2833, 30.4141],
            'East': [1.9577, 30.4735],
            'West': [1.5797, 29.3508],
            'Central': [1.9456, 30.0586]
        }

        unemployment_map_data = simulated_data.groupby('Region').mean().reset_index()
        unemployment_map_data['lat'] = unemployment_map_data['Region'].map(lambda x: region_coordinates[x][0])
        unemployment_map_data['lon'] = unemployment_map_data['Region'].map(lambda x: region_coordinates[x][1])

        fig_map = px.scatter_mapbox(
            unemployment_map_data, lat="lat", lon="lon", hover_name="Region", size="Unemployed", color="Region",
            hover_data={"lat": False, "lon": False}, zoom=6, height=400
        )
        fig_map.update_layout(mapbox_style="open-street-map")
        fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, paper_bgcolor='rgba(0,0,0,0)', font_color='white')
        st.plotly_chart(fig_map, use_container_width=True)

# Data Analysis Page with Dynamic Widgets and AI Summary
elif page == "Data Analysis":
    st.markdown("## 📊 Data Analysis Section")

    selected_region = st.selectbox("Select a Region", regions)
    filtered_data = simulated_data[simulated_data['Region'] == selected_region]

    st.markdown("### Youth Employment vs Unemployment by Region")
    bubble_fig = px.scatter(
        filtered_data, x='Youth Employed', y='Unemployed', size='Youth Employed', color='Month',
        title=f"Youth Employed vs Unemployed in {selected_region}", hover_name="Month", size_max=60
    )
    bubble_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color='white', title_font_color="white"
    )
    st.plotly_chart(bubble_fig, use_container_width=True)

    # AI-generated summary of data
    st.markdown("### AI Summary of Data Insights")
    data_summary = hugging_face_model(f"Summarize the unemployment and employment trends in {selected_region}", max_length=100)[0]['generated_text']
    st.markdown(f"**AI's Summary:** {data_summary}")

# AI-Powered Insights Page
elif page == "AI-Powered Insights":
    st.markdown("## 🤖 AI-Powered Insights by CognitivessAI")
    
    st.markdown("### Ask Questions About the Dataset")
    user_query = st.text_input("Ask CognitivessAI any questions about the dataset, trends, or predictions:")
    
    if user_query:
        with st.spinner('CognitivessAI is analyzing...'):
            ai_response = hugging_face_model(user_query, max_length=150)[0]['generated_text']
            st.markdown(f"**AI's Response:** {ai_response}")

# Footer with Recommendations
st.markdown("""
    <div class='footer'>
        <p>Dashboard designed and developed for data insights on youth unemployment.</p>
        <p>Key Recommendations:</p>
        <ul>
            <li>Focus on improving job creation in regions with high unemployment.</li>
            <li>Invest in skill development programs for the youth.</li>
            <li>Encourage entrepreneurship to reduce reliance on formal employment.</li>
        </ul>
        <p>© 2024 Unemployment Insights | All rights reserved.</p>
    </div>
    """, unsafe_allow_html=True)
