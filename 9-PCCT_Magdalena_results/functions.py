import numpy as np
import matplotlib.pyplot as plt

def get_parameters():
    """Return the parameters from Table 3"""
    return {
        'a1': 0.5,
        'a2': 0.015,  # keV^-1
        'a3': 0.042,  # keV^-1
        'a4': 0.213e-3,  # keV^-2
        'a5': 1.61,   # keV
        'a6': 0.025
    }

def c2(E, Ee, a1, a2):
    """Piecewise function for c2(E)"""
    return np.where(E > Ee, a1 * np.exp(-a2 * E), 0)

def c3(E, a3, a4):
    """Linear function for c3(E)"""
    return a3 - a4 * E

def sigma(E, a5, a6):
    """Linear function for σ(E)"""
    return a5 + a6 * E

def background(U, E, c3_val, sigma_val):
    """Calculate background B(U,E)"""
    threshold = E - 3 * sigma_val
    ramp_width = 6 * sigma_val
    return np.where(
        U < threshold,
        c3_val,
        np.where(
            U < threshold + ramp_width,
            c3_val * (1 - (U - threshold) / ramp_width),
            0
        )
    )

def response_function(U, E, c1):
    """Calculate the response function R(U,E)"""
    params = get_parameters()
    Ee = 25.0  # escape energy for CdTe in keV
    c1_val = c1(E) if callable(c1) else c1
    c2_val = c2(E, Ee, params['a1'], params['a2'])
    c3_val = c3(E, params['a3'], params['a4'])
    sigma_val = sigma(E, params['a5'], params['a6'])
    gaussian1 = (1 / (np.sqrt(2*np.pi) * sigma_val)) * \
        np.exp(-0.5 * ((U - E)**2) / (sigma_val**2))
    gaussian2 = (1 / (np.sqrt(2*np.pi) * sigma_val)) * \
        np.exp(-0.5 * ((U - (E - Ee))**2) / (sigma_val**2))
    B = background(U, E, c3_val, sigma_val)
    return c1_val * gaussian1 + c2_val * gaussian2 + B

def detector_response(energy_spectrum, energies, c1):
    """Calculate the detector response to an energy spectrum"""
    U = np.linspace(min(energies), max(energies), len(energies))
    response = np.zeros_like(U)
    for E, spectrum_value in zip(energies, energy_spectrum):
        response += spectrum_value * response_function(U, E, c1)
    return U, response

def bin_true_spectrum(energy_spectrum, indices, energies, c1):
    """ Calculate the amount of photons captured in a bin from the true spectrum """    
    U = np.linspace(min(energies), max(energies), len(energies))
    response_bin = np.zeros_like(U)
    for ii, (E, spectrum_value) in enumerate(zip(energies[indices[0]:indices[1]], energy_spectrum[indices[0]:indices[1]])):
        response_bin[ii] = np.sum((spectrum_value * response_function(U, E, c1))[indices[0]:indices[1]])
    return U, response_bin

def plot_true_responses(U_high_bin, response_low_bin_low, response_low_bin_high, xx_low, U_low_bin, response_high_bin_low, response_high_bin_high, xx_high, yy_low, c1, k_indices_low, k_indices_high, yy_high):
    plt.figure()
    plt.subplot(2, 1, 1)
    plt.plot(U_low_bin, response_low_bin_low, label='Low energy')
    plt.plot(U_low_bin, response_low_bin_high, label='High energy')
    plt.plot(xx_low, yy_low, label='True spectrum')
    plt.axvline(x=xx_low[k_indices_low[0]], color='r', linestyle='--')
    plt.axvline(x=xx_low[k_indices_low[1]], color='r', linestyle='--')
    plt.axvline(x=xx_low[k_indices_low[2]], color='r', linestyle='--')
    plt.xlabel('Energy [keV]')
    plt.ylabel('Response')
    plt.title('Amount of photons captured in a bin from the true spectrum')
    plt.legend()

    plt.subplot(2, 1, 2)
    plt.plot(U_high_bin, response_high_bin_low, label='Low energy')
    plt.plot(U_high_bin, response_high_bin_high, label='High energy')
    plt.plot(xx_high, yy_high, label='True spectrum')
    plt.axvline(x=xx_high[k_indices_high[0]], color='r', linestyle='--')
    plt.axvline(x=xx_high[k_indices_high[1]], color='r', linestyle='--')
    plt.axvline(x=xx_high[k_indices_high[2]], color='r', linestyle='--')
    plt.xlabel('Energy [keV]')
    plt.ylabel('Response')
    plt.title('Amount of photons captured in a bin from the true spectrum')
    plt.legend()
    plt.tight_layout()
    plt.show()

