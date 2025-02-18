import json
import pandas as pd
from ydata_profiling import ProfileReport

file_path = "../../data/processed/CleanedProcessed2.json"
with open(file_path, "r", encoding="utf-8") as file:
    data = json.load(file)

df = pd.DataFrame(data)
profile = ProfileReport(df, title="Data Profiling Report", explorative=True)
profile.to_file("../../reports/cleaned_data_report.html")
