import base64
import dash
from dash import dcc, html, Input, Output, State
import io
import nrrd
import numpy as np
import tempfile
import plotly.graph_objs as go
import flask_caching


from gecco.utils import write_run_all_script, write_python_script_head
import os

import mpl_interactions as pli
from gecco import patient_data
import gecco as fc
import numpy as np
from gecco.utils import nrrd_to_mhd, cropping_tool

# Initialize Dash app
app = dash.Dash(__name__)

cache = flask_caching.Cache(app.server, config={
    'CACHE_TYPE': 'simple',  # Use 'redis' or 'filesystem' for multi-user apps
})

# Define app layout
app.layout = html.Div([
    html.Div([
        html.Img(src='/assets/gecco_logo.png',
                 style={'height': '50px', 'width': 'auto', 'margin-right': '10px'}),
        html.H1('GECCO Real Time Image Simulator', style={
                'font-family': 'Roboto, sans-serif', 'font-weight': '700', 'display': 'inline-block'})
    ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center', 'margin-bottom': '20px'}),
    html.Div([
        html.Div([
            dcc.Upload(
                id='upload-image',
                children=html.Div(
                    ['Upload Image: Drag and Drop or ', html.A('Select Files')]),
                style={'width': '100%', 'height': '60px', 'lineHeight': '60px', 'borderWidth': '1px',
                       'borderStyle': 'dashed', 'borderRadius': '5px', 'textAlign': 'center', 'margin': '10px', 'borderColor': 'blue', 'margin-bottom': '20px'},
                multiple=False,
            ),
        ], style={'display': 'flex', 'width': '100%', 'align-items': 'center', 'justify-content': 'center'}),
        html.Div([
            html.H3('Image Preprocessing Controls',
                    title='Adjust the settings to process the uploaded image'),
            html.Div([
                html.Label(
                    'Slice Slider', title='Slide to select the slice of the image to display'),
                dcc.Slider(id='slice-slider', min=0, max=200, step=1,
                           value=50, marks={i: str(i) for i in range(0, 200, 50)}),
            ], title='Adjust the slider to select the image slice you want to view'),
            html.Div([
                html.Label('Crop Y-Axis',
                           title='Adjust to crop the image on the X-axis'),
                dcc.RangeSlider(id='crop-slider-x', min=0, max=512, step=1,
                                value=[0, 512], marks={i: str(i) for i in range(0, 513, 50)}),
            ], title='Use this slider to crop the image horizontally'),
            html.Div([
                html.Label('Crop X-Axis',
                           title='Adjust to crop the image on the Y-axis'),
                dcc.RangeSlider(id='crop-slider-y', min=0, max=512, step=1,
                                value=[0, 512], marks={i: str(i) for i in range(0, 513, 50)}),
            ], title='Use this slider to crop the image vertically'),
            html.Div([
                html.Label('Transpose Image:',
                           title='Select how to transpose the image'),
                dcc.RadioItems(id='transpose-options', options=[{'label': 'None', 'value': 'no_transpose'}, {'label': 'XY', 'value': 'transpose_xy'}, {
                               'label': 'YZ', 'value': 'transpose_yz'}, {'label': 'XZ', 'value': 'transpose_xz'}], value='no_transpose', labelStyle={'display': 'inline-block'}),
            ], title='Select the transpose option for the image, should plot axially', style={'display': 'flex'}),

        ], style={'width': '40%', 'display': 'inline-block', 'margin-left': '10px', 'margin-right': 'auto'}, title='Use these controls to adjust how the image is processed'),
        html.Div([
            html.H3('Simulation Settings',
                    title='Adjust the settings for the simulation'),
            html.Div([
                html.Label('Peak Tube Voltage (kV)',
                           title='Adjust the simulated tube kVp for the simulation'),
                dcc.Slider(id='kvp-slider', min=60, max=140, step=1,
                           value=80, marks={i: str(i) for i in range(60, 140, 20)}),
            ], title='Adjust the brightness of the image'),
            html.Div([
                html.Label('Tube Current (mAs)',
                           title='Adjust the tube current of the simulation'),
                dcc.Slider(id='mas-slider', min=100, max=1000, step=1,
                           value=1000, marks={i: str(i) for i in range(100, 1000, 300)}),
            ], title='Adjust the contrast of the image'),
            html.Div([
                html.Label('Scatter Fraction (%)',
                           title='Adjust the amount of scatter in the scatter approximation'),
                dcc.Slider(id='scatter-slider', min=0, max=20, step=1,
                           value=0, marks={i: str(i) for i in range(0, 20, 5)}),
            ], title='Adjust the simulation settings for scatter fraction'),
            html.Div([
                html.Label('Bowtie Filter:',
                           title='Select additional image processing options'),
                dcc.RadioItems(id='bowtie-buttons', options=[{'label': 'Full-Fan', 'value': 'full_fan'}, {
                               'label': 'Half-Fan', 'value': 'half_fan'}, {'label': 'None', 'value': 'no_fan'}], value='full_fan', labelStyle={'display': 'inline-block'}),

            ], title='Select additional image processing options', style={'display': 'flex'}),

        ], style={'width': '40%', 'display': 'inline-block', 'margin-left': 'auto', 'margin-right': 'auto', 'margin-bottom': '20px'}, title='Additional image processing controls'),
        html.Div([
            html.Button('Initialize Simulation',
                        id='apply-modifications-btn', n_clicks=0,
                        style={
                            'height': '50px',
                            'width': '200px',
                            'font-size': '20px',
                            'background-color': '#6686e8',  # Bootstrap primary button color
                            'color': 'white',  # Text color
                            'border': 'none',
                            'border-radius': '5px',  # Rounded corners
                            'cursor': 'pointer',  # Cursor changes to pointer on hover
                            'transition': 'background-color 0.3s'  # Smooth transition for hover effect
                        }),
        ]),  # Center the button in its div
        html.Div([
            html.H3('Image Outputs',
                    title='View the original and modified images here'),
            html.Div(id='output-image', style={'width': '50%',
                     'display': 'inline-block'}, title='Original image output'),
            html.Div(id='output-image-modified', style={
                     'width': '50%', 'display': 'inline-block'}, title='Modified image output'),
        ], title='This section displays the original and processed images'),
        html.Div([
            html.H3('Image Windowing Controls',
                    title='Adjust the window and level of the image'),
            html.Div([
                html.Label('Window Width',
                           title='Adjust the window width of the image'),
                dcc.Slider(id='window-slider', min=1, max=1000, step=1,
                           value=400, marks={i: str(i) for i in range(1, 1000, 200)}),
            ], title='Adjust the window width of the image'),
            html.Div([
                html.Label('Window Level',
                           title='Adjust the window level of the image'),
                dcc.Slider(id='level-slider', min=-1000, max=1000, step=1,
                           value=0, marks={i: str(i) for i in range(-1000, 1000, 500)}),
            ], title='Adjust the window level of the image'),
        ], style={'width': '40%', 'display': 'inline-block', 'margin-left': '10px', 'margin-right': 'auto'}, title='Use these controls to adjust the window and level of the image'),
    ]),
])


@ app.callback(
    [Output('output-image', 'children')],
    [Input('upload-image', 'contents'),
     Input('slice-slider', 'value'),
     Input('crop-slider-x', 'value'),
     Input('crop-slider-y', 'value'),
     Input('transpose-options', 'value'),
     ],
    [Input('upload-image', 'filename'),
     Input('window-slider', 'value'),
     Input('level-slider', 'value')]
)
def update_output(contents, slice_index, crop_x, crop_y, transpose_option, filename, window, level):
    if contents is not None:
        img_cropped_modified, aspect = get_and_crop(
            contents, slice_index, crop_x, crop_y, transpose_option)

        zmin = level - (window / 2)
        zmax = level + (window / 2)
        fig_modified = go.Figure()
        fig_modified.add_trace(go.Heatmap(
            z=img_cropped_modified, colorscale='gray', zmin=zmin, zmax=zmax))
        fig_modified.update_layout(title=f'Planning CT Slice: {slice_index}',
                                   xaxis_title='X', yaxis_title='Y',
                                   xaxis=dict(constrain='domain'),
                                   yaxis=dict(scaleanchor='x', scaleratio=aspect), width=700, height=700)

        return [dcc.Graph(figure=fig_modified)]

    return ["Please upload a file."]


@cache.memoize(timeout=600)  # Cache the output of this function for 60 seconds
def get_and_crop(contents, slice_index, crop_x, crop_y, transpose_option):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)

    with tempfile.NamedTemporaryFile(delete=True) as temp_file:
        temp_file.write(decoded)
        temp_file.flush()
        temp_file.seek(0)
        nrrd_data, header = nrrd.read(temp_file.name)

    app.layout['slice-slider'].max = nrrd_data.shape[0] - 1
    app.layout['crop-slider-x'].max = nrrd_data.shape[1] - 1
    app.layout['crop-slider-y'].max = nrrd_data.shape[2] - 1

    # Original image processing
    # img = nrrd_data[:, :, slice_index]

    # img_cropped = img[crop_x[0]:crop_x[1], crop_y[0]:crop_y[1]]
    # fig_original = go.Figure()
    # fig_original.add_trace(go.Heatmap(z=img_cropped, colorscale='gray'))
    # fig_original.update_layout(title=f'Original Slice: {slice_index}',
    #                            xaxis_title='X', yaxis_title='Y',
    #                            xaxis=dict(constrain='domain'),
    #                            yaxis=dict(scaleanchor='x', scaleratio=1))

    # Modified image processing based on transpose option
    if transpose_option == 'transpose_xy':
        nrrd_data = nrrd_data.transpose((0, 2, 1))
        header['space directions'] = header['space directions'][np.array([
            0, 2, 1])]
    elif transpose_option == 'transpose_yz':
        nrrd_data = nrrd_data.transpose((1, 2, 0))
        header['space directions'] = header['space directions'][np.array([
            1, 2, 0])]
    elif transpose_option == 'transpose_xz':
        nrrd_data = nrrd_data.transpose((2, 1, 0))
        header['space directions'] = header['space directions'][np.array([
            2, 1, 0])]

    space = np.abs(header['space directions']).max(axis=1)
    aspect = space[0] / space[1]

    img_modified = nrrd_data[:, :, slice_index]
    img_cropped_modified = img_modified[crop_x[0]:crop_x[1], crop_y[0]:crop_y[1]]
    return img_cropped_modified, aspect


def initialize_simulation(contents, crop_x, crop_y, slice_index, transpose_option, bowtie_option):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)

    with tempfile.NamedTemporaryFile(delete=True) as temp_file:
        temp_file.write(decoded)
        temp_file.flush()
        temp_file.seek(0)
        nrrd_data, header = nrrd.read(temp_file.name)

    # Original image plotting

    # Modified image processing based on transpose option
    if transpose_option == 'transpose_xy':
        nrrd_data = nrrd_data.transpose((0, 2, 1))
        header['space directions'] = header['space directions'][np.array([
                                                                         0, 2, 1])]
    elif transpose_option == 'transpose_yz':
        nrrd_data = nrrd_data.transpose((1, 2, 0))
        header['space directions'] = header['space directions'][np.array([
                                                                         1, 2, 0])]
    elif transpose_option == 'transpose_xz':
        nrrd_data = nrrd_data.transpose((2, 1, 0))
        header['space directions'] = header['space directions'][np.array([
                                                                         2, 1, 0])]

    if bowtie_option == 'full_fan':
        is_fullfan = True
    elif bowtie_option == 'half_fan':
        is_fullfan = False
    else:
        is_fullfan = None

    # Ensure slice_index is within the valid range
    if slice_index < 0:
        slice_index = 0
    elif slice_index >= nrrd_data.shape[2]:
        slice_index = nrrd_data.shape[2] - 2

    # ensure that the crop values are within the valid range
    if crop_x[0] < 0:
        crop_x[0] = 0
    if crop_x[1] > nrrd_data.shape[0]:
        crop_x[1] = nrrd_data.shape[0]

    if crop_y[0] < 0:
        crop_y[0] = 0
    if crop_y[1] > nrrd_data.shape[1]:
        crop_y[1] = nrrd_data.shape[1]
    # img = nrrd_data[:, :, slice_index]
    img_cropped = nrrd_data[crop_x[0]:crop_x[1],
                            crop_y[0]:crop_y[1], slice_index:slice_index+2]

    # print(img_cropped.shape)
    spectrum = fc.calculate_spectrum_sp(100, 12)

    nrrd_file = 'temp'

    nrrd_to_mhd(nrrd_file, force=True, tr=[0, 1, 2], crop=[None, None, None, None, None, None], flip=[False, False, False],
                nrrd_data=img_cropped, nrrd_header=header)

    phantom_rtis = patient_data.patient_phantom(
        nrrd_file, 1e7, is_fullfan=is_fullfan)

    # Beam filters
    spectrum.filter('Be', 1.5)
    spectrum.filter('Al', 2.75)
    spectrum.filter('Ti', 0.89)

    # Detector filters
    spectrum.filter('Al', 3.7)
    spectrum.filter('C', 3.8*(2/1.7))  # Difference in density

    phantom_rtis.initialize_fastmc(1, spectrum)

    print(phantom_rtis)
    phantom_rtis.phantom = phantom_rtis.phantom[:, :, 0]
    phantom_rtis.density = phantom_rtis.density[:, :, 0]

    # print(phantom_rtis.phantom.shape)
    # insert a new axis to the phantom
    phantom_rtis.phantom = phantom_rtis.phantom[np.newaxis, ...]
    phantom_rtis.density = phantom_rtis.density[np.newaxis, ...]

    phantom_rtis.geomet.nVoxel = np.array(phantom_rtis.phantom.shape)
    # rearange the voxel dimensions to match the phantom
    phantom_rtis.geomet.dVoxel = phantom_rtis.geomet.dVoxel[np.array([
        2, 0, 1])]
    phantom_rtis.geomet.sVoxel = phantom_rtis.geomet.dVoxel * phantom_rtis.geomet.nVoxel

    phantom_rtis.geomet.nDetector = np.array([1, 512])
    phantom_rtis.geomet.dDetector = np.array(
        [phantom_rtis.geomet.dVoxel[0], 0.8])
    phantom_rtis.geomet.sDetector = phantom_rtis.geomet.dDetector * \
        phantom_rtis.geomet.nDetector

    phantom_rtis.geomet.mode = "parallel"

    phantom_rtis.retain_partial_calcs = True
    phantom_rtis.run_gecco(1e10, 815, conv_on=False, filter_on=False)

    phantom_rtis.reweight(100, scat=0.05, mAs=400)

    print(phantom_rtis)

    return phantom_rtis


