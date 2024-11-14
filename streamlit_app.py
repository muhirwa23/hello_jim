# Import necessary libraries
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import requests
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import datetime
from textblob import TextBlob
import nltk
from wordcloud import WordCloud
import os
from groq import Groq
import time

# Download NLTK data (if not already downloaded)
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

# Set page configuration
st.set_page_config(
    page_title="Rwanda Mental Health Dashboard",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Sidebar Language Support & Custom Styling
def set_language():
    if 'language' not in st.session_state:
        st.session_state['language'] = 'English'
    lang = st.sidebar.selectbox("Choose Language / Hitamo Ururimi", ["English", "Kinyarwanda"], index=0)
    st.session_state['language'] = lang

# Define translations for localization
def _(text):
    translations = {
        "Welcome to the Rwanda Mental Health Dashboard": "Murakaza neza kuri Dashboard y'Ubuzima bwo mu Mutwe mu Rwanda",
        "This dashboard provides insights into the mental health of Rwandan youth. Explore data visualizations, predictive modeling, and engage with our interactive chatbot.":
            "Iyi dashboard itanga ishusho y'ubuzima bwo mu mutwe bw'urubyiruko rw'u Rwanda. Reba ibigaragara mu mibare, gutekereza ku byashoboka, no gukoresha chatbot yacu.",
        # Additional translations
    }
    return translations.get(text, text) if st.session_state.get('language') == "Kinyarwanda" else text

# Apply custom CSS for a refined UI like Tableau
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .css-1d391kg { width: 300px; }
    .stButton>button { color: white; background-color: #FF6B6B; border-radius: 5px; height: 50px; width: 100%; font-size: 18px; }
    .stProgress > div > div > div > div { background-color: #FF6B6B; }
    h1, h2, h3, h4 { color: #2F4F4F; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
    .sidebar-header { font-size: 20px; color: #2F4F4F; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

# Data Loading
@st.cache_data  # Efficient data caching
def load_data():
    # Update with paths
    youth_health_data = pd.read_csv("youth_health_data_expanded (1).csv")  
    mental_health_data = pd.read_csv("mental_health_indicators_rwa (1).csv")  
    dhs_data = pd.read_csv("dhs_data.csv")  
    general_population_data = pd.read_csv("general_population_data.csv")  
    mental_health_youth_data = pd.read_csv("mental_health_data_rwanda_youth.csv")  
    return youth_health_data, mental_health_data, dhs_data, general_population_data, mental_health_youth_data

youth_health_data, mental_health_data, dhs_data, general_population_data, mental_health_youth_data = load_data()

# Sidebar navigation with Menu
set_language()
menu_options = [
    _("Home"),
    _("Data Visualization"),
    _("Predictive Modeling"),
    _("Chatbot"),
    _("Community Forum"),
    _("Contact Professionals")
]
menu_icons = ["house", "bar-chart", "cpu", "chat-dots", "people", "telephone"]

selected_option = option_menu(
    menu_title=_("Main Menu"),
    options=menu_options,
    icons=menu_icons,
    menu_icon="cast",
    default_index=0,
    styles={
        "container": {"padding": "0!important", "background-color": "#f0f2f6"},
        "icon": {"color": "#FF6B6B", "font-size": "18px"},
        "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px", "--hover-color": "#e0e0e0"},
        "nav-link-selected": {"background-color": "#FF6B6B"},
    },
)

# Add Sidebar with Tips and Contacts
st.sidebar.header("📚 " + _("Resources"))
with st.sidebar.expander(_("Hotlines and Contacts")):
    st.markdown("""
        - **Rwanda Mental Health Hotline**: 1234
        - **Online Resources**:
          - [Ministry of Health Rwanda](https://www.moh.gov.rw)
          - [WHO Mental Health](https://www.who.int/mental_health/en/)
    """)
st.sidebar.header("💡 " + _("Daily Tip"))
tips = [
    _("Take a short walk to clear your mind."),
    _("Practice deep breathing exercises."),
    _("Reach out to a friend or family member."),
    _("Write down your thoughts in a journal."),
    _("Try a new hobby or activity."),
    _("Maintain a balanced diet and stay hydrated."),
]
tip = np.random.choice(tips)
st.sidebar.info(f"**{_('Tip')}:** {tip}")

# Home Page Section
def home():
    st.title("🧠 " + _("Mental Health Dashboard for Rwandan Youth"))
    st.markdown("### " + _("Welcome to the Mental Health Dashboard"))
    st.markdown(_("This dashboard provides insights into the mental health of Rwandan youth. Explore data visualizations, predictive modeling, and engage with our interactive chatbot."))
    st.image("https://www.who.int/images/default-source/mca/mca-covid-image-hi-res.jpg", use_column_width=True)
    st.markdown(_("Navigate through the sidebar to explore different sections of the dashboard."))

# Enhanced Data Visualization Section
def data_visualization(youth_data, mental_data, dhs_data, gen_pop_data, mental_youth_data):
    st.header("📊 " + _("Data Visualization"))
    
    # Gender Distribution - Youth Health Data
    if 'Gender' in youth_data.columns:
        st.subheader(_("Gender Distribution"))
        gender_counts = youth_data['Gender'].value_counts()
        fig = px.pie(names=gender_counts.index, values=gender_counts.values, color=gender_counts.index, hole=0.5)
        fig.update_layout(margin=dict(l=10, r=10, t=50, b=10))
        st.plotly_chart(fig, use_container_width=True)

    # Age Distribution - General Population Data
    if 'Age' in gen_pop_data.columns:
        st.subheader(_("Age Distribution - General Population"))
        fig = px.histogram(gen_pop_data, x='Age', nbins=20, title=_("Age Distribution of General Population"))
        fig.update_layout(margin=dict(l=10, r=10, t=50, b=10))
        st.plotly_chart(fig, use_container_width=True)

    # Correlation Matrix - Mental Health Data
    if {'Depression_Score', 'Anxiety_Score', 'Stress_Level'}.issubset(mental_data.columns):
        st.subheader(_("Correlation Between Mental Health Metrics"))
        corr_data = mental_data[['Depression_Score', 'Anxiety_Score', 'Stress_Level']].corr()
        fig = px.imshow(corr_data, text_auto=True, aspect="auto", title=_("Correlation Heatmap"))
        fig.update_layout(margin=dict(l=10, r=10, t=50, b=10))
        st.plotly_chart(fig, use_container_width=True)

    # Regional Depression Scores - DHS Data
    if 'Region' in dhs_data.columns and 'Depression_Score' in dhs_data.columns:
        st.subheader(_("Regional Distribution of Depression Scores"))
        region_data = dhs_data.groupby('Region')['Depression_Score'].mean().reset_index()
        fig = px.choropleth(region_data, locations="Region", color="Depression_Score", hover_name="Region", color_continuous_scale="Blues")
        st.plotly_chart(fig, use_container_width=True)

# Predictive Modeling Section (with Models)
def predictive_modeling():
    st.header("🤖 " + _("Predictive Modeling"))
    
    # User input for predictive modeling
    with st.form(key='prediction_form'):
        col1, col2, col3 = st.columns(3)
        with col1:
            age = st.slider(_("Age"), min_value=15, max_value=25, value=20)
        with col2:
            social_media = st.slider(_("Social Media Usage (hours/day)"),
        with col3:
            physical_activity = st.slider(_("Physical Activity (hours/week)"), min_value=0, max_value=14, value=4)
        sleep_duration = st.slider(_("Sleep Duration (hours/night)"), min_value=4, max_value=12, value=7)

        # Additional Model Parameters
        st.markdown("#### " + _("Model Parameters"))
        model_choice = st.selectbox(
            _("Select Model"),
            options=["Random Forest", "Support Vector Machine", "Logistic Regression"]
        )
        confidence_threshold = st.slider(_("Confidence Threshold"), 0.5, 1.0, 0.7)
        include_probability = st.checkbox(_("Include Probability in Output"))
        
        # Submit button for form
        submit_button = st.form_submit_button(label=_('Predict'))

    if submit_button:
        # Example predictive logic based on selected model
        if model_choice == "Random Forest":
            prediction = age * 0.25 + social_media * 0.15 - physical_activity * 0.2 + sleep_duration * 0.3
            model_name = "Random Forest Model"
        elif model_choice == "Support Vector Machine":
            prediction = age * 0.3 + social_media * 0.1 - physical_activity * 0.25 + sleep_duration * 0.25
            model_name = "Support Vector Machine"
        else:
            prediction = age * 0.2 + social_media * 0.1 - physical_activity * 0.3 + sleep_duration * 0.4
            model_name = "Logistic Regression"
        
        # Display prediction and additional details
        st.success(f"{_('Predicted Score')}: **{prediction:.2f}**")
        st.write(f"Using {model_name} with a confidence threshold of {confidence_threshold}.")
        
        # Show probability if selected
        if include_probability:
            probability = min(1, max(0, prediction / 100))  # Simulated probability value
            st.info(f"{_('Prediction Probability')}: {probability:.2%}")

        # Display feature importance (simulated)
        feature_importance = {
            "Age": abs(age * 0.2),
            "Social Media Usage": abs(social_media * 0.15),
            "Physical Activity": abs(physical_activity * 0.25),
            "Sleep Duration": abs(sleep_duration * 0.3)
        }
        importance_df = pd.DataFrame(
            feature_importance.items(),
            columns=["Feature", "Importance"]
        ).sort_values(by="Importance", ascending=False)
        
        st.subheader(_("Feature Importance"))
        fig = px.bar(importance_df, x="Feature", y="Importance", title=_("Feature Importance in Prediction"))
        fig.update_layout(margin=dict(l=10, r=10, t=50, b=10))
        st.plotly_chart(fig, use_container_width=True)

# Chatbot Interface using Groq API
def chatbot_interface():
    st.header("🗣️ " + _("Mental Health Chatbot"))

    # Chatbot introduction
    st.markdown("""
    <div style="text-align: center;">
        <h3>Hello! I'm <strong>Menti</strong>, your mental health assistant 🤖</h3>
        <p>Feel free to share your thoughts, ask about mental health resources, or get tips for stress management.</p>
    </div>
    """, unsafe_allow_html=True)

    # Custom CSS for chatbot UI
    st.markdown("""
    <style>
    .chat-container {
        display: flex;
        flex-direction: column;
        max-height: 450px;
        overflow-y: auto;
        background-color: #f0f2f5;
        border-radius: 10px;
        padding: 15px;
        margin-top: 20px;
        border: 1px solid #ddd;
    }
    .user-message, .assistant-message {
        padding: 12px 15px;
        border-radius: 20px;
        font-size: 16px;
        margin-bottom: 10px;
        max-width: 75%;
    }
    .user-message {
        background-color: #DCF8C6;
        align-self: flex-end;
        text-align: right;
    }
    .assistant-message {
        background-color: #FFFFFF;
        border: 1px solid #FF6B6B;
        color: #333;
        align-self: flex-start;
        text-align: left;
    }
    .chat-input {
        width: 100%;
        padding: 10px;
        border-radius: 20px;
        border: 1px solid #ccc;
        font-size: 16px;
        margin-top: 15px;
    }
    .send-button {
        background-color: #FF6B6B;
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: 20px;
        font-size: 16px;
        cursor: pointer;
        margin-top: 10px;
    }
    .send-button:hover {
        background-color: #FF4C4C;
    }
    </style>
    """, unsafe_allow_html=True)

    if 'history' not in st.session_state:
        st.session_state['history'] = []

    # Display chat history
    chat_html = '<div class="chat-container">'
    for chat in st.session_state['history']:
        user_html = f'<div class="user-message">{chat["user"]}</div>'
        assistant_html = f'<div class="assistant-message">{chat["assistant"]}</div>'
        chat_html += user_html + assistant_html
    chat_html += '</div>'
    st.markdown(chat_html, unsafe_allow_html=True)

    # User input
    user_input = st.text_input(_("You") + ":", "", key="input", placeholder="Type your message here...", label_visibility="collapsed")

    # Process the user's input
    if user_input:
        st.session_state['history'].append({"user": user_input, "assistant": "Menti is typing..."})
        st.experimental_rerun()  # Temporarily display typing indicator

        # Generate response from Groq API
        assistant_response = generate_text(user_input)
        
        # Update chat history with actual response
        st.session_state['history'][-1]["assistant"] = assistant_response
        st.experimental_rerun()  # Refresh with updated response

    # Display send button
    st.markdown('<button class="send-button">Send</button>', unsafe_allow_html=True)

# Function to generate text from Groq API
def generate_text(prompt, max_tokens=100):
    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192",  
            max_tokens=max_tokens,
            temperature=0.7
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        print(f"An error occurred: {e}")
        return "I'm having trouble connecting right now. Please try again later."

# Sidebar innovations and mental health resources
def innovative_features():
    st.sidebar.markdown("---")
    st.sidebar.header("📚 " + _("Mental Health Resources"))
    with st.sidebar.expander(_("Hotlines and Contacts")):
        st.markdown("""
        - **Rwanda Mental Health Hotline**: 1234
        - **Online Resources**:
          - [Ministry of Health Rwanda](https://www.moh.gov.rw)
          - [WHO Mental Health](https://www.who.int/mental_health/en/)
    """)
    st.sidebar.header("💡 " + _("Daily Tip"))
    tips = [
        _("Take a short walk to clear your mind."),
        _("Practice deep breathing exercises."),
        _("Reach out to a friend or family member."),
        _("Write down your thoughts in a journal."),
        _("Try a new hobby or activity."),
        _("Maintain a balanced diet and stay hydrated."),
        _("Set achievable goals and celebrate small wins."),
        _("Get enough sleep to rejuvenate your mind."),
        _("Listen to your favorite music to relax."),
        _("Practice mindfulness or meditation.")
    ]
    tip = np.random.choice(tips)
    st.sidebar.info(f"**{_('Tip')}:** {tip}")

# Contact Professionals Feature
def contact_professionals():
    st.header("📞 " + _("Contact a Professional"))

    st.write(_("Here you can find contact information for mental health professionals and hospitals in Rwanda."))

    professionals = [
        {
            "name": "Dr. Jean Mukiza",
            "phone": "+250781234567",
            "email": "jean.mukiza@example.com",
            "location": "Kigali"
        },
        {
            "name": "Dr. Aline Uwase",
            "phone": "+250789876543",
            "email": "aline.uwase@example.com",
            "location": "Northern Province"
        },
        {
            "name": "Kigali Mental Health Hospital",
            "phone": "+250788123456",
            "email": "info@kigalimhh.rw",
            "location": "Kigali"
        }
    ]

    # Display professionals in a table with contact options
    for prof in professionals:
        st.subheader(prof["name"])
        col1
        col1, col2 = st.columns([1, 3])
        with col1:
            st.write(f"**{_('Location')}:** {prof['location']}")
            st.write(f"**{_('Phone Number')}:** {prof['phone']}")
            st.write(f"**{_('Email')}:** {prof['email']}")
        with col2:
            if st.button(f"{_('Call')} {prof['name']}", key=prof["phone"]):
                st.info(f"{_('Dialing')} {prof['phone']}...")
            if st.button(f"{_('Email')} {prof['name']}", key=prof["email"]):
                st.info(f"{_('Opening email client for')} {prof['email']}...")
        st.write("---")

# Main function to navigate the app
def main():
    set_language()

    # Sidebar navigation
    options = [
        _("Home"),
        _("Data Visualization"),
        _("Predictive Modeling"),
        _("Chatbot"),
        _("Community Forum"),
        _("Contact Professionals")
    ]
    icons = ["house", "bar-chart", "cpu", "chat-dots", "people", "telephone"]

    selected = option_menu(
        menu_title=_("Main Menu"),
        options=options,
        icons=icons,
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "#f0f2f6"},
            "icon": {"color": "#FF6B6B", "font-size": "18px"},
            "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px", "--hover-color": "#e0e0e0"},
            "nav-link-selected": {"background-color": "#FF6B6B"},
        },
    )

    innovative_features()

    # Load data if not loaded already
    if 'data' not in st.session_state:
        youth_data, mental_data, dhs_data, gen_pop_data, mental_youth_data = load_data()
        st.session_state['data'] = youth_data, mental_data, dhs_data, gen_pop_data, mental_youth_data
    youth_data, mental_data, dhs_data, gen_pop_data, mental_youth_data = st.session_state['data']

    # Handle navigation selection
    if selected == _("Home"):
        home()
    elif selected == _("Data Visualization"):
        data_visualization(youth_data, mental_data, dhs_data, gen_pop_data, mental_youth_data)
    elif selected == _("Predictive Modeling"):
        predictive_modeling()
    elif selected == _("Chatbot"):
        chatbot_interface()
    elif selected == _("Community Forum"):
        community_forum()
    elif selected == _("Contact Professionals"):
        contact_professionals()

# Run the Streamlit app
if __name__ == '__main__':
    main()
