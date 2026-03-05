# 🏠 Task 6: House Price Prediction (Regression)

## Objective
Build machine learning regression models to accurately predict house selling prices based on property features and characteristics. Learn real estate domain knowledge, feature engineering, and model comparison techniques.

## Problem Statement
Real estate markets require accurate price predictions for property valuation, investment decisions, and market analysis. This project creates regression models that predict house prices using features like:
- **Size metrics**: Square footage, lot size
- **Structure**: Bedrooms, bathrooms, garage spaces
- **Condition**: Age, maintenance condition
- **Location**: Location score/desirability factor

## Dataset
Synthetic house price dataset with 500 properties containing:
- `square_feet`: Property size (1,000 - 10,000 sq ft)
- `bedrooms`: Number of bedrooms (1-5)
- `bathrooms`: Number of bathrooms (1-4)
- `age_years`: Age of property (0-100 years)
- `garage_spaces`: Number of garage spaces (0-3)
- `lot_size`: Lot size in square feet (2,000 - 20,000 sq ft)
- `location_score`: Location desirability (1-10)
- `price`: Sale price (target variable) - $100K - $3M range

### Real Data Sources
- [Kaggle House Prices Dataset](https://www.kaggle.com/c/house-prices-advanced-regression-techniques)
- [California Housing Dataset](https://www.kaggle.com/codenamev/california-housing-prices)
- [Ames Housing Dataset](https://www.kaggle.com/c/house-prices-advanced-regression-techniques)

## Technologies & Libraries
- **Data Processing**: pandas, numpy
- **Visualization**: matplotlib, seaborn
- **Machine Learning**: scikit-learn
- **Model Types**: Linear Regression, Ridge/Lasso, Random Forest, Gradient Boosting, SVR
- **Evaluation**: MAE, RMSE, R², MAPE, cross-validation

## Project Structure
```
Task_6_House_Price/
├── House_Price_Prediction.ipynb    # Main analysis notebook
├── utils/
│   └── data_utils.py               # Data loading, preprocessing, feature engineering
├── models/
│   └── train_model.py              # Model training and evaluation functions
├── requirements.txt                 # Python dependencies
└── README.md                        # This file
```

## Key Methodology

### 1. **Data Exploration & Analysis**
- Load and inspect house price dataset
- Analyze price distribution (histogram, statistics)
- Feature correlation analysis (heatmap)
- Identify missing values and outliers
- Check for data anomalies

### 2. **Feature Engineering**
- Create interaction features:
  - `price_per_sqft`: Price normalized by size
  - `sqft_per_bedroom`: Space efficiency metric
- Polynomial features:
  - `square_feet_squared`: Non-linear relationship
- Age-based features:
  - `is_new`: Binary flag for recent properties
  - `is_old`: Binary flag for older properties
- Luxury indicators:
  - `luxury_score`: Composite metric from amenities

### 3. **Data Preprocessing**
- Handle missing values (median imputation)
- Scale numerical features (StandardScaler)
- Encode categorical variables (LabelEncoder)
- Remove duplicates
- Split data (80% train, 20% test)

### 4. **Model Training**
Train and compare multiple regression models:

**Linear Models:**
- **Linear Regression**: Baseline model, interpretable coefficients
- **Ridge (L2 Regularization)**: Prevents overfitting, keeps all features
- **Lasso (L1 Regularization)**: Feature selection through coefficient shrinkage

**Tree-Based Models:**
- **Random Forest**: Ensemble of decision trees, feature importance, robust to outliers
- **Gradient Boosting**: Sequential tree building, lower bias, captures complex patterns

**Kernel-Based:**
- **Support Vector Regression (SVR)**: Non-linear regression with RBF kernel

### 5. **Model Evaluation**
Metrics for regression problems:

| Metric | Formula | Interpretation |
|--------|---------|-----------------|
| **MAE** (Mean Absolute Error) | $\frac{1}{n}\sum\|y_i - \hat{y}_i\|$ | Average prediction error ($) |
| **RMSE** (Root Mean Squared Error) | $\sqrt{\frac{1}{n}\sum(y_i - \hat{y}_i)^2}$ | Penalizes large errors ($) |
| **R² Score** | $1 - \frac{\sum(y_i - \hat{y}_i)^2}{\sum(y_i - \bar{y})^2}$ | % variance explained (0-1) |
| **MAPE** (Mean Absolute Percentage Error) | $\frac{100}{n}\sum\|\frac{y_i - \hat{y}_i}{y_i}\|$ | Percentage error (%) |

### 6. **Analysis & Insights**
- Visualize actual vs predicted prices
- Generate residual plots to check for patterns
- Extract feature importance/coefficients
- Compare model performance
- Identify key price drivers

## Expected Results

### Model Performance Comparison
```
                    MAE          RMSE         R²
Linear Regression   $85K         $110K        0.92
Ridge               $82K         $108K        0.93
Lasso               $90K         $115K        0.91
Random Forest       $65K         $85K         0.96
Gradient Boosting   $60K         $78K         0.97
SVR                 $75K         $95K         0.94
```

### Top Price Drivers (by importance)
1. **Square Footage** (40%): Size is strongest predictor
2. **Bedrooms** (18%): More rooms increase value
3. **Location Score** (15%): Location/desirability crucial
4. **Age** (12%): Newer properties command premium
5. **Bathrooms** (8%): Bathroom count matters less than bedrooms
6. **Garage** (5%): Amenity value
7. **Lot Size** (2%): Less important than structure

## Skills Covered

### Machine Learning
- [ ] Regression model selection and training
- [ ] Hyperparameter tuning with GridSearchCV
- [ ] Cross-validation for model validation
- [ ] Ensemble methods (voting, weighted predictions)
- [ ] Model comparison and selection criteria

### Data Science
- [ ] Exploratory Data Analysis (EDA)
- [ ] Feature engineering and feature selection
- [ ] Data cleaning and preprocessing
- [ ] Statistical analysis (correlation, distribution)
- [ ] Outlier detection (IQR method, Z-score)

### Real Estate Domain
- [ ] Understanding price drivers
- [ ] Property valuation concepts
- [ ] Market analysis techniques
- [ ] Feature importance in real estate context
- [ ] Investment decision support

### Visualization
- [ ] Correlation heatmaps
- [ ] Distribution plots
- [ ] Scatter plots for relationships
- [ ] Feature importance bar charts
- [ ] Actual vs predicted scatter plots

## Code Examples

### Load & Prepare Data
```python
from utils.data_utils import load_house_price_dataset, engineer_features, scale_features

# Load dataset
df = load_house_price_dataset()

# Engineer features
df = engineer_features(df)

# Prepare for modeling
X = df.drop('price', axis=1)
y = df['price']

X_train_scaled, X_test_scaled, scaler = scale_features(X_train, X_test)
```

### Train Models
```python
from models.train_model import train_random_forest, train_gradient_boosting, evaluate_regression_model

# Train models
rf = train_random_forest(X_train, y_train, n_estimators=100, max_depth=20)
gb = train_gradient_boosting(X_train, y_train)

# Evaluate
rf_metrics = evaluate_regression_model(rf, X_test, y_test)
gb_metrics = evaluate_regression_model(gb, X_test, y_test)

print(f"Random Forest R²: {rf_metrics['R2']:.4f}")
print(f"Gradient Boosting R²: {gb_metrics['R2']:.4f}")
```

### Feature Importance
```python
from models.train_model import get_feature_importance

importance = get_feature_importance(rf, X.columns)
print(importance)
```

## Advanced Topics

### 1. **Hyperparameter Optimization**
Use GridSearchCV to find optimal parameters:
```python
from models.train_model import hyperparameter_optimization

best_rf, best_params = hyperparameter_optimization(X_train, y_train, model_type='random_forest')
print(f"Best params: {best_params}")
```

### 2. **Ensemble Methods**
Combine predictions from multiple models:
```python
from models.train_model import ensemble_predict

models = {'rf': rf, 'gb': gb, 'ridge': ridge}
weights = {'rf': 0.5, 'gb': 0.3, 'ridge': 0.2}
ensemble_pred = ensemble_predict(models, X_test, weights)
```

### 3. **Residual Analysis**
Check model assumptions:
```python
residuals = y_test - y_pred
# Should be:
# - Normally distributed
# - Zero mean
# - Constant variance (homoscedasticity)
# - No pattern with predictions
```

## Common Issues & Solutions

| Problem | Cause | Solution |
|---------|-------|----------|
| High RMSE | Model underfitting | Use more complex models (GB, RF) |
| Overfitting (high train R², low test R²) | Model too complex | Increase regularization (alpha), limit tree depth |
| Extreme predictions | Outliers in training data | Remove or cap outliers, use robust models |
| Poor performance on new data | Data distribution shift | Validate on similar properties, update model periodically |
| Feature importance seems wrong | Correlated features | Use correlation analysis, consider feature selection |

## Real-World Applications

### 1. **Property Valuation**
- Automated valuation models (AVMs)
- Appraisal support systems
- Fair market assessment

### 2. **Investment Analysis**
- ROI estimation for real estate investors
- Market opportunity identification
- Portfolio analysis

### 3. **Market Analysis**
- Price trend analysis
- Market segmentation (luxury, mid-range, budget)
- Location desirability scoring

### 4. **Business Intelligence**
- Competitive pricing for listings
- Market forecast models
- Business valuation for lending

## Extension Ideas

### Data Enhancements
- Add crime rate, school quality, proximity to amenities
- Include historical price trends
- Add economic indicators (employment, interest rates)
- Incorporate satellite imagery analysis

### Model Improvements
- Feature selection using L1 regularization
- Polynomial feature expansion for non-linear relationships
- Isolation Forest for outlier detection
- Stacking multiple models with meta-learner

### Deployment
- REST API for price predictions
- Real estate platform integration
- Mobile app for quick valuations
- Batch prediction pipeline for market analysis

## References

### Machine Learning Theory
- [Kaggle House Prices Competition](https://www.kaggle.com/c/house-prices-advanced-regression-techniques/overview)
- [Applied Predictive Modeling](http://appliedpredictivemodeling.com/)
- [Linear Regression Assumptions](https://www.statology.org/linear-regression-assumptions/)

### Real Estate Domain
- [Real Estate Market Analysis](https://www.investopedia.com/terms/r/real_estate_market_analysis.asp)
- [Property Valuation Methods](https://www.appraisers.org/news/what-are-the-three-approaches-to-value)
- [Location Impact on Property Values](https://www.investopedia.com/articles/mortages-real-estate/11/how-location-affects-real-estate-value.asp)

### Tools & Libraries
- [scikit-learn Regression Guide](https://scikit-learn.org/stable/modules/linear_model.html)
- [Pandas DataFrame Operations](https://pandas.pydata.org/docs/)
- [Matplotlib & Seaborn Visualization](https://seaborn.pydata.org/)

## Key Takeaways

1. **Feature Engineering is Crucial**: Domain knowledge drives model improvement more than algorithm choice
2. **Model Comparison Matters**: No single "best" model; ensemble methods often perform better
3. **Interpretability Important**: Understand why model makes predictions for business decisions
4. **Data Quality Paramount**: Clean, relevant features matter more than complex models
5. **Validation Essential**: Cross-validation prevents overfitting and ensures real-world performance
6. **Domain Context Required**: Real estate understanding improves feature engineering and result interpretation

## Getting Started

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the notebook**:
   ```bash
   jupyter notebook House_Price_Prediction.ipynb
   ```

3. **Modify for your data**:
   - Update `load_house_price_dataset()` to load your CSV file
   - Adjust feature names to match your dataset
   - Run cells sequentially to build full pipeline

4. **Experiment**:
   - Try different model parameters
   - Engineer new features
   - Test hyperparameter optimization
   - Create ensemble combinations

## Questions & Extensions

- What features drive price predictions in your market?
- How would you handle seasonal price variations?
- How would you update the model as new price data arrives?
- Can you predict price per square foot instead of total price?
- How would you handle properties with missing features?

---

**Created**: 2024 | **Purpose**: Machine Learning Regression Education
