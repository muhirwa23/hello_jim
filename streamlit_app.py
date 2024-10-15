import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Machine Learning Libraries (Example)
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Set up page configuration
st.set_page_config(
    page_title="AI-Powered Data Science Dashboard", 
    page_icon="🔍", 
    layout="wide"
)

# Custom CSS for UI/UX Design
st.markdown("""
    <style>
    .main {
        background-color: #F0F8FF;
    }
    .stSidebar {
        background-color: #002B5B;
        color: white;
    }
    h1 {
        font-size: 2.5em;
        color: #002B5B;
        font-weight: bold;
        text-align: center;
    }
    .css-1aumxhk {
        background-color: #007BFF;
        color: white;
        border-radius: 8px;
    }
    .stButton button {
        background-color: #007BFF;
        color: white;
        border-radius: 5px;
    }
    .stTabs .tab-bar {
        border-bottom: 2px solid #007BFF;
    }
    .ml-section {
        background-color: #F0F8FF;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar - Navigation
st.sidebar.title("🔍 AI & Data Science Dashboard")
st.sidebar.subheader("Navigation")
page = st.sidebar.radio("Select Page", ["Home", "Data Analysis", "Model Training", "Model Predictions"])

# Header Animation
st.markdown("<h1 class='animate-fade'>🔍 AI-Powered Data Science Dashboard</h1>", unsafe_allow_html=True)

# Define the layout of the application
if page == "Home":
    st.markdown("## Welcome to the **Home** Page of the AI-Powered Dashboard")
    
    # A dynamic two-column layout
    col1, col2 = st.columns(2)

    # First Column: Introduction
    with col1:
        st.write("""
        This dashboard is designed for **data scientists** and **machine learning practitioners** to:
        - Perform exploratory **data analysis** with interactive charts
        - **Train models** directly from the dashboard
        - **Visualize model performance**
        - Analyze **predictions** with easy-to-use interfaces.
        """)

    # Second Column: Image or Animation
    with col2:
        st.image("https://via.placeholder.com/400x300.png?text=Data+Science+Visualization", caption="AI & Data Science", use_column_width=True)

# Data Analysis Section
elif page == "Data Analysis":
    st.markdown("## 📊 **Data Analysis** Section")

    # Load Sample Dataset (Iris dataset)
    st.subheader("Dataset Overview")
    iris = load_iris()
    df = pd.DataFrame(iris.data, columns=iris.feature_names)
    df['target'] = iris.target

    # Show DataFrame
    st.write("### Iris Dataset")
    st.dataframe(df)

    # Add Plots
    st.write("### Feature Distributions")
    fig = px.scatter_matrix(df, dimensions=iris.feature_names, color="target", title="Iris Feature Correlation")
    st.plotly_chart(fig, use_container_width=True)

# Model Training Section
elif page == "Model Training":
    st.markdown("## 🧠 **Train Your Machine Learning Model**")

    st.write("""
    This section allows you to upload your dataset, configure model parameters, and train a model using the 
    Random Forest algorithm.
    """)

    # Allow file upload
    uploaded_file = st.file_uploader("Upload your dataset (.csv)", type=["csv"])
    
    if uploaded_file:
        data = pd.read_csv(uploaded_file)
        st.write("### Uploaded Dataset", data.head())

        # Sidebar for model configuration
        st.sidebar.subheader("Model Configuration")
        test_size = st.sidebar.slider("Test Size (%)", 10, 50, 20)
        n_estimators = st.sidebar.slider("Number of Trees in Forest", 50, 200, 100)
        
        # Model training process
        if st.sidebar.button("Train Model"):
            X = data.iloc[:, :-1]
            y = data.iloc[:, -1]
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size/100, random_state=42)

            # Training Random Forest
            model = RandomForestClassifier(n_estimators=n_estimators, random_state=42)
            model.fit(X_train, y_train)
            accuracy = model.score(X_test, y_test)
            st.write(f"Model Accuracy: {accuracy * 100:.2f}%")

# Model Predictions Section
elif page == "Model Predictions":
    st.markdown("## 🔮 **Model Predictions**")

    st.write("""
    In this section, you can generate predictions using the trained machine learning model.
    """)

    # Placeholder for prediction input
    st.write("### Enter Features for Prediction")
    feature_1 = st.number_input("Feature 1")
    feature_2 = st.number_input("Feature 2")
    feature_3 = st.number_input("Feature 3")
    feature_4 = st.number_input("Feature 4")

    if st.button("Predict"):
        # Using the pre-trained model (from the previous section) to predict
        if 'model' in globals():
            prediction = model.predict([[feature_1, feature_2, feature_3, feature_4]])
            st.write(f"Predicted Class: {prediction[0]}")
        else:
            st.warning("No model trained yet! Go to 'Model Training' first.")
