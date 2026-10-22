import pandas as pd
import pickle
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score

with open("model/logistic_reg_model.pkl", "rb") as file:
    model = pickle.load(file)


# def predict_delay(csv_path):
#     # take CSV file and convert into dataframe then predict the delay with the use of pipeline and 
#     # give confusion matrix classification report null values shape information describe accuracy duplicated rows and
#     # also give all features that are important for the prediction by the model and other
#     # many details to LLM and then give prompt to the LLM to take these details and generate the full summary of this and
#     # reason of why delay is predicted and how to solve this.


#     try:

#         df = pd.read_csv(csv_path)

#         X = df.drop(columns=["Delayed"])
#         y = df['Delayed']

#         X['Date'] = pd.to_datetime(X['Date'], errors="coerce")

#         X['Day'] = X['Date'].dt.day
#         X['Month'] = X['Date'].dt.month
#         X['Year'] = X['Date'].dt.year

#         X.drop(columns=['Date'], inplace=True)

#         null_values = X.isnull().sum().to_string()

#         duplicate_rows = X.duplicated().sum()

#         shape = X.shape

#         describe = X.describe().to_string()

#         y_pred = pipeline.predict(X)

#         accuracy = accuracy_score(y,y_pred)

#         classify_report = classification_report(y,y_pred)

#         matrix = confusion_matrix(y,y_pred)

#         features = pipeline.named_steps['preprocessing'].get_feature_names_out()

#         coeficient= pipeline.named_steps['model'].coef_[0]

#         feature_importance = {
#             "Feature":features,
#             "Imporatnace":coeficient,
#             "Absolute_Imporatnace":abs(coeficient)
#         }

#         return f"""
#         Dataset : {X}

#         Null values : {null_values}
        
#         Duplicate Rows : {duplicate_rows}

#         Shape : {shape}

#         Describe : {describe}

#         Accuracy : {accuracy}

#         Classification Report : {classify_report}

#         Confusion Matrix : {matrix}

#         Feature Importance : {feature_importance}
        
#         Predicted Label : {y_pred}
#         """

#     except Exception as e:
#         return f"Error : {e}"

class Pipeline:
    def __init__(self, csv_file, model):
        self.csv_file = csv_file
        self.model = model

    def read_csv(self):
        if pd.errors.EmptyDataError:
            raise ValueError("The CSV is empty. It must contain Data.")
        
        df = pd.read_csv(self.csv_file)

        return df

    def split_feature(self, df):
        if not isinstance(df, pd.DataFrame):
            raise TypeError("Input must be pandas DataFrame.")
        
        if "Delayed" not in df.columns:
            raise KeyError("Target feature name must be 'Delayed'.")

        if df.empty:
            raise ValueError("Dataset should contain data not empty.")
        
        X = df.drop(columns=["Delayed"])
        y = df['Delayed']

        return X, y

    def change_dtype(self, X):
        if not isinstance(X, pd.DataFrame):
            raise TypeError("Input Type must be pandas DataFrame.")
        
        if 'Date' not in X.columns:
            raise KeyError("'Date' feature not found in Dataset")

        try:
            X['Date'] = pd.to_datetime(X['Date'], errors="coerce")

            X['Day'] = X['Date'].dt.day
            X['Month'] = X['Date'].dt.month
            X['Year'] = X['Date'].dt.year
            
            X.drop(columns=['Date'], inplace=True)
            
            return X
        
        except TypeError:
            raise TypeError("'Date' feature type must be datetime or str")


    def check_data_quality(self, X):
        if not isinstance(X, pd.DataFrame):
            raise TypeError("Input Type must be pandas DataFrame.")

        null_values = X.isnull().sum().to_string()
        
        duplicate_rows = X.duplicated().sum()
        
        shape = X.shape
        
        describe = X.describe().to_string()

        return {
            "Dataset":X,
            "Null Values":null_values,
            "Duplicate Rows":duplicate_rows,
            "Shape":shape,
            "Describe":describe
        }

    def prediction_report(self, X, y):
        if not isinstance(X, pd.DataFrame):
            raise TypeError("Input Type must be pandas DataFrame.")

        y_pred = self.model.predict(X)

        accuracy = accuracy_score(y,y_pred)
        
        classify_report = classification_report(y,y_pred)
        
        matrix = confusion_matrix(y,y_pred)
        
        features = self.model.named_steps['preprocessing'].get_feature_names_out()
        
        coeficient= self.model.named_steps['model'].coef_[0]
        
        feature_importance = {
            "Feature":features,
            "Imporatnace":coeficient,
            "Absolute_Imporatnace":abs(coeficient)
        }

        return {
            "Predicted Label":y_pred,
            "Accuracy":accuracy,
            "Classification report":classify_report,
            "Confusion Matrix":matrix,
            "Feature Importance":feature_importance
        }