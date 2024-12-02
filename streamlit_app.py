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

