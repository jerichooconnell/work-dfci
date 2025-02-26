# %matplotlib inline

import fastcat as fc
import numpy as np
import matplotlib.pyplot as plt
import spekpy as sp
import pandas as pd
from multiprocessing import Pool
from functools import partial
from functions import detector_response, find_closest_indices, calculate_fluence, calculate_mean_energy, print_results, plot_spectra, plot_detector_responses
from functions import response_function, calculate_mean_attenuation_coefficient, print_mean_attenuation_coefficients
from functions import bin_true_spectrum, plot_true_responses

# Set debug mode
DEBUG = False

# Get attenuation coefficients for Bismuth and Gadolinium
mu_bi = fc.get_mu(z=79)
mu_gd = fc.get_mu(z=64)

energies = np.linspace(10, 500, 5000)
mu_bismuth = [mu_bi(energy) for energy in energies]
mu_gadolinium = [mu_gd(energy) for energy in energies]

# K-edge energies
k_bi = 80.7
# k_gd = 50.2

# Make an empty data frame to store the results
results_df = pd.DataFrame(columns=['low_bin', 'high_bin', 'low_filter', 'high_filter',
                                   'fluence_W_to_bi_high', 'fluence_W_to_bi_low',
                                   'fluence_bi_high', 'fluence_bi_low',
                                   'mean_energy_W_to_bi_high', 'mean_energy_W_to_bi_low',
                                   'mean_energy_bi_high', 'mean_energy_bi_low',
                                   'mu_at_mean_energy_W_to_bi_low', 'mu_at_mean_energy_W_to_bi_high',
                                   'mu_at_mean_energy_bi_low', 'mu_at_mean_energy_bi_high',
                                   'std_mu_bi_low', 'std_mu_bi_high', 'energy_deposited_water', 'energy_deposited_water_high',
                                   'cnr'])

# Generate normalized spectrum
s_norm = sp.Spek(140, 14)
s_norm.filter('Al', 4)
s_norm.filter('Water', 80)
xx_norm, yy_norm = s_norm.get_spectrum()
yy_norm /= 0.134 * np.max(yy_norm)

