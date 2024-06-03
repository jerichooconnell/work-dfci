# Could you make a gui out of this script that allows you to add layers to the detector and then filter a given spectrum through the detector and plot the results?

import spekpy as sp
from matplotlib.widgets import Button, TextBox, CheckButtons
from copy import deepcopy as __deepcopy__
from detector_class import Detector
import matplotlib.pyplot as plt


class Detector_GUI(object):
    '''
    This class is a gui for the detector class.
    '''

    def __init__(self, spectrum, detector=None):
        '''
        This function initializes the gui.
        '''
        # Initialize the detector.
        if detector == None:
            self.detector = Detector()
        else:
            self.detector = detector

        self.spectrum = spectrum
        # make a deep copy of the spectrum
        self.spectrum2 = __deepcopy__(spectrum)
        # Initialize the gui.
        self.gui = self.initialize_gui_lower()
        self.update_radio_buttons()

        if self.detector.layers != []:
            self.plot_detector()
            self.filter_spectrum()
            self.plot_spectra()
            self.plot_HU()
        # Update radio buttons
        # plt.tight_layout()
        plt.show()

    def initialize_gui_lower(self):
        # this function initializes the gui with all boxes 0.05 lower
        # Initialize the gui.
        gui = {}
        # Initialize the gui window.
        gui['window'] = plt.figure(figsize=(15, 10))
        # Initialize the gui axes.
        gui['axes'] = {}
        lower = 0.02
        left = 0.05
        self.lower = lower
        self.left = left
        gui['axes']['detector'] = gui['window'].add_subplot(2, 3, 1)
        gui['axes']['Absorbed Spectrum'] = gui['window'].add_subplot(2, 3, 2)
        gui['axes']['Attenuation Coefficient'] = gui['window'].add_subplot(
            2, 3, 4)
        gui['axes']['Initial Spectrum'] = gui['window'].add_subplot(2, 3, 5)
        # Add another axis for the HU plot
        gui['axes']['HU'] = gui['window'].add_subplot(3, 3, 3)
        # Initialize the gui buttons.
        gui['buttons'] = {}
        gui['buttons']['Add Layer'] = plt.axes(
            [0.7-left, 0.05-lower, 0.1, 0.075])
        gui['buttons']['Filter Spectrum'] = plt.axes(
            [0.81-left, 0.05-lower, 0.1, 0.075])
        # Initialize the gui text boxes put them in the top right corner.
        gui['text boxes'] = {}
        gui['text boxes']['Material'] = plt.axes(
            [0.7-left, 0.55-lower, 0.1, 0.075])
        gui['text boxes']['Thickness'] = plt.axes(
            [0.81-left, 0.55-lower, 0.1, 0.075])
        # # Initialize the gui text also in the top right corner.
        gui['text'] = {}
        gui['text']['Material'] = plt.axes([0.7-left, 0.59-lower, 0.01, 0.075])
        gui['text']['Thickness'] = plt.axes(
            [0.81-left, 0.59-lower, 0.01, 0.075])

        # Turn off the axes for the text
        for ax in gui['text'].values():
            ax.axis('off')
        # Initialize the gui text.
        gui['text']['Material'].text(0.5, 0.5, 'Material')
        gui['text']['Thickness'].text(0.5, 0.5, 'Thickness')
        # Initialize the gui text boxes.
        gui['text boxes']['Material'] = TextBox(
            gui['text boxes']['Material'], '')
        gui['text boxes']['Thickness'] = TextBox(
            gui['text boxes']['Thickness'], '')
        # Add a text box to specify water padding
        gui['text boxes']['Water Padding'] = plt.axes(
            [0.92-left, 0.55-lower, 0.1, 0.075])
        gui['text boxes']['Water Padding'] = TextBox(
            gui['text boxes']['Water Padding'], '')
        # Add a text box to specify the kVp of the spectrum
        gui['text boxes']['kVp'] = plt.axes(
            [0.92-left, 0.35-lower, 0.1, 0.075])
        gui['text boxes']['kVp'] = TextBox(gui['text boxes']['kVp'], '')
        # Add text to the text box
        gui['text']['kVp'] = plt.axes(
            [0.92-left, 0.39-lower, 0.01, 0.075])
        gui['text']['kVp'].axis('off')
        gui['text']['kVp'].text(0.5, 0.5, 'kVp')
        # Make a button that updates the kVp of the spectrum
        gui['buttons']['Change kVp'] = plt.axes(
            [0.92-left, 0.25-lower, 0.1, 0.075])
        gui['buttons']['Change kVp'] = Button(
            gui['buttons']['Change kVp'], 'Change kVp')
        # gui['text boxes']['kVp'].text = str(self.spectrum.state.model_parameters.kvp)
        # Add text to the text box
        gui['text']['Water Padding'] = plt.axes(
            [0.92-left, 0.59-lower, 0.01, 0.075])
        gui['text']['Water Padding'].axis('off')
        gui['text']['Water Padding'].text(0.5, 0.5, 'Water Padding')
        # Initialize the gui buttons.
        gui['buttons']['Add Layer'] = Button(
            gui['buttons']['Add Layer'], 'Add Layer')
        gui['buttons']['Filter Spectrum'] = Button(
            gui['buttons']['Filter Spectrum'], 'Update Spectrum')
        # Initialize the gui callbacks.
        gui['callbacks'] = {}
        gui['callbacks']['Change kVp'] = gui['buttons']['Change kVp'].on_clicked(
            self.change_spectra)
        gui['callbacks']['Add Layer'] = gui['buttons']['Add Layer'].on_clicked(
            self.add_layer)
        gui['callbacks']['Filter Spectrum'] = gui['buttons']['Filter Spectrum'].on_clicked(
            self.filter_spectrum)
        # Add a remove one layer button
        gui['buttons']['Remove Layer'] = plt.axes(
            [0.7-left, 0.15-lower, 0.1, 0.075])
        gui['buttons']['Remove Layer'] = Button(
            gui['buttons']['Remove Layer'], 'Remove Layer')
        gui['callbacks']['Remove Layer'] = gui['buttons']['Remove Layer'].on_clicked(
            self.remove_layer)
        # Add a radio button that allows you to normalize the spectra
        gui['radio buttons'] = {}
        gui['radio buttons']['Normalize'] = plt.axes(
            [0.7-left, 0.25-lower, 0.1, 0.075])
        gui['radio buttons']['Normalize'] = CheckButtons(
            gui['radio buttons']['Normalize'], ['Normalize'])
        gui['radio buttons']['Normalize'].on_clicked(self.plot_spectra)
        # Add a radio button that allows you to plot a log of the spectrum
        gui['radio buttons']['Log'] = plt.axes(
            [0.81-left, 0.25-lower, 0.1, 0.075])
        gui['radio buttons']['Log'] = CheckButtons(
            gui['radio buttons']['Log'], ['Log'])

        gui['radio buttons']['Log'].on_clicked(self.plot_spectra)
        # Add a radio button that allows you to toggle the legend
        gui['buttons']['Toggle Legend'] = plt.axes(
            [0.81-left, 0.45-lower, 0.1, 0.075])
        gui['buttons']['Toggle Legend'] = CheckButtons(
            gui['buttons']['Toggle Legend'], ['Legend'])
        gui['buttons']['Toggle Legend'].on_clicked(self.plot_spectra)
        # Add a button to change a layer
        gui['buttons']['Change Layer'] = plt.axes(
            [0.81-left, 0.15-lower, 0.055, 0.075])
        gui['buttons']['Change Layer'] = Button(
            gui['buttons']['Change Layer'], 'Change Layer')
        gui['callbacks']['Change Layer'] = gui['buttons']['Change Layer'].on_clicked(
            self.change_layer)
        # Add a text box to select which layer to change
        gui['text boxes']['Layer'] = plt.axes(
            [0.81-left, 0.35-lower, 0.1, 0.075])
        gui['text boxes']['Layer'] = TextBox(gui['text boxes']['Layer'], '')
        # Add text to the text box
        gui['text']['Layer'] = plt.axes(
            [0.81-left, 0.39-lower, 0.01, 0.075])
        gui['text']['Layer'].axis('off')
        gui['text']['Layer'].text(0.5, 0.5, 'Layer to change')
        # Add a button to plot HU values
        gui['buttons']['HU'] = plt.axes(
            [0.87-left, 0.15-lower, 0.04, 0.075])
        gui['buttons']['HU'] = Button(gui['buttons']['HU'], 'Plot $\mu$')
        gui['callbacks']['HU'] = gui['buttons']['HU'].on_clicked(
            self.plot_HU)
        # Add a radio button to toggle HU plot to mu and back
        gui['radio buttons']['mu'] = plt.axes(
            [0.87-left, 0.25-lower, 0.04, 0.075])
        gui['radio buttons']['mu'] = CheckButtons(
            gui['radio buttons']['mu'], ['HU'])
        gui['radio buttons']['mu'].on_clicked(self.plot_HU)
        # Add an info radio button that displays a blurb about the program
        gui['radio buttons']['Info'] = plt.axes(
            [0.95-left, 0.1-lower, 0.04, 0.04])
        gui['radio buttons']['Info'] = CheckButtons(
            gui['radio buttons']['Info'], ['Info'])
        gui['radio buttons']['Info'].on_clicked(self.show_info)
        gui['text']['Info'] = plt.axes(
            [0.1-self.left, 0.3-self.lower, 0.4, 0.4])
        gui['text']['Info'].axis('off')

        return gui

    def show_info(self, event):
        '''
        This function displays a blurb about the program in a text
        '''
        # Clear the axes
        self.gui['text']['Info'].clear()
        # Check if the info button is checked
        if self.gui['radio buttons']['Info'].get_status()[0]:
            # Turn off the x and y labels
            self.gui['text']['Info'].set_xticks([])
            self.gui['text']['Info'].set_yticks([])
            self.gui['text']['Info'].text(0.1, 0.1, '''
    Add Layer: Add a layer to the detector,
    Filter Spectrum: Filter the spectrum through the detector (updates plots),
    Remove Layer: Remove the last layer from the detector,
    Change Layer: Change a layer in the detector using 
                  material and thickness in text boxes,
    Plot $\mu$: Plot the estimated $\mu$ values for each layer 
              ~ log(E/E_0) with E being the total energy absorbed in the layer after filtration
              by the material in the text boxes and E_0 being the 
              total energy absorbed without filtration by the material in the text boxes
              or water padding HU toggle (tries to) plot HU values instead of $\mu$ values,
    Change kVp: Change the kVp of the spectrum using the value in the kVp box,
    Toggle Legend: Toggle the legend on the spectra plots,
    Normalize: Normalize the spectra,
    Log: Plot the spectra on a log scale,
    Layer: Select which layer to change,
    Material: Enter the material of the layer to add or change,
    Thickness: Enter the thickness of the layer to add or change,
    Water Padding: Enter the thickness of water padding to add when calculating HU values,
    kVp: Enter the kVp of the spectrum,''')
        else:
            self.gui['text']['Info'].axis('off')
            self.gui['text']['Info'].text(0.5, 0.5, '')
        # Show the changes
        self.gui['window'].canvas.draw()

    def plot_HU(self, event=None):
        '''
        This function plots the HU values for each layer.
        '''
        # Plot the spectra first
        self.plot_spectra()
        # Clear the HU axes
        self.gui['axes']['HU'].clear()
        # Get the material from the material text box

        material = self.gui['text boxes']['Material'].text

        if material == '':
            print('Material empty')
            material = 'Ca'
        # Make it so that this is the opposite of the radio button
        mu = not self.gui['radio buttons']['mu'].get_status()[0]
        # Also pass in which specttra to plot
        spectras_bool = self.gui['radio buttons']['Layers'].get_status()
        # convert the spectras bool to a list of integers
        spectras = [i for i in range(len(spectras_bool)) if spectras_bool[i]]
        # Get the thickness
        try:
            thickness = float(self.gui['text boxes']['Thickness'].text)
        except:
            print('Thickness not a number')
            thickness = 1
        try:
            water_padding = float(self.gui['text boxes']['Water Padding'].text)
        except:
            print('Water padding not a number')
            water_padding = 0
        # Plot the HU values
        self.detector.plot_HU_values(self.gui['axes']['HU'],
                                     material, thickness=thickness,
                                     water_padding=water_padding, mu=mu,
                                     spectras=spectras)
        # Redraw the plot.
        self.gui['window'].canvas.draw()

    def remove_layer(self, event):
        '''
        This function removes the last layer from the detector.
        '''
        # Remove the last layer from the detector.
        self.detector.layers = self.detector.layers[:-1]
        # Plot the detector.
        self.plot_detector()
        self.update_radio_buttons()
        # Clear the text boxes.
        # self.clear_text_boxes()
        # Clear the spectra.
        self.plot_spectra()

    def change_layer(self, event):
        '''
        This function changes a layer in the detector.
        '''
        # Get the layer to change
        layer = int(self.gui['text boxes']['Layer'].text)
        # Get the material, thickness, and density.
        self.detector.materials[layer] = self.gui['text boxes']['Material'].text
        self.detector.thicknesses[layer] = float(
            self.gui['text boxes']['Thickness'].text)
        # self.detector.densities[layer] = float(
        #     self.gui['text boxes']['Density'].text)
        # Change the layer in the detector.
        self.detector.reinitialize_detector()
        # Plot the detector.
        self.plot_detector()
        self.update_radio_buttons()
        # Clear the text boxes.
        # self.clear_text_boxes()
        # Clear the spectra.
        self.plot_spectra()

    def update_radio_buttons(self):
        # Include a radio button to toggle each layer on and off for plotting
        self.gui['radio buttons']['Layers'] = plt.axes(
            [0.70-self.left, 0.355-self.lower, 0.1, 0.17])
        self.gui['radio buttons']['Layers'] = CheckButtons(self.gui['radio buttons']['Layers'], [
                                                           f'({i})' + self.detector.layers[i].layer['material'][:12] for i in range(len(self.detector.layers))])
        # Make the chekcboxes all checked
        for i in range(len(self.detector.layers)):
            self.gui['radio buttons']['Layers'].set_active(i)
        # self.gui['radio buttons']['Layers'].on_clicked(self.plot_spectra)

    def add_layer(self, event):
        '''
        This function adds a layer to the detector.
        '''
        # Get the material, thickness, and density.
        material = self.gui['text boxes']['Material'].text
        thickness = float(self.gui['text boxes']['Thickness'].text)
        # density = float(self.gui['text boxes']['Density'].text)
        # Add the layer to the detector.
        self.detector.add_layers([material], [thickness])
        # Plot the detector.
        self.plot_detector()
        self.update_radio_buttons()
        # Clear the text boxes.
        # self.clear_text_boxes()
        # update radio buttons
        # self.update_radio_buttons()
        self.plot_spectra()

    def filter_spectrum(self, event=None):
        '''
        This function filters a given spectrum through the detector.
        '''
        self.spectrum = __deepcopy__(self.spectrum2)
        # Filter the spectrum through the detector.
        self.detector.filter_spectrum_through_detector(self.spectrum)
        # Put the mean energy and total fluence absorbed for each layer in the text boxes
        # for i in range(len(self.detector.spectra)):
        #     self.gui['text boxes']['Mean Energy'].text = str(self.detector.spectra[i].filtered_spectrum['mean energy absorbed'])
        #     self.gui['text boxes']['Total Fluence'].text = str(self.detector.spectra[i].filtered_spectrum['total fluence absorbed'])
        # Plot the spectra.
        self.plot_spectra()

    def plot_detector(self):
        '''
        This function plots the detector.
        '''
        # Clear the axes.
        for ax in self.gui['axes'].values():
            ax.clear()
        # Plot the detector.
        self.detector.plot_detector(self.gui['axes']['detector'])
        # Redraw the plot.
        self.gui['window'].canvas.draw()

    def plot_spectra(self, event=None):
        '''
        This function plots the spectra.
        '''
        # Clear the spectra axes
        for ax in [self.gui['axes']['Absorbed Spectrum'], self.gui['axes']['Attenuation Coefficient'], self.gui['axes']['Initial Spectrum']]:
            ax.clear()
        # Get radio button output for plotting spectra
        spectra = self.gui['radio buttons']['Layers'].get_status()
        # turn the radio button output into a list of integers
        spectra = [i for i in range(len(spectra)) if spectra[i]]
        # Check if you should normalize the spectra
        # Check if you should plot the spectra on a log scale
        logy = self.gui['radio buttons']['Log'].get_status()[0]
        norm = self.gui['radio buttons']['Normalize'].get_status()[0]
        legend = self.gui['buttons']['Toggle Legend'].get_status()[0]
        self.detector.plot_absorbed_spectra(
            self.gui['axes']['Absorbed Spectrum'], norm=norm, spectras=spectra, log=logy, legend=legend)
        self.detector.plot_initial_spectra(
            self.gui['axes']['Initial Spectrum'], norm=norm, spectras=spectra, log=logy, legend=legend)

        # Plot the attenuation coefficient.
        self.detector.plot_attenuation(
            self.gui['axes']['Attenuation Coefficient'])

        # Redraw the plot.
        self.gui['window'].canvas.draw()
        # Update radio buttons
        # self.update_radio_buttons()

    def clear_text_boxes(self):
        '''
        This function clears the text boxes.
        '''
        # Clear the text boxes.
        self.gui['text boxes']['Material'].text = ''
        self.gui['text boxes']['Thickness'].text = ''
        self.gui['text boxes']['Density'].text = ''

    def clear_detector(self):
        '''
        This function clears the detector.
        '''
        # Clear the detector.
        self.detector = Detector()
        # Plot the detector.
        self.plot_detector()

        # Clear the spectra.
        self.plot_spectra()

    def clear_spectra(self):
        '''
        This function clears the spectra.
        '''
        # Clear the spectra.
        self.detector.spectra = []
        # Plot the spectra.
        self.plot_spectra()
        # Clear the text boxes.
        # self.clear_text_boxes()

    def change_spectra(self, event=None):
        '''
        This function changes the kVp of the spectra
        '''
        # Get the kVp.
        kvp = float(self.gui['text boxes']['kVp'].text)
        # Change the kVp.
        self.spectrum = sp.Spek(kvp=kvp, th=14)
        self.spectrum2 = __deepcopy__(self.spectrum)
        # Filter the spectrum through the detector.
        self.detector.filter_spectrum_through_detector(self.spectrum)
        # Plot the spectra.
        self.plot_spectra()


if __name__ == '__main__':
    materials = ['Al', 'Ti', 'Water', 'Cesium Iodide',
                 'Sn', 'Si', 'Perovskite', 'Si']
    densities = [None, None, 1, None, None, None, None, None]
    thicknesses = [1, 1, 1, 0.6, 0.1, 0.1, 0.6, 0.1]
    # colors = ['gray','darkgray','blue','red','whitesmoke','white','red','white']

    spectra = sp.Spek(kvp=140, th=14)

    # Create the detector
    detector = Detector()
    detector.add_layers(materials, thicknesses, densities=densities)
    # Initialize the gui.
    gui = Detector_GUI(spectra, detector=detector)
