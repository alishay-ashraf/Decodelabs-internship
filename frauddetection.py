# Import core libraries
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.datasets import make_classification # Added to simulate data

from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline as ImbPipeline

# 1. Load Data (Simulating the 284,807 transaction dataset pool)
print("Generating simulated credit card dataset...")
total_samples = 284807  # From slide specifications
fraud_rate = 0.0017     # 0.17% fraud rate
weights = [1 - fraud_rate, fraud_rate] # [0.9983, 0.0017]

X, y = make_classification(
    n_samples=total_samples,
    n_features=10,        # Simulating 10 transaction features
    weights=weights,      # Imposing the extreme class imbalance
    random_state=42
)
print(f"Dataset ready! Legitimate: {np.bincount(y)[0]}, Fraudulent: {np.bincount(y)[1]}")

# 2. Strict 80/20 Train/Test Split (Before SMOTE to avoid Data Leakage!)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, stratify=y, random_state=42
)

# 3. Define the Leak-Free Pipeline Template
def create_fraud_pipeline(classifier):
    return ImbPipeline([
        ('scaler', StandardScaler()),
        ('smote', SMOTE(random_state=42)),
        ('classifier', classifier)
    ])

# 4. Instantiate Models
lr_pipeline = create_fraud_pipeline(LogisticRegression(max_iter=1000, random_state=42))
rf_pipeline = create_fraud_pipeline(RandomForestClassifier(n_estimators=10, random_state=42, n_jobs=-1))

# 5. Model Evaluation Helper (Ignoring baseline Accuracy)
def evaluate_pipeline(pipeline, name):
    print(f"\n=== Training & Evaluating: {name} ===")
    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)
    y_proba = pipeline.predict_proba(X_test)[:, 1]
    
    # Strict Evaluation Metrics (Discarding 'Accuracy')
    print(classification_report(y_test, y_pred, target_names=['Legitimate', 'Fraud']))
    print(f"ROC-AUC Score: {roc_auc_score(y_test, y_proba):.4f}")

# Run evaluations
evaluate_pipeline(lr_pipeline, "Logistic Regression + SMOTE")
evaluate_pipeline(rf_pipeline, "Random Forest + SMOTE")