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
    }
    if st.session_state.get('language') == "Kinyarwanda":
        return translations.get(text, text)
    else:
        return text

# Simulate data function for visualization
@st.cache(allow_output_mutation=True)
def simulate_data():
    np.random.seed(42)
    num_samples = 1000
    data = pd.DataFrame({
        'Age': np.random.randint(15, 25, num_samples),
        'Gender': np.random.choice(['Male', 'Female'], num_samples),
        'Depression_Score': np.random.normal(50, 15, num_samples),
        'Anxiety_Score': np.random.normal(50, 15, num_samples),
        'Stress_Level': np.random.normal(50, 15, num_samples),
        'Social_Media_Usage': np.random.randint(0, 12, num_samples),  # Hours per day
        'Physical_Activity': np.random.randint(0, 14, num_samples),    # Hours per week
        'Sleep_Duration': np.random.normal(7, 1.5, num_samples),      # Hours per night
        'Region': np.random.choice(['Kigali', 'Northern', 'Southern', 'Eastern', 'Western'], num_samples),
        'Date': pd.date_range(start='2022-01-01', periods=num_samples, freq='D').tolist()
    })
    # Ensure scores are within 0-100
    for score in ['Depression_Score', 'Anxiety_Score', 'Stress_Level']:
        data[score] = data[score].clip(0, 100)
    # Ensure no missing values in 'Region'
    data['Region'] = data['Region'].fillna('Unknown')
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

    # Add a Summary Statistics Section
    st.subheader("📈 " + _("Summary Statistics"))
    st.markdown("Display key statistics about the dataset to provide a quick overview.")
    summary = data.describe().T
    summary['median'] = data.median()
    st.dataframe(summary[['mean', 'median', 'std', 'min', 'max']].round(2))

    # Key Performance Indicators (KPIs)
    st.subheader("🚀 " + _("Key Performance Indicators"))
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1:
        st.metric(label=_("Total Users"), value=len(data))
    with col2:
        avg_dep = data['Depression_Score'].mean().round(2)
        st.metric(label=_("Average Depression Score"), value=avg_dep)
    with col3:
        avg_anx = data['Anxiety_Score'].mean().round(2)
        st.metric(label=_("Average Anxiety Score"), value=avg_anx)
    with col4:
        avg_str = data['Stress_Level'].mean().round(2)
        st.metric(label=_("Average Stress Level"), value=avg_str)
    with col5:
        avg_sm = data['Social_Media_Usage'].mean().round(2)
        st.metric(label=_("Average Social Media Usage"), value=f"{avg_sm} hrs/day")
    with col6:
        avg_pa = data['Physical_Activity'].mean().round(2)
        st.metric(label=_("Average Physical Activity"), value=f"{avg_pa} hrs/week")

