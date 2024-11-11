import streamlit as st
import pandas as pd
import plotly.express as px
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import random
import numpy as np

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
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #d8eae6;
        color: #2e4e4e;
        text-align: center;
        padding: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Function to simulate realistic data
@st.cache_data
def simulate_data():
    years = list(range(2015, 2024))
    genders = ['Male', 'Female']
    age_groups = ['18-25', '26-35', '36-45', '46-60', '60+']
    regions = ['Kigali', 'Northern', 'Southern', 'Eastern', 'Western']
    
    data = []
    for year in years:
        for gender in genders:
            prevalence_rate = round(random.uniform(5, 20), 2)  # Prevalence rate between 5% and 20%
            data.append({
                'Year': year,
                'Gender': gender,
                'Prevalence_Rate': prevalence_rate
            })
    
    prevalence_df = pd.DataFrame(data)
    
    # Age and Gender Demographics
    demographics_data = []
    for age in age_groups:
        for gender in genders:
            count = random.randint(100, 1000)
            demographics_data.append({
                'Age_Group': age,
                'Gender': gender,
                'Count': count
            })
    demographics_df = pd.DataFrame(demographics_data)
    
    # Treatment Accessibility
    facilities_data = []
    for region in regions:
        facilities_count = random.randint(5, 50)
        facilities_data.append({
            'Region': region,
            'Facilities_Count': facilities_count
        })
    facilities_df = pd.DataFrame(facilities_data)
    
    # Merge all data for visualization purposes
    merged_df = prevalence_df.copy()
    merged_df = merged_df.merge(demographics_df, how='left', on='Gender')
    merged_df = merged_df.merge(facilities_df, how='left', on='Region')
    
    return prevalence_df, demographics_df, facilities_df

# Load simulated data
prevalence_df, demographics_df, facilities_df = simulate_data()

# Load AI Model with caching
@st.cache_resource
def load_model():
    try:
        tokenizer = AutoTokenizer.from_pretrained("tiiuae/falcon-mamba-7b")
        model = AutoModelForCausalLM.from_pretrained(
            "tiiuae/falcon-mamba-7b",
            device_map="auto",
            torch_dtype=torch.float16,
            low_cpu_mem_usage=True
        )
        return tokenizer, model
    except Exception as e:
        st.error(f"Error loading AI model: {e}")
        return None, None

# Load the AI model (this may take time and requires sufficient resources)
tokenizer, model = load_model()

# Sidebar Navigation
st.sidebar.title("Navigation")
navigation = st.sidebar.radio("", ["Home", "Statistics", "Recommendations", "Resources"])

# Home Page
if navigation == "Home":
    st.title("Mental Health in Rwanda")
    st.markdown("### A Comprehensive Overview")
    st.image("https://images.unsplash.com/photo-1529070538774-1843cb3265df?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80", use_column_width=True)
    st.markdown("""
    Welcome to the Mental Health in Rwanda Dashboard. This platform is dedicated to providing insightful data and resources to promote mental well-being across the country.
    """)
    st.markdown("#### Key Focus Areas")
    st.markdown("""
    - **Awareness of Mental Health Challenges**
    - **Accessibility of Treatment**
    - **Support Systems Available**
    """)

# Statistics Page
elif navigation == "Statistics":
    st.title("Mental Health Statistics")
    st.markdown("### Insightful Data Visualizations")
    
    # Prevalence Rates Over Years
    st.subheader("Prevalence Rates Over Years")
    fig1 = px.line(
        prevalence_df,
        x='Year',
        y='Prevalence_Rate',
        color='Gender',
        markers=True,
        labels={'Prevalence_Rate': 'Prevalence Rate (%)'},
        title='Mental Health Prevalence Rates by Gender (2015-2023)'
    )
    st.plotly_chart(fig1, use_container_width=True)

    # Age and Gender Demographics
    st.subheader("Age and Gender Demographics")
    fig2 = px.bar(
        demographics_df,
        x='Age_Group',
        y='Count',
        color='Gender',
        barmode='group',
        labels={'Count': 'Number of Individuals'},
        title='Distribution by Age Group and Gender'
    )
    st.plotly_chart(fig2, use_container_width=True)

    # Treatment Accessibility
    st.subheader("Treatment Accessibility")
    fig3 = px.scatter(
        facilities_df,
        x='Region',
        y='Facilities_Count',
        size='Facilities_Count',
        color='Region',
        title='Mental Health Facilities Across Regions',
        labels={'Facilities_Count': 'Number of Facilities'},
        hover_data=['Facilities_Count']
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
        options=[
            "Anxiety", 
            "Depression", 
            "Stress Management", 
            "PTSD", 
            "Community Support", 
            "Professional Counseling"
        ]
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
    
    st.markdown("---")
    st.markdown("### Chat with Our AI Support")
    st.markdown("#### *Please note: This AI provides general information and support. For personalized advice, please consult a mental health professional.*")
    
    if tokenizer and model:
        user_input = st.text_input("How can I assist you today?")
        if st.button("Send"):
            if user_input.strip() != "":
                with st.spinner("Generating response..."):
                    try:
                        inputs = tokenizer(user_input, return_tensors="pt").to(model.device)
                        outputs = model.generate(
                            **inputs,
                            max_length=500,
                            do_sample=True,
                            top_p=0.95,
                            top_k=60
                        )
                        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
                        st.success("AI Response:")
                        st.write(response)
                    except Exception as e:
                        st.error(f"Error generating response: {e}")
            else:
                st.warning("Please enter a message to send.")
    else:
        st.warning("AI model is not available at the moment.")

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
        - Find a support group in your area: [Support Groups Directory](https://www.rmhc.org.rw/support-groups)
    """)

    # Emergency Contact
    st.markdown("#### **Emergency Assistance**")
    st.write("If you or someone you know is in crisis, please call the Mental Health Emergency Hotline:")
    st.write("**+250 987 654 321**")

# Footer
st.markdown(
    """
    <div class="footer">
        &copy; 2024 Mental Health in Rwanda Dashboard | 
        <a href="#">Privacy Policy</a> | 
        <a href="#">Terms of Service</a>
    </div>
    """,
    unsafe_allow_html=True
)
