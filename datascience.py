import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer


def secure_input_fidelity(df: pd.DataFrame) -> pd.DataFrame:
    """Module 1: Securing Input Fidelity - Missing Data Handling

    Applies strict, rules-based logic thresholds to handle MCAR/MAR scenarios.
    """
    df_cleaned = df.copy()
    total_rows = len(df_cleaned)

    for col in df_cleaned.columns:
        # Calculate missingness proportion per feature
        missing_count = df_cleaned[col].isna().sum()
        missing_prop = missing_count / total_rows

        # If no missing data, move to the next column
        if missing_prop == 0:
            continue

        print(
            f"Feature '{col}': Missingness = {missing_prop:.2%} ({missing_count} rows)"
        )

        # Threshold 1: < 5% -> Drop Rows
        if missing_prop < 0.05:
            print(f"--> Strategy Applied: Row Deletion (< 5%)")
            df_cleaned = df_cleaned.dropna(subset=[col])
            # Recalculate total rows since the dataframe size changed
            total_rows = len(df_cleaned)

        # Threshold 2: 5% to 20% -> Global Median (Skewed Numeric)
        elif 0.05 <= missing_prop <= 0.20:
            if pd.api.types.is_numeric_dtype(df_cleaned[col]):
                print(f"--> Strategy Applied: Global Median Imputation (5%-20%)")
                median_value = df_cleaned[col].median()
                df_cleaned[col] = df_cleaned[col].fillna(median_value)
            else:
                # Fallback for categorical if present in sub-groups
                print(f"--> Strategy Applied: Mode Imputation for Categorical")
                mode_value = df_cleaned[col].mode()[0]
                df_cleaned[col] = df_cleaned[col].fillna(mode_value)

    # Threshold 3: > 20% -> Multi-Dimensional KNN Estimation
    # (Applied globally to remaining high-missingness numeric features to capture complex relationships)
    high_missing_cols = [
        col
        for col in df_cleaned.columns
        if (df_cleaned[col].isna().sum() / len(df_cleaned)) > 0.20
    ]

    if high_missing_cols:
        print(
            f"\nFeatures triggering KNN Imputer (> 20%): {high_missing_cols}"
        )
        # Using numeric columns for distance calculations
        numeric_cols = df_cleaned.select_dtypes(include=[np.number]).columns
        imputer = KNNImputer(n_neighbors=5)

        # Fit and transform the numeric space
        df_cleaned[numeric_cols] = imputer.fit_transform(
            df_cleaned[numeric_cols]
        )
        print("--> Strategy Applied: KNN Multi-Dimensional Estimation")

    return df_cleaned


# --- SIMULATION AND TESTING ---
if __name__ == "__main__":
    # Generating a chaotic raw mock dataset to simulate target thresholds
    np.random.seed(42)
    data_size = 100
    mock_data = {
        "Feature_A": np.random.normal(10, 2, data_size),  # Needs row deletion (<5%)
        "Feature_B": np.random.exponential(
            5, data_size
        ),  # Highly skewed, needs Median (5-20%)
        "Feature_C": np.random.uniform(
            50, 100, data_size
        ),  # Complex feature, needs KNN (>20%)
        "Feature_D": np.random.normal(5, 1, data_size),  # Clean control column
    }

    df_raw = pd.DataFrame(mock_data)

    # Injecting missing values precisely to trigger each framework tier
    df_raw.iloc[[5, 42, 88], 0] = np.nan  # 3% missing
    df_raw.iloc[10:22, 1] = np.nan  # 12% missing
    df_raw.iloc[30:55, 2] = np.nan  # 25% missing

    print("=== RAW CHAOTIC DATA METRICS ===")
    print(df_raw.isna().sum())
    print("-" * 40)

    print("\n=== EXECUTING PIPELINE MODULE 1 ===")
    df_processed = secure_input_fidelity(df_raw)

    print("-" * 40)
    print("\n=== POST-PROCESSING METRICS ===")
    print(df_processed.isna().sum())

import numpy as np
import pandas as pd


def neutralize_outliers_iqr(
    df: pd.DataFrame, factor: float = 1.5
) -> pd.DataFrame:
    """Module 1 (Part 2): Outlier Neutralization via Interquartile Range (IQR).

    Uses robust non-parametric boundaries to cap extreme statistical anomalies.
    """
    df_filtered = df.copy()

    # Apply only to continuous numeric columns
    numeric_cols = df_filtered.select_dtypes(include=[np.number]).columns

    print("\n=== EXECUTING IQR OUTLIER NEUTRALIZATION ===")

    for col in numeric_cols:
        # Calculate Quartiles
        Q1 = df_filtered[col].quantile(0.25)
        Q3 = df_filtered[col].quantile(0.75)

        # Calculate IQR range
        IQR = Q3 - Q1

        # Establish rigid mathematical boundaries
        lower_bound = Q1 - (factor * IQR)
        upper_bound = Q3 + (factor * IQR)

        # Detect if anomalies exist before capping
        outliers_lower = (df_filtered[col] < lower_bound).sum()
        outliers_upper = (df_filtered[col] > upper_bound).sum()
        total_outliers = outliers_lower + outliers_upper

        if total_outliers > 0:
            print(
                f"Feature '{col}': Found {total_outliers} outliers "
                f"({outliers_lower} low, {outliers_upper} high). "
                f"Boundaries: [{lower_bound:.2f}, {upper_bound:.2f}]"
            )

            # Vectorized capping (clipping) to secure distribution variance
            df_filtered[col] = np.clip(
                df_filtered[col], lower_bound, upper_bound
            )
            print(f"--> Strategy Applied: Capped values at thresholds.")

    return df_filtered