@ cache.memoize(timeout=300)  # Cache the initialized simulation for 5 minutes
def get_cached_simulation(contents, crop_x, crop_y, slice_index, transpose_option, bowtie_option):
    return initialize_simulation(contents, crop_x, crop_y, slice_index, transpose_option, bowtie_option)


@ app.callback(
    [Output('output-image-modified', 'children')],
    [Input('apply-modifications-btn', 'n_clicks')],
    [State('upload-image', 'contents'),
     State('slice-slider', 'value'),
     State('crop-slider-x', 'value'),
     State('crop-slider-y', 'value'),
     State('transpose-options', 'value'),
     State('upload-image', 'filename')],
    [
        Input('kvp-slider', 'value'),
        Input('mas-slider', 'value'),
        Input('scatter-slider', 'value'),
        Input('bowtie-buttons', 'value'),
        Input('window-slider', 'value'),
        Input('level-slider', 'value')
    ]
)
def update_output2(n_clicks, contents, slice_index, crop_x, crop_y, transpose_option, filename, kvp, mAs, scat, bowtie_option, window, level):
    if n_clicks > 0 and contents is not None:

        phantom_rtis = get_cached_simulation(
            contents, crop_x, crop_y, slice_index, transpose_option, bowtie_option)

        phantom_rtis.reweight(kVp=kvp, scat=scat, mAs=mAs)
        img_modified = phantom_rtis.img.squeeze()

        # interp_water = fc.get_mu_over_rho('SchneiderMaterialsWeight7')
        # mu_water = 0

        # for weight, energy in zip(phantom_rtis.w_fluence_times_p_detected, phantom_rtis.energies):
        #     mu_water += interp_water(energy)*weight
        #     print(energy, interp_water(energy), weight)

        # print(mu_water)
        mu_water = phantom_rtis.img[phantom_rtis.phantom == 6].mean()

        print(mu_water)
        # 1000*(img_modified - mu_water)/mu_water
        img_cropped_modified = np.flipud(
            1000*(img_modified - mu_water)/mu_water)

        scale_ratio = phantom_rtis.geomet.dVoxel[1] / \
            phantom_rtis.geomet.dVoxel[2]

        # print(scale_ratio)

        zmin = level - (window / 2)
        zmax = level + (window / 2)
        fig_modified = go.Figure()
        fig_modified.add_trace(go.Heatmap(
            z=img_cropped_modified, colorscale='gray', zmin=zmin, zmax=zmax))
        fig_modified.update_layout(title=f'RTIS Simulation Slice: {slice_index}', xaxis_title='X', yaxis_title='Y', xaxis=dict(
            constrain='domain'), yaxis=dict(scaleanchor='x', scaleratio=scale_ratio), width=700, height=700)

        return [dcc.Graph(figure=fig_modified)]

    return ["Please upload a file and apply modifications."
            ]


if __name__ == '__main__':
    app.run_server(debug=True)
