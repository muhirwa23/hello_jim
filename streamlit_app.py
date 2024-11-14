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
st.markdown("""
<style>
/* Main container */
.main {
    background-color: #f5f5f5;
    padding: 0;
    font-family: 'Arial', sans-serif;
}

/* Sidebar */
.css-1d391kg {  /* Adjusts the width of the sidebar */
    width: 300px;
}
.css-1lcbmhc {  /* Adjusts the width of the main content */
    margin-left: 300px;
}

/* Button styling */
.stButton>button {
    color: white;
    background-color: #FF6B6B;
    border-radius: 5px;
    height: 50px;
    width: 100%;
    font-size: 18px;
}

/* Progress bar */
.stProgress > div > div > div > div {
    background-color: #FF6B6B;
}

/* Chat messages */
.chat-message {
    padding: 10px;
    border-radius: 10px;
    margin-bottom: 5px;
    max-width: 70%;
    font-size: 16px;
}
.user-message {
    background-color: #D1F7C4;
    align-self: flex-end;
}
.assistant-message {
    background-color: #FFFFFF;
    align-self: flex-start;
}
.chat-container {
    display: flex;
    flex-direction: column;
    max-height: 400px;
    overflow-y: auto;
}

/* Header styles */
h1, h2, h3, h4 {
    color: #2F4F4F;
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    font-weight: bold;
}

/* Sidebar Headers */
.sidebar-header {
    font-size: 20px;
    color: #2F4F4F;
    margin-bottom: 10px;
}

/* Tooltip styling */
.tooltip {
    position: relative;
    display: inline-block;
}
.tooltip .tooltiptext {
    visibility: hidden;
    width: 220px;
    background-color: #555;
    color: #fff;
    text-align: center;
    border-radius: 6px;
    padding: 10px;
    position: absolute;
    z-index: 1;
    bottom: 125%; /* Position above */
    left: 50%;
    margin-left: -110px;
    opacity: 0;
    transition: opacity 0.3s;
}
.tooltip:hover .tooltiptext {
    visibility: visible;
    opacity: 1;
}
</style>
""", unsafe_allow_html=True)

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
        "Navigate through the sidebar to explore different sections of the dashboard.":
            "Koresha urutonde ruri ku ruhande kugira ngo urebe ibice bitandukanye bya dashboard.",
        "Gender Distribution": "Igitsina",
        "Age Distribution": "Ikigereranyo cy'Imyaka",
        "Regional Distribution": "Ikigereranyo cy'Intara",
        "Mental Health Metrics Over Time": "Ibipimo by'Ubuzima bwo mu Mutwe mu Gihe",
        "Select metrics to display:": "Hitamo ibipimo ushaka kwerekana:",
        "Correlation Matrix": "Imbonerahamwe y'Isano",
        "Scatter Plot Matrix": "Ishusho y'Imbonerahamwe",
        "Predicting Depression Scores": "Gutekereza ku Manota y'Agahinda",
        "Adjust the input parameters to predict the depression score.":
            "Hindura ibipimo by'inyongera kugira ngo uteganye amanota y'agahinda.",
        "Feature Importance": "Iby'Ingenzi mu Bipimo",
        "Model Performance": "Imikorere y'Icyitegererezo",
        "Make a Prediction": "Kora Iteganyizo",
        "Age": "Imyaka",
        "Social Media Usage (hours/day)": "Gukoresha Imbuga Nkoranyambaga (amasaha/umunsi)",
        "Physical Activity (hours/week)": "Imyitozo ngororamubiri (amasaha/icyumweru)",
        "Sleep Duration (hours/night)": "Igihe cyo Kuryama (amasaha/ijoro)",
        "Predict": "Teganya",
        "Predicted Depression Score": "Amanota y'Agahinda yateganyijwe",
        "Note: Higher scores indicate higher levels of depression.":
            "Icyitonderwa: Amanota menshi agaragaza urwego rwo hejuru rw'agahinda.",
        "Mental Health Chatbot": "Chatbot y'Ubuzima bwo mu Mutwe",
        "Hello! I'm **Menti**, your mental health assistant. How can I help you today?":
            "Muraho! Ndi **Menti**, umufasha wawe mu buzima bwo mu mutwe. Nigute nakugira inama uyu munsi?",
        "You": "Wowe",
        "Tip": "Inama",
        "Main Menu": "Menyu Nyamukuru",
        "Home": "Ahabanza",
        "Data Visualization": "Kwerekana Imibare",
        "Predictive Modeling": "Gukora Icyitegererezo",
        "Chatbot": "Chatbot",
        "Community Forum": "Urubuga rw'Abaturage",
        "Contact Professionals": "Guhamagara Ababigize umwuga",
        "Chat with Professional": "Vugana n'Umuhanga",
        "Login/SignUp": "Injira/Iyandikishe",
        "Login": "Injira",
        "SignUp": "Iyandikishe",
        "Menu": "Menyu",
        "Email": "Imeli",
        "Password": "Ijambo ry'Ibanga",
        "Create a New Account": "Fungura Konti Nshya",
        "Logged in as": "Winjiye nka",
        "Logout": "Sohoka",
        "Invalid credentials or user does not exist.": "Amakuru winjije si yo cyangwa umukoreshwa ntabaho.",
        "Account created successfully! Please login.": "Konti yawe yashyizweho neza! Nyamuneka injira.",
        "Error creating account": "Ikosa mu gushyiraho konti",
        "Please login to access more features.": "Nyamuneka injira kugira ngo ubone ibindi bikorwa.",
        "Username (anonymous)": "Izina (hatabayeho kumenyekana)",
        "Share your thoughts or experiences": "Sangiza ibitekerezo cyangwa ubunararibonye bwawe",
        "Post": "Ohereza",
        "Your post has been shared!": "Ubutumwa bwawe bwashyizweho!",
        "Recent Posts": "Ubutumwa Bwanyuma",
        "at": "ku",
        "Connect with others anonymously to share experiences and support each other.": "Hura n'abandi mu ibanga kugira ngo musangire ubunararibonye no gufashanya.",
        "Chatting with": "Uri kuvugana na",
        "Choose a professional to chat with": "Hitamo umuhanga wo kuganira na we",
        "Please login to access the chat feature.": "Nyamuneka injira kugira ngo ubone igikorwa cyo kuganira.",
        "Type your message here...": "Andika ubutumwa bwawe hano...",
        "Send": "Ohereza",
        "Contact a Professional": "Vugana n'Umuhanga",
        "Here you can find contact information for mental health professionals and hospitals in Rwanda.": "Hano ushobora kubona amakuru yo kuvugana n'abahanga mu buzima bwo mu mutwe n'amavuriro mu Rwanda.",
        "Location": "Aho aherereye",
        "Phone Number": "Numero ya Telefone",
        "Call": "Hamagara",
        "Dialing": "Hamagara",
        "Email": "Imeli",
        "Opening email client for": "Ufunguye porogaramu ya imeli kuri",
        "Sentiment Analysis": "Isesengura ry'Umubabaro",
        "Sentiment Over Time": "Umubabaro mu Gihe",
        "Word Cloud": "Ishusho y'Amagambo",
        "Depression Trends": "Ibigenda Byerekeye Depression",
        "Anxiety Trends": "Ibigenda Byerekeye Anxiety",
        "Stress Trends": "Ibigenda Byerekeye Stress",
        "Heatmap by Region": "Heatmap mu Ntara",
        "Word Frequency in Posts": "Frequency y'Amagambo mu Butumwa",
        "Interactive Charts": "Ishusho Zikora",
    }
    if st.session_state.get('language') == "Kinyarwanda":
        return translations.get(text, text)
    else:
        return text

