# I would like a detector class that takes in different materials attenuation coefficients and material thicknesses and densities and is able to filter a given polyenergetic specta.
# I would also like to be able to plot the spectra before and after filtration and calculate the fluence before and after filtration.
# I would also like to be able to plot the ratio of the filtered spectrum to the unfiltered spectrum and the difference between the filtered and unfiltered spectra.
# I would also like to be able to plot the ratio of the filtered spectrum to the unfiltered spectrum and the difference between the filtered and unfiltered spectra.
# I would also like to be able to plot the ratio of the filtered spectrum to the unfiltered spectrum and the difference between the filtered and unfiltered spectra.
# I would also like to be able to plot the ratio of the filtered spectrum to the unfiltered spectrum and the difference between the filtered and unfiltered spectra.
# I would also like to be able to plot the ratio of the filtered spectrum to the unfiltered spectrum and the difference between the filtered and unfiltered spectra.
# I would also like to be able to plot the ratio of the filtered spectrum to the unfiltered spectrum and the difference between the filtered and unfiltered spectra.
# I would also like to be able to plot the ratio of the filtered spectrum to the unfiltered spectrum and the difference between the filtered and unfiltered spectra.

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

custom_colors = mcolors.TABLEAU_COLORS


class Detector(object):
    # This class takes in different materials attenuation coefficients and material thicknesses and densities and is able to filter a given polyenergetic spectrum.
    # It will be initialized empty and then filled with the different materials and their properties.

    def __init__(self):
        # This function initializes the detector.
        self.layers = []
        self.spectra = []
        self.total_thickness = 0

    class layer(object):
        def __init__(self, material, thickness, density, total_thickness):
            # This function initializes a layer of the detector.
            # It takes in the material name, thickness in cm, and density in g/cm^3.
            # It puts them into a dataframe.
            # It also calculates the attenuation coefficient for the layer.

            # Initialize the dataframe.
            self.layer = {}
            self.layer['material'] = material
            self.layer['thickness'] = thickness
            self.layer['density'] = density
            # self.attenuation_coefficient = xdb.material_mu(self.layer['material'],
            #                                                self.energy,self.layer['density'])
            # self.attenuation_coefficient = xdb.material_mu(self.material,self.energy,self.density)
            if self.layer['thickness'] <= 5:
                self.layer['total_thickness'] = self.layer['thickness'] + \
                    total_thickness
            else:
                self.layer['total_thickness'] = 5 + \
                    total_thickness

        def plot_layer(self, axis, color):
            '''
            This function plots the detector layer as a box of the given width.
            axis: matplotlib axis objectS
            '''
            # This function plots the detector layer as a box of the given width.
            if self.layer['thickness'] <= 5:
                axis.add_patch(plt.Rectangle(
                    (0, -self.layer['total_thickness']+self.layer['thickness']), 1, -self.layer['thickness'], color=color))
                axis.annotate(self.layer['material'] + ' (' + f'{self.layer["thickness"]}' + ')', xy=(0.5, -self.layer['total_thickness'] + 0.5*self.layer['thickness']),
                              color='k', fontsize=12, ha='center', va='center')
            else:
                axis.add_patch(plt.Rectangle(
                    (0, -self.layer['total_thickness']+5), 1, -5, color=color))
                axis.annotate(self.layer['material'] + ' ()' + f'{self.layer["thickness"]}' + ')', xy=(0.5, -self.layer['total_thickness'] + 0.5*5),
                              color='k', fontsize=12, ha='center', va='center')

    def add_layers(self, materials, thicknesses, densities=None):
        # This function adds a layer to the detector.
        # It takes in the material name, thickness in cm, and density in g/cm^3.
        # It will add the layer to the detector.
        # It will also calculate the attenuation coefficient for the layer.
        # It will also calculate the total thickness of the detector.
        # Add the layer to the detector.
        for material, thickness in zip(materials, thicknesses):

            self.layers.append(self.layer(
                material, thickness, 1, self.total_thickness))
            if thickness <= 5:
                self.total_thickness += thickness
            else:
                self.total_thickness += 5

        self.materials = materials
        self.thicknesses = thicknesses
        self.densities = densities

    def reinitialize_detector(self):
        '''
        This function reinitializes the detector.
        '''
        # This function reinitializes the detector.
        self.layers = []
        self.spectra = []
        self.total_thickness = 0
        for material, thickness, density in zip(self.materials, self.thicknesses, self.densities):
            if density == None:
                self.layers.append(self.layer(
                    material, thickness, 1, self.total_thickness))
            else:
                self.layers.append(self.layer(
                    material, thickness, density, self.total_thickness))
            if thickness <= 5:
                self.total_thickness += thickness
            else:
                self.total_thickness += 5

    class filtered_spectrum(object):
        '''
        This function filters a given polyenergetic spectrum.
        It takes in a spectrum.
        It will filter the spectrum through the detector layer given'''

        def __init__(self, spectrum, layer):
            '''
            This function filters a given polyenergetic spectrum.
            It takes in a spectrum.
            It will filter the spectrum through the detector.

            spectrum: spekpy spectrum object
            '''
            # This function filters a given polyenergetic spectrum.
            # It takes in a spectrum.
            # It will filter the spectrum through the detector.
            # It will return save each filtered spectrum in a dataframe.
            # It will also save the spectra absorbed by each layer in a dataframe.

            # Initialize the dataframe.
            self.spectrum = spectrum
            self.filtered_spectrum = {}
            # get the initial spectrum
            energy, fluence_i = spectrum.get_spectrum()
            self.filter_spectrum(
                spectrum, layer['material'], layer['thickness'], layer['density'])
            # get the final spectrum
            energy, fluence_f = spectrum.get_spectrum()

            self.filtered_spectrum['energy'] = energy
            self.filtered_spectrum['initial spectrum'] = fluence_i
            self.filtered_spectrum['final spectrum'] = fluence_f
            self.filtered_spectrum['absorbed spectrum'] = fluence_i - fluence_f
            self.filtered_spectrum['mean energy absorbed'] = np.sum(
                self.filtered_spectrum['absorbed spectrum']*self.filtered_spectrum['energy'])/np.sum(self.filtered_spectrum['absorbed spectrum'])
            self.filtered_spectrum['total fluence absorbed'] = np.sum(
                self.filtered_spectrum['absorbed spectrum'])
            self.filtered_spectrum['material'] = layer['material']
            self.filtered_spectrum['thickness'] = layer['thickness']
            self.filtered_spectrum['density'] = layer['density']

        def filter_spectrum(self, spectrum, material, thickness, density):
            '''
            This function filters a given polyenergetic spectrum by a given layer.
            spectrum: spekpy spectrum object
            material: string
            thickness: float
            density: float
            '''
            # if the materials are a list
            if type(material) == list:
                # filter the spectrum through each material
                for mat, thick, dens in zip(material, thickness, density):
                    if density == 1:
                        spectrum.filter(mat, thick)
                    else:
                        spectrum.filter(mat, thick)
            # if the materials are not a list
            else:
                # filter the spectrum through the material
                if density == 1:
                    spectrum.filter(material, thickness)
                else:
                    spectrum.filter(material, thickness)

        def plot_initial_spectrum(self, axis, norm=False, log=False):
            '''
            This function plots the initial spectrum.
            axis: matplotlib axis object
            norm: boolean
            Whether or not to normalize the spectrum
            log: boolean
            Whether or not to plot the spectrum on a log scale
            '''
            # This function plots the filtered spectrum.
            # Print the total fluence absorded by the layer in scientific notation
            if log:
                if norm:
                    axis.semilogy(self.filtered_spectrum['energy'],
                                  self.filtered_spectrum['initial spectrum']/np.sum(
                                      self.filtered_spectrum['initial spectrum']),
                                  label=self.filtered_spectrum['material'] + ' ' + f"{self.filtered_spectrum['total fluence absorbed']:.{2}e}" + ' $cm^{-2}$')
                else:
                    axis.semilogy(self.filtered_spectrum['energy'],
                                  self.filtered_spectrum['initial spectrum']+1,
                                  label=self.filtered_spectrum['material'] + ' ' + f"{self.filtered_spectrum['total fluence absorbed']:.{2}e}" + ' $cm^{-2}$')
            else:
                if norm:
                    axis.plot(self.filtered_spectrum['energy'],
                              self.filtered_spectrum['initial spectrum']/np.sum(
                                  self.filtered_spectrum['initial spectrum']),
                              label=self.filtered_spectrum['material'] + ' ' + f"{self.filtered_spectrum['total fluence absorbed']:.{2}e}" + ' $cm^{-2}$')
                else:
                    axis.plot(self.filtered_spectrum['energy'],
                              self.filtered_spectrum['initial spectrum'],
                              label=self.filtered_spectrum['material'] + ' ' + f"{self.filtered_spectrum['total fluence absorbed']:.{2}e}" + ' $cm^{-2}$')

        def plot_final_spectrum(self, axis, norm=False, log=False):
            '''
            This function plots the final spectrum.
            axis: matplotlib axis object
            '''
            # This function plots the filtered spectrum.
            if log:
                if norm:
                    axis.semilogy(self.filtered_spectrum['energy'],
                                  self.filtered_spectrum['final spectrum']/np.sum(
                                      self.filtered_spectrum['final spectrum']),
                                  label=self.filtered_spectrum['material'])
                else:
                    axis.semilogy(self.filtered_spectrum['energy'],
                                  self.filtered_spectrum['final spectrum']+1,
                                  label=self.filtered_spectrum['material'])
            else:
                if norm:
                    axis.plot(self.filtered_spectrum['energy'],
                              self.filtered_spectrum['final spectrum']/np.sum(
                                  self.filtered_spectrum['final spectrum']),
                              label=self.filtered_spectrum['material'])
                else:
                    axis.plot(self.filtered_spectrum['energy'],
                              self.filtered_spectrum['final spectrum'],
                              label=self.filtered_spectrum['material'])

        def plot_absorbed_spectrum(self, axis, norm=False, log=False):
            '''
            This function plots the absorbed spectrum.
            axis: matplotlib axis object
            norm: boolean
            Whether or not to normalize the spectrum
            log: boolean
            Whether or not to plot the spectrum on a log scale
            '''
            # This function plots the filtered spectrum.
            if log:
                if norm:
                    axis.semilogy(self.filtered_spectrum['energy'],
                                  self.filtered_spectrum['absorbed spectrum']/np.sum(
                                      self.filtered_spectrum['absorbed spectrum']),
                                  label=self.filtered_spectrum['material'] + ' ' + str(round(self.filtered_spectrum['mean energy absorbed'], 1)) + ' keV')
                else:
                    # add the mean absorbed energy to the plot label up to 1 decimal place
                    axis.semilogy(self.filtered_spectrum['energy'],
                                  self.filtered_spectrum['absorbed spectrum']+1,
                                  label=self.filtered_spectrum['material'] + ' ' + str(round(self.filtered_spectrum['mean energy absorbed'], 1)) + ' keV')
            else:
                if norm:
                    axis.plot(self.filtered_spectrum['energy'],
                              self.filtered_spectrum['absorbed spectrum']/np.sum(
                                  self.filtered_spectrum['absorbed spectrum']),
                              label=self.filtered_spectrum['material'] + ' ' + str(round(self.filtered_spectrum['mean energy absorbed'], 1)) + ' keV')
                else:
                    # add the mean absorbed energy to the plot label up to 1 decimal place
                    axis.plot(self.filtered_spectrum['energy'],
                              self.filtered_spectrum['absorbed spectrum']+1,
                              label=self.filtered_spectrum['material'] + ' ' + str(round(self.filtered_spectrum['mean energy absorbed'], 1)) + ' keV')

        def plot_all_spectrum(self, axis):
            '''
            This function plots the initial, final, and absorbed spectrum.
            axis: matplotlib axis object
            '''
            # This function plots the filtered spectrum.
            axis.plot(self.filtered_spectrum['energy'],
                      self.filtered_spectrum['initial spectrum'],
                      label='spectrum before' + self.filtered_spectrum['material'])
            axis.plot(self.filtered_spectrum['energy'],
                      self.filtered_spectrum['final spectrum'],
                      label='spectrum after' + self.filtered_spectrum['material'])
            axis.plot(self.filtered_spectrum['energy'],
                      self.filtered_spectrum['absorbed spectrum'],
                      label='spectrum absorbed by' + self.filtered_spectrum['material'])
            # axis.set_xlabel('Energy [keV]')
            axis.set_ylabel('Fluence $[cm^{-1} keV^{-2}]$')
            axis.set_title('Filtered spectra')
            axis.legend()

        def plot_attenuation(self, axis):
            '''
            This function plots the attenuation coefficient for the layer.
            axis: matplotlib axis object
            '''

            atten = self.spectrum.mu_data.get_mu_t(self.filtered_spectrum['material'],
                                                   np.logspace(1, 3, 2000), 1)
            axis.loglog(np.logspace(1, 3, 2000), atten,
                        label=self.filtered_spectrum['material'])

        def get_HU_value(self, material, water_padding=1, thickness=1, mu=False):
            '''
            This function calculates the weighted attenuation coefficient for the layer.
            material: string
            water_padding: float
            The amount of water padding to add to the layer that is removed during imaging
            thickness: float
            The thickness of the layer
            '''
            # Get the attenuation coefficients for the material and water
            mu_t_material = self.spectrum.mu_data.get_mu_t(
                material, self.filtered_spectrum['energy'], thickness)
            mu_t_self = self.spectrum.mu_data.get_mu_t(
                self.filtered_spectrum['material'], self.filtered_spectrum['energy'], self.filtered_spectrum['thickness'])
            mu_t_padding = self.spectrum.mu_data.get_mu_t(
                'Water', self.filtered_spectrum['energy'], water_padding+thickness)
            # Exponentially attenuate the spectrum
            spec_test = self.filtered_spectrum['initial spectrum'] * \
                np.exp(-mu_t_material)
            # Expenentially attenuate by some water as well
            if not mu:
                spec_test = spec_test*np.exp(-mu_t_padding)
            # The amount of the spectrum that is attenuated by the material
            final_signal = spec_test - spec_test*np.exp(-mu_t_self)
            # Estimate the attenuation coefficient of the material
            mu_material = -np.log(np.sum(final_signal)/np.sum(
                self.filtered_spectrum['absorbed spectrum']))/(thickness)
            # calculate the attenuation coefficient of water
            spec_water = self.filtered_spectrum['initial spectrum'] * \
                np.exp(-mu_t_padding)
            final_signal_water = spec_water - spec_water*np.exp(-mu_t_self)
            mu_water = -np.log(np.sum(final_signal_water) /
                               np.sum(self.filtered_spectrum['absorbed spectrum']))/(thickness)
            if mu:
                return mu_material
            else:
                return 1000*(mu_material - mu_water)/mu_water

    def filter_spectrum_through_detector(self, spectrum):
        '''
        This function filters a given polyenergetic spectrum through each layer of the detector
        '''
        self.spectra = []

        for layer in self.layers:
            self.spectra.append(self.filtered_spectrum(spectrum, layer.layer))

    def plot_initial_spectra(self, axis, norm=False, spectras=None, log=False, legend=True):
        '''
        This function plots the filtered spectra.
        axis: matplotlib axis object
        '''
        if spectras == None:
            spectra = self.spectra
        else:
            spectra = [self.spectra[i] for i in spectras]
        for spectrum in spectra:
            spectrum.plot_initial_spectrum(axis, norm=norm, log=log)
        axis.set_xlabel('Energy [keV]')
        if norm:
            axis.set_ylabel('Normalized Fluence')
        else:
            axis.set_ylabel('Fluence $[cm^{-1} keV^{-2}]$')
        axis.set_title('Incident Spectra')
        if legend:
            axis.legend()

    def plot_final_spectra(self, axis, norm=False, spectras=None, log=False, legend=True):
        '''
        This function plots the filtered spectra.
        axis: matplotlib axis object
        '''
        if spectras == None:
            spectra = self.spectra
        else:
            spectra = [self.spectra[i] for i in spectras]
        for spectrum in spectra:
            spectrum.plot_final_spectrum(axis, norm=norm, log=log)
        axis.set_xlabel('Energy [keV]')
        if norm:
            axis.set_ylabel('Normalized Fluence')
        else:
            axis.set_ylabel('Fluence $[cm^{-1} keV^{-2}]$')
        axis.set_title('Final Spectra')
        if legend:
            axis.legend()

    def plot_absorbed_spectra(self, axis, norm=False, spectras=None, log=False, legend=True):
        '''
        This function plots the filtered spectra.
        axis: matplotlib axis object
        '''
        if spectras == None:
            spectra = self.spectra
        else:
            spectra = [self.spectra[i] for i in spectras]

        for spectrum in spectra:
            spectrum.plot_absorbed_spectrum(axis, norm=norm, log=log)

        # axis.set_xlabel('Energy [keV]')
        if norm:
            axis.set_ylabel('Normalized Fluence')
        else:
            axis.set_ylabel('Fluence $[cm^{-1} keV^{-2}]$')
        axis.set_title('Absorbed Spectra')
        if legend:
            axis.legend()

    def plot_detector(self, axis, colors=None):
        '''
        This function plots the detector.
        axis: matplotlib axis object
        '''
        for layer, color in zip(self.layers, custom_colors if colors == None else colors):
            layer.plot_layer(axis, color)
        axis.set_ylabel('Thickness [cm]')
        axis.set_xticks([])
        axis.set_ylim(-layer.layer['total_thickness'], 0)

    def plot_attenuation(self, axis):
        '''
        This function plots the attenuation coefficient for the detector.
        axis: matplotlib axis object
        '''
        for spectrum in self.spectra:
            spectrum.plot_attenuation(axis)
        axis.set_xlabel('Energy [keV]')
        axis.set_ylabel('Attenuation Coefficient [cm$^2$/g]')
        axis.set_title('Attenuation Coefficient')
        axis.legend()

    def get_HU_values(self, material, thickness=1, water_padding=1, mu=False):
        '''
        This function calculates the weighted attenuation coefficient for the detector.
        materials: list of strings
        '''
        HU_values = []
        for spectrum in self.spectra:
            HU_values.append(spectrum.get_HU_value(
                material, thickness=thickness, water_padding=water_padding, mu=mu))

        return HU_values

    def plot_HU_values(self, axis, material, thickness=1, water_padding=1, spectras=None, mu=True):
        '''
        This function plots the HU values of a given material for each spectra
        axis: matplotlib axis object
        '''
        HU_values = self.get_HU_values(material, thickness=thickness,
                                       water_padding=water_padding, mu=mu)
        # select which spectra to plot
        if spectras == None:
            HU_plots = HU_values
        else:
            HU_plots = [HU_values[i] for i in spectras]
        axis.bar(np.arange(len(HU_plots)), HU_plots)
        # axis.set_xlabel('Layer')
        if mu:
            axis.set_ylabel('Attenuation Coefficient')
            axis.set_title('Attenuation Coefficient est. '+material)
        else:
            axis.set_ylabel('HU value')
            axis.set_title('HU values est. '+material)
        # Set the xticks to the label materials in spectra
        axis.set_xticks(np.arange(len(spectras)))
        # set the xticks but truncate at 4 characters
        axis.set_xticklabels(
            [self.spectra[ii].filtered_spectrum['material'][:4] for ii in spectras])
        # axis.set_ylim(-500,1000)