# --- SIMULATION AND TESTING ---
if __name__ == "__main__":
    # Let's generate a clean distribution and intentionally inject chaotic outliers
    np.random.seed(42)
    df_test = pd.DataFrame(
        {
            "Feature_A": np.random.normal(
                loc=50, scale=5, size=100
            ),  # Mean=50, Std=5
            "Feature_B": np.random.normal(
                loc=10, scale=2, size=100
            ),  # Mean=10, Std=2
        }
    )

    # Injecting massive hardware glitches / transcription anomalies
    df_test.loc[15, "Feature_A"] = 150.0  # Extreme upper outlier
    df_test.loc[42, "Feature_A"] = -25.0  # Extreme lower outlier
    df_test.loc[77, "Feature_B"] = 99.0  # Extreme upper outlier

    print("=== DATA SUMMARY BEFORE IQR CAPPING ===")
    print(df_test.describe().loc[["min", "max"]])

    # Execute our structural engineering rule
    df_secured = neutralize_outliers_iqr(df_test)

    print("\n=== DATA SUMMARY AFTER IQR CAPPING ===")
    print(df_secured.describe().loc[["min", "max"]])

import numpy as np
import pandas as pd


def execute_process_engine(df: pd.DataFrame) -> pd.DataFrame:
    """Module 2: PROCESS - The Engine

    Engineers 3 new predictive features and eliminates multi-collinearity.
    """
    df_processed = df.copy()

    print("\n=== EXECUTING PIPELINE MODULE 2: PROCESS ===")

    # -------------------------------------------------------------------------
    # PART 1: FEATURE ENGINEERING (Vectorized Math Operations)
    # -------------------------------------------------------------------------
    print("\nEngineering new predictive features...")

    # Feature 1: Interaction Term (Captures non-linear joint variations)
    df_processed["Feature_Interaction_AB"] = (
        df_processed["Feature_A"] * df_processed["Feature_B"]
    )
    print("--> Engineered Feature 1: 'Feature_Interaction_AB' (A * B)")

    # Feature 2: Relative Ratios (Normalizes scales relative to population variance)
    # Adding a small epsilon (1e-5) to prevent catastrophic division-by-zero errors
    df_processed["Feature_Ratio_CD"] = df_processed["Feature_C"] / (
        df_processed["Feature_D"] + 1e-5
    )
    print("--> Engineered Feature 2: 'Feature_Ratio_CD' (C / D)")

    # Feature 3: Mathematical Transformation (Log transform to pull right-skewed data into a normal shape)
    # Using np.log1p (log(1 + x)) to handle zero value spaces gracefully
    df_processed["Feature_Log_B"] = np.log1p(df_processed["Feature_B"])
    print("--> Engineered Feature 3: 'Feature_Log_B' (Natural Log of B)")

    # -------------------------------------------------------------------------
    # PART 2: COLLINEARITY ERADICATION
    # -------------------------------------------------------------------------
    print("\nScanning optimization space for multi-collinearity...")

    # Establish an explicit mathematical correlation boundary (e.g., 85%)
    correlation_threshold = 0.85

    # Calculate Pearson correlation matrix across numeric spaces
    numeric_df = df_processed.select_dtypes(include=[np.number])
    corr_matrix = numeric_df.corr().abs()

    # Isolate the upper triangle of the matrix to avoid cross-checking features with themselves
    upper_tri = corr_matrix.where(
        np.triu(np.ones(corr_matrix.shape), k=1).astype(bool)
    )

    # Detect features that breech our safety threshold
    to_drop = [
        column
        for column in upper_tri.columns
        if any(upper_tri[column] > correlation_threshold)
    ]

    if to_drop:
        print(
            f"--> Critical Warning: Redundant collinearity detected in features: {to_drop}"
        )
        df_processed = df_processed.drop(columns=to_drop)
        print(f"--> Strategy Applied: Dropped features to stabilize gradients.")
    else:
        print("--> Optimization space secure. Zero dangerous collinearity patterns found.")

    return df_processed


# --- SIMULATION AND TESTING ---
if __name__ == "__main__":
    # Let's create a post-Module 1 mock dataset to feed our engine
    np.random.seed(42)
    data_size = 100
    mock_cleaned_data = {
        "Feature_A": np.random.uniform(10, 50, data_size),
        "Feature_B": np.random.exponential(scale=5, size=data_size),
        "Feature_C": np.random.normal(loc=100, scale=15, size=data_size),
        "Feature_D": np.random.normal(loc=25, scale=3, size=data_size),
    }

    df_inputs_secured = pd.DataFrame(mock_cleaned_data)

    # Intentionally injecting a feature that is highly collinear to Feature_A
    # This simulates a redundant column that would ruin real-numbered coordinate optimization
    df_inputs_secured["Feature_Collinear_A"] = (
        df_inputs_secured["Feature_A"] * 2.01
    ) + np.random.normal(0, 0.1, data_size)

    # Run the engine
    df_final_engine = execute_process_engine(df_inputs_secured)

    print("\n=== POST-PROCESS STAGE METRICS ===")
    print(f"Final Dataframe Columns: {list(df_final_engine.columns)}")