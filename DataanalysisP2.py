import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 1. LOAD THE DATASET
try:
    df = pd.read_csv('your_dataset.csv')
    print("Dataset loaded successfully!")
except FileNotFoundError:
    print("File not found. Using a synthetic dataset for demonstration purposes.")
    np.random.seed(42)
    df = pd.DataFrame({
        'ID': range(1, 101),
        'Age': np.random.randint(18, 70, size=100),
        'Salary': np.random.normal(55000, 15000, size=100).astype(int),
        'Department': np.random.choice(['HR', 'IT', 'Sales', 'Marketing'], size=100)
    })
    df.loc[98, 'Salary'] = 250000  # High outlier
    df.loc[99, 'Salary'] = -5000    # Invalid/Low outlier

# 2. CALCULATE BASIC STATISTICS (Requirement 1)
print("\n" + "="*40)
print("PART 1: DESCRIPTIVE STATISTICS")
print("="*40)

print("\n--- Summary Statistics (df.describe) ---")
print(df.describe())  # Five-number summary skeleton

for col in df.select_dtypes(include=[np.number]).columns:
    if col == 'ID': continue
    print(f"\nMetrics for column [{col}]:")
    print(f"  • Count:  {df[col].count()}")
    print(f"  • Mean:   {df[col].mean():.2f}")
    print(f"  • Median: {df[col].median():.2f}")

# 3. IDENTIFY TRENDS & OUTLIERS (Requirement 2)
print("\n" + "="*40)
print("PART 2: OUTLIER & TREND DETECTION")
print("="*40)

for col in ['Age', 'Salary']:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
    print(f"\nOutliers detected in [{col}] (Outside {lower_bound:.1f} to {upper_bound:.1f}):")
    if len(outliers) > 0:
        print(outliers[[col]])
    else:
        print("  None detected.")

# Categorical Breakdown to identify group-level trends
print("\n--- Trend Analysis: Average Salary by Department ---")
dept_trends = df.groupby('Department')['Salary'].agg(['count', 'mean', 'median'])
print(dept_trends)

# Visualizing Distributions and Outliers
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
sns.boxplot(data=df, y='Salary', color='skyblue')
plt.title('Salary Boxplot (Outlier Detection)')

plt.subplot(1, 2, 2)
sns.histplot(data=df, x='Salary', kde=True, color='salmon')
plt.title('Salary Distribution Curve')

plt.tight_layout()
plt.show()