def bin_true_spectrum(energy_spectrum, indices, energies, c1):
    """ Calculate the amount of photons captured in a bin from the true spectrum """
    U = np.linspace(min(energies), max(energies), len(energies))
    response_bin_low = np.zeros_like(U)
    response_bin_high = np.zeros_like(U)
    for ii, (E, spectrum_value) in enumerate(zip(energies, energy_spectrum)):
        response_bin_low[ii] = np.sum(
            (spectrum_value * response_function(U, E, c1))[indices[1]:indices[0]])
        response_bin_high[ii] = np.sum(
            (spectrum_value * response_function(U, E, c1))[indices[0]:indices[2]])
    return U, response_bin_low, response_bin_high


def find_closest_indices(energies, k_values):
    return [np.argmin(np.abs(energies - k)) for k in k_values]

def calculate_fluence(yy, indices):
    return np.sum(yy[indices[1]:indices[0]]) / np.sum(yy), np.sum(yy[indices[0]:indices[2]]) / np.sum(yy)

def calculate_mean_energy(xx, yy, indices):
    return np.mean(xx * (yy / np.sum(yy))), np.sum(xx[indices[1]:indices[0]] * (yy[indices[1]:indices[0]] / np.sum(yy[indices[1]:indices[0]]))), np.sum(xx[indices[0]:indices[2]] * (yy[indices[0]:indices[2]] / np.sum(yy[indices[0]:indices[2]])))

def calculate_mean_attenuation_coefficient(mu, xx, yy, indices):
    return np.sum(mu[indices[1]:indices[0]] * (yy[indices[1]:indices[0]] / np.sum(yy[indices[1]:indices[0]]))), np.sum(mu[indices[0]:indices[2]] * (yy[indices[0]:indices[2]] / np.sum(yy[indices[0]:indices[2]])))

def print_results(fluence_W_to_bi_high, fluence_W_to_bi_low, fluence_bi_high, fluence_bi_low, mean_energy_W_to_bi_high, mean_energy_W_to_bi_low, mean_energy_bi_high, mean_energy_bi_low, mu_at_mean_energy_W_to_bi_low, mu_at_mean_energy_W_to_bi_high, mu_at_mean_energy_bi_low, mu_at_mean_energy_bi_high):
    print(f'Fluence between W and Bi k-edges (120 kVp, 1 mm Cu, 0.89 mm Bi): {fluence_W_to_bi_high:.2f}')
    print(f'Fluence between W and Bi k-edges (140 kVp, 1 mm Cu, 0.89 mm Bi): {fluence_W_to_bi_low:.2f}')
    print(f'Fluence above Bi k-edge (120 kVp, 1 mm Cu, 0.89 mm Bi): {fluence_bi_high:.2f}')
    print(f'Fluence above Bi k-edge (140 kVp, 1 mm Cu, 0.89 mm Bi): {fluence_bi_low:.2f}')
    print(f'Mean energy between W and Bi k-edges (120 kVp, 1 mm Cu, 0.89 mm Bi): {mean_energy_W_to_bi_high:.2f} keV')
    print(f'Mean energy between W and Bi k-edges (140 kVp, 1 mm Cu, 0.89 mm Bi): {mean_energy_W_to_bi_low:.2f} keV')
    print(f'Mean energy above Bi k-edge (120 kVp, 1 mm Cu, 0.89 mm Bi): {mean_energy_bi_high:.2f} keV')
    print(f'Mean energy above Bi k-edge (140 kVp, 1 mm Cu, 0.89 mm Bi): {mean_energy_bi_low:.2f} keV')
    print(f'Mass attenuation coefficient at mean energy between W and Bi k-edges (140 kVp, 1 mm Cu, 0.89 mm Bi): {mu_at_mean_energy_W_to_bi_low:.2f} cm^2/g')
    print(f'Mass attenuation coefficient at mean energy between W and Bi k-edges (120 kVp, 1 mm Cu, 0.89 mm Bi): {mu_at_mean_energy_W_to_bi_high:.2f} cm^2/g')
    print(f'Mass attenuation coefficient at mean energy above Bi k-edge (140 kVp, 1 mm Cu, 0.89 mm Bi): {mu_at_mean_energy_bi_low:.2f} cm^2/g')
    print(f'Mass attenuation coefficient at mean energy above Bi k-edge (120 kVp, 1 mm Cu, 0.89 mm Bi): {mu_at_mean_energy_bi_high:.2f} cm^2/g')

