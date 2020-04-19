import numpy
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from utilities import Infected

beta = 0.2  # Contact rate
sigma = 1 / 14  # 1/Latent Period (Latent Rate)
gama = 1 / 31  # 1/Recovery Period (Recovery Rate)


def coronaCases(x, t):
    n = numpy.sum(x)
    s = x[0]
    e = x[1]
    i = x[2]
    dsdt = -(beta * s * i / n)
    dedt = (beta * s * i / n) - (sigma * e)
    didt = sigma * e - gama * i
    drdt = gama * i
    return [dsdt, dedt, didt, drdt]


def Initial_data(Population, Infected, Recovered, Deceased):
    suspectibles = Population - (Recovered + Deceased)
    expected = sigma * beta * suspectibles / sigma * gama
    return [suspectibles, expected, Infected, Recovered]


t = numpy.linspace(0, 90, 90)  # Plotting for 90 days starting from today

x = odeint(coronaCases, Initial_data(36000000, Infected("Todays_data.csv", "KL"), 270, 2), t)
S = x[:, 0]
E = x[:, 1]
I = x[:, 2]
R = x[:, 3]

plt.ylabel('Peoples in Thousands')
plt.xlabel('Days')
plt.plot(t, S, label="suspectibles")
plt.plot(t, E, label="exposed")
plt.plot(t, I, label="infected")
plt.plot(t, R, label="recovered")
plt.legend(loc='best')
plt.show()
