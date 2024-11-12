# app.py

import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import datetime
import time
import re
import firebase_admin
from firebase_admin import credentials, firestore, auth as firebase_auth
from textblob import TextBlob
import nltk

# Download NLTK data
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

# Initialize Firebase Admin SDK
def initialize_firebase():
    if not firebase_admin._apps:
        try:
            # Use Streamlit secrets to store credentials securely
            cred_info = {
                "type": st.secrets["firebase"]["type"],
                "project_id": st.secrets["firebase"]["project_id"],
                "private_key_id": st.secrets["firebase"]["315c2f7e72dca93253e29f39546938736754abb7"], 
               # "private_key": st.secrets["firebase"][""-----315c2f7e72dca93253e29f39546938736754abb7-----\n...-----END PRIVATE KEY-----\n""].replace('\\n', '\n'),
                "client_email": st.secrets["firebase"]["firebase-adminsdk-ga5rt@ment-heath-ai.iam.gserviceaccount.com"],
                "client_id": st.secrets["firebase"]["103021278198169092289"],
                "auth_uri": st.secrets["firebase"]["https://accounts.google.com/o/oauth2/auth"],
                "token_uri": st.secrets["firebase"]["https://oauth2.googleapis.com/token"],
                "auth_provider_x509_cert_url": st.secrets["firebase"]["https://www.googleapis.com/oauth2/v1/certs"],
                "client_x509_cert_url": st.secrets["firebase"]["https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-ga5rt%40ment-heath-ai.iam.gserviceaccount.com"],
                "universe_domain": st.secrets["firebase"]["googleapis.com"]
            }
            cred = credentials.Certificate(cred_info)
            firebase_admin.initialize_app(cred)
        except Exception as e:
            st.error(f"Failed to initialize Firebase: {e}")
            st.stop()

initialize_firebase()

