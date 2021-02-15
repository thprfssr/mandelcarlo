import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.optimize as spo
import glob
from uncertainties import ufloat

# Read all the data
filenames = glob.glob('data/run-*.tsv')
dfs = [pd.read_csv(f, sep = '\t') for f in filenames]
df = pd.concat(dfs, ignore_index = True)
n = df['threshold']
A = df['A']
u_A = df['u(A)']

# Fit the data
popt, pcov = spo.curve_fit(

        f = lambda x, a, b, c: a * x**2 + b * x + c,
        xdata = 1/n,
        ydata = A,
        sigma = u_A
        )
u_a = pcov[0][0]**(1/2)
u_b = pcov[1][1]**(1/2)
u_c = pcov[2][2]**(1/2)
a = popt[0]
b = popt[1]
c = popt[2]
print('a =', ufloat(a, u_a))
print('b =', ufloat(b, u_b))
print('c =', ufloat(c, u_c))
print(pcov)

# Plot the data and the fit
X = np.linspace(min(1/n), max(1/n), 1000)
plt.errorbar(1/n, A, u_A, capsize = 5, fmt = 'o')
plt.plot(X, a * X**2 + b * X + c)

# Take care of labels
plt.xlabel(r'$\frac{1}{n}$')
plt.ylabel(r'$A_n$')
plt.title(r'Partial Mandelbrot areas vs. $\frac{1}{n}$')

plt.show()
