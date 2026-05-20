import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.impute import SimpleImputer

def get_dataset_stats(df):
    """Returns basic stats about the dataset."""
    stats = {
        'total_rows': len(df),
        'total_cols': len(df.columns),
        'missing_values': df.isnull().sum().sum(),
        'duplicate_rows': df.duplicated().sum(),
        'num_cols': len(df.select_dtypes(include=['number']).columns),
        'cat_cols': len(df.select_dtypes(include=['object', 'category']).columns)
    }
    return stats

def remove_duplicates(df):
    """Removes duplicate rows."""
    return df.drop_duplicates()

def handle_missing_values(df, strategy='drop'):
    """Handles missing values based on the strategy."""
    df_cleaned = df.copy()
    if strategy == 'drop':
        df_cleaned = df_cleaned.dropna()
    elif strategy == 'mean':
        num_cols = df_cleaned.select_dtypes(include=['number']).columns
        if not num_cols.empty:
            imputer = SimpleImputer(strategy='mean')
            df_cleaned[num_cols] = imputer.fit_transform(df_cleaned[num_cols])
        # For categorical, fill with mode
        cat_cols = df_cleaned.select_dtypes(exclude=['number']).columns
        if not cat_cols.empty:
            for col in cat_cols:
                df_cleaned[col] = df_cleaned[col].fillna(df_cleaned[col].mode()[0])
    return df_cleaned

def correct_datatypes(df):
    """Attempts to auto-correct datatypes."""
    df_cleaned = df.copy()
    for col in df_cleaned.columns:
        if df_cleaned[col].dtype == 'object':
            # Try converting to numeric
            try:
                df_cleaned[col] = pd.to_numeric(df_cleaned[col])
            except ValueError:
                # Try converting to datetime
                try:
                    df_cleaned[col] = pd.to_datetime(df_cleaned[col])
                except (ValueError, TypeError):
                    pass
    return df_cleaned

def normalize_numeric_data(df):
    """Normalizes numeric columns using StandardScaler."""
    df_cleaned = df.copy()
    num_cols = df_cleaned.select_dtypes(include=['number']).columns
    if not num_cols.empty:
        scaler = StandardScaler()
        df_cleaned[num_cols] = scaler.fit_transform(df_cleaned[num_cols])
    return df_cleaned

def remove_outliers(df, threshold=3):
    """Removes outliers using Z-score method for numeric columns."""
    df_cleaned = df.copy()
    num_cols = df_cleaned.select_dtypes(include=['number']).columns
    if not num_cols.empty:
        from scipy import stats
        z_scores = np.abs(stats.zscore(df_cleaned[num_cols].dropna()))
        # keep rows where all z-scores for numeric columns are < threshold
        # To avoid issues with NaNs, we only filter rows that have valid z-scores
        mask = (z_scores < threshold).all(axis=1)
        # We need to map mask back to original dataframe index, handling NaNs
        valid_indices = df_cleaned[num_cols].dropna().index[mask]
        
        # Keep rows that are either not outlier or have NaNs (outlier detection skipped for NaNs)
        df_cleaned = df_cleaned.loc[df_cleaned.index.isin(valid_indices) | df_cleaned[num_cols].isnull().any(axis=1)]
    return df_cleaned

def encode_categorical_data(df):
    """Encodes categorical data using LabelEncoder."""
    df_cleaned = df.copy()
    cat_cols = df_cleaned.select_dtypes(include=['object', 'category']).columns
    if not cat_cols.empty:
        encoder = LabelEncoder()
        for col in cat_cols:
            # fill NaNs with a placeholder before encoding to avoid errors
            df_cleaned[col] = df_cleaned[col].fillna('Missing')
            df_cleaned[col] = encoder.fit_transform(df_cleaned[col].astype(str))
    return df_cleaned
