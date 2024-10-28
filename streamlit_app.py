import streamlit as st
import pandas as pd
import plotly.express as px

# Set page configuration
st.set_page_config(
    page_title="Mental Health in Rwanda Dashboard",
    page_icon=":herb:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for styling
st.markdown(
    """
    <style>
    body {
        background-color: #f0f5f5;
        color: #2e4e4e;
    }
    .sidebar .sidebar-content {
        background-color: #d8eae6;
    }
    .stButton>button {
        background-color: #88bdbc;
        color: white;
    }
    .stButton>button:hover {
        background-color: #659b99;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Load data function
@st.cache_data
def load_data():
    # Replace with actual data loading logic
    data = pd.read_csv('data/mental_health_rwanda.csv')
    return data

data = load_data()

# Sidebar Navigation
st.sidebar.title("Navigation")
navigation = st.sidebar.radio("", ["Home", "Statistics", "Recommendations", "Resources"])

# Home Page
if navigation == "Home":
    st.title("Mental Health in Rwanda")
    st.markdown("### A Comprehensive Overview")
    st.image("images/rwanda_culture.jpg", use_column_width=True)
    st.markdown("""
    Welcome to the Mental Health in Rwanda Dashboard. This platform is dedicated to providing insightful data and resources to promote mental well-being across the country.
    """)
    st.markdown("#### Key Focus Areas")
    st.write("- **Awareness of Mental Health Challenges**")
    st.write("- **Accessibility of Treatment**")
    st.write("- **Support Systems Available**")

# Statistics Page
elif navigation == "Statistics":
    st.title("Mental Health Statistics")
    st.markdown("### Insightful Data Visualizations")
    
    # Prevalence Rates Over Years
    st.subheader("Prevalence Rates Over Years")
    fig1 = px.line(
        data,
        x='Year',
        y='Prevalence_Rate',
        color='Gender',
        labels={'Prevalence_Rate': 'Prevalence Rate (%)'},
        title='Mental Health Prevalence Rates by Gender'
    )
    st.plotly_chart(fig1, use_container_width=True)

    # Age and Gender Demographics
    st.subheader("Age and Gender Demographics")
    fig2 = px.bar(
        data,
        x='Age_Group',
        y='Count',
        color='Gender',
        barmode='group',
        title='Distribution by Age Group and Gender'
    )
    st.plotly_chart(fig2, use_container_width=True)

    # Treatment Accessibility
    st.subheader("Treatment Accessibility")
    fig3 = px.scatter(
        data,
        x='Region',
        y='Facilities_Count',
        size='Facilities_Count',
        color='Region',
        title='Mental Health Facilities Across Regions',
        labels={'Facilities_Count': 'Number of Facilities'}
    )
    st.plotly_chart(fig3, use_container_width=True)

# Recommendations Page
elif navigation == "Recommendations":
    st.title("Personalized Recommendations")
    st.markdown("### Find Resources Tailored to Your Needs")

    # User Interaction Simulation
    st.markdown("#### Please select your areas of interest:")
    interests = st.multiselect(
        "",
        options=["Anxiety", "Depression", "Stress Management", "PTSD", "Community Support", "Professional Counseling"]
    )

    # AI-Driven Recommendations Placeholder
    if interests:
        st.markdown("#### Recommended Resources:")
        for interest in interests:
            st.write(f"- **{interest} Support Programs**")
            st.write(f"  - Description: Comprehensive resources for managing {interest.lower()}.")
            st.write(f"  - [Learn More](#)")
    else:
        st.write("Select at least one interest to see recommendations.")

# Resources Page
elif navigation == "Resources":
    st.title("Support Resources")
    st.markdown("### Organizations and Contact Information")

    # List of Resources
    st.markdown("""
    - **Rwanda Mental Health Coalition**
        - Website: [www.rmhc.org.rw](https://www.rmhc.org.rw)
        - Contact: +250 123 456 789
    - **Ministry of Health - Mental Health Division**
        - Website: [www.moh.gov.rw/mentalhealth](https://www.moh.gov.rw/mentalhealth)
        - Hotline: 114
    - **Local Support Groups**
        - Find a support group in your area: [Support Groups Directory](#)
    """)

    # Emergency Contact
    st.markdown("#### **Emergency Assistance**")
    st.write("If you or someone you know is in crisis, please call the Mental Health Emergency Hotline:")
    st.write("**+250 987 654 321**")

# Footer
st.markdown("---")
st.markdown("""
<center>
    &copy; 2023 Mental Health in Rwanda Dashboard | 
    [Privacy Policy](#) | 
    [Terms of Service](#)
</center>
""", unsafe_allow_html=True)