# Simulate data function for visualization
def simulate_data():
    np.random.seed(42)
    num_samples = 500
    data = pd.DataFrame({
        'Age': np.random.randint(15, 25, num_samples),
        'Gender': np.random.choice(['Male', 'Female'], num_samples),
        'Depression_Score': np.random.normal(50, 15, num_samples),
        'Anxiety_Score': np.random.normal(50, 15, num_samples),
        'Stress_Level': np.random.normal(50, 15, num_samples),
        'Social_Media_Usage': np.random.randint(0, 10, num_samples),  # Hours per day
        'Physical_Activity': np.random.randint(0, 7, num_samples),    # Hours per week
        'Sleep_Duration': np.random.normal(7, 1.5, num_samples),      # Hours per night
        'Region': np.random.choice(['Kigali', 'Northern', 'Southern', 'Eastern', 'Western'], num_samples),
        'Date': pd.date_range(start='2022-01-01', periods=num_samples, freq='D')
    })
    # Ensure scores are within 0-100
    for score in ['Depression_Score', 'Anxiety_Score', 'Stress_Level']:
        data[score] = data[score].clip(0, 100)
    return data

# Predictive Modeling Function
def predictive_modeling():
    st.header("🤖 " + _("Predictive Modeling"))
    st.markdown(_("### Predict your Depression Score"))

    # User input form
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
        # Simple model for prediction (linear approximation)
        depression_score = (age * 0.3) + (social_media * 0.5) - (physical_activity * 0.2) + (sleep_duration * 0.4)
        depression_score = np.clip(depression_score, 0, 100)  # Ensures the score stays within 0-100 range
        st.success(f"{_('Predicted Depression Score')}: **{depression_score:.2f}**")
        st.info(_("Note: Higher scores indicate higher levels of depression."))

