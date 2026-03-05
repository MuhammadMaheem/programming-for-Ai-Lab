"""
Data Utilities for House Price Prediction
Handles data loading, preprocessing, feature engineering, and analysis
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from typing import Tuple, Dict, List
import warnings
warnings.filterwarnings('ignore')


def load_house_price_dataset(source: str = 'generate') -> pd.DataFrame:
    """
    Load house price dataset
    
    Args:
        source: 'generate' for synthetic data, or path to CSV file
    
    Returns:
        DataFrame with house features and prices
    """
    if source == 'generate':
        np.random.seed(42)
        n_samples = 500
        
        df = pd.DataFrame({
            'square_feet': np.random.uniform(1000, 10000, n_samples),
            'bedrooms': np.random.randint(1, 6, n_samples),
            'bathrooms': np.random.randint(1, 4, n_samples),
            'age_years': np.random.randint(0, 100, n_samples),
            'garage_spaces': np.random.randint(0, 4, n_samples),
            'lot_size': np.random.uniform(2000, 20000, n_samples),
            'location_score': np.random.uniform(1, 10, n_samples),
            'condition': np.random.choice(['Poor', 'Fair', 'Good', 'Excellent'], n_samples)
        })
        
        # Create realistic price target
        df['price'] = (
            150 * df['square_feet'] +
            30000 * df['bedrooms'] +
            20000 * df['bathrooms'] -
            500 * df['age_years'] +
            15000 * df['garage_spaces'] +
            df['lot_size'] * 3 +
            50000 * df['location_score'] +
            np.random.normal(0, 50000, n_samples)
        )
        
        return df
    else:
        # Load from CSV
        df = pd.read_csv(source)
        return df


def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean dataset - handle missing values and outliers
    
    Args:
        df: Input DataFrame
    
    Returns:
        Cleaned DataFrame
    """
    df = df.copy()
    
    # Handle missing values
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        if df[col].isnull().sum() > 0:
            df[col].fillna(df[col].median(), inplace=True)
    
    categorical_cols = df.select_dtypes(include=['object']).columns
    for col in categorical_cols:
        if df[col].isnull().sum() > 0:
            df[col].fillna(df[col].mode()[0], inplace=True)
    
    # Remove duplicates
    df = df.drop_duplicates(subset=None, keep='first')
    
    return df


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create new features for better model performance
    
    Args:
        df: Input DataFrame
    
    Returns:
        DataFrame with engineered features
    """
    df = df.copy()
    
    # Create interaction features
    if 'square_feet' in df.columns and 'bedrooms' in df.columns:
        df['price_per_sqft'] = df.get('price', 0) / df['square_feet']
        df['sqft_per_bedroom'] = df['square_feet'] / df['bedrooms']
    
    # Create polynomial features
    if 'square_feet' in df.columns:
        df['square_feet_squared'] = df['square_feet'] ** 2
    
    # Age-related features
    if 'age_years' in df.columns:
        df['is_new'] = (df['age_years'] < 5).astype(int)
        df['is_old'] = (df['age_years'] > 50).astype(int)
    
    # Luxury indicator
    if all(col in df.columns for col in ['bedrooms', 'bathrooms', 'garage_spaces']):
        df['luxury_score'] = df['bedrooms'] * 2 + df['bathrooms'] + df['garage_spaces']
    
    return df


def scale_features(X_train: pd.DataFrame, X_test: pd.DataFrame) -> Tuple:
    """
    Scale numeric features using StandardScaler
    
    Args:
        X_train: Training features
        X_test: Test features
    
    Returns:
        Tuple of (scaled X_train, scaled X_test, scaler)
    """
    numeric_cols = X_train.select_dtypes(include=[np.number]).columns
    
    scaler = StandardScaler()
    X_train_scaled = X_train.copy()
    X_test_scaled = X_test.copy()
    
    X_train_scaled[numeric_cols] = scaler.fit_transform(X_train[numeric_cols])
    X_test_scaled[numeric_cols] = scaler.transform(X_test[numeric_cols])
    
    return X_train_scaled, X_test_scaled, scaler


def encode_categorical(X_train: pd.DataFrame, X_test: pd.DataFrame) -> Tuple:
    """
    Encode categorical features using LabelEncoder
    
    Args:
        X_train: Training features
        X_test: Test features
    
    Returns:
        Tuple of (encoded X_train, encoded X_test, encoder_dict)
    """
    X_train_encoded = X_train.copy()
    X_test_encoded = X_test.copy()
    
    categorical_cols = X_train.select_dtypes(include=['object']).columns
    encoders = {}
    
    for col in categorical_cols:
        encoder = LabelEncoder()
        X_train_encoded[col] = encoder.fit_transform(X_train[col].astype(str))
        X_test_encoded[col] = encoder.transform(X_test[col].astype(str))
        encoders[col] = encoder
    
    return X_train_encoded, X_test_encoded, encoders


def get_feature_statistics(df: pd.DataFrame) -> Dict:
    """
    Get detailed statistics for all features
    
    Args:
        df: Input DataFrame
    
    Returns:
        Dictionary with feature statistics
    """
    stats = {
        'numeric': df.describe().to_dict(),
        'missing_values': df.isnull().sum().to_dict(),
        'data_types': df.dtypes.to_dict(),
        'duplicates': df.duplicated().sum()
    }
    
    return stats


def detect_outliers(df: pd.DataFrame, column: str, method: str = 'iqr') -> pd.Series:
    """
    Detect outliers using IQR or Z-score method
    
    Args:
        df: Input DataFrame
        column: Column to check for outliers
        method: 'iqr' or 'zscore'
    
    Returns:
        Boolean Series indicating outliers
    """
    if method == 'iqr':
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        return (df[column] < lower_bound) | (df[column] > upper_bound)
    
    elif method == 'zscore':
        from scipy import stats
        z_scores = np.abs(stats.zscore(df[column].dropna()))
        return z_scores > 3


def analyze_price_distribution(df: pd.DataFrame, price_column: str = 'price') -> Dict:
    """
    Analyze price distribution and patterns
    
    Args:
        df: Input DataFrame
        price_column: Name of price column
    
    Returns:
        Dictionary with distribution analysis
    """
    if price_column not in df.columns:
        return {}
    
    prices = df[price_column]
    
    analysis = {
        'min': prices.min(),
        'max': prices.max(),
        'mean': prices.mean(),
        'median': prices.median(),
        'std': prices.std(),
        'skewness': prices.skew(),
        'kurtosis': prices.kurtosis(),
        'q25': prices.quantile(0.25),
        'q75': prices.quantile(0.75)
    }
    
    return analysis


def get_feature_price_correlation(df: pd.DataFrame, price_column: str = 'price') -> pd.Series:
    """
    Get correlation of all features with price
    
    Args:
        df: Input DataFrame
        price_column: Name of price column
    
    Returns:
        Series of correlations sorted by absolute value
    """
    numeric_df = df.select_dtypes(include=[np.number])
    correlations = numeric_df.corr()[price_column].drop(price_column)
    return correlations.sort_values(ascending=False)