# Data visualization function with more charts and dashboard-like layout
def data_visualization(data):
    st.header("📊 " + _("Data Visualization"))

    # Apply Filters
    st.sidebar.header(_("Data Filters"))
    selected_region = st.sidebar.multiselect(_("Select Region(s)"), options=data['Region'].unique(), default=data['Region'].unique())
    selected_gender = st.sidebar.multiselect(_("Select Gender(s)"), options=data['Gender'].unique(), default=data['Gender'].unique())
    age_range = st.sidebar.slider(_("Select Age Range"), min_value=15, max_value=25, value=(15,25))
    date_range = st.sidebar.date_input(_("Select Date Range"), [data['Date'].min(), data['Date'].max()])

    # Filter data based on selections
    filtered_data = data[
        (data['Region'].isin(selected_region)) &
        (data['Gender'].isin(selected_gender)) &
        (data['Age'] >= age_range[0]) & (data['Age'] <= age_range[1]) &
        (data['Date'] >= pd.to_datetime(date_range[0])) & (data['Date'] <= pd.to_datetime(date_range[1]))
    ]

    st.markdown(f"**{len(filtered_data)}** records found based on the selected filters.")

    # Tabs for organizing visualizations
    tabs = st.tabs(["Overview", "Demographics", "Mental Health Metrics", "Advanced Analysis"])

    # Overview Tab
    with tabs[0]:
        st.subheader(_("Key Metrics Overview"))
        col1, col2, col3 = st.columns(3)
        with col1:
            avg_dep = filtered_data['Depression_Score'].mean().round(2)
            st.metric(label=_("Average Depression Score"), value=avg_dep)
        with col2:
            avg_anx = filtered_data['Anxiety_Score'].mean().round(2)
            st.metric(label=_("Average Anxiety Score"), value=avg_anx)
        with col3:
            avg_str = filtered_data['Stress_Level'].mean().round(2)
            st.metric(label=_("Average Stress Level"), value=avg_str)

        # Geographical Map
        st.subheader(_("Geographical Distribution of Depression Scores"))
        region_metrics = filtered_data.groupby('Region')['Depression_Score'].mean().reset_index()
        fig = px.choropleth(
            region_metrics,
            locations='Region',
            locationmode='USA-states',  # Adjust as per your map requirements
            color='Depression_Score',
            color_continuous_scale='Viridis',
            scope='africa',
            labels={'Depression_Score': 'Avg Depression Score'},
            title='Average Depression Score by Region'
        )
        st.plotly_chart(fig, use_container_width=True)

    # Demographics Tab
    with tabs[1]:
        st.subheader(_("User Demographics"))

        # Age Distribution
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(_("**Age Distribution**"))
            fig = px.histogram(filtered_data, x='Age', nbins=10, color='Gender', barmode='overlay', opacity=0.7)
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            st.markdown(_("**Gender Distribution**"))
            fig = px.pie(filtered_data, names='Gender', title='Gender Distribution', color_discrete_map={'Male': '#636EFA', 'Female': '#EF553B'})
            st.plotly_chart(fig, use_container_width=True)

        # Treemap
        st.markdown(_("**User Distribution by Region and Gender**"))
        fig = px.treemap(filtered_data, path=['Region', 'Gender'], title='User Distribution', color='Gender',
                         color_discrete_map={'Male': '#636EFA', 'Female': '#EF553B'})
        st.plotly_chart(fig, use_container_width=True)

    # Mental Health Metrics Tab
    with tabs[2]:
        st.subheader(_("Mental Health Metrics"))

        # Mental Health Trends over Time (Depression, Anxiety, Stress)
        st.markdown(_("**Mental Health Trends Over Time**"))
        metrics = ['Depression_Score', 'Anxiety_Score', 'Stress_Level']
        selected_metrics = st.multiselect(_("Select metrics to display:"), metrics, default=metrics)
        if selected_metrics:
            fig = px.line(
                filtered_data, x='Date', y=selected_metrics,
                labels={'value': _('Score'), 'variable': _('Metric')},
                color_discrete_sequence=px.colors.qualitative.G10
            )
            st.plotly_chart(fig, use_container_width=True)

        # Distribution Plots
        st.markdown(_("**Distribution of Mental Health Scores**"))
        col1, col2, col3 = st.columns(3)
        with col1:
            fig = px.histogram(filtered_data, x='Depression_Score', nbins=20, title='Depression Score Distribution', color='Gender', barmode='overlay', opacity=0.7)
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            fig = px.histogram(filtered_data, x='Anxiety_Score', nbins=20, title='Anxiety Score Distribution', color='Gender', barmode='overlay', opacity=0.7)
            st.plotly_chart(fig, use_container_width=True)
        with col3:
            fig = px.histogram(filtered_data, x='Stress_Level', nbins=20, title='Stress Level Distribution', color='Gender', barmode='overlay', opacity=0.7)
            st.plotly_chart(fig, use_container_width=True)

    # Advanced Analysis Tab
    with tabs[3]:
        st.subheader(_("Advanced Analysis"))

        # Correlation Matrix
        st.markdown(_("**Correlation Matrix**"))
        corr = filtered_data[['Depression_Score', 'Anxiety_Score', 'Stress_Level', 'Social_Media_Usage', 
                            'Physical_Activity', 'Sleep_Duration', 'Age']].corr()
        fig = px.imshow(corr, text_auto=True, aspect="auto", color_continuous_scale='RdBu_r')
        fig.update_layout(title_text=_("Correlation Matrix of Mental Health Metrics"))
        st.plotly_chart(fig, use_container_width=True)

        # Scatter Plot Matrix
        st.markdown(_("**Scatter Plot Matrix**"))
        fig = px.scatter_matrix(
            filtered_data,
            dimensions=['Depression_Score', 'Anxiety_Score', 'Stress_Level', 'Social_Media_Usage', 'Physical_Activity', 'Sleep_Duration'],
            color='Gender',
            title=_("Scatter Plot Matrix of Mental Health Metrics"),
            color_discrete_map={'Male': '#636EFA', 'Female': '#EF553B'}
        )
        st.plotly_chart(fig, use_container_width=True)

        # Trellis Plot (Faceted Scatter)
        st.markdown(_("**Trellis Plot: Depression vs. Anxiety by Gender**"))
        fig = px.scatter(
            filtered_data,
            x='Depression_Score',
            y='Anxiety_Score',
            color='Gender',
            facet_col='Gender',
            trendline='ols',
            title='Depression vs. Anxiety Scores by Gender'
        )
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
        # Simulate chatbot response using TextBlob for sentiment analysis
        blob = TextBlob(user_input)
        sentiment = blob.sentiment.polarity
        if sentiment > 0.1:
            assistant_response = "That's great to hear! How can I assist you further?"
        elif sentiment < -0.1:
            assistant_response = "I'm sorry you're feeling this way. Please consider reaching out to a professional for support."
        else:
            assistant_response = "I understand. Could you please provide more details or specify how I can help you?"

        st.session_state.history.append({"user": user_input, "assistant": assistant_response})

    # Display conversation history
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
    for chat in st.session_state.history:
        st.markdown(f"<div class='chat-message user-message'><strong>{_('You')}:</strong> {chat['user']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='chat-message assistant-message'><strong>Menti:</strong> {chat['assistant']}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Optionally, add a Word Cloud based on user inputs
    if st.checkbox(_("Show Word Cloud of Your Conversations")):
        all_text = ' '.join([chat['user'] for chat in st.session_state.history])
        if all_text:
            wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_text)
            plt.figure(figsize=(10, 5))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis('off')
            st.pyplot(plt)
        else:
            st.write(_("No conversations to display."))

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

