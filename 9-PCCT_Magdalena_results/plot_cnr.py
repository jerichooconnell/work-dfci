import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns

def add_cnr_over_dose_column(df):
    # Calculate CNR_over_dose
    df['CNR_over_dose'] = df['cnr'] / ((df['energy_deposited_water']**2 + df['energy_deposited_water_high']**2)**0.5)**.5
    return df

def plot_cnr_over_dose(df):
    # Set up the plotting style
    sns.set(style="whitegrid")

    # Plot CNR_over_dose as a function of low_bin and high_bin
    fig = plt.figure(figsize=(12, 6))
    ax = fig.add_subplot(111, projection='3d')
    sc = ax.scatter(df['low_bin'], df['high_bin'], df['CNR_over_dose'], c=df['CNR_over_dose'], cmap='viridis')
    ax.set_title('CNR_over_dose as a function of low_bin and high_bin')
    ax.set_xlabel('low_bin')
    ax.set_ylabel('high_bin')
    ax.set_zlabel('CNR_over_dose')
    fig.colorbar(sc, ax=ax, label='CNR_over_dose')
    plt.show()

    # Plot CNR_over_dose as a function of low_filter and high_filter
    fig = plt.figure(figsize=(12, 6))
    ax = fig.add_subplot(111, projection='3d')
    sc = ax.scatter(df['low_filter'], df['high_filter'], df['CNR_over_dose'], c=df['CNR_over_dose'], cmap='viridis')
    ax.set_title('CNR_over_dose as a function of low_filter and high_filter')
    ax.set_xlabel('low_filter')
    ax.set_ylabel('high_filter')
    ax.set_zlabel('CNR_over_dose')
    fig.colorbar(sc, ax=ax, label='CNR_over_dose')
    plt.show()

    # Plot CNR_over_dose as a function of low_bin and low_filter
    fig = plt.figure(figsize=(12, 6))
    ax = fig.add_subplot(111, projection='3d')
    sc = ax.scatter(df['low_bin'], df['low_filter'], df['CNR_over_dose'], c=df['CNR_over_dose'], cmap='viridis')
    ax.set_title('CNR_over_dose as a function of low_bin and low_filter')
    ax.set_xlabel('low_bin')
    ax.set_ylabel('low_filter')
    ax.set_zlabel('CNR_over_dose')
    fig.colorbar(sc, ax=ax, label='CNR_over_dose')
    plt.show()

    # Plot CNR_over_dose as a function of high_bin and high_filter
    fig = plt.figure(figsize=(12, 6))
    ax = fig.add_subplot(111, projection='3d')
    sc = ax.scatter(df['high_bin'], df['high_filter'], df['CNR_over_dose'], c=df['CNR_over_dose'], cmap='viridis')
    ax.set_title('CNR_over_dose as a function of high_bin and high_filter')
    ax.set_xlabel('high_bin')
    ax.set_ylabel('high_filter')
    ax.set_zlabel('CNR_over_dose')
    fig.colorbar(sc, ax=ax, label='CNR_over_dose')
    plt.show()

if __name__ == '__main__':
    # Load the data
    df = pd.read_csv('/home/jericho/1-Workspace/9-PCCT_Magdalena_results/results.csv')

    # Add the CNR_over_dose column
    df = add_cnr_over_dose_column(df)

    # Plot the CNR_over_dose
    plot_cnr_over_dose(df)