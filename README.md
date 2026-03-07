# Insurance Fraud Detection System

A comprehensive Machine Learning solution designed to detect and predict fraudulent insurance claims. This project features a robust back-end prediction engine powered by various machine learning models (XGBoost, Random Forest, Logistic Regression) and a modern, responsive React-based front-end dashboard for seamless user interaction and analytics.

---

## 📸 Project Screenshots

### 1. Home Page
*(A brief overview and welcome page for the application)*
<img width="1300" height="649" alt="image" src="https://github.com/user-attachments/assets/1a5c200a-e933-4299-877e-48eb44690449" />


### 2. Analytics Dashboard
*(Interactive fraud statistics and visualization dashboard)*
![Dashboard](screenshots/dashboard.png)

### 3. Claim Prediction Form
*(Input form to evaluate new insurance claims for potential fraud)*
![Prediction Form](screenshots/prediction_form.png)

### 4. Prediction Result
*(Detailed analysis, risk level assessment, and recommendation)*
![Prediction Result](screenshots/prediction_result.png)

---

## 🏗️ System Architecture & Workflow

The system is decoupled into two primary components: the **Frontend** UI and the **Backend** API.

### Workflow:
1. **Data Input**: The end-user (e.g., insurance agent, fraud investigator) inputs claim details (Claim Amount, Age, Policy Duration, Claim Type, etc.) via the React Frontend.
2. **API Request**: The React app sends a POST request with the claim data to the Flask Backend.
3. **Data Preprocessing**: The Flask app forwards the data to the prediction module, where the inputs are scaled, encoded, and prepared matching the training data format.
4. **Model Inference**: The data is passed to the trained Machine Learning model (XGBoost by default) to calculate the `fraud_probability`.
5. **Risk Assessment**: Based on the probability score, the backend assigns a Risk Level (HIGH, MEDIUM, LOW) and assesses the contributing risk factors based on feature thresholds.
6. **Result Display**: The JSON response is sent back to the React app, which displays a comprehensive result card visually breaking down the risk factors and final recommendation.

---

## 💻 Frontend (Insurance Fraud Detection UI)

The frontend is a fast, responsive Single Page Application (SPA) built to provide investigators with a clean and intuitive interface.

### Tech Stack:
- **React.js (v19)**: Component-based UI formulation.
- **Vite**: Ultra-fast build tool and development server.
- **Tailwind CSS & PostCSS**: Utility-first styling for creating a modern, sleek interface.
- **Chart.js & React-Chartjs-2**: Visualizing fraud analytics and statistics on the dashboard.
- **React Router**: Seamless client-side routing across Home, Dashboard, and Prediction pages.
- **Axios**: Handling RESTful API communication.

### Key Features:
- **Interactive Dashboard**: View real-time aggregated metrics such as total predictions, confirmed fraud cases, and fraud rate percentages.
- **Prediction Interface**: Dynamic form validating and collecting 9 specific data points for the ML model.
- **Result Explainer**: Not just a binary yes/no, but detailed explanations on *why* a claim was flagged based on its factors.

---

## ⚙️ Backend (Insurance-Fraud-Backend)

The backend is built with Python and Flask. It serves as the bridge between the machine learning models and the client application.

### Tech Stack:
- **Python 3**: Core language.
- **Flask**: Lightweight WSGI web application framework.
- **Pandas & NumPy**: Data manipulation and numerical operations.
- **Scikit-Learn**: For data preprocessing, scaling, and baseline models (Logistic Regression, Random Forest).
- **XGBoost**: Gradient boosted decision trees for state-of-the-art tabular data prediction.

### Key Features:
- **RESTful API endpoints**:
  - `/health`: System health check.
  - `/predict`: Single claim prediction.
  - `/predict-batch`: Bulk claim prediction processing.
  - `/fraud-statistics`: Aggregation endpoint for the Dashboard.
  - `/features`: Exposing expected inputs dynamically.
