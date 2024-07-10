# Import necessary libraries
import dash
import base64
import io

from dash import dcc, html, Input, Output, State
import plotly.graph_objs as go
import numpy as np
import SimpleITK as sitk
# Import other necessary modules (gecco, etc.)
# Read the mhd file from data
from gecco import patient_data
import gecco as fc
import numpy as np
from gecco.utils import nrrd_to_mhd
import nrrd

# Initialize Dash app
app = dash.Dash(__name__)

# Define app layout
app.layout = html.Div([
    dcc.Upload(id='upload-nrrd',
               children=html.Div(['Drag and Drop or ', html.A('Select Files')])),
    dcc.Slider(id='kvp-slider', min=60, max=140, value=100,
               marks={i: str(i) for i in range(60, 141, 10)}),
    dcc.Graph(id='plot-area')
])

# Callback for updating the plot based on the selected file and kVp


@app.callback(
    Output('plot-area', 'figure'),
    [Input('upload-nrrd', 'contents'), Input('kvp-slider', 'value')]
)
def update_plot(selected_file, selected_kvp):
    if selected_file is not None:
        content_type, content_string = selected_file.split(',')
        decoded = base64.b64decode(content_string)
        try:
            # Assuming the file is an NRRD file, you might need to adjust this for other file types
            nrrd_contents = io.BytesIO(decoded)
            print(nrrd_contents)
            data, header = nrrd.read(nrrd_contents)
            print(data.shape)
            # Now call your processing function
            fig = process_and_plot(
                nrrd_contents, selected_kvp)
            return fig
        except Exception as e:
            print(e)
            return go.Figure()  # Return an empty figure or some error message
    return go.Figure()

# Define a function to process the NRRD file and generate the plot


def process_and_plot(nrrd_contents, kvp):
    # Convert the contents to an NRRD file format
    # Use the gecco library and other necessary processing as in the original script
    # Return a plotly figure

    # '/media/jericho/T7/dfci_laptop_backup/Documents/christian_patient_data/BRAIN/2_Stereo_CNS_Scan.nrrd'
    nrrd_file = nrrd_contents
    phantom_rtis = patient_data.patient_phantom(nrrd_file, 1e7)

    spectrum = fc.calculate_spectrum_sp(100, 12)

    spectrum.filter('Be', 1.5)
    spectrum.filter('Al', 2.75)
    spectrum.filter('Ti', 0.89)

    # Detector filters
    spectrum.filter('Al', 3.7)
    spectrum.filter('C', 3.8*(2/1.7))  # Difference in density
    phantom_rtis.initialize_fastmc(1, spectrum)

    phantom_rtis.phantom = phantom_rtis.phantom[:, 60:, :]
    phantom_rtis.density = phantom_rtis.density[:, 60:, :]

    # insert a new axis to the phantom
    phantom_rtis.phantom = phantom_rtis.phantom[np.newaxis, ...]
    phantom_rtis.density = phantom_rtis.density[np.newaxis, ...]

    phantom_rtis.geomet.nVoxel = np.array([1, 452, 512])
    phantom_rtis.geomet.dVoxel = np.array([0.8, 0.8, 0.8])
    phantom_rtis.geomet.sVoxel = phantom_rtis.geomet.dVoxel * phantom_rtis.geomet.nVoxel

    phantom_rtis.geomet.nDetector = np.array([1, 512])
    phantom_rtis.geomet.dDetector = np.array(
        [phantom_rtis.geomet.dVoxel[0], 0.8])
    phantom_rtis.geomet.sDetector = phantom_rtis.geomet.dDetector * \
        phantom_rtis.geomet.nDetector

    phantom_rtis.geomet.mode = "parallel"

    # phantom_rtis.bowtie_file = '/home/jericho/Software/gecco/gecco/data/bowties/no_bowtie.dat'
    phantom_rtis.retain_partial_calcs = True
    phantom_rtis.run_gecco(1e10, 815, conv_on=False, filter_on=False)

    phantom_rtis.reweight(100, scat=0.05, mAs=400)

    img = phantom_rtis.img.squeeze()
    water = np.mean(img[236:250, 285:300])
    air = np.mean(img[120:180, 60:140])
    # convert to HU using the water calibration
    img = (img - water)/(water - air) * 1000

    # Plot the image using plotly
    fig = go.Figure()
    fig.add_trace(go.Heatmap(z=img, colorscale='gray'))
    fig.update_layout(title=f'kVp: {kvp}', xaxis_title='X', yaxis_title='Y')

    return fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
