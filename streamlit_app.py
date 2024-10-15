import streamlit as st
import pandas as pd
import plotly.express as px

# Set page configuration
st.set_page_config(page_title="Modern Dashboard", layout="wide", page_icon="📊")

# Add some custom CSS for a modern feel
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
        font-family: 'Helvetica', sans-serif;
    }
    h1 {
        color: #333333;
        font-weight: bold;
    }
    .stButton button {
        background-color: #007BFF;
        color: white;
        font-size: 18px;
        border-radius: 10px;
    }
    .css-1aumxhk {
        background-color: #007BFF;
        color: white;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# Header
st.markdown("<h1 style='text-align: center;'>📊 Modern Interactive Dashboard</h1>", unsafe_allow_html=True)
st.markdown("### A Dashboard with an Interactive UI/UX Experience", unsafe_allow_html=True)

# Sidebar for navigation
st.sidebar.title("🔍 Explore the Data")
st.sidebar.markdown("Use the sidebar to navigate and filter data")

# Dummy DataFrame
df = pd.DataFrame({
    'Category': ['A', 'B', 'C', 'D'],
    'Values': [300, 500, 250, 400]
})

# Create a filter in the sidebar
category_filter = st.sidebar.multiselect("Select Category", df['Category'].unique())

# Apply filter
if category_filter:
    df = df[df['Category'].isin(category_filter)]

# Create the dashboard layout using columns
col1, col2 = st.columns(2)

# Column 1: Display a pie chart
with col1:
    st.markdown("### Data Breakdown (Pie Chart)")
    fig_pie = px.pie(df, values='Values', names='Category', title='Category Breakdown')
    fig_pie.update_traces(textinfo='percent+label')
    st.plotly_chart(fig_pie, use_container_width=True)

# Column 2: Display a bar chart
with col2:
    st.markdown("### Category Values (Bar Chart)")
    fig_bar = px.bar(df, x='Category', y='Values', color='Category', title='Values by Category')
    fig_bar.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(255,255,255,0.6)')
    st.plotly_chart(fig_bar, use_container_width=True)

# Interactive user input: Create a slider
st.markdown("### Adjust Values")
value_input = st.slider("Select a value for category A", min_value=100, max_value=600, step=50)

# Update the dataframe based on user input and replot
df.loc[df['Category'] == 'A', 'Values'] = value_input
st.markdown(f"**Updated Value for Category A:** {value_input}")

# Footer
st.markdown("---")
st.markdown("<h5 style='text-align: center;'>Built with ❤️ using Streamlit & Plotly</h5>", unsafe_allow_html=True)
