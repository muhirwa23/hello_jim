# Import necessary libraries
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import requests
import datetime
from textblob import TextBlob
import nltk
from wordcloud import WordCloud
import os
from groq import Groq  # Ensure Groq is installed and imported
import time

# Download NLTK data (if not already downloaded)
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

# Set page configuration
st.set_page_config(
    page_title="Mental Health Dashboard",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Apply custom CSS for styling
st.markdown("""<style>
.main { background-color: #f5f5f5; padding: 0; }
.css-1d391kg { width: 300px; }
.stButton>button { color: white; background-color: #FF6B6B; border-radius: 5px; height: 50px; width: 100%; font-size: 18px; }
.stProgress > div > div > div > div { background-color: #FF6B6B; }
.chat-message { padding: 10px; border-radius: 10px; margin-bottom: 5px; max-width: 70%; font-size: 16px; }
.user-message { background-color: #D1F7C4; align-self: flex-end; }
.assistant-message { background-color: #FFFFFF; align-self: flex-start; }
.chat-container { display: flex; flex-direction: column; max-height: 400px; overflow-y: auto; }
h1, h2, h3, h4 { color: #2F4F4F; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
.sidebar-header { font-size: 20px; color: #2F4F4F; margin-bottom: 10px; }
</style>""", unsafe_allow_html=True)

# Multilingual Support
def set_language():
    if 'language' not in st.session_state:
        st.session_state['language'] = 'English'
    lang = st.sidebar.selectbox("Choose Language / Hitamo Ururimi", ["English", "Kinyarwanda"], index=0)
    st.session_state['language'] = lang

def _(text):
    translations = {
        "Welcome to the Mental Health Dashboard": "Murakaza neza kuri Dashboard y'Ubuzima bwo mu Mutwe",
        "This dashboard provides insights into the mental health of Rwandan youth. Explore data visualizations, predictive modeling, and engage with our interactive chatbot.":
            "Iyi dashboard itanga ishusho y'ubuzima bwo mu mutwe bw'urubyiruko rw'u Rwanda. Reba ibigaragara mu mibare, gutekereza ku byashoboka, no gukoresha chatbot yacu.",
        # Add more translations as needed
    }
    if st.session_state.get('language') == "Kinyarwanda":
        return translations.get(text, text)
    else:
        return text

# Load all provided datasets
import pandas as pd
import streamlit as st

# Load all provided datasets
@st.cache_data  # Use st.cache_data instead of st.cache
def load_data():
    # Update these paths to match the exact file names
    youth_health_data = pd.read_csv("youth_health_data_expanded (1).csv")  
    mental_health_data = pd.read_csv("mental_health_indicators_rwa (1).csv")  
    dhs_data = pd.read_csv("dhs_data.csv")  
    general_population_data = pd.read_csv("general_population_data.csv")  
    mental_health_youth_data = pd.read_csv("mental_health_data_rwanda_youth.csv")  
    return youth_health_data, mental_health_data, dhs_data, general_population_data, mental_health_youth_data
# Load the data
youth_health_data, mental_health_data, dhs_data, general_population_data, mental_health_youth_data = load_data()
# Function for the home page
def home():
    st.title("🧠 " + _("Mental Health Dashboard for Rwandan Youth"))
    st.markdown("### " + _("Welcome to the Mental Health Dashboard"))
    st.markdown(_("This dashboard provides insights into the mental health of Rwandan youth. Explore data visualizations, predictive modeling, and engage with our interactive chatbot."))
    st.image("https://www.who.int/images/default-source/mca/mca-covid-image-hi-res.jpg", use_column_width=True)
    st.markdown(_("Navigate through the sidebar to explore different sections of the dashboard."))

# Enhanced Data Visualization with Tableau-Style Widgets and Separate Containers
def data_visualization(youth_data, mental_data, dhs_data, gen_pop_data, mental_youth_data):
    st.header("📊 " + _("Data Visualization"))

    # Age Distribution - General Population Data
    if 'Age' in gen_pop_data.columns:
        with st.container():
            st.subheader(_("Age Distribution - General Population"))
            fig = px.histogram(
                gen_pop_data, 
                x='Age', 
                nbins=20, 
                title=_("Age Distribution of General Population"),
                template="presentation"
            )
            fig.update_layout(
                margin=dict(l=10, r=10, t=50, b=10),
                paper_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")

    # Depression and Anxiety Distribution - Mental Health Data
    if 'Depression_Score' in mental_data.columns and 'Anxiety_Score' in mental_data.columns:
        with st.container():
            st.subheader(_("Distribution of Depression and Anxiety Scores"))
            fig_dep = px.histogram(
                mental_data, 
                x='Depression_Score', 
                nbins=20, 
                marginal="rug", 
                title=_("Depression Score Distribution"),
                template="presentation"
            )
            fig_anx = px.histogram(
                mental_data, 
                x='Anxiety_Score', 
                nbins=20, 
                marginal="rug", 
                title=_("Anxiety Score Distribution"),
                template="presentation"
            )
            for fig in [fig_dep, fig_anx]:
                fig.update_layout(
                    margin=dict(l=10, r=10, t=50, b=10),
                    paper_bgcolor="rgba(0,0,0,0)"
                )
                st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Correlation Heatmap - Mental Health Data
    if {'Depression_Score', 'Anxiety_Score', 'Stress_Level'}.issubset(mental_data.columns):
        with st.container():
            st.subheader(_("Correlation Between Mental Health Metrics"))
            corr_data = mental_data[['Depression_Score', 'Anxiety_Score', 'Stress_Level']].corr()
            fig = px.imshow(
                corr_data, 
                text_auto=True, 
                aspect="auto", 
                title=_("Correlation Heatmap of Mental Health Metrics"),
                template="presentation"
            )
            fig.update_layout(
                margin=dict(l=10, r=10, t=50, b=10),
                paper_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Gender-Based Depression Score - Youth Data
    if 'Gender' in youth_data.columns and 'Depression_Score' in youth_data.columns:
        with st.container():
            st.subheader(_("Depression Score by Gender"))
            gender_counts = youth_data.groupby('Gender')['Depression_Score'].mean().reset_index()
            fig = px.bar(
                gender_counts, 
                x='Gender', 
                y='Depression_Score', 
                title=_("Average Depression Score by Gender"),
                template="presentation"
            )
            fig.update_layout(
                margin=dict(l=10, r=10, t=50, b=10),
                paper_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Time Series of Depression Score - Mental Health Youth Data
    if 'Date' in mental_youth_data.columns and 'Depression_Score' in mental_youth_data.columns:
        with st.container():
            st.subheader(_("Time Series of Depression Scores"))
            fig = px.line(
                mental_youth_data, 
                x='Date', 
                y='Depression_Score', 
                title=_("Depression Score Over Time"),
                template="presentation"
            )
            fig.update_layout(
                margin=dict(l=10, r=10, t=50, b=10),
                paper_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Regional Distribution of Depression Scores - DHS Data
    if 'Region' in dhs_data.columns and 'Depression_Score' in dhs_data.columns:
        with st.container():
            st.subheader(_("Regional Distribution of Depression Scores"))
            region_data = dhs_data.groupby('Region')['Depression_Score'].mean().reset_index()
            fig = px.choropleth(
                region_data,
                locations="Region",
                color="Depression_Score",
                hover_name="Region",
                color_continuous_scale="Blues",
                title=_("Average Depression Score by Region"),
                locationmode="country names",
                template="presentation"
            )
            fig.update_geos(fitbounds="locations", visible=False)
            fig.update_layout(
                margin=dict(l=10, r=10, t=50, b=10),
                paper_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Box Plot Analysis - DHS Data
    if 'Region' in dhs_data.columns and 'Anxiety_Score' in dhs_data.columns:
        with st.container():
            st.subheader(_("Box Plot Analysis of Anxiety Scores by Region"))
            fig = px.box(
                dhs_data, 
                x="Region", 
                y="Anxiety_Score", 
                title=_("Box Plot of Anxiety Scores by Region"),
                template="presentation"
            )
            fig.update_layout(
                margin=dict(l=10, r=10, t=50, b=10),
                paper_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Sunburst Chart - Hierarchical Demographics in Mental Health Youth Data
    if {'Region', 'Gender', 'Age', 'Depression_Score'}.issubset(mental_youth_data.columns):
        with st.container():
            st.subheader(_("Hierarchical Demographics Analysis"))
            fig = px.sunburst(
                mental_youth_data,
                path=['Region', 'Gender', 'Age'],
                values='Depression_Score',
                title=_("Hierarchical Sunburst of Depression Scores by Region, Gender, and Age"),
                color='Depression_Score',
                template="presentation"
            )
            fig.update_layout(
                margin=dict(l=10, r=10, t=50, b=10),
                paper_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig, use_container_width=True)

# Sample Usage
data_visualization(youth_health_data, mental_health_data, dhs_data, general_population_data, mental_health_youth_data)


# Function for predictive modeling (API Integration)
def predictive_modeling():
    st.header("🤖 " + "Predictive Modeling")

    st.markdown("### " + _("Predicting Depression Scores"))
    st.markdown(_("Adjust the input parameters to predict the depression score."))

    # Prediction form
    with st.form(key='prediction_form'):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            age = st.slider(_("Age"), min_value=15, max_value=25, value=20)
        with col2:
            social_media = st.slider(_("Social Media Usage (hours/day)"), min_value=0, max_value=12, value=3)
        with col3:
            physical_activity = st.slider(_("Physical Activity (hours/week)"), min_value=0, max_value=14, value=4)
        with col4:
            sleep_duration = st.slider(_("Sleep Duration (hours/night)"), min_value=4, max_value=12, value=7)
        submit_button = st.form_submit_button(label=_('Predict'))

    if submit_button:
        # Example predictive 
        prediction = age * 0.2 + social_media * 0.1 - physical_activity * 0.3 + sleep_duration * 0.2
        st.success(f"{_('Predicted Depression Score')}: **{prediction:.2f}**")
        st.info(_("Note: Higher scores indicate higher levels of depression."))

# Set up the Groq API key securely
os.environ["GROQ_API_KEY"] = "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"
client = Groq(api_key=os.environ["GROQ_API_KEY"])

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

# Enhanced Chatbot Interface with Mental Health Focus
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

    # Display chat history in chat bubble format
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


# Function for the chatbot interface
# Sidebar innovations and mental health resources
def innovative_features():
    st.sidebar.markdown("---")
    st.sidebar.header("📚 " + _("Mental Health Resources"))
    with st.sidebar.expander(_("Hotlines and Contacts"), expanded=True):
        st.markdown("""
        - **Hotlines:**
            - Rwanda Mental Health Hotline: **1234**
        - **Online Resources:**
            - [Ministry of Health Rwanda](https://www.moh.gov.rw)
            - [WHO Mental Health](https://www.who.int/mental_health/en/)
        """)
    st.sidebar.header("💡 " + _("Daily Mental Health Tip"))
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

# Community Forum
def community_forum():
    st.header("🌐 " + _("Community Forum"))
    st.write(_("Connect with others anonymously to share experiences and support each other."))

    if 'forum_posts' not in st.session_state:
        st.session_state['forum_posts'] = []

    with st.form(key='forum_form'):
        username = st.text_input(_("Username (anonymous)"), "Anonymous")
        post_content = st.text_area(_("Share your thoughts or experiences"))
        submit_post = st.form_submit_button(label=_('Post'))

    if submit_post and post_content:
        st.session_state['forum_posts'].append({"username": username, "content": post_content, "time": datetime.datetime.now()})
        st.success(_("Your post has been shared!"))

    st.subheader(_("Recent Posts"))
    for post in reversed(st.session_state['forum_posts']):
        st.markdown(f"**{post['username']}** {_('at')} {post['time'].strftime('%Y-%m-%d %H:%M:%S')}")
        st.markdown(f">{post['content']}")
        st.write("---")

# Contact Professionals Feature
def contact_professionals():
    st.header("📞 " + _("Contact a Professional"))

    st.write(_("Here you can find contact information for mental health professionals and hospitals in Rwanda."))

    # Simulated list of professionals
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
            "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#e0e0e0"},
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

if __name__ == '__main__':
    main()
