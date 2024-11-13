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
@st.cache
def load_data():
    # Update these paths to your provided datasets
    youth_health_data = pd.read_csv("/youth_health_data.csv")  
    mental_health_data = pd.read_csv("/mental_health_indicators.csv")  
    dhs_data = pd.read_csv("/dhs_data.csv")  
    general_population_data = pd.read_csv("/general_population_data.csv")  
    mental_health_youth_data = pd.read_csv("/mental_health_data_rwanda_youth.csv")  
    return youth_health_data, mental_health_data, dhs_data, general_population_data, mental_health_youth_data

youth_health_data, mental_health_data, dhs_data, general_population_data, mental_health_youth_data = load_data()

# Function for the home page
def home():
    st.title("🧠 " + _("Mental Health Dashboard for Rwandan Youth"))
    st.markdown("### " + _("Welcome to the Mental Health Dashboard"))
    st.markdown(_("This dashboard provides insights into the mental health of Rwandan youth. Explore data visualizations, predictive modeling, and engage with our interactive chatbot."))
    st.image("https://www.who.int/images/default-source/mca/mca-covid-image-hi-res.jpg", use_column_width=True)
    st.markdown(_("Navigate through the sidebar to explore different sections of the dashboard."))

# Function for combined data visualization
def data_visualization(youth_data, mental_data, dhs_data, gen_pop_data, mental_youth_data):
    st.header("📊 " + _("Data Visualization"))

    # Gender Distribution across Datasets
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("#### " + _("Gender Distribution"))
        gender_counts = youth_data['Gender'].value_counts()
        fig = px.pie(names=gender_counts.index, values=gender_counts.values, color=gender_counts.index, hole=0.5)
        fig.update_traces(textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)

    # Age Distribution (Histogram) using general population data
    with col2:
        st.markdown("#### " + _("Age Distribution"))
        fig = px.histogram(gen_pop_data, x='Age', nbins=10)
        st.plotly_chart(fig, use_container_width=True)

    # Depression and Anxiety Rates from Mental Health Indicators Dataset
    with col3:
        st.markdown("#### " + _("Mental Health Indicators"))
        fig = px.histogram(mental_data, x='Depression_Score', color='Anxiety_Score', marginal="rug")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Time-Series Analysis
    st.subheader(_("Mental Health Metrics Over Time"))
    metrics = ['Depression_Score', 'Anxiety_Score', 'Stress_Level']
    selected_metrics = st.multiselect(_("Select metrics to display:"), metrics, default=metrics)
    if selected_metrics:
        fig = px.line(mental_youth_data, x='Date', y=selected_metrics, labels={'value': _('Score'), 'variable': _('Metric')})
        fig.update_layout(title=_("Time Series of Selected Mental Health Metrics"), xaxis_title="Date", yaxis_title="Score")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Regional Analysis of DHS Data
    st.subheader(_("Regional Analysis of Mental Health Metrics"))
    region_data = dhs_data.groupby('Region').mean().reset_index()
    fig = px.choropleth(
        region_data,
        locations="Region",
        color="Depression_Score",
        hover_name="Region",
        color_continuous_scale="Viridis",
        locationmode="country names"
    )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(title_text=_("Depression Score by Region"))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Demographic Breakdown by Age and Gender
    st.subheader(_("Demographic Breakdown by Age and Gender"))
    demographic_data = youth_data.groupby(['Gender', 'Age']).mean().reset_index()
    fig = px.bar(demographic_data, x="Age", y="Depression_Score", color="Gender", barmode="group")
    fig.update_layout(title=_("Average Depression Score by Age and Gender"), xaxis_title="Age", yaxis_title="Depression Score")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Box Plot Analysis for DHS Data
    st.subheader(_("Box Plot Analysis for DHS Data"))
    metric_for_boxplot = st.selectbox(_("Select a metric to view outliers:"), ['Depression_Score', 'Anxiety_Score'])
    fig = px.box(dhs_data, x="Region", y=metric_for_boxplot, color="Region")
    fig.update_layout(title=f"{_('Box Plot of')} {metric_for_boxplot} {_('by Region')}", yaxis_title=metric_for_boxplot)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Sunburst Diagram for Hierarchical Demographics
    st.subheader(_("Hierarchical Demographic Analysis"))
    fig = px.sunburst(mental_youth_data, path=['Region', 'Gender', 'Age'], values='Depression_Score', color='Depression_Score')
    fig.update_layout(title=_("Sunburst Diagram of Demographic Breakdown by Region, Gender, and Age"))
    st.plotly_chart(fig, use_container_width=True)

# Function for predictive modeling (API Integration)
def predictive_modeling():
    st.header("🤖 "
def predictive_modeling():
    st.header("🤖 " + _("Predictive Modeling"))

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
        # Example predictive formula (replace with actual model integration if available)
        prediction = age * 0.2 + social_media * 0.1 - physical_activity * 0.3 + sleep_duration * 0.2
        st.success(f"{_('Predicted Depression Score')}: **{prediction:.2f}**")
        st.info(_("Note: Higher scores indicate higher levels of depression."))

# Function for the chatbot interface
def chatbot_interface():
    st.header("🗣️ " + _("Mental Health Chatbot"))

    st.write(_("Hello! I'm **Menti**, your mental health assistant. How can I help you today?"))

    if 'history' not in st.session_state:
        st.session_state['history'] = []

    # Chat interface
    user_input = st.text_input(_("You") + ":", "", key="input")
    if user_input:
        # Example response from a chatbot; replace with actual chatbot API if available
        assistant_response = "I'm here to listen and provide guidance. What are you experiencing?"
        st.session_state.history.append({"user": user_input, "assistant": assistant_response})

    # Display conversation history
    for chat in st.session_state.history:
        st.markdown(f"<div class='chat-message user-message'><strong>{_('You')}:</strong> {chat['user']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='chat-message assistant-message'><strong>Menti:</strong> {chat['assistant']}</div>", unsafe_allow_html=True)

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
