"""
Model Training Module for House Price Prediction
Handles model training, evaluation, and hyperparameter optimization
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.model_selection import GridSearchCV, cross_val_score
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, mean_absolute_percentage_error
from typing import Tuple, Dict, Any
import warnings
warnings.filterwarnings('ignore')


def train_linear_regression(X_train: np.ndarray, y_train: np.ndarray) -> LinearRegression:
    """
    Train Linear Regression model
    
    Args:
        X_train: Training features
        y_train: Training target
    
    Returns:
        Trained LinearRegression model
    """
    model = LinearRegression()
    model.fit(X_train, y_train)
    return model


def train_ridge(X_train: np.ndarray, y_train: np.ndarray, alpha: float = 1.0) -> Ridge:
    """
    Train Ridge Regression model
    
    Args:
        X_train: Training features
        y_train: Training target
        alpha: Regularization strength
    
    Returns:
        Trained Ridge model
    """
    model = Ridge(alpha=alpha)
    model.fit(X_train, y_train)
    return model


def train_lasso(X_train: np.ndarray, y_train: np.ndarray, alpha: float = 1.0) -> Lasso:
    """
    Train Lasso Regression model
    
    Args:
        X_train: Training features
        y_train: Training target
        alpha: Regularization strength
    
    Returns:
        Trained Lasso model
    """
    model = Lasso(alpha=alpha, max_iter=10000)
    model.fit(X_train, y_train)
    return model


def train_random_forest(X_train: np.ndarray, y_train: np.ndarray, 
                       n_estimators: int = 100, max_depth: int = 20) -> RandomForestRegressor:
    """
    Train Random Forest Regressor
    
    Args:
        X_train: Training features
        y_train: Training target
        n_estimators: Number of trees
        max_depth: Maximum depth of trees
    
    Returns:
        Trained RandomForestRegressor
    """
    model = RandomForestRegressor(
        n_estimators=n_estimators,
        max_depth=max_depth,
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train, y_train)
    return model


def train_gradient_boosting(X_train: np.ndarray, y_train: np.ndarray,
                           n_estimators: int = 100, learning_rate: float = 0.1,
                           max_depth: int = 5) -> GradientBoostingRegressor:
    """
    Train Gradient Boosting Regressor
    
    Args:
        X_train: Training features
        y_train: Training target
        n_estimators: Number of boosting stages
        learning_rate: Shrinks contribution of each tree
        max_depth: Maximum depth of trees
    
    Returns:
        Trained GradientBoostingRegressor
    """
    model = GradientBoostingRegressor(
        n_estimators=n_estimators,
        learning_rate=learning_rate,
        max_depth=max_depth,
        random_state=42,
        subsample=0.8
    )
    model.fit(X_train, y_train)
    return model


def train_svr(X_train: np.ndarray, y_train: np.ndarray, 
              kernel: str = 'rbf', C: float = 100) -> SVR:
    """
    Train Support Vector Regression
    
    Args:
        X_train: Training features
        y_train: Training target
        kernel: Kernel type ('linear', 'rbf', 'poly')
        C: Regularization parameter
    
    Returns:
        Trained SVR model
    """
    model = SVR(kernel=kernel, C=C, epsilon=0.01)
    model.fit(X_train, y_train)
    return model


def evaluate_regression_model(model: Any, X_test: np.ndarray, 
                             y_test: np.ndarray) -> Dict[str, float]:
    """
    Evaluate regression model with multiple metrics
    
    Args:
        model: Trained model
        X_test: Test features
        y_test: Test target
    
    Returns:
        Dictionary with evaluation metrics
    """
    y_pred = model.predict(X_test)
    
    metrics = {
        'MAE': mean_absolute_error(y_test, y_pred),
        'RMSE': np.sqrt(mean_squared_error(y_test, y_pred)),
        'R2': r2_score(y_test, y_pred),
        'MAPE': mean_absolute_percentage_error(y_test, y_pred)
    }
    
    return metrics


def hyperparameter_optimization(X_train: np.ndarray, y_train: np.ndarray,
                               model_type: str = 'random_forest') -> Tuple[Any, Dict]:
    """
    Optimize hyperparameters using GridSearchCV
    
    Args:
        X_train: Training features
        y_train: Training target
        model_type: Type of model ('random_forest', 'gradient_boosting', 'ridge')
    
    Returns:
        Tuple of (best_model, best_params)
    """
    if model_type == 'random_forest':
        param_grid = {
            'n_estimators': [50, 100, 150],
            'max_depth': [10, 15, 20],
            'min_samples_split': [2, 5]
        }
        model = RandomForestRegressor(random_state=42)
    
    elif model_type == 'gradient_boosting':
        param_grid = {
            'n_estimators': [50, 100],
            'learning_rate': [0.01, 0.05, 0.1],
            'max_depth': [3, 5, 7]
        }
        model = GradientBoostingRegressor(random_state=42)
    
    elif model_type == 'ridge':
        param_grid = {'alpha': [0.1, 1.0, 10.0, 100.0]}
        model = Ridge()
    
    else:
        raise ValueError(f"Unknown model type: {model_type}")
    
    grid_search = GridSearchCV(model, param_grid, cv=5, n_jobs=-1, verbose=1)
    grid_search.fit(X_train, y_train)
    
    return grid_search.best_estimator_, grid_search.best_params_


def ensemble_predict(models: Dict[str, Any], X_test: np.ndarray, 
                    weights: Dict[str, float] = None) -> np.ndarray:
    """
    Make predictions using ensemble of models
    
    Args:
        models: Dictionary of trained models
        X_test: Test features
        weights: Dictionary of weights for each model
    
    Returns:
        Array of ensemble predictions
    """
    if weights is None:
        weights = {name: 1.0 / len(models) for name in models}
    
    ensemble_pred = np.zeros(X_test.shape[0])
    
    for model_name, model in models.items():
        weight = weights.get(model_name, 1.0 / len(models))
        predictions = model.predict(X_test)
        ensemble_pred += weight * predictions
    
    return ensemble_pred


def cross_validate_model(model: Any, X_train: np.ndarray, y_train: np.ndarray,
                        cv: int = 5) -> Dict[str, float]:
    """
    Perform cross-validation on model
    
    Args:
        model: Trained model
        X_train: Training features
        y_train: Training target
        cv: Number of folds
    
    Returns:
        Dictionary with cross-validation scores
    """
    cv_scores = cross_val_score(model, X_train, y_train, cv=cv, 
                                scoring='r2', n_jobs=-1)
    
    return {
        'mean_r2': cv_scores.mean(),
        'std_r2': cv_scores.std(),
        'fold_scores': cv_scores
    }


def calculate_residuals(y_true: np.ndarray, y_pred: np.ndarray) -> np.ndarray:
    """
    Calculate prediction residuals
    
    Args:
        y_true: True values
        y_pred: Predicted values
    
    Returns:
        Array of residuals
    """
    return y_true - y_pred


def get_feature_coefficients(model: Any, feature_names: list) -> pd.DataFrame:
    """
    Extract feature coefficients from linear models
    
    Args:
        model: Trained linear model
        feature_names: Names of features
    
    Returns:
        DataFrame with feature coefficients
    """
    if hasattr(model, 'coef_'):
        coef_df = pd.DataFrame({
            'Feature': feature_names,
            'Coefficient': model.coef_
        })
        coef_df['Abs_Coefficient'] = np.abs(coef_df['Coefficient'])
        coef_df = coef_df.sort_values('Abs_Coefficient', ascending=False)
        return coef_df
    
    return pd.DataFrame()


def get_feature_importance(model: Any, feature_names: list) -> pd.DataFrame:
    """
    Extract feature importance from tree-based models
    
    Args:
        model: Trained tree-based model
        feature_names: Names of features
    
    Returns:
        DataFrame with feature importance scores
    """
    if hasattr(model, 'feature_importances_'):
        importance_df = pd.DataFrame({
            'Feature': feature_names,
            'Importance': model.feature_importances_
        })
        importance_df = importance_df.sort_values('Importance', ascending=False)
        return importance_df
    
    return pd.DataFrame()


def model_comparison_summary(models: Dict[str, Any], X_test: np.ndarray,
                            y_test: np.ndarray) -> pd.DataFrame:
    """
    Create comparison summary of multiple models
    
    Args:
        models: Dictionary of trained models
        X_test: Test features
        y_test: Test target
    
    Returns:
        DataFrame with comparison metrics
    """
    results = []
    
    for model_name, model in models.items():
        metrics = evaluate_regression_model(model, X_test, y_test)
        metrics['Model'] = model_name
        results.append(metrics)
    
    return pd.DataFrame(results).set_index('Model')