def print_mean_attenuation_coefficients(mu_W_to_bi, mu_bi):
    print(f'Mean mass attenuation coefficient between W and Bi k-edges: {mu_W_to_bi:.2f} cm^2/g')
    print(f'Mean mass attenuation coefficient above Bi k-edge: {mu_bi:.2f} cm^2/g')

def plot_spectra(xx_low, yy_low, xx_high, yy_high, k_W, k_bi, k_top, xx_norm, yy_norm):
    plt.figure(figsize=(8, 8))
    plt.subplot(2, 2, 2)
    plt.plot(xx_low, yy_low, label='Low-energy spectrum', c='darkblue')
    plt.title('b) EKCT spectra')
    plt.plot(xx_high, yy_high, label='High-energy spectrum', c='red')
    plt.axvline(69.5, color='k', linestyle='-.')
    plt.axvline(k_bi, color='k', linestyle='--')
    plt.ylim(0, 1.1)
    plt.xlim(40, 140)
    plt.axvspan(k_W, k_bi + 6, color='darkblue', alpha=0.1)
    plt.axvspan(k_bi, k_top + 6, color='red', alpha=0.1)
    plt.xlabel('Energy (keV)')
    plt.ylabel('Fluence')
    plt.grid()
    plt.legend()

    plt.suptitle('Conventional k-edge CT (KCT) vs enhanced k-edge CT (EKCT)')
    plt.subplot(2, 2, 1)
    plt.plot(xx_norm, yy_norm, label='K-edge spectrum', c='k')
    plt.title('a) KCT spectrum')
    plt.axvline(69.5, color='k', linestyle='-.', label=f'W K-edge 69.5 keV')
    plt.axvline(k_bi, color='k', linestyle='--', label=f'Bi K-edge {k_bi} keV')
    plt.axvspan(k_W, k_bi, color='darkblue', alpha=0.1, label='Low-energy bin')
    plt.axvspan(k_bi, k_top, color='red', alpha=0.1, label='High-energy bin')
    plt.ylim(0, 1.1)
    plt.xlim(40, 140)
    plt.xlabel('Energy (keV)')
    plt.ylabel('Fluence')
    plt.grid()
    plt.legend()

    plt.tight_layout()
    plt.show()

def plot_detector_responses(U_low, response_low, U_high, response_high, U_low2, response_low_true, response_low_false, U_high2, response_high_true, response_high_false, k_W, k_bi, k_top, U_norm, response_norm, U_norm_low, response_norm_true_low, response_norm_false_low, U_norm_high, response_norm_true_high, response_norm_false_high):
    plt.subplot(2, 2, 4)
    plt.plot(U_low, response_low, label='Low-energy detector response', c='darkblue', alpha=0.4)
    plt.plot(U_high, response_high, label='High-energy detector response', c='red', alpha=0.4)
    plt.title('d) EKCT detector response')

    plt.plot(U_low2, response_low_true, label='Low-energy detector response', c='darkblue', linestyle='--')
    plt.plot(U_high2, response_high_true, label='High-energy detector response', c='red', linestyle='--')
    plt.plot(U_low2, response_low_false, label='Low-energy detector response', c='darkblue', linestyle=':')
    plt.plot(U_high2, response_high_false, label='High-energy detector response', c='red', linestyle=':')
    plt.axvspan(k_W, k_bi + 6, color='darkblue', alpha=0.1)
    plt.axvspan(k_bi, k_top + 6, color='red', alpha=0.1)
    plt.xlim(40, 140)
    plt.ylim(0, 1.1)
    plt.xlabel('Measured energy (keV)')
    plt.ylabel('Counts')
    plt.grid()

    plt.subplot(2, 2, 3)
    plt.plot(U_norm, response_norm, alpha=0.4, label='Total', c='k')
    plt.plot(U_norm_low, response_norm_true_low, label='True', c='k', linestyle='--')
    plt.plot(U_norm_high, response_norm_true_high, c='k', linestyle='--')
    plt.plot(U_norm_low, response_norm_false_low, label='False', c='k', linestyle=':')
    plt.plot(U_norm_high, response_norm_false_high, c='k', linestyle=':')
    plt.title('c) KCT detector response')
    plt.axvspan(k_W, k_bi, color='darkblue', alpha=0.1)
    plt.axvspan(k_bi, k_top - 1, color='red', alpha=0.1)
    plt.xlim(40, 140)
    plt.ylim(0, 1.1)
    plt.legend()
    plt.xlabel('Measured energy (keV)')
    plt.ylabel('Counts')
    plt.grid()

    plt.tight_layout()
    plt.show()