# Geographical Distribution Map (Additional Feature)
def geographical_distribution_map(data):
    st.subheader(_("Geographical Distribution of Mental Health Scores"))
    region_metrics = data.groupby('Region')[['Depression_Score', 'Anxiety_Score', 'Stress_Level']].mean().reset_index()

    # Assuming you have a GeoJSON file for Rwanda regions, you can create a choropleth map.
    # For demonstration, we'll use a simplified approach.

    # Placeholder for actual geographical mapping
    # You need to provide the correct GeoJSON or use Plotly's built-in map features
    try:
        fig = px.choropleth(
            region_metrics,
            locations='Region',
            locationmode='country names',  # Adjust as needed
            color='Depression_Score',
            color_continuous_scale='Viridis',
            scope='africa',
            labels={'Depression_Score': 'Avg Depression Score'},
            title='Average Depression Score by Region'
        )
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error generating geographical map: {e}")

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

    # Simulate data once to avoid regenerating it on every interaction
    data = simulate_data()

    # Display user authentication sidebar
    user_authentication()

    # Handle navigation
    if selected == _("Home"):
        home(data)
    elif selected == _("Data Visualization"):
        data_visualization(data)
    elif selected == _("Predictive Modeling"):
        predictive_modeling()
    elif selected == _("Chatbot"):
        chatbot_interface()
    elif selected == _("Community Forum"):
        community_forum()
    elif selected == _("Contact Professionals"):
        contact_professionals()
    elif selected == _("Sentiment Analysis"):
        sentiment_analysis()
    elif selected == _("Analytics"):
        st.header(_("Analytics"))
        st.markdown(_("This section can include advanced analytics features such as predictive modeling insights, trend analysis, and more."))
        # Placeholder for future analytics features
    elif selected == _("Settings"):
        st.header(_("Settings"))
        st.markdown(_("Customize your dashboard settings here."))
        # Placeholder for future settings features

if __name__ == '__main__':
    main()