def process_combination(low_filter, high_filter):
    # Generate spectra
    s_low = sp.Spek(140, 14)
    s_low.filter('Au', low_filter)
    xx_in, yy_in = s_low.get_spectrum()
    s_low.filter('Water', 100)
    xx_low, yy_low = s_low.get_spectrum()

    s_high = sp.Spek(140, 14)
    s_high.filter('Pb', high_filter)
    xx_in_high, yy_in_high = s_high.get_spectrum()
    s_high.filter('Water', 100)
    xx_high, yy_high = s_high.get_spectrum()
    yy_high[-1] = 0  # Insert another entry of 121 keV 0 fluence to the spectrum

    energy_deposited_water = np.sum(xx_in*(yy_in- yy_low))
    energy_deposited_water_high = np.sum(xx_in_high*(yy_in_high - yy_high))

    yy_low_unnormalized = yy_low.copy()
    yy_high_unnormalized = yy_high.copy()

    # Normalize spectra
    yy_low /= np.max(yy_low)
    yy_high /= np.max(yy_high)

    # Calculate detector responses
    c1 = 1
    U_high, response_high = detector_response(yy_high, xx_norm, c1)
    U_low, response_low = detector_response(yy_low, xx_norm, c1)
    U_norm, response_norm = detector_response(yy_norm, xx_norm, c1)

    # Interpolate high-energy spectrum to match normalized spectrum
    yy_high_interp = np.interp(xx_norm, xx_high, yy_high)

    m_response_high = np.max(response_high)
    m_response_low = np.max(response_low)
    m_response_norm = np.max(response_norm)

    # Normalize responses
    response_high /= np.max(response_high)
    response_low /= np.max(response_low)
    response_norm /= np.max(response_norm)

    mu_bi_low = [mu_bi(energy) for energy in xx_low]
    mu_bi_high = [mu_bi(energy) for energy in xx_high]

    yy_low2 = yy_low.copy()
    yy_high2 = yy_high.copy()

    local_results = []

    for low_bin in range(1, 24):
        for high_bin in range(1, 24):

            yy_low = yy_low2.copy()
            yy_high = yy_high2.copy()

            # Define energy bins
            k_20 = 20
            k_W = k_bi - low_bin
            k_top = k_bi + high_bin

            # Find the closest indices to the k-edge energies
            k_indices_high = find_closest_indices(xx_high, [k_bi, k_W, k_top])
            k_indices_low = find_closest_indices(xx_low, [k_bi, k_W, k_top])

            if DEBUG:
                print(k_indices_low)

            # Calculate fluence percentages
            fluence_W_to_bi_high, fluence_bi_high = calculate_fluence(yy_high, k_indices_high)
            fluence_W_to_bi_low, fluence_bi_low = calculate_fluence(yy_low, k_indices_low)

            # Calculate mean energies
            mean_energy_high, mean_energy_W_to_bi_high, mean_energy_bi_high = calculate_mean_energy(xx_high, yy_high, k_indices_high)
            mean_energy_low, mean_energy_W_to_bi_low, mean_energy_bi_low = calculate_mean_energy(xx_low, yy_low, k_indices_low)

            # Print fluence and mean energy results
            if DEBUG:
                print_results(fluence_W_to_bi_high, fluence_W_to_bi_low, fluence_bi_high, fluence_bi_low, mean_energy_W_to_bi_high, mean_energy_W_to_bi_low, mean_energy_bi_high, mean_energy_bi_low, mu_bi(mean_energy_W_to_bi_low), mu_bi(mean_energy_W_to_bi_high), mu_bi(mean_energy_bi_low), mu_bi(mean_energy_bi_high))

            # Find closest indices for response calculations
            k_bi_index_low2 = np.argmin(np.abs(xx_low - (k_bi + 6)))
            k_top_index_high2 = np.argmin(np.abs(xx_norm - 112))

            k_bi_index_high = np.argmin(np.abs(xx_high - k_bi))
            k_top_index_high = np.argmin(np.abs(xx_high - k_top))

            k_W_index_low = np.argmin(np.abs(xx_low - k_W))
            k_bi_index_low = np.argmin(np.abs(xx_low - k_bi))
            k_top_index_low = np.argmin(np.abs(xx_low - k_top))

            # Plot spectra
            if DEBUG:
                plot_spectra(xx_low, yy_low, xx_high, yy_high, k_W, k_bi, k_top, xx_norm, yy_norm)

            # Calculate true and false responses
            U_high2, response_high_true = detector_response(yy_high_interp[k_bi_index_high:k_top_index_high2], xx_norm[k_bi_index_high:k_top_index_high2], c1)
            U_low2, response_low_true = detector_response(yy_low[k_W_index_low:k_bi_index_low2], xx_low[k_W_index_low:k_bi_index_low2], c1)
            U_norm_low, response_norm_true_low = detector_response(yy_norm[k_W_index_low:k_bi_index_low], xx_norm[k_W_index_low:k_bi_index_low], c1)
            U_norm_high, response_norm_true_high = detector_response(yy_norm[k_bi_index_low:k_top_index_low], xx_norm[k_bi_index_high:k_top_index_high], c1)

            # Normalize true responses
            response_high_true /= m_response_high
            response_low_true /= m_response_low
            response_norm_true_low /= m_response_norm
            response_norm_true_high /= m_response_norm

            # Calculate false responses
            response_low_false = response_low[k_W_index_low:k_bi_index_low2] - response_low_true
            response_high_false = response_high[k_bi_index_high:k_top_index_high2] - response_high_true
            response_norm_false_low = response_norm[k_W_index_low:k_bi_index_low] - response_norm_true_low
            response_norm_false_high = response_norm[k_bi_index_low:k_top_index_low] - response_norm_true_high

            # Plot detector responses
            if DEBUG:
                plot_detector_responses(U_low, response_low, U_high, response_high, U_low2, response_low_true, response_low_false, U_high2, response_high_true, response_high_false, k_W, k_bi, k_top, U_norm, response_norm, U_norm_low, response_norm_true_low, response_norm_false_low, U_norm_high, response_norm_true_high, response_norm_false_high)

            # Calculate the amount of photons captured in a bin from the true spectrum
            U_low_bin, response_low_bin_low, response_low_bin_high = bin_true_spectrum(yy_low_unnormalized, k_indices_low, xx_low, c1)
            U_high_bin, response_high_bin_low, response_high_bin_high = bin_true_spectrum(yy_high_unnormalized, k_indices_high, xx_high, c1)

            mu_at_mean_energy_W_to_bi_low, mu_at_mean_energy_W_to_bi_high = calculate_mean_attenuation_coefficient(mu_bi_low, xx_low, response_low_bin_low, k_indices_low)
            mu_at_mean_energy_bi_low, mu_at_mean_energy_bi_high = calculate_mean_attenuation_coefficient(mu_bi_high, xx_high, response_high_bin_high, k_indices_high)

            std_mu_bi_low = np.sum(response_low_bin_low)**0.5
            std_mu_bi_high = np.sum(response_high_bin_high)**0.5

            if DEBUG:
                print_mean_attenuation_coefficients(mu_at_mean_energy_W_to_bi_low, mu_at_mean_energy_bi_low)
                print_mean_attenuation_coefficients(mu_at_mean_energy_W_to_bi_high, mu_at_mean_energy_bi_high)

                plot_true_responses(U_high_bin, response_low_bin_low, response_low_bin_high, xx_low, U_low_bin, response_high_bin_low, response_high_bin_high, xx_high, yy_low, c1, k_indices_low, k_indices_high, yy_high_interp)

            cnr = np.abs(mu_at_mean_energy_bi_high - mu_at_mean_energy_W_to_bi_low) / np.sqrt(1/(std_mu_bi_high)**2 + 1/(std_mu_bi_low)**2)

            if DEBUG:
                print(cnr)
                input()

            local_results.append({
                'low_bin': low_bin, 'high_bin': high_bin, 'low_filter': low_filter, 'high_filter': high_filter,
                'fluence_W_to_bi_high': fluence_W_to_bi_high,
                'fluence_W_to_bi_low': fluence_W_to_bi_low,
                'fluence_bi_high': fluence_bi_high,
                'fluence_bi_low': fluence_bi_low,
                'mean_energy_W_to_bi_high': mean_energy_W_to_bi_high,
                'mean_energy_W_to_bi_low': mean_energy_W_to_bi_low,
                'mean_energy_bi_high': mean_energy_bi_high,
                'mean_energy_bi_low': mean_energy_bi_low,
                'mu_at_mean_energy_W_to_bi_low': mu_at_mean_energy_W_to_bi_low,
                'mu_at_mean_energy_W_to_bi_high': mu_at_mean_energy_W_to_bi_high,
                'mu_at_mean_energy_bi_low': mu_at_mean_energy_bi_low,
                'mu_at_mean_energy_bi_high': mu_at_mean_energy_bi_high,
                'energy_deposited_water': energy_deposited_water,
                'energy_deposited_water_high': energy_deposited_water_high,
                'std_mu_bi_low': std_mu_bi_low, 'std_mu_bi_high': std_mu_bi_high, 'cnr': cnr
            })

    return local_results

if __name__ == '__main__':
    with Pool() as pool:
        results = pool.starmap(process_combination, [(low_filter, high_filter) for low_filter in np.arange(0.1, 2.1, 0.1) for high_filter in np.arange(0.1, 2.1, 0.1)])
    
    # Flatten the list of results
    results_flat = [item for sublist in results for item in sublist]
    
    # Convert to DataFrame
    results_df = pd.DataFrame(results_flat)
    
    # Save to CSV
    results_df.to_csv('results.csv', index=False)