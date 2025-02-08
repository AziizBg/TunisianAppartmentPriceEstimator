import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OrdinalEncoder, LabelEncoder, StandardScaler


def tryPop(item, field):
    if field in item.keys():
        item.pop(field)


def TransforRecord(records):
    df = pd.DataFrame(records)
    binary_columns = ["parking", "heating", "air_conditioning", "balcony", "elevator", "equipped_kitchen", "garage"]
    df[binary_columns] = df[binary_columns].applymap(lambda x: 1 if x.lower() == "yes" else 0)
    for col in ["state", "municipality", "delegation"]:
        encoder = LabelEncoder()
        df[col] = encoder.fit_transform(df[col])
    scaler = StandardScaler()
    numerical_cols = ["bedrooms", "bathrooms", "surface"]  # Add other numerical features
    df[numerical_cols] = scaler.fit_transform(df[numerical_cols])
    imputer = SimpleImputer(strategy='mean')
    df = pd.DataFrame(imputer.fit_transform(df), columns=df.columns)
    feature_names = df.drop(columns=["price", "delegation", "state", "balcony"]).columns.tolist()
    print(feature_names)
    data = df.drop(columns=["price", "delegation", "state"]).values
    labels = df["price"].values
    return data, labels
