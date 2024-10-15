import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Set page config for a professional look
st.set_page_config(page_title="Outstanding Dashboard", page_icon="📊", layout="wide")

# CSS for custom animations and design
st.markdown("""
    <style>
    .main {
        background-color: #F5F7F9;
    }
    .stSidebar {
        background-color: #002B5B;
        color: white;
    }
    h1 {
        font-size: 2.5em;
        color: #002B5B;
        font-weight: bold;
        text-align: center;
    }
    .css-1aumxhk {
        background-color: #007BFF;
        color: white;
        border-radius: 8px;
    }
    .stButton button {
        background-color: #007BFF;
        color: white;
        border-radius: 5px;
    }
    .animate-fade {
        animation: fadeIn 2s ease-in-out;
    }
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.title("📊 Navigation")
page = st.sidebar.radio("Go to", ["Home", "Data Insights", "Trends", "Predictions"])

# Dummy DataFrame
df = pd.DataFrame({
    'Category': ['A', 'B', 'C', 'D', 'E'],
    'Values': [150, 450, 200, 300, 500]
})

# Dummy dataset for trends
time_series_data = pd.DataFrame({
    'Date': pd.date_range(start='1/1/2022', periods=100),
    'Value': [i**0.5 + (i/10) for i in range(100)]
})

# Header with animations
st.markdown("<h1 class='animate-fade'>📊 Outstanding Interactive Dashboard</h1>", unsafe_allow_html=True)

# Home Page Layout
if page == "Home":
    st.markdown("## Welcome to the **Home** Page")
    col1, col2 = st.columns(2)

    # Pie Chart
    with col1:
        st.markdown("### Category Breakdown")
        fig_pie = px.pie(df, values='Values', names='Category', title='Category Distribution')
        fig_pie.update_traces(textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)

    # Bar Chart
    with col2:
        st.markdown("### Category Values")
        fig_bar = px.bar(df, x='Category', y='Values', color='Category', title='Category Values')
        fig_bar.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(255,255,255,0.8)')
        st.plotly_chart(fig_bar, use_container_width=True)

elif page == "Data Insights":
    st.markdown("## **Data Insights** Page")
    
    # Data Summary
    st.write("### Data Overview")
    st.dataframe(df)

    # Animated Line Chart
    st.markdown("### Trends Over Time")
    fig_line = px.line(time_series_data, x='Date', y='Value', title='Time Series Data')
    fig_line.update_traces(line=dict(color='royalblue', width=3), marker=dict(size=8, symbol='circle'))
    st.plotly_chart(fig_line, use_container_width=True)

elif page == "Trends":
    st.markdown("## **Trends** Page")
    
    # Multi-chart layout
    col1, col2 = st.columns(2)

    # Box plot on left
    with col1:
        st.markdown("### Distribution of Values (Box Plot)")
        fig_box = px.box(df, x='Category', y='Values', color='Category', title='Category Distribution')
        st.plotly_chart(fig_box, use_container_width=True)

    # Scatter plot on right
    with col2:
        st.markdown("### Correlation of Categories")
        fig_scatter = px.scatter(df, x='Category', y='Values', color='Category', title='Category Correlation')
        st.plotly_chart(fig_scatter, use_container_width=True)

elif page == "Predictions":
    st.markdown("## **Predictions** Page")
    
    # Sample Prediction Chart using a basic model output
    st.markdown("### Predicted Future Values (Line Chart)")
    future_data = pd.DataFrame({
        'Date': pd.date_range(start='1/1/2023', periods=50),
        'Predicted Values': [i * 1.02 for i in range(50)]
    })
    
    fig_future = px.line(future_data, x='Date', y='Predicted Values', title="Predicted Future Trends")
    st.plotly_chart(fig_future, use_container_width=True)

# Footer
st.markdown("<h5 style='text-align: center;'>Built with ❤️ using Streamlit & React Components</h5>", unsafe_allow_html=True)
