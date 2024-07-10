import base64
import dash
from dash import dcc, html, Input, Output, State
import io
import nrrd
import numpy as np
import tempfile
import plotly.graph_objs as go


# Initialize Dash app
app = dash.Dash(__name__)

# Define app layout
app.layout = html.Div([
    # Add a div for the title and logo
    html.Div([
        html.Img(src='/assets/gecco_logo.png',
                 style={'height': '50px', 'width': 'auto', 'margin-right': '10px'}),
        html.H1('GECCO Real Time Image Simulator', style={
                'font-family': 'Roboto, sans-serif', 'font-weight': '700', 'display': 'inline-block'})
    ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center', 'margin-bottom': '20px'}),
    html.Div([
        html.Div([
            # Tooltip for the upload section title
            html.H3('Upload Image', title='Upload your NRRD image file here'),
            dcc.Upload(
                id='upload-image',
                children=html.Div(
                    ['Drag and Drop or ', html.A('Select Files')]),
                style={
                    'width': '50%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px'
                },
                multiple=False,
            ),
        ]),

        html.Div([
            # Tooltip for the controls section title
            html.H3('Image Preprocessing Controls',
                    title='Adjust the settings to process the uploaded image'),
            html.Div([
                # Tooltip for the slice slider
                html.Label(
                    'Slice Slider', title='Slide to select the slice of the image to display'),
                dcc.Slider(
                    id='slice-slider',
                    min=0,
                    max=200,
                    step=1,
                    value=50,
                    marks={i: str(i) for i in range(0, 200, 50)},
                ),
            ], style={'width': '50%'}, title='Adjust the slider to select the image slice you want to view'),

            html.Div([
                # Tooltip for the X-axis crop slider
                html.Label('Crop Slider X-Axis',
                           title='Adjust to crop the image on the X-axis'),
                dcc.RangeSlider(
                    id='crop-slider-x',
                    min=0,
                    max=512,
                    step=1,
                    value=[100, 400],
                    marks={i: str(i) for i in range(0, 513, 50)},
                ),
            ], style={'width': '50%'}, title='Use this slider to crop the image horizontally'),

            html.Div([
                # Tooltip for the Y-axis crop slider
                html.Label('Crop Slider Y-Axis',
                           title='Adjust to crop the image on the Y-axis'),
                dcc.RangeSlider(
                    id='crop-slider-y',
                    min=0,
                    max=512,
                    step=1,
                    value=[100, 400],
                    marks={i: str(i) for i in range(0, 513, 50)},
                ),
            ], style={'width': '50%'}, title='Use this slider to crop the image vertically'),

            html.Div([
                # Tooltip for the transpose options
                html.Label('Transpose Options',
                           title='Select how to transpose the image'),
                dcc.RadioItems(
                    id='transpose-options',
                    options=[
                        {'label': 'No transpose', 'value': 'no_transpose'},
                        {'label': 'Transpose XY', 'value': 'transpose_xy'},
                        {'label': 'Transpose YZ', 'value': 'transpose_yz'},
                        {'label': 'Transpose XZ', 'value': 'transpose_xz'},
                    ],
                    value='no_transpose',
                    labelStyle={'display': 'block'},
                ),
            ], style={'width': '50%'}, title='Select the transpose option for the image, should plot axially'),
        ], title='Use these controls to adjust how the image is processed'),

        html.Div([
            # Tooltip for the image outputs section title
            html.H3('Image Outputs',
                    title='View the original and modified images here'),
            html.Div(id='output-image', style={'width': '50%',
                 'display': 'inline-block'}, title='Original image output'),
            html.Div(id='output-image-modified',
                     style={'width': '50%', 'display': 'inline-block'}, title='Modified image output'),
        ], title='This section displays the original and processed images'),
    ]),
])


@ app.callback(
    [Output('output-image', 'children'),
     Output('output-image-modified', 'children')],
    [Input('upload-image', 'contents'),
     Input('slice-slider', 'value'),
     Input('crop-slider-x', 'value'),
     Input('crop-slider-y', 'value'),
     Input('transpose-options', 'value')],
    [State('upload-image', 'filename')]
)
def update_output(contents, slice_index, crop_x, crop_y, transpose_option, filename):
    if contents is not None:
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
        img = nrrd_data[:, :, slice_index]
        img_cropped = img[crop_x[0]:crop_x[1], crop_y[0]:crop_y[1]]
        fig_original = go.Figure()
        fig_original.add_trace(go.Heatmap(z=img_cropped, colorscale='gray'))
        fig_original.update_layout(title=f'Original Slice: {slice_index}',
                                   xaxis_title='X', yaxis_title='Y',
                                   xaxis=dict(constrain='domain'),
                                   yaxis=dict(scaleanchor='x', scaleratio=1))

        # Modified image processing based on transpose option
        if transpose_option == 'transpose_xy':
            nrrd_data = nrrd_data.transpose((0, 2, 1))
        elif transpose_option == 'transpose_yz':
            nrrd_data = nrrd_data.transpose((1, 2, 0))
        elif transpose_option == 'transpose_xz':
            nrrd_data = nrrd_data.transpose((2, 1, 0))
        img_modified = nrrd_data[:, :, slice_index]
        img_cropped_modified = img_modified[crop_x[0]:crop_x[1], crop_y[0]:crop_y[1]]
        fig_modified = go.Figure()
        fig_modified.add_trace(go.Heatmap(
            z=img_cropped_modified, colorscale='gray'))
        fig_modified.update_layout(title=f'Modified Slice: {slice_index}',
                                   xaxis_title='X', yaxis_title='Y',
                                   xaxis=dict(constrain='domain'),
                                   yaxis=dict(scaleanchor='x', scaleratio=1))

        return dcc.Graph(figure=fig_original), dcc.Graph(figure=fig_modified)

    return "Please upload a file.", "Please upload a file."


if __name__ == '__main__':
    app.run_server(debug=True)
