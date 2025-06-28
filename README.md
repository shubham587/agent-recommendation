# 🤖 AI Coding Agent Recommender

Smart recommendation system that helps developers choose the best AI coding assistant for their specific programming tasks.

## 🚀 Quick Start

### Clone Repository
```bash
git clone https://github.com/shubham587/agent-recommendation.git
```

### Backend Setup
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```
Backend will run on `http://localhost:5001`

### Frontend Setup
```bash
cd frontend
npm install
npm start
```
Frontend will run on `http://localhost:3000`

## 📋 How to Use

1. Open `http://localhost:3000` in your browser
2. Describe your coding project in the text area
3. Click "Get AI Agent Recommendations"
4. View your personalized recommendations with explanations

## 💡 Example Prompts

Try these example prompts to see the system in action:

**Beginner Web Development:**
```
I want to build my first React web application. I'm a complete beginner and need help with basic syntax, component structure, and learning best practices.
```

**Enterprise Java Project:**
```
I'm working on a large-scale Java enterprise application with Spring Boot, microservices architecture, and need an AI assistant for complex business logic and code optimization.
```

**Data Science Python:**
```
I'm building a machine learning pipeline in Python using pandas, scikit-learn, and TensorFlow. Need help with data preprocessing, model selection, and performance optimization.
```

**Mobile App Development:**
```
I want to create a cross-platform mobile app using React Native. I need assistance with navigation, state management, and API integration.
```

## 🛠️ Tech Stack

- **Backend**: Python Flask + JSON Database
- **Frontend**: React + Chakra UI
- **Algorithm**: Multi-criteria scoring system

 