# Home page design with Hierarchical Demographic Analysis chart
def home(data):
    st.title("🧠 " + _("Mental Health Dashboard for Rwandan Youth"))
    st.markdown("### " + _("Welcome to the Mental Health Dashboard"))
    st.markdown(_("This dashboard provides insights into the mental health of Rwandan youth. Explore data visualizations, predictive modeling, and engage with our interactive chatbot."))

    # Hierarchical Demographic Analysis Chart
    st.subheader(_("Hierarchical Demographic Analysis"))
    demographic_counts = data.groupby(['Age', 'Region', 'Gender']).size().reset_index(name='Counts')
    fig = px.sunburst(demographic_counts, path=['Region', 'Age', 'Gender'], values='Counts', color='Gender', 
                      color_discrete_map={'Male': '#636EFA', 'Female': '#EF553B'})
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(_("**Navigate through the sidebar to explore different sections of the dashboard.**"))

# Data visualization function with more charts
def data_visualization(data):
    st.header("📊 " + _("Data Visualization"))

    # Mental Health Trends over Time (Depression, Anxiety, Stress)
    st.subheader(_("Mental Health Trends Over Time"))
    metrics = ['Depression_Score', 'Anxiety_Score', 'Stress_Level']
    selected_metrics = st.multiselect(_("Select metrics to display:"), metrics, default=metrics)
    if selected_metrics:
        fig = px.line(
            data, x='Date', y=selected_metrics,
            labels={'value': _('Score'), 'variable': _('Metric')},
            color_discrete_sequence=px.colors.qualitative.G10
        )
        st.plotly_chart(fig, use_container_width=True)

    # Heatmap by Region
    st.subheader(_("Heatmap by Region"))
    region_metrics = data.groupby('Region').mean().reset_index()
    fig = go.Figure(data=go.Heatmap(
        z=region_metrics[['Depression_Score', 'Anxiety_Score', 'Stress_Level']].values,
        x=['Depression Score', 'Anxiety Score', 'Stress Level'],
        y=region_metrics['Region'],
        colorscale='Viridis'
    ))
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

    # Boxplot for Stress Levels
    st.subheader(_("Stress Level Distribution"))
    fig = px.box(data, y='Stress_Level', color='Gender', 
                 title="Stress Levels by Gender", 
                 labels={"Stress_Level": "Stress Level", "Gender": "Gender"})
    st.plotly_chart(fig, use_container_width=True)

# Chatbot Interface
def chatbot_interface():
    st.header("🧠 " + _("Mental Health Chatbot"))

    st.write(_("Hello! I'm **Menti**, your mental health assistant. How can I help you today?"))

    if 'history' not in st.session_state:
        st.session_state['history'] = []

    # Chat interface
    user_input = st.text_input(_("You") + ":", "", key="input")
    if user_input:
        # Simulate chatbot response
        assistant_response = f"**Menti**: Based on your query, here's some information related to mental health."
        st.session_state.history.append({"user": user_input, "assistant": assistant_response})

    # Display conversation history
    for chat in st.session_state.history:
        st.markdown(f"<div class='chat-message user-message'><strong>{_('You')}:</strong> {chat['user']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='chat-message assistant-message'><strong>Menti:</strong> {chat['assistant']}</div>", unsafe_allow_html=True)

# Main function to control flow
def main():
    set_language()

    # Sidebar navigation
    options = [
        _("Home"),
        _("Data Visualization"),
        _("Predictive Modeling"),
        _("Chatbot"),
    ]
    icons = ["house", "bar-chart", "cpu", "chat-dots"]

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

    # Simulate data once to avoid regenerating it on every interaction
    if 'data' not in st.session_state:
        st.session_state['data'] = simulate_data()
    data = st.session_state['data']

    if selected == _("Home"):
        home(data)
    elif selected == _("Data Visualization"):
        data_visualization(data)
    elif selected == _("Predictive Modeling"):
        predictive_modeling()
    elif selected == _("Chatbot"):
        chatbot_interface()

if __name__ == '__main__':
    main()
