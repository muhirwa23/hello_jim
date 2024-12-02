import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import datetime
from textblob import TextBlob
import nltk
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os
import openai
from langdetect import detect
from googletrans import Translator
import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt
openai.api_key = os.getenv("OPENAI_API_KEY")

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
        "Hierarchical Demographic Analysis": "Isesengura ry'Ubwoko bw'Abaturage",
        "Mental Health Trends Over Time": "Ibigenda mu buzima bwo mu mutwe mu gihe",
        "Stress Level Distribution": "Ikigero cy'Ibibazo by'Umuhangayiko",
        "Predict your Depression Score": "Teganya Amanota yawe y'Agahinda",
        "Your Prediction": "Iteganyabikorwa cyawe",
        "User Login": "Injira y'Umukoresha",
        "User Signup": "Iyandikishe y'Umukoresha",
        "Dashboard": "Dashboard",
        "Analytics": "Igenzura",
        "Settings": "Imiterere",
        "Geographical Distribution": "Ikigereranyo cy'Aho aherereye",
        "Key Performance Indicators": "Ibipimo by'Ingenzi by'Imikorere",
        "User Demographics": "Demographics z'Abakoresha",
        "Data Filters": "Guhitamo Data",
        "Apply Filters": "Shyira mu bikorwa Guhitamo",
        "Reset Filters": "Subiza Guhitamo",
        "Total Users": "Abakoresha bose",
        "Average Depression Score": "Amanota y'Agahinda Akarerwa",
        "Average Anxiety Score": "Amanota y'Agahinda Akarerwa",
        "Average Stress Level": "Ikigero cy'Umuhangayiko Akarerwa",
        "Average Social Media Usage": "Gukoresha Imbuga Nkoranyambaga Akarerwa",
        "Average Physical Activity": "Imyitozo ngororamubiri Akarerwa",
        "Average Sleep Duration": "Igihe cyo Kuryama Akarerwa",
        "Hotline": "Hotline",
        "Resources to Read": "Ibikoresho byo Gusoma",
        "Rwanda Biomedical Center (RBC)": "Rwanda Biomedical Center (RBC)",
        "Ambulance Service": "Ambulance Service",
        "Mental Health Resources": "Ibikoresho by'Ubuzima bwo mu Mutwe",
        "Visit our resources page for more information.": "Suzuma urupapuro rw'ibikoresho byacu kugira ngo ubone amakuru menshi.",
        "Resources": "Ibikoresho",
    }
    if st.session_state.get('language') == "Kinyarwanda":
        return translations.get(text, text)
    else:
        return text
       
# Chatbot Interface
openai.api_key = os.getenv("OPENAI_API_KEY")
import streamlit as st
import openai
import os
from langdetect import detect
from googletrans import Translator
import time

translator = Translator()

