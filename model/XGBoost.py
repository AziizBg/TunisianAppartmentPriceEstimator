import json
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from src.data.Tokenization.DataTransformer import TransforRecord
from sklearn.metrics import mean_squared_error, r2_score

# Load data
with open('../data/processed/CleanedProcessed1.json', 'r', encoding="utf-8") as file:
    data = json.load(file)

# Transform data
X, y = TransforRecord(data)
print("Data (Features):")
print(X)
print("\nLabels (Target - Price):")
print(y)
# Split dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Convert training and testing data to DMatrix format
dtrain = xgb.DMatrix(X_train, label=y_train)
dtest = xgb.DMatrix(X_test, label=y_test)

# Define parameters
params = {
    'objective': 'reg:squarederror',  # Regression task
    'eval_metric': 'rmse',            # Root Mean Squared Error
    'max_depth': 7,                   # Maximum depth of trees
    'eta': 0.01,                       # Learning rate
    'subsample': 0.9,                 # Subsample ratio
    'colsample_bytree': 0.8,          # Feature columns ratio
}

num_rounds = 3000  # Number of boosting rounds

# Cross-validation
cv_results = xgb.cv(
    params=params,
    dtrain=dtrain,
    num_boost_round=num_rounds,
    nfold=5,                          # Number of folds for cross-validation
    early_stopping_rounds=50,         # Stop training early if no improvement after 10 rounds
    metrics={'rmse'},                 # Evaluation metric
    as_pandas=True                    # Return results as a pandas DataFrame
)

# Print the optimal number of rounds from cross-validation
optimal_num_rounds = cv_results.shape[0]
print(f"Optimal number of rounds: {optimal_num_rounds}")

# Train the model using the optimal number of rounds
model = xgb.train(params, dtrain, num_boost_round=optimal_num_rounds)

# Predict on the test set
y_pred = model.predict(dtest)

# Calculate RMSE
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
print(f"RMSE: {rmse:.2f}")

# Calculate R²
r2 = r2_score(y_test, y_pred)
print(f"R²: {r2:.4f}")

# Approximate accuracy (optional)
accuracy = 100 - (np.mean(np.abs(y_test - y_pred) / y_test) * 100)
print(f"Accuracy (approximation): {accuracy:.2f}%")
