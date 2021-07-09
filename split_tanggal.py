import numpy as np
import pandas as pd
def getCSV(start_date, end_date):
    df = pd.read_csv('data/question_philoit.csv')
    df = df[['created_at','content']]
    df['created_at']= pd.to_datetime(df['created_at'])
    df['content'] = df['content'].apply(str)
    df = df[(df['created_at'] > start_date) & (df['created_at'] < end_date)]
    df.to_csv(f"static/csv/questions_{start_date}_{end_date}.csv", index=False)
    return f"static/csv/questions_{start_date}_{end_date}.csv"