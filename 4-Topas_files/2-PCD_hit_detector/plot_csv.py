import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def plot_csv(filename):
    # Read the CSV file, skipping the first 8 lines
    df = pd.read_csv(filename, header=None, skiprows=8)

    # Generate energy values using the binning information
    # Binned by energy deposited in step in 100 bins of 0.001 MeV from 0 MeV to 0.1 MeV
    energy_values = np.linspace(0, 0.1, 500)

    # Plot the data
    plt.semilogy(energy_values, df.iloc[0][1:-1])
    plt.xlabel('Energy (MeV)')
    plt.ylabel('Energy Deposit (MeV)')
    plt.title('Energy Deposited in Phantom')
    plt.show()


# Call the function with your filename
# plot_csv("Case3BinnedByEnergyDepositedInStep.csv")
plot_csv("Case2BinnedByIncidentPreStepEnergy.csv")