# Add CSS styles to improve chatbot UI
def add_custom_css():
    st.markdown(
        """
        <style>
        .chat-container {
            max-width: 700px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f0f4f8;  /* Light blue medical theme */
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .chat-message {
            padding: 10px;
            border-radius: 10px;
            margin-bottom: 10px;
        }
        .user-message {
            background-color: #d1e7dd;
            text-align: right;
        }
        .assistant-message {
            background-color: #eaf1f8;  /* Soft blue for assistant messages */
        }
        .user-message strong, .assistant-message strong {
            color: #007bff;  /* Medical blue for usernames */
        }
        .input-container {
            max-width: 700px;
            margin: 0 auto;
            margin-top: 20px;
        }
        .header-container {
            max-width: 700px;
            margin: 0 auto;
            text-align: center;
            margin-bottom: 20px;
        }
        .stButton>button {
            background-color: #007bff;
            color: white;
            border-radius: 8px;
            border: none;
            padding: 10px 20px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #0056b3;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Chatbot Interface
def chatbot_interface():
    add_custom_css() 
    st.markdown("<div class='header-container'><h1>🤖 Mental Health Chatbot</h1></div>", unsafe_allow_html=True)
    st.write("<div class='header-container'><p>Hello! I'm <strong>Menti</strong>, your mental health assistant. How can I help you today?</p></div>", unsafe_allow_html=True)

    if 'history' not in st.session_state:
        st.session_state['history'] = []

    st.markdown("<div class='input-container'>", unsafe_allow_html=True)
    user_input = st.text_input("You:", "", key="input")
    if st.button("Send"):
        if user_input:
            with st.spinner('Menti is typing...'):
                user_lang = detect(user_input)
                translated_input = translator.translate(user_input, src=user_lang, dest="en").text if user_lang != "en" else user_input

                # Adding context for the full conversation history to make it more like ChatGPT
                messages = [
                    {"role": "system", "content": "You are a compassionate and multilingual mental health assistant."}
                ]
                for chat in st.session_state.history:
                    messages.append({"role": "user", "content": chat['user']})
                    messages.append({"role": "assistant", "content": chat['assistant']})
                messages.append({"role": "user", "content": translated_input})

                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=messages,
                    temperature=0.7,
                    max_tokens=150
                )
                assistant_reply = response['choices'][0]['message']['content']
                if user_lang != "en":
                    assistant_reply = translator.translate(assistant_reply, src="en", dest=user_lang).text

                st.session_state.history.append({"user": user_input, "assistant": assistant_reply})
                time.sleep(1)  # Adding a slight delay to mimic typing

    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
    for chat in st.session_state.history:
        st.markdown(f"<div class='chat-message user-message'><strong>You:</strong> {chat['user']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='chat-message assistant-message'><strong>Menti:</strong> {chat['assistant']}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    chatbot_interface()

# Community Forum (Simulated Feature)
def community_forum():
    st.header("👥 " + _("Community Forum"))
    st.markdown(_("Connect with others anonymously to share experiences and support each other."))

    if 'posts' not in st.session_state:
        st.session_state['posts'] = []

    with st.form(key='post_form'):
        username = st.text_input(_("Username (anonymous)"), "")
        post_content = st.text_area(_("Share your thoughts or experiences"))
        submit_post = st.form_submit_button(label=_('Post'))

    if submit_post:
        if username.strip() == "":
            username = "Anonymous"
        st.session_state.posts.append({
            "username": username,
            "content": post_content,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        st.success(_("Your post has been shared!"))

    st.subheader(_("Recent Posts"))
    for post in reversed(st.session_state.posts[-10:]):
        st.markdown(f"**{post['username']}** { _('at') } {post['timestamp']}")
        st.markdown(f"{post['content']}")
        st.markdown("---")

# Contact Professionals (Simulated Feature)
def contact_professionals():
    st.header("📞 " + _("Contact a Professional"))
    st.markdown(_("Here you can find contact information for mental health professionals and hospitals in Rwanda."))

    # Simulated contact data
    professionals = pd.DataFrame({
        'Location': ['Kigali', 'Northern', 'Southern', 'Eastern', 'Western'],
        'Name': ['Dr. Amani', 'Dr. Bosco', 'Dr. Clara', 'Dr. Daniel', 'Dr. Eva'],
        'Phone Number': ['+250 788 123456', '+250 788 654321', '+250 788 112233', '+250 788 445566', '+250 788 778899'],
        'Email': ['amani@example.com', 'bosco@example.com', 'clara@example.com', 'daniel@example.com', 'eva@example.com']
    })

    st.table(professionals)

    # Interactive contact options
    selected_professional = st.selectbox(_("Choose a professional to contact"), professionals['Name'])
    prof_info = professionals[professionals['Name'] == selected_professional].iloc[0]

    st.markdown(f"**{_('Location')}:** {prof_info['Location']}")
    st.markdown(f"**{_('Phone Number')}:** {prof_info['Phone Number']}")
    st.markdown(f"**{_('Email')}:** {prof_info['Email']}")

    col1, col2 = st.columns(2)
    with col1:
        if st.button(_("Call")):
            st.info(_("Dialing ") + f"{prof_info['Phone Number']}...")
    with col2:
        if st.button(_("Email")):
            st.info(_("Opening email client for ") + f"{prof_info['Email']}...")

# Enhanced Sentiment Analysis Feature
def sentiment_analysis():
    st.header("📊 " + _("Sentiment Analysis"))

    if 'posts' not in st.session_state or len(st.session_state.posts) == 0:
        st.info(_("No posts available for sentiment analysis."))
        return

    sentiments = []
    for post in st.session_state.posts:
        blob = TextBlob(post['content'])
        sentiments.append(blob.sentiment.polarity)

    sentiment_df = pd.DataFrame({
        'Post': [post['content'] for post in st.session_state.posts],
        'Sentiment': sentiments,
        'Date': [post['timestamp'] for post in st.session_state.posts]
    })

    st.subheader(_("Sentiment Over Time"))
    fig = px.line(sentiment_df, x='Date', y='Sentiment', title='Sentiment Over Time', markers=True)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader(_("Word Cloud of Posts"))
    all_text = ' '.join([post['content'] for post in st.session_state.posts])
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    st.pyplot(plt)

# User Authentication (Simulated Feature)
def user_authentication():
    st.sidebar.subheader(_("Login/SignUp"))

    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False
        st.session_state['username'] = ''

    if st.session_state['authenticated']:
        st.sidebar.write(f"{_('Logged in as')}: {st.session_state['username']}")
        if st.sidebar.button(_("Logout")):
            st.session_state['authenticated'] = False
            st.sidebar.success(_("You have been logged out."))
    else:
        auth_option = st.sidebar.selectbox(_("Select Option"), ["Login", "SignUp"])
        if auth_option == "Login":
            with st.sidebar.form(key='login_form'):
                username = st.text_input(_("Username"))
                password = st.text_input(_("Password"), type='password')
                login_button = st.form_submit_button(label=_('Login'))
            if login_button:
                # Simulate authentication
                if username == "admin" and password == "password":
                    st.session_state['authenticated'] = True
                    st.session_state['username'] = username
                    st.sidebar.success(_("Logged in successfully!"))
                else:
                    st.sidebar.error(_("Invalid credentials or user does not exist."))
        elif auth_option == "SignUp":
            with st.sidebar.form(key='signup_form'):
                new_username = st.text_input(_("Username"))
                new_password = st.text_input(_("Password"), type='password')
                signup_button = st.form_submit_button(label=_('SignUp'))
            if signup_button:
                # Simulate account creation
                st.sidebar.success(_("Account created successfully! Please login."))
                # In a real app, you'd save the user details to a database

# Hotline and Resources Section in Sidebar
def sidebar_hotline_and_resources():
    st.sidebar.markdown("---")
    st.sidebar.header(_("Hotline"))
    st.sidebar.markdown("""
    **Rwanda Biomedical Center (RBC):**  
    📞 +250 788 000000  

    **Ambulance Service:**  
    📞 +250 788 111111  

    **Police Support:**  
    📞 +250 788 222222  

    **Emergency Services:**  
    📞 +250 788 333333  
    """)

    st.sidebar.header(_("Resources to Read"))
    st.sidebar.markdown("""
    - [Mental Health Awareness](https://www.who.int/mental_health/en/)
    - [Understanding Depression](https://www.mentalhealth.gov/)
    - [Anxiety Disorders Information](https://adaa.org/)
    - [Stress Management Techniques](https://www.apa.org/topics/stress)
    """)

# Main function to control flow
def main():
    set_language()

    # Sidebar navigation with additional options
    options = [
        _("Home"),
        _("Data Visualization"),
        _("Predictive Modeling"),
        _("Chatbot"),
        _("Community Forum"),
        _("Contact Professionals"),
        _("Sentiment Analysis"),
        _("Analytics"),
        _("Settings"),
    ]
    icons = ["house", "bar-chart", "cpu", "chat-dots", "people", "telephone", "emoji-smile", "graph-up", "gear"]

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

   # Load the mental health data once to avoid regenerating it on every interaction
data = load_data()

# Display user authentication sidebar
user_authentication()

# Add Hotline and Resources to the sidebar
sidebar_hotline_and_resources()

# Handle navigation based on user's selection
if selected == _("Home"):
    home(data)
elif selected == _("Data Visualization"):
    data_visualization(data)
elif selected == _("Predictive Modeling"):
    predictive_modeling(data)  # Pass the data for predictive modeling
elif selected == _("Chatbot"):
    chatbot_interface()
elif selected == _("Community Forum"):
    community_forum()
elif selected == _("Contact Professionals"):
    contact_professionals()
elif selected == _("Sentiment Analysis"):
    sentiment_analysis(data)  # Pass the data if needed for sentiment analysis
# elif selected == _("Analytics"):
#    st.header(_("Analytics"))
#    st.markdown(_("This section can include advanced analytics features such as predictive modeling insights, trend analysis, and more."))
    # Placeholder for future analytics features
# elif selected == _("Settings"):
#    st.header(_("Settings"))
#    st.markdown(_("Customize your dashboard settings here."))
    # Placeholder for future settings features

if __name__ == '__main__':
    main()