db = firestore.client()

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
}
/* Sidebar */
.stSidebar {
    background-color: #fff;
}
.stButton>button {
    color: white;
    background-color: #ff7f50;
}
/* Progress bar */
.stProgress > div > div > div > div {
    background-color: #ff7f50;
}
/* Chat messages */
.chat-message {
    padding: 10px;
    border-radius: 5px;
    margin-bottom: 5px;
    max-width: 70%;
}
.user-message {
    background-color: #DCF8C6;
    align-self: flex-end;
}
.professional-message {
    background-color: #FFFFFF;
    align-self: flex-start;
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
/* Headers */
h1, h2, h3, h4 {
    color: #333;
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
        "Gender Distribution": "Igendera",
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
        # Add more translations as needed
    }
    if st.session_state.get('language') == "Kinyarwanda":
        return translations.get(text, text)
    else:
        return text

# User Authentication
def user_authentication():
    if 'user' not in st.session_state:
        st.session_state['user'] = None

    menu = ["Home", "Login", "SignUp"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        if st.session_state['user']:
            st.sidebar.write(f"Logged in as: {st.session_state['user']['email']}")
            if st.sidebar.button("Logout"):
                st.session_state['user'] = None
                st.experimental_rerun()
        else:
            st.sidebar.write("Please login to access more features.")
    elif choice == "Login":
        st.title("Login")
        email = st.text_input("Email")
        password = st.text_input("Password", type='password')
        if st.button("Login"):
            try:
                user = firebase_auth.get_user_by_email(email)
                # Implement proper password verification in production
                st.session_state['user'] = {"uid": user.uid, "email": email}
                st.success("Logged in successfully!")
                st.experimental_rerun()
            except Exception as e:
                st.error("Invalid credentials or user does not exist.")
    elif choice == "SignUp":
        st.title("Create a New Account")
        email = st.text_input("Email")
        password = st.text_input("Password", type='password')
        if st.button("Sign Up"):
            try:
                user = firebase_auth.create_user(email=email, password=password)
                st.success("Account created successfully! Please login.")
            except Exception as e:
                st.error(f"Error creating account: {e}")

# Function to simulate data
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

# Function for the home page
def home():
    st.title("🧠 " + _("Mental Health Dashboard for Rwandan Youth"))
    st.markdown("### " + _("Welcome to the Mental Health Dashboard"))
    st.markdown(_("""
    This dashboard provides insights into the mental health of Rwandan youth. Explore data visualizations, predictive modeling, and engage with our interactive chatbot.
    """))
    st.image("https://www.who.int/images/default-source/mca/mca-covid-image-hi-res.jpg", use_column_width=True)
    st.markdown(_("""
    **Navigate through the sidebar to explore different sections of the dashboard.**
    """))

# Function for data visualization
def data_visualization(data):
    st.header("📊 " + _("Data Visualization"))

    st.subheader(_("Demographics Overview"))
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("#### " + _("Gender Distribution"))
        gender_counts = data['Gender'].value_counts()
        fig = px.pie(
            names=gender_counts.index,
            values=gender_counts.values,
            color=gender_counts.index,
            color_discrete_map={'Male': '#636EFA', 'Female': '#EF553B'},
            hole=0.5
        )
        fig.update_traces(textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### " + _("Age Distribution"))
        fig = px.histogram(data, x='Age', nbins=10, color_discrete_sequence=['#00CC96'])
        st.plotly_chart(fig, use_container_width=True)

    with col3:
        st.markdown("#### " + _("Regional Distribution"))
        region_counts = data['Region'].value_counts().reset_index()
        region_counts.columns = ['Region', 'Count']
        fig = px.bar(region_counts, x='Region', y='Count', color='Region',
                     color_discrete_sequence=px.colors.qualitative.Set2)
        st.plotly_chart(fig, use_container_width=True)

    st.subheader(_("Mental Health Metrics Over Time"))
    metrics = ['Depression_Score', 'Anxiety_Score', 'Stress_Level']
    selected_metrics = st.multiselect(_("Select metrics to display:"), metrics, default=metrics)
    if selected_metrics:
        fig = px.line(
            data, x='Date', y=selected_metrics,
            labels={'value': _('Score'), 'variable': _('Metric')},
            color_discrete_sequence=px.colors.qualitative.G10
        )
        st.plotly_chart(fig, use_container_width=True)

    st.subheader(_("Correlation Matrix"))
    corr_matrix = data[['Depression_Score', 'Anxiety_Score', 'Stress_Level',
                        'Social_Media_Usage', 'Physical_Activity', 'Sleep_Duration']].corr()
    fig = px.imshow(corr_matrix, text_auto=True, aspect="auto",
                    color_continuous_scale='RdBu_r', zmin=-1, zmax=1)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader(_("Scatter Plot Matrix"))
    fig = px.scatter_matrix(
        data,
        dimensions=['Depression_Score', 'Anxiety_Score', 'Stress_Level',
                    'Social_Media_Usage', 'Physical_Activity', 'Sleep_Duration'],
        color='Gender',
        color_discrete_map={'Male': '#636EFA', 'Female': '#EF553B'}
    )
    st.plotly_chart(fig, use_container_width=True)

# Function for predictive modeling
def predictive_modeling(data):
    st.header("🤖 " + _("Predictive Modeling"))

    st.markdown("### " + _("Predicting Depression Scores"))
    st.markdown(_("""
    Adjust the input parameters to predict the depression score.
    """))

    # Prepare the data
    features = ['Age', 'Social_Media_Usage', 'Physical_Activity', 'Sleep_Duration']
    X = data[features]
    y = data['Depression_Score']

    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    # Train the model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Feature importance
    st.subheader(_("Feature Importance"))
    importance = model.feature_importances_
    feature_importance = pd.DataFrame({'Feature': features, 'Importance': importance})
    fig = px.bar(feature_importance, x='Importance', y='Feature', orientation='h',
                 color='Importance', color_continuous_scale='Viridis')
    st.plotly_chart(fig, use_container_width=True)

    # Model evaluation
    st.subheader(_("Model Performance"))
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    st.write(f"{_('Mean Squared Error on Test Set')}: **{mse:.2f}**")

    # Prediction form
    st.subheader(_("Make a Prediction"))
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
        input_features = np.array([[age, social_media, physical_activity, sleep_duration]])
        prediction = model.predict(input_features)
        st.success(f"{_('Predicted Depression Score')}: **{prediction[0]:.2f}**")
        st.info(_("Note: Higher scores indicate higher levels of depression."))

# Function for the chatbot
def chatbot_interface():
    st.header("🗣️ " + _("Mental Health Chatbot"))

    st.write(_("Hello! I'm **Menti**, your mental health assistant. How can I help you today?"))

    if 'history' not in st.session_state:
        st.session_state['history'] = []

    # Chat interface
    user_input = st.text_input(_("You") + ":", "", key="input")
    if user_input:
        # Sentiment Analysis
        def analyze_sentiment(text):
            text = re.sub(r'[^\w\s]', '', text)
            analysis = TextBlob(text)
            return analysis.sentiment.polarity

        sentiment = analyze_sentiment(user_input)
        if sentiment < -0.5:
            response = _("I'm sorry to hear that you're feeling this way. Would you like to talk about it?")
        elif sentiment < 0:
            response = _("It seems you're not feeling well. I'm here to listen if you want to share.")
        elif sentiment == 0:
            response = _("Thank you for sharing. How else can I assist you?")
        else:
            response = _("I'm glad to hear that! Is there anything else you'd like to discuss?")
        st.session_state.history.append({"user": user_input, "assistant": response})

    # Display conversation history
    for chat in st.session_state.history:
        st.markdown(f"<div class='chat-message user-message'><strong>{_('You')}:</strong> {chat['user']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='chat-message assistant-message'><strong>Menti:</strong> {chat['assistant']}</div>", unsafe_allow_html=True)

# Innovative features in the sidebar
def innovative_features():
    st.sidebar.markdown("---")
    st.sidebar.header("📚 " + _("Mental Health Resources"))
    st.sidebar.markdown("""
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

# Real-time Chat with Professionals
def chat_with_professional():
    st.header("💬 " + _("Chat with a Professional"))

    if 'user' not in st.session_state or not st.session_state['user']:
        st.warning(_("Please login to access the chat feature."))
        return

    # Simulated list of professionals online
    professionals = [
        {
            "name": "Dr. Jean Mukiza",
            "uid": "prof_jean",
        },
        {
            "name": "Dr. Aline Uwase",
            "uid": "prof_aline",
        },
    ]

    # Select a professional to chat with
    professional = st.selectbox(_("Choose a professional to chat with"), professionals, format_func=lambda x: x['name'])
    chat_id = f"{st.session_state['user']['uid']}_{professional['uid']}"

    st.write(f"{_('Chatting with')} **{professional['name']}**")

    # Chat container
    messages_ref = db.collection("chats").document(chat_id).collection("messages")
    messages = messages_ref.order_by("timestamp").stream()
    messages_list = []
    for msg in messages:
        messages_list.append(msg.to_dict())

    # Display messages
    chat_container = st.container()
    with chat_container:
        for msg in messages_list:
            if msg['sender'] == st.session_state['user']['uid']:
                st.markdown(f"<div class='chat-message user-message'>{msg['content']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='chat-message professional-message'><strong>{professional['name']}:</strong> {msg['content']}</div>", unsafe_allow_html=True)

    # Message input
    message = st.text_input(_("Type your message here..."))
    if st.button(_("Send")):
        if message.strip() != "":
            new_message = {
                "sender": st.session_state['user']['uid'],
                "receiver": professional['uid'],
                "content": message,
                "timestamp": datetime.datetime.utcnow()
            }
            messages_ref.add(new_message)
            st.experimental_rerun()

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
        st.session_state.forum_posts.append({"username": username, "content": post_content, "time": datetime.datetime.now()})
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
        },
        # Add more professionals or entities as needed
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
                # Integrate with a VoIP service API or similar if needed
            if st.button(f"{_('Email')} {prof['name']}", key=prof["email"]):
                st.info(f"{_('Opening email client for')} {prof['email']}...")
                # Use mailto link or integrate with email service if needed
        st.write("---")

# Main function
def main():
    set_language()
    user_authentication()

    # Sidebar navigation
    if 'user' in st.session_state and st.session_state['user']:
        options = [
            "Home",
            "Data Visualization",
            "Predictive Modeling",
            "Chatbot",
            "Community Forum",
            "Contact Professionals",
            "Chat with Professional"
        ]
        icons = ["house", "bar-chart", "cpu", "chat-dots", "people", "telephone", "chat"]
    else:
        options = ["Home", "Login/SignUp"]
        icons = ["house", "person"]

    selected = option_menu(
        menu_title=_("Main Menu"),
        options=options,
        icons=icons,
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "#f0f2f6"},
            "icon": {"color": "#ff7f50", "font-size": "18px"},
            "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "#ff7f50"},
        },
    )

    innovative_features()

    data = simulate_data()

    if selected == "Home":
        home()
    elif selected == "Data Visualization":
        data_visualization(data)
    elif selected == "Predictive Modeling":
        predictive_modeling(data)
    elif selected == "Chatbot":
        chatbot_interface()
    elif selected == "Community Forum":
        community_forum()
    elif selected == "Contact Professionals":
        contact_professionals()
    elif selected == "Chat with Professional":
        chat_with_professional()
    elif selected == "Login/SignUp":
        user_authentication()

if __name__ == '__main__':
    main()
