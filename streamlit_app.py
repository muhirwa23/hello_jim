import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Set up the page configuration
st.set_page_config(
    page_title="World-Class AI-Powered Dashboard",
    page_icon="🚀",
    layout="wide",
)

# Custom CSS for Tailwind-like styling and animations
st.markdown("""
    <style>
    /* Global styles */
    body {
        font-family: 'Poppins', sans-serif;
    }
    .main {
        background-color: #F0F8FF;
    }
    /* Sidebar Styling */
    .stSidebar {
        background-color: #002B5B;
        color: white;
    }
    .css-1aumxhk {
        background-color: #007BFF;
        color: white;
        border-radius: 8px;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
    }
    /* Button styling */
    .stButton button {
        background-color: #007BFF;
        color: white;
        border-radius: 5px;
        font-size: 16px;
        padding: 10px;
        transition: 0.3s;
    }
    .stButton button:hover {
        background-color: #0056b3;
    }
    /* Header styling */
    h1 {
        font-size: 3em;
        font-weight: bold;
        color: #002B5B;
        text-align: center;
    }
    /* Card layout styling */
    .card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    .card h3 {
        font-size: 1.5em;
        font-weight: 600;
        margin-bottom: 15px;
    }
    .card p {
        font-size: 1.1em;
    }
    .ml-section {
        background-color: #F0F8FF;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
        margin-bottom: 30px;
    }
    /* Responsive design */
    @media screen and (max-width: 768px) {
        h1 {
            font-size: 2em;
        }
        .card {
            padding: 15px;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.title("🚀 AI & Data Science Dashboard")
st.sidebar.subheader("Navigation")
page = st.sidebar.radio("Select Page", ["Home", "Data Analysis", "Model Training", "Model Predictions"])

# Main header
st.markdown("<h1>🚀 AI-Powered Data Science Dashboard</h1>", unsafe_allow_html=True)

# Home Page
if page == "Home":
    st.markdown("## Welcome to the **Home** Page of this AI Dashboard!")
    
    # Two-column layout
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="card">
            <h3>Dashboard Features</h3>
            <p>This world-class dashboard allows you to perform:</p>
            <ul>
                <li>Interactive Data Analysis with visual charts</li>
                <li>Model Training with real-time feedback</li>
                <li>AI-Powered Predictions using trained models</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.image("https://via.placeholder.com/400x300.png?text=Data+Science+Visualization", caption="AI & Data Science", use_column_width=True)

# Data Analysis Page
elif page == "Data Analysis":
    st.markdown("## 📊 **Data Analysis** Section")

    # Load Iris Dataset
    iris = load_iris()
    df = pd.DataFrame(iris.data, columns=iris.feature_names)
    df['target'] = iris.target

    # Display DataFrame
    st.write("### Iris Dataset")
    st.dataframe(df)

    # Scatter Matrix
    st.write("### Feature Distributions")
    fig = px.scatter_matrix(df, dimensions=iris.feature_names, color="target", title="Iris Feature Correlation")
    st.plotly_chart(fig, use_container_width=True)

# Model Training Page
elif page == "Model Training":
    st.markdown("## 🧠 **Train Your Machine Learning Model**")

    # File uploader
    uploaded_file = st.file_uploader("Upload your dataset (.csv)", type=["csv"])

    if uploaded_file:
        data = pd.read_csv(uploaded_file)
        st.write("### Uploaded Dataset", data.head())

        # Sidebar Model Configuration
        st.sidebar.subheader("Model Configuration")
        test_size = st.sidebar.slider("Test Size (%)", 10, 50, 20)
        n_estimators = st.sidebar.slider("Number of Trees in Forest", 50, 200, 100)

        if st.sidebar.button("Train Model"):
            X = data.iloc[:, :-1]
            y = data.iloc[:, -1]
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size/100, random_state=42)

            # Training the model
            model = RandomForestClassifier(n_estimators=n_estimators, random_state=42)
            model.fit(X_train, y_train)
            accuracy = model.score(X_test, y_test)
            st.write(f"Model Accuracy: {accuracy * 100:.2f}%")

# Model Predictions Page
elif page == "Model Predictions":
    st.markdown("## 🔮 **Model Predictions**")

    st.write("### Enter Features for Prediction")
    feature_1 = st.number_input("Feature 1")
    feature_2 = st.number_input("Feature 2")
    feature_3 = st.number_input("Feature 3")
    feature_4 = st.number_input("Feature 4")

    if st.button("Predict"):
        if 'model' in globals():
            prediction = model.predict([[feature_1, feature_2, feature_3, feature_4]])
            st.write(f"Predicted Class: {prediction[0]}")
        else:
            st.warning("No model trained yet! Go to 'Model Training' first.")
