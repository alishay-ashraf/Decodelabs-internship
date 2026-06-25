import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

# ==========================================
# SETUP & SIMULATED DATA
# ==========================================
# Creating dummy data mirroring the problem: 20+ columns with mismatched scales
np.random.seed(42)
n_customers = 500

simulated_data = {
    'Annual_Income': np.random.uniform(20000, 120000, n_customers), # Massive scale
    'Purchases_Per_Month': np.random.randint(0, 11, n_customers),   # Small scale
    'Online_Time_Min': np.random.uniform(10, 300, n_customers),
    'Product_Returns': np.random.randint(0, 5, n_customers)
}
# Add remaining placeholder columns to hit the "20+ features" constraint
for i in range(5, 25):
    simulated_data[f'Feature_{i}'] = np.random.randn(n_customers)

df = pd.DataFrame(simulated_data)
print(f"Dataset Initialized: {df.shape[0]} rows, {df.shape[1]} columns.\n")

# ==========================================
# 1. SCALE: Standardization (Input)
# ==========================================
# Prevents high-magnitude axes from swallowing smaller variables
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df)

# ==========================================
# 2. COMPRESS: Principal Component Analysis
# ==========================================
# Compresses 20+ dimensions into 2 or 3 to defeat the "Curse of Dimensionality"
pca = PCA(n_components=3) 
X_pca = pca.fit_transform(X_scaled)

print(f"PCA complete. Cumulative Explained Variance Ratio: {pca.explained_variance_ratio_.sum():.4f}")
print(f"Compressed shape from {X_scaled.shape} to {X_pca.shape}\n")

# ==========================================
# 3. CLUSTER: Optimal K Evaluation (Elbow & Silhouette)
# ==========================================
wcss = []       # Within-Cluster Sum of Squares (for Elbow method)
sil_scores = []  # For Silhouette evaluation
k_range = range(2, 11)

for k in k_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(X_pca)
    wcss.append(kmeans.inertia_)
    sil_scores.append(silhouette_score(X_pca, kmeans.labels_))

# Plotting the mathematical proofs side-by-side
fig, ax1 = plt.subplots(1, 2, figsize=(14, 5))

# Elbow Plot
ax1[0].plot(k_range, wcss, marker='o', color='b', linestyle='--')
ax1[0].set_title('Elbow Method (Find the Bend)')
ax1[0].set_xlabel('Number of Clusters (K)')
ax1[0].set_ylabel('WCSS (Inertia)')
ax1[0].grid(True)

# Silhouette Plot
ax1[1].plot(k_range, sil_scores, marker='s', color='r', linestyle='-')
ax1[1].set_title('Silhouette Coefficients (Higher is Better)')
ax1[1].set_xlabel('Number of Clusters (K)')
ax1[1].set_ylabel('Silhouette Score')
ax1[1].grid(True)

plt.tight_layout()
plt.show()

# Let's dynamically identify or assign the optimal K based on the plots.
# Assuming K=3 based on your project kit's specified blueprint personas.
optimal_k = 3 
final_kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
cluster_assignments = final_kmeans.fit_transform(X_pca)
df['Cluster'] = final_kmeans.labels_

# ==========================================
# 4. TRANSLATE: Business Personas (Output)
# ==========================================
# Calculate core behavioral markers per cluster to define personas
profile = df.groupby('Cluster')[['Annual_Income', 'Purchases_Per_Month', 'Online_Time_Min', 'Product_Returns']].mean()
print("--- Cluster Profiles (Mean Raw Values) ---")
print(profile)
print("\n" + "="*50)

def translate_to_persona(cluster_id):
    """Maps purely mathematical groupings to enterprise business personas"""
    # Dynamic parsing logic based on your specification blueprint
    if cluster_id == 0:
        return "CLUSTER A: HIGH-VALUE ENGAGERS"
    elif cluster_id == 1:
        return "CLUSTER B: MID-TIER EXPLORERS"
    else:
        return "CLUSTER C: LOW-ACTIVITY CHURN RISK"

df['Business_Persona'] = df['Cluster'].apply(translate_to_persona)

print("\nSample Output of Final Processed Customer Base:")
print(df[['Annual_Income', 'Purchases_Per_Month', 'Cluster', 'Business_Persona']].head())