import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt

# Set up Streamlit Page Configuration
st.set_page_config(
    page_title="Unemployment in Youth - Rwanda",
    page_icon="📊",
    layout="wide"
)

# Custom CSS for Tailwind-inspired design and SVG icons
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
        padding: 10px 20px;
    }
    .metric-container {
        display: flex;
        justify-content: space-around;
        background-color: #292b2e;
        border-radius: 10px;
        padding: 20px;
    }
    .metric-box {
        background-color: #1a202c;
        padding: 15px;
        border-radius: 8px;
        text-align: center;
        width: 150px;
    }
    .metric-box h3 {
        font-size: 1.2em;
        margin-bottom: 5px;
    }
    .metric-box p {
        font-size: 1.5em;
        font-weight: bold;
    }
    .icon {
        width: 20px;
        height: 20px;
        margin-right: 10px;
        vertical-align: middle;
    }
    .footer {
        text-align: center;
        padding: 10px;
        color: white;
        font-size: 0.9em;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.title("🔍 Unemployment Dashboard")
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

# Tailwind CSS-inspired widgets for Metrics in Home Page
if page == "Home":
    st.markdown("## 🏠 Welcome to the **Unemployment in Youth - Rwanda Dashboard**")
    
    # KPI Metrics with Tailwind-inspired styling
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

    # Seaborn Visualization
    st.markdown("### Monthly Success and Failure Rates with Seaborn")
    
    sns.set_theme(style="darkgrid")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(data=dummy_data, x='Month', y='Success Rate', ax=ax, label="Success Rate", marker="o")
    sns.lineplot(data=dummy_data, x='Month', y='Failure Rate', ax=ax, label="Failure Rate", marker="x")
    ax.set_title("Success & Failure Rates Over Time", fontsize=16)
    st.pyplot(fig)

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

# Footer with SVG Icon
st.markdown("""
    <footer class='footer'>
        <p>Powered by Streamlit and Plotly with 💻 from Rwanda's Data Science Solutions</p>
    </footer>
    """, unsafe_allow_html=True)
