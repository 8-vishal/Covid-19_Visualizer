import requests
import pandas as pd


def CSV_creator():
    """Scrape the website for the Data in CSV format"""
    url = "https://docs.google.com/spreadsheets/u/1/d/e/2PACX-1vSz8Qs1gE_IYpzlkFkCXGcL_BqR8hZieWVi-rphN1gfrO3H4lDtVZs4kd0C3P8Y9lhsT1rhoB-Q_cP4/pubhtml"
    html = requests.get(url).content
    df_list = pd.read_html(html)
    df = df_list[0]
    return df.to_csv('Todays_data.csv')


def Infected(path, StateCode):
    """Give total of infected in a state"""
    df = pd.read_csv(path)
    df = df.iloc[2:]
    df = df[['Unnamed: 1','Unnamed: 3', 'Unnamed: 9', 'Unnamed: 10','Unnamed: 14']]
    df = pd.DataFrame.rename(df,
                             columns={'Unnamed: 1': 'PatientNo.', 'Unnamed: 3': 'StartDate', 'Unnamed: 9': 'Statecode',
                                      'Unnamed: 10': 'CurrentStatus','Unnamed: 14': 'TransmissionType'})
    df = df[df["Statecode"] == StateCode]
    patientS = [1] * len(df)
    df["patient"] = patientS
    df["StartDate"] = pd.to_datetime(df['StartDate'], format='%d/%m/%Y')
    df = df[["StartDate", "patient"]]
    df = df.sort_index(ascending=True)
    df = df.groupby(df["StartDate"]).aggregate({"patient": 'sum'})
    return df['patient'].sum()


def Recovered(path, StateCode):
    """Give total of recovered in a state"""
    df = pd.read_csv(path)
    df = df.iloc[2:]
    df = df[['Unnamed: 1', 'Unnamed: 3', 'Unnamed: 9', 'Unnamed: 10', 'Unnamed: 14']]
    df = pd.DataFrame.rename(df,
                             columns={'Unnamed: 1': 'PatientNo.', 'Unnamed: 3': 'StartDate', 'Unnamed: 9': 'Statecode',
                                      'Unnamed: 10': 'CurrentStatus', 'Unnamed: 14': 'TransmissionType'})
    df = df[df["Statecode"] == StateCode]
    df = df.loc[df['CurrentStatus'] == 'Recovered']
    patientS = [1] * len(df)
    df["patient"] = patientS
    df["StartDate"] = pd.to_datetime(df['StartDate'], format='%d/%m/%Y')
    df = df[["StartDate", "patient"]]
    df = df.sort_index(ascending=True)
    df = df.groupby(df["StartDate"]).aggregate({"patient": 'sum'})
    return df['patient'].sum()


def Cleaned_CSV_data(path, StateCode):
    """provide cleaned dataa for a state in csv format"""
    df = pd.read_csv(path)
    df = df.iloc[2:]
    df = df[['Unnamed: 1', 'Unnamed: 3', 'Unnamed: 9', 'Unnamed: 10', 'Unnamed: 14']]
    df = pd.DataFrame.rename(df,
                             columns={'Unnamed: 1': 'PatientNo.', 'Unnamed: 3': 'StartDate', 'Unnamed: 9': 'Statecode',
                                      'Unnamed: 10': 'CurrentStatus', 'Unnamed: 14': 'TransmissionType'})
    df = df[df["Statecode"] == StateCode]
    return df

