"""
I modified suspectibles population acording to the reproductive rate and then scale
the value by 1.1 to match the approximate scenario.
"""

import numpy
import pandas as pd
from scipy.integrate import odeint
from datetime import date
import matplotlib.pyplot as plt
import datetime as dtime

today = date.today()
sigma = 1 / 18  # 1/Latent Period (Latent Rate)
gama = 1 / 33  # 1/Recovery Period (Recovery Rate)
B = 40  # Lockdown percentage

states_list = ['India', 'Maharashtra', 'Delhi', 'Gujarat', 'Rajasthan', 'Tamil Nadu', 'Madhya Pradesh', 'Uttar Pradesh', 'Telangana',
               'Andhra Pradesh', 'Karnataka', 'Kerala', 'Jammu and Kashmir', 'West Bengal', 'Haryana', 'Punjab', 'Bihar',
               'Odisha', 'Uttarakhand', 'Jharkhand', 'Himachal Pradesh', 'Chhattisgarh', 'Assam', 'Chandigarh', 'Ladakh',
               'Andaman and Nicobar Islands', 'Meghalaya', 'Goa', 'Puducherry', 'Manipur', 'Tripura', 'Mizoram', 'Arunachal Pradesh',
               'Nagaland', 'Dadra and Nagar Haveli and Daman and Diu', 'Lakshadweep', 'Sikkim']

state_codes = {
    'Andaman and Nicobar Islands': 'AN', 'Andhra Pradesh': 'AP', 'Arunachal Pradesh': 'AR', 'Assam': 'AS', 'Bihar': 'BR', 'Chandigarh': 'CH', 'Chattisgarh': 'CT',
    'Dadra and Nagar Haveli and Daman and Diu': 'DNDD', 'Delhi': 'DL', 'Goa': 'GA', 'Gujarat': 'GJ', 'Haryana': 'HR', 'Himachal Pradesh': 'HP',
    'Jammu and Kashmir': 'JK', 'Jharkhand': 'JH', 'Karnataka': 'KA', 'Kerala': 'KL', 'Lakshadweep': 'LD', 'Madhya Pradesh': 'MP', 'Maharashtra': 'MH',
    'Manipur': 'MN', 'Meghalaya': 'ML', 'Mizoram': 'MZ', 'Nagaland': 'NL', 'Odisha': 'OR', 'Pondicherry': 'PY', 'Punjab': 'PB', 'Rajasthan': 'RJ', 'Sikkim': 'SK',
    'Tamil Nadu': 'TN', 'Telangana': 'TG', 'Tripura': 'TR', 'Uttar Pradesh': 'UP', 'Uttarakhand': 'UT', 'West Bengal': 'WB', 'India': 'TT', 'Ladakh': 'LA'}


def CasesDiif_equ(x, t):
    """ SEIR model Equations"""
    beta = 1 - float(B) / 100
    n = numpy.sum(x)
    s = x[0]
    e = x[1]
    i = x[2]
    dsdt = -(float(beta) * s * i / n)
    dedt = (float(beta) * s * i / n) - (float(sigma) * e)
    didt = float(sigma) * e - float(gama) * i
    drdt = float(gama) * i
    return [dsdt, dedt, didt, drdt]


def Initial_data(state):
    """ Load initial data from covid19india.org for MODEL """
    beta = 1 - float(B) / 100
    df = pd.read_csv('https://api.covid19india.org/csv/latest/state_wise.csv')
    df = df[['State_code', 'Confirmed', 'Recovered', 'Deaths', 'Active']]
    df.iloc[34] += df.iloc[35]
    df.drop(index=35, inplace=True)
    df = df[df['State_code'] == state_codes[str(state)]]
    ac, rec, dea, conf = df.iloc[0][4], df.iloc[0][2], df.iloc[0][3], df.iloc[0][1]
    suspectibles = 1.1 * (beta / gama) * ac
    exposed = float(sigma) * beta * suspectibles / float(sigma) * float(gama)
    return [suspectibles, exposed, ac, rec]


def PLOTTING(n_days, state):
    """ Plot data for given state
     India is also considered as state just for namesake """
    da_ys = numpy.linspace(0, int(n_days), int(n_days))
    date_lis = []
    for i in range(0, n_days):
        d = today + dtime.timedelta(days=i)
        date_lis.append(str(d.strftime("%x")))

    x = odeint(CasesDiif_equ, Initial_data(state), da_ys)
    x = numpy.array(x)
    s = x[:, 0].astype(int)
    e = x[:, 1].astype(int)
    i = x[:, 2].astype(int)
    r = x[:, 3].astype(int)
    plt.ylabel('Peoples in Thousands')
    plt.xlabel('Days')
    plt.plot(date_lis, s, label="suspectibles")
    plt.plot(date_lis, e, label="exposed")
    plt.plot(date_lis, i, label="infected")
    plt.plot(date_lis, r, label="recovered")
    plt.legend(loc='best')
    return plt.show()

PLOTTING(60, 'India')
