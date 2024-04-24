# %%

import math
import numpy as np
import matplotlib.pyplot as plt

# Constants
a1 = 0.5
a2 = 0.015  # Unit is keV^-1, assuming this is the value
a3 = 0.035  # Unit is keV^-1, assuming this is the value
a4 = 0.213e-3  # Unit is keV^-2, assuming this is the value
a5 = 1.64  # Unit is keV, assuming this is the value
a6 = 0.025

# Escape photon energy for CdTe (assumed to be 25 keV)
Ee = 25

# Function to calculate c2(E)


def c2(E, Ee):
    if E >= Ee:
        return a1 * np.exp(-(a2 * E))
    else:
        return 0

# Function to calculate c3(E)


def c3(E):
    return a3 - a4 * E

# Function to calculate sigma(E)


def sigma(E):
    return a5 + a6 * E

# Function to calculate B(U, E)


def B(U, E):
    Bs = []
    for u in U:
        sigma1 = sigma(E)
        if u < (E - 3 * sigma1):
            Bs.append(c3(E))
        elif E - 3 * sigma1 <= u <= E + 3 * sigma1:
            # Linearly ramped down to zero within the width of 6sigma1
            slope = -c3(E) / (6 * sigma1)
            intercept = - slope * (E + 3 * sigma1)
            Bs.append(slope * (u) + intercept)
        else:
            Bs.append(0)

    print(intercept, slope)
    return Bs


def R(U, E):
    # Define constants
    # c1 = 1  # Assuming c1 is 1, change if needed
    # c2 = 1  # Assuming c2 is 1, change if needed
    # Er = 0  # Assuming Er is 0, change if needed
    # B = 0   # Assuming B(U, E) is 0, change if needed

    # # Define variables
    # sigma1 = 1  # Assuming sigma1(E) is 1, change if needed
    # sigma2 = 1  # Assuming sigma2(E) is 1, change if needed

    sig = sigma(E)

    c1 = 1
    # Calculation
    term1 = (1 / (math.sqrt(2 * math.pi) * sig)) * \
        np.exp(-((U - E) ** 2) / (2 * sig ** 2))
    term2 = (c2(E, Ee) / (math.sqrt(2 * math.pi) * sig)) * \
        np.exp(-((U - (E - Ee)) ** 2) / (2 * sig ** 2))

    # print(term1, term2)
    # print(B(U, E))

    return c1*(term1 + term2) + B(U, E)


# Example usage
U_value = np.linspace(0, 100, 200)  # Change U_value as needed
E_value = 75   # Change E_value as needed


result = R(U_value, E_value)


plt.figure()
plt.plot(U_value, result)

# %%
