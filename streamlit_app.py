import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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
page = st.sidebar.radio("Select a Page", ["Home", "Data Analysis", "Statistics", "Dynamic Charts", "Model Training", "Predictions"])

# Dummy Data for Visuals
dummy_data = pd.DataFrame({
    'Month': ['January', 'February', 'March', 'April', 'May'],
    'Success Rate': [80, 85, 78, 88, 92],
    'Failure Rate': [20, 15, 22, 12, 8],
    'Youth Employed': [500, 520, 480, 600, 630],
    'Unemployed': [50, 40, 60, 30, 25],
    'Region': ['North', 'South', 'East', 'West', 'Central']
})

# Home Page with Metrics
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

    # Line Chart for Success and Failure Rates
    st.markdown("### Monthly Success and Failure Rates")
    fig = px.line(dummy_data, x='Month', y=['Success Rate', 'Failure Rate'], markers=True)
    fig.update_layout(
        title="Success & Failure Rates Over Time",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        title_font_color="white"
    )
    st.plotly_chart(fig, use_container_width=True)

elif page == "Data Analysis":
    st.markdown("## 📊 Data Analysis Section")

    # Bubble Chart
    st.markdown("### Youth Employment vs Unemployment (Bubble Chart)")
    bubble_fig = px.scatter(
        dummy_data, x='Youth Employed', y='Unemployed', size='Youth Employed', color='Region',
        title="Youth Employed vs Unemployed by Region",
        hover_name="Region", size_max=60
    )
    bubble_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        title_font_color="white"
    )
    st.plotly_chart(bubble_fig, use_container_width=True)

    # Dynamic Pie Chart Animation (Change Over Time)
    st.markdown("### Unemployment Status Over Time (Animated Pie Chart)")
    pie_animation_fig = px.pie(
        dummy_data, values='Unemployed', names='Month', title="Unemployment Distribution by Month",
        color_discrete_sequence=px.colors.sequential.RdBu, hole=0.4
    )
    pie_animation_fig.update_traces(textinfo='percent+label')
    pie_animation_fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        title_font_color="white"
    )
    st.plotly_chart(pie_animation_fig, use_container_width=True)

elif page == "Statistics":
    st.markdown("## 📈 Data Statistics")

    # Heatmap for Correlation
    st.markdown("### Correlation Heatmap of Employment Data")
    heatmap_data = dummy_data[['Success Rate', 'Failure Rate', 'Youth Employed', 'Unemployed']].corr()
    heatmap_fig = px.imshow(heatmap_data, text_auto=True, title="Correlation Heatmap")
    heatmap_fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        title_font_color="white"
    )
    st.plotly_chart(heatmap_fig, use_container_width=True)

    # Scatter Plot with Trend Line
    st.markdown("### Scatter Plot of Youth Employed vs Unemployment")
    scatter_fig = px.scatter(dummy_data, x='Youth Employed', y='Unemployed', trendline="ols",
                             title="Scatter Plot with Trendline for Unemployment vs Youth Employed")
    scatter_fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        title_font_color="white"
    )
    st.plotly_chart(scatter_fig, use_container_width=True)

elif page == "Dynamic Charts":
    st.markdown("## 📊 Dynamic Visuals")

    # Treemap for Hierarchical Representation
    st.markdown("### Treemap of Youth Employment by Region")
    treemap_fig = px.treemap(dummy_data, path=['Region'], values='Youth Employed', title="Treemap of Employment by Region")
    treemap_fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        title_font_color="white"
    )
    st.plotly_chart(treemap_fig, use_container_width=True)

    # Box Plot for Data Spread Analysis
    st.markdown("### Box Plot of Success and Failure Rates")
    box_fig = px.box(dummy_data, y=['Success Rate', 'Failure Rate'], title="Box Plot of Success & Failure Rates")
    box_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        title_font_color="white"
    )
    st.plotly_chart(box_fig, use_container_width=True)

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

    # Feature inputs for predictions
    feature1 = st.number_input("Feature 1", min_value=0.0, max_value=10.0, step=0.1)
    feature2 = st.number_input("Feature 2", min_value=0.0, max_value=10.0, step=0.1)
    feature3 = st.number_input("Feature 3", min_value=0.0, max_value=10.0, step=0.1)
    feature4 = st.number_input("Feature 4", min_value=0.0, max_value=10.0, step=0.1)

    # Placeholder for prediction output
    if st.button("Generate Prediction"):
        # Placeholder for linking to a trained model
        st.write("Prediction Results: Class 1")

# Footer with SVG Icon
st.markdown("""
    <footer class='footer'>
        <p>Powered by Streamlit and Plotly with 💻 from Rwanda's Data Science Solutions</p>
    </footer>
    """, unsafe_allow_html=True)