- **Enriched Predictions**: Logic to determine `HIGH`, `MEDIUM`, or `LOW` risk tiers and highlight features that contributed most heavily to the score (e.g., unusually high claim amount or frequent past claims).
- **In-memory Tracker**: Keeps count of processed claims and their outcomes during the active session.

---

## 🚀 Setup & Installation

Follow these steps to run the complete project locally.

### 1. Clone the repository
```bash
git clone https://github.com/your-username/Insurance-Fraud-Detection.git
cd Insurance-Fraud-Detection
```

### 2. Start the Backend API
```bash
# Navigate to the backend directory
cd Insurance-Fraud-Backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# Install dependencies
pip install -r requirements.txt

# Run the Flask server
python app.py
```
*The backend server will run at `http://localhost:5000`.*

### 3. Start the Frontend Application
Open a new terminal window:
```bash
# Navigate to the frontend directory
cd "Insurance Fraud Detection UI"

# Install Node modules
npm install

# Start the Vite development server
npm run dev
```
*The frontend interface will run at `http://localhost:5173`.*

---

## 🧠 Machine Learning Engine

This project relies on a rigorous machine learning pipeline to preprocess data, engineer features, and train multiple classifier models to find the most accurate algorithm.

### 1. The Dataset
The backend expects a dataset (`data/insurance_data.csv`) representing historical insurance claims. 
- **Numeric Features**: Real-world metrics like Claim Amount, Claimant Age, Policy Duration, and Previous Claims.
- **Categorical Features**: Descriptive attributes like Claim Type (Auto, Medical, Property), Policy Type, State, and Claim Status.
- **Target Variable**: A discrete binary fraud indicator (e.g., `fraud` or `is_fraud`) dictating whether a claim was legitimate (0) or fraudulent (1).

### 2. Data Preprocessing & Feature Engineering
Before hitting the algorithms, the data runs through `/src/preprocess.py`:
- **Missing Data Handling**: Numeric gaps are imputed using the column mean to preserve data integrity. Unresolvable rows are dropped.
- **Label Encoding**: Categorical fields (like States and Policies) are transformed into machine-readable numeric integers using Scikit-Learn's `LabelEncoder`.
- **Feature Scaling**: Input variables are standardized using `StandardScaler` to ensure uniform influence and accelerate gradient descent converge.
- **Feature Interactions**: The pipeline automatically derives interaction features by multiplying priority numeric columns (e.g., creating `claim_amount_x_claimant_age`), giving the model an edge in spotting highly nuanced fraud relationships.

### 3. Model Training Algorithms
The processed data is split into an 80% training set and a 20% test set inside `/src/train_model.py`. The suite trains three distinct models:
- **Logistic Regression**: Acts as a linear baseline gauge. Fast and highly interpretable.
- **Random Forest Classifier**: An ensemble method fitted with 100 decision trees and `class_weight='balanced'` to offset the traditional imbalance problem in fraud datasets.
- **XGBoost Classifier**: The ultimate gradient-boosting workhorse, heavily optimized with explicit tree depths (`max_depth=6`) to minimize log-loss and pick up complex non-linear fraud signals.

### 4. Evaluation & Selection
Once fitted, the algorithms are competitively scored using:
- **Accuracy, Precision, Recall, F1-Score, and ROC-AUC**.
The framework automatically crowns the **Best Model** based strictly on the **Highest F1-Score** (to maximize the balance between incorrectly flagging a valid claim vs missing a fraudulent one). 
The winning model, alongside its `scaler.pkl` and `label_encoders.pkl` preprocessing pipeline, is serialized and written to the `model/` directory, immediately ready for Flask API inference.

### Retraining Instructions
If you wish to retrain the models on an updated dataset:
1. Place your new dataset at `Insurance-Fraud-Backend/data/insurance_data.csv`.
2. Ensure you are in the activated virtual environment.
3. Run the training orchestrator:
```bash
cd Insurance-Fraud-Backend/src
python train_model.py
```

---

## 📄 License
This project is developed for the detection of insurance fraud using modern web technologies and machine learning.
