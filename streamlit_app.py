import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Set up Streamlit Page Configuration
st.set_page_config(
    page_title="Complex AI Dashboard",
    page_icon="📊",
    layout="wide"
)

# Custom CSS for styling the dashboard (dark theme)
st.markdown("""
    <style>
    .main {
        background-color: #1c1e21;
        color: white;
    }
    h1 {
        color: #F0F8FF;
        font-size: 2.5em;
        font-weight: bold;
        text-align: center;
    }
    .stSidebar {
        background-color: #292b2e;
        color: white;
    }
    .stButton button {
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
    }
    .stProgress {
        background-color: #4CAF50;
    }
    .css-1aumxhk {
        background-color: #007BFF;
        color: white;
        border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.title("🔍 AI & Data Dashboard")
st.sidebar.subheader("Navigation")
page = st.sidebar.radio("Select a Page", ["Home", "Data Analysis", "Statistics", "Model Training", "Predictions"])

# Dummy Data for Visuals
dummy_data = pd.DataFrame({
    'Month': ['January', 'February', 'March', 'April', 'May'],
    'Success Rate': [80, 85, 78, 88, 92],
    'Failure Rate': [20, 15, 22, 12, 8]
})

# Dummy Pie Chart Data
pie_chart_data = pd.DataFrame({
    'Category': ['Succeed', 'Fail', 'Exchange'],
    'Percentage': [75, 15, 10]
})

# Page Layout for each page
if page == "Home":
    st.markdown("## 🏠 Welcome to the **AI & Data Dashboard**")

    # Top-level KPIs
    kpi1, kpi2, kpi3 = st.columns(3)

    with kpi1:
        st.metric(label="Total Success", value="85%", delta="5%")
    
    with kpi2:
        st.metric(label="Total Exchange", value="45%", delta="-10%")
    
    with kpi3:
        st.metric(label="Total Failures", value="15%", delta="-2%")

    # Example Chart
    st.markdown("### Monthly Success and Failure Rates")
    fig = px.line(dummy_data, x='Month', y=['Success Rate', 'Failure Rate'], title="Success & Failure Over Time")
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        title_font_color="white"
    )
    st.plotly_chart(fig, use_container_width=True)

elif page == "Data Analysis":
    st.markdown("## 📊 Data Analysis Section")

    # Radar Chart
    radar_fig = go.Figure()
    radar_fig.add_trace(go.Scatterpolar(
        r=[850, 750, 650, 550, 450],
        theta=['Feb', 'Oct', 'Nov', 'Aug', 'Mar'],
        fill='toself',
        name='Data Exchange'
    ))
    radar_fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 1000])
        ),
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
    )
    st.markdown("### Departmental Data Sampling")
    st.plotly_chart(radar_fig, use_container_width=True)

elif page == "Statistics":
    st.markdown("## 📈 Data Statistics")

    # Bar Chart
    st.markdown("### Data Sampling per Day")
    days_data = pd.DataFrame({
        'Day': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
        'Sample Count': [300, 400, 350, 450, 380, 300, 200]
    })
    fig = px.bar(days_data, x='Day', y='Sample Count', title="Data Sampling by Day")
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        title_font_color="white"
    )
    st.plotly_chart(fig, use_container_width=True)

elif page == "Model Training":
    st.markdown("## 🧠 Train Your Machine Learning Model")

    uploaded_file = st.file_uploader("Upload your dataset (.csv)", type=["csv"])
    if uploaded_file:
        data = pd.read_csv(uploaded_file)
        st.write("### Uploaded Dataset")
        st.dataframe(data)

elif page == "Predictions":
    st.markdown("## 🔮 Predictions Section")
    st.write("Enter the features to generate predictions.")

    feature1 = st.number_input("Feature 1", min_value=0.0, max_value=10.0, step=0.1)
    feature2 = st.number_input("Feature 2", min_value=0.0, max_value=10.0, step=0.1)
    feature3 = st.number_input("Feature 3", min_value=0.0, max_value=10.0, step=0.1)
    feature4 = st.number_input("Feature 4", min_value=0.0, max_value=10.0, step=0.1)

    if st.button("Generate Prediction"):
        # You can link this to a trained model
        st.write("Prediction Results: Class 1")

# Footer
st.markdown("""
    <footer style='text-align:center; padding:10px;'>
        <p>Powered by Streamlit and Plotly</p>
    </footer>
    """, unsafe_allow_html=True)
