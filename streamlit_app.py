# app.py

import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import os
import joblib
import datetime
import altair as alt
import nltk
from textblob import TextBlob
import re
import base64
from io import BytesIO
import time

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
    .main {
        background-color: #f5f5f5;
    }
    .stButton>button {
        color: white;
        background-color: #ff7f50;
    }
    .stProgress > div > div > div > div {
        background-color: #ff7f50;
    }
</style>
""", unsafe_allow_html=True)

# Multilingual Support
def set_language():
    lang = st.sidebar.selectbox("Choose Language / Hitamo Ururimi", ["English", "Kinyarwanda"])
    return lang

language = set_language()

def _(text):
    translations = {
        "Welcome to the Mental Health Dashboard": "Murakaza neza kuri Dashboard y'Ubuzima bwo mu Mutwe",
        "This dashboard aims to provide insights into the mental health of Rwandan youth and offer solutions through data visualization, predictive modeling, and an interactive chatbot.":
            "Iyi dashboard igamije gutanga ishusho y'ubuzima bwo mu mutwe bw'urubyiruko rw'u Rwanda no gutanga ibisubizo binyuze mu kugaragaza amakuru, gutekereza ku byashoboka, no gukoresha chatbot.",
        # Add more translations as needed
    }
    if language == "Kinyarwanda":
        return translations.get(text, text)
    else:
        return text

# Simulate real-time data
def simulate_real_time_data():
    np.random.seed(int(time.time()) % 10000)
    data = pd.DataFrame({
        'Timestamp': [datetime.datetime.now() - datetime.timedelta(minutes=i) for i in range(200)],
        'Age': np.random.randint(15, 25, 200),
        'Gender': np.random.choice(['Male', 'Female'], 200),
        'Depression_Score': np.random.normal(50, 15, 200),
        'Anxiety_Score': np.random.normal(50, 15, 200),
        'Stress_Level': np.random.normal(50, 15, 200),
        'Social_Media_Usage': np.random.randint(1, 10, 200),
        'Physical_Activity': np.random.randint(0, 5, 200),
        'Region': np.random.choice(['Kigali', 'Northern', 'Southern', 'Eastern', 'Western'], 200)
    })
    return data

# Innovative features
def innovative_features():
    st.sidebar.markdown("---")
    st.sidebar.header("📚 Mental Health Resources / Amakuru ku buzima bwo mu mutwe")
    st.sidebar.markdown("""
    - **Hotlines / Nimero z'Ubufasha:**
        - Rwanda Mental Health Hotline: **1234**
    - **Online Resources / Imbuga z'Ubuzima bwo mu Mutwe:**
        - [Ministry of Health Rwanda](https://www.moh.gov.rw)
        - [WHO Mental Health](https://www.who.int/mental_health/en/)
    """)
    
    st.sidebar.header("💡 Daily Mental Health Tip / Inama y'Umunsi")
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
    st.sidebar.info(f"**{_('Tip')} / Inama:** {tip}")
    
    # Gamification Elements
    st.sidebar.header("🎯 Daily Challenge / Inshingano y'Umunsi")
    challenges = [
        _("Spend 30 minutes exercising today."),
        _("Call someone you haven't talked to in a while."),
        _("Try a new healthy recipe."),
        _("Write down three things you're grateful for."),
        _("Take a break from social media for a day.")
    ]
    challenge = np.random.choice(challenges)
    st.sidebar.success(f"**{_('Challenge')} / Inshingano:** {challenge}")
    
    # Reward System
    if 'points' not in st.session_state:
        st.session_state['points'] = 0
    st.sidebar.markdown(f"**{_('Points')} / Amanota:** {st.session_state['points']}")
    if st.sidebar.button(_("Complete Challenge") + " / Kuzuza Inshingano"):
        st.session_state['points'] += 10
        st.sidebar.balloons()
        st.sidebar.success(_("Great job on completing the challenge!") + " / Wakoze cyane kuzuza inshingano!")

# Data Visualization
def data_visualization(data):
    st.header("📊 " + _("Data Visualization") + " / Kwerekana Amakuru")
    
    st.subheader(_("Demographics Overview") + " / Isura Rusange y'Amakuru")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### " + _("Gender Distribution") + " / Igendero")
        gender_counts = data['Gender'].value_counts()
        fig = px.pie(
            names=gender_counts.index,
            values=gender_counts.values,
            color=gender_counts.index,
            color_discrete_map={'Male': '#636EFA', 'Female': '#EF553B'},
            hole=0.4
        )
        fig.update_layout(showlegend=True)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### " + _("Age Distribution") + " / Imyaka")
        fig = px.histogram(data, x='Age', nbins=10, color_discrete_sequence=['#00CC96'])
        st.plotly_chart(fig, use_container_width=True)
    
    with col3:
        st.markdown("### " + _("Stress Level by Gender") + " / Urwego rw'Umuvuduko w'Ubuzima bwo mu Mutwe n'Igitsina")
        fig = px.box(data, x='Gender', y='Stress_Level', color='Gender',
                     color_discrete_map={'Male': '#636EFA', 'Female': '#EF553B'})
        st.plotly_chart(fig, use_container_width=True)
    
    st.subheader(_("Mental Health Scores Over Time") + " / Amanota y'Ubuzima bwo mu Mutwe Mu Gihe")
    fig = px.line(
        data, x='Timestamp', y=['Depression_Score', 'Anxiety_Score', 'Stress_Level'],
        labels={'value': _('Score'), 'variable': _('Metric')},
        color_discrete_sequence=px.colors.qualitative.G10
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader(_("Physical Activity vs. Anxiety Score") + " / Imyitozo ngororamubiri na Anxiete")
    fig = px.scatter(
        data, x='Physical_Activity', y='Anxiety_Score', color='Gender',
        labels={'Physical_Activity': _('Physical Activity (hours/week)'), 'Anxiety_Score': _('Anxiety Score')},
        color_discrete_map={'Male': '#636EFA', 'Female': '#EF553B'},
        trendline='ols',
        hover_data=['Age']
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader(_("Regional Distribution") + " / Ikarita y'U Rwanda")
    region_counts = data['Region'].value_counts().reset_index()
    region_counts.columns = ['Region', 'Count']
    fig = px.bar(region_counts, x='Region', y='Count', color='Region',
                 color_discrete_sequence=px.colors.qualitative.Set2)
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader(_("Correlation Matrix") + " / Ishusho y'Isano")
    corr = data[['Depression_Score', 'Anxiety_Score', 'Stress_Level', 'Social_Media_Usage', 'Physical_Activity']].corr()
    fig = px.imshow(corr, text_auto=True, aspect="auto", color_continuous_scale='RdBu_r', zmin=-1, zmax=1)
    st.plotly_chart(fig, use_container_width=True)

# Predictive Modeling
def predictive_modeling(data):
    st.header("🤖 " + _("Predictive Modeling") + " / Guhanga Icyashoboka")
    
    X = data[['Age', 'Social_Media_Usage', 'Physical_Activity']]
    y = data['Depression_Score']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    
    model = RandomForestRegressor(n_estimators=100)
    model.fit(X_train, y_train)
    
    st.subheader(_("Model Performance") + " / Imikorere y'Icyitegererezo")
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    st.write(f"Mean Squared Error / Ikosa Ryo Ku Gipimo: **{mse:.2f}**")
    
    st.subheader(_("Feature Importance") + " / Icy'ingenzi mu Bipimo")
    feat_importances = pd.Series(model.feature_importances_, index=X.columns)
    fig = px.bar(feat_importances, x=feat_importances.values, y=feat_importances.index, orientation='h',
                 labels={'x': _('Importance'), 'y': _('Feature')},
                 color=feat_importances.values, color_continuous_scale='Viridis')
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader(_("Make a Prediction") + " / Kora Iteganyizo")
    with st.form(key='prediction_form'):
        col1, col2, col3 = st.columns(3)
        with col1:
            age = st.slider(_("Age"), min_value=15, max_value=25, value=20)
        with col2:
            social_media = st.slider(_("Social Media Usage (hours/day)"), min_value=0, max_value=24, value=2)
        with col3:
            physical_activity = st.slider(_("Physical Activity (hours/week)"), min_value=0, max_value=40, value=3)
        submit_button = st.form_submit_button(label=_('Predict') + " / Teganya")
    
    if submit_button:
        input_features = np.array([[age, social_media, physical_activity]])
        prediction = model.predict(input_features)
        st.success(f"{_('Predicted Depression Score')}: **{prediction[0]:.2f}**")
        st.info(_("Note: Higher scores indicate higher levels of depression.") + " / Icyitonderwa: Amanota menshi agaragaza urwego rwo hejuru rw'agahinda.")

# Sentiment Analysis Chatbot
def chatbot_interface():
    st.header("🗣️ Menti AI Chatbot")
    
    st.write(_("Hello! I'm **Menti**, your mental health assistant. How can I help you today?") +
             " / Muraho! Ndi **Menti**, umufasha wawe mu buzima bwo mu mutwe. Nigute nakugira inama uyu munsi?")
    
    if 'history' not in st.session_state:
        st.session_state['history'] = []
    
    # Chat interface
    user_input = st.text_input(_("You") + " / Wowe:", "", key="input")
    if user_input:
        # Sentiment Analysis
        def analyze_sentiment(text):
            text = re.sub(r'[^\w\s]', '', text)
            analysis = TextBlob(text)
            return analysis.sentiment.polarity
        
        sentiment = analyze_sentiment(user_input)
        if sentiment < -0.5:
            response = _("I'm sorry to hear that you're feeling this way. Would you like to talk about it?") + \
                " / Mbabajwe no kumva ko wiyumva utyo. Ushobora kumbwira byinshi?"
        elif sentiment < 0:
            response = _("It seems you're not feeling well. I'm here to listen if you want to share.") + \
                " / Bisa nk'aho utameze neza. Ndi hano kugira ngo nkumve niba ushaka gusangiza."
        elif sentiment == 0:
            response = _("Thank you for sharing. How else can I assist you?") + \
                " / Urakoze kudusangiza. Ni iki kindi nakumarira?"
        else:
            response = _("I'm glad to hear that! Is there anything else you'd like to discuss?") + \
                " / Nishimiye kumva ibyo! Hari ikindi ushaka tuganireho?"
        st.session_state.history.append({"user": user_input, "assistant": response})
    
    # Display conversation history
    for chat in st.session_state.history:
        st.markdown(f"**{_('You')} / Wowe:** {chat['user']}")
        st.markdown(f"**Menti:** {chat['assistant']}")
        st.write("---")

# Community Forum
def community_forum():
    st.header("🌐 " + _("Community Forum") + " / Urubuga rw'Abaturage")
    st.write(_("Connect with others anonymously to share experiences and support each other.") +
             " / Huza n'abandi mu ibanga kugira ngo musangire ubunararibonye no gufashanya.")
    
    if 'forum_posts' not in st.session_state:
        st.session_state['forum_posts'] = []
    
    with st.form(key='forum_form'):
        username = st.text_input(_("Username (anonymous)") + " / Izina (mu ibanga):", "Anonymous")
        post_content = st.text_area(_("Share your thoughts or experiences") + " / Sangiza ibitekerezo byawe cyangwa ubunararibonye:")
        submit_post = st.form_submit_button(label=_('Post') + " / Ohereza")
    
    if submit_post and post_content:
        st.session_state.forum_posts.append({"username": username, "content": post_content, "time": datetime.datetime.now()})
        st.success(_("Your post has been shared!") + " / Ubutumwa bwawe bwoherejwe!")
    
    st.subheader(_("Recent Posts") + " / Ubutumwa Bushya")
    for post in reversed(st.session_state.forum_posts):
        st.markdown(f"**{post['username']}** at {post['time'].strftime('%Y-%m-%d %H:%M:%S')}")
        st.markdown(f">{post['content']}")
        st.write("---")

# Main function
def main():
    # Sidebar navigation
    with st.sidebar:
        selected = option_menu(
            menu_title="Main Menu / Iby'ingenzi",
            options=["Home / Ahabanza", "Data Visualization / Kwerekana Amakuru", "Predictive Modeling / Guhanga Icyashoboka", "Chatbot / Chatbot", "Community Forum / Urubuga rw'Abaturage"],
            icons=["house", "bar-chart", "cpu", "chat-dots", "people"],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"padding": "0!important", "background-color": "#f0f2f6"},
                "icon": {"color": "orange", "font-size": "25px"},
                "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
                "nav-link-selected": {"background-color": "#ff7f50"},
            },
        )
    
    innovative_features()
    
    data = simulate_real_time_data()
    
    if selected == 'Home / Ahabanza':
        st.title("🧠 Mental Health Dashboard for Rwandan Youth / Dashboard y'Ubuzima bwo mu Mutwe bw'Urubyiruko rw'u Rwanda")
        st.markdown(f"## {_('Welcome to the Mental Health Dashboard')}")
        st.markdown(_("""
        This dashboard aims to provide insights into the mental health of Rwandan youth and offer solutions through data visualization, predictive modeling, and an interactive chatbot.
        """))
        st.image("https://www.who.int/images/default-source/mca/mca-covid-image-hi-res.jpg", use_column_width=True)
        
    elif selected == 'Data Visualization / Kwerekana Amakuru':
        data_visualization(data)
        
    elif selected == 'Predictive Modeling / Guhanga Icyashoboka':
        predictive_modeling(data)
        
    elif selected == 'Chatbot / Chatbot':
        chatbot_interface()
    
    elif selected == 'Community Forum / Urubuga rw'Abaturage':
        community_forum()
        
if __name__ == '__main__':
    main()
