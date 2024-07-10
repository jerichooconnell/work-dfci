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
    dcc.Upload(
        id='upload-image',
        children=html.Div(['Drag and Drop or ', html.A('Select Files')]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=False
    ),
    dcc.Slider(
        id='slice-slider',
        min=0,
        max=200,  # Placeholder value, will be dynamically updated
        step=1,
        value=50,
        marks={i: str(i) for i in range(0, 200, 50)},  # Label every 50 steps
    ),
    dcc.RangeSlider(
        id='crop-slider-x',
        min=0,
        max=512,  # Placeholder value, will be dynamically updated
        step=1,
        value=[100, 400],
        marks={i: str(i) for i in range(0, 513, 50)},  # Label every 50 steps
    ),
    dcc.RangeSlider(
        id='crop-slider-y',
        min=0,
        max=512,  # Placeholder value, will be dynamically updated
        step=1,
        value=[100, 400],
        marks={i: str(i) for i in range(0, 513, 50)},  # Label every 50 steps
    ),
    html.Div(id='output-image'),
])


@app.callback(
    Output('output-image', 'children'),
    [Input('upload-image', 'contents'),
     Input('slice-slider', 'value'),
     Input('crop-slider-x', 'value'),
     Input('crop-slider-y', 'value')],
    [State('upload-image', 'filename')]
)
def update_output(contents, slice_index, crop_x, crop_y, filename):
    if contents is not None:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)

        with tempfile.NamedTemporaryFile(delete=True) as temp_file:
            temp_file.write(decoded)
            temp_file.flush()
            temp_file.seek(0)
            nrrd_data, header = nrrd.read(temp_file.name)

        # Update sliders' max values based on the image dimensions
        app.layout['slice-slider'].max = nrrd_data.shape[0] - 1
        app.layout['crop-slider-x'].max = nrrd_data.shape[1] - 1
        app.layout['crop-slider-y'].max = nrrd_data.shape[2] - 1

        # Select the slice
        img = nrrd_data[:, :, slice_index]
        print(nrrd_data.shape)

        # Crop the image
        img_cropped = img[crop_x[0]:crop_x[1], crop_y[0]:crop_y[1]]

        fig = go.Figure()
        fig.add_trace(go.Heatmap(z=img_cropped, colorscale='gray'))
        fig.update_layout(title=f'Slice: {slice_index}',
                          xaxis_title='X', yaxis_title='Y',
                          xaxis=dict(
                              constrain='domain'  # This option ensures that the aspect ratio is maintained
                          ),
                          yaxis=dict(
                              scaleanchor='x',
                              scaleratio=1,
                          ))

        return dcc.Graph(figure=fig)

    return "Please upload a file."


if __name__ == '__main__':
    app.run_server(debug=True)

# import base64
# import dash
# from dash import dcc, html, Input, Output, State, ctx
# import io
# import nrrd
# import numpy as np
# import plotly.graph_objs as go
# import tempfile
# # import plotly.graph_objs as go

# # Initialize Dash app
# app = dash.Dash(__name__)

# # Define app layout
# app.layout = html.Div([
#     dcc.Store(id='nrrd-store'),  # Store for NRRD data
#     dcc.Upload(
#         id='upload-image',
#         children=html.Div(['Drag and Drop or ', html.A('Select Files')]),
#         style={
#             'width': '100%',
#             'height': '60px',
#             'lineHeight': '60px',
#             'borderWidth': '1px',
#             'borderStyle': 'dashed',
#             'borderRadius': '5px',
#             'textAlign': 'center',
#             'margin': '10px'
#         },
#         multiple=False
#     ),
#     dcc.Slider(
#         id='slice-slider',
#         min=0, max=200, step=1, value=50,
#         marks={i: str(i) for i in range(0, 200, 50)},
#     ),
#     dcc.RangeSlider(
#         id='crop-slider-x',
#         min=0, max=512, step=1, value=[10, 90],
#         marks={i: str(i) for i in range(0, 513, 50)},
#     ),
#     dcc.RangeSlider(
#         id='crop-slider-y',
#         min=0, max=512, step=1, value=[100, 400],
#         marks={i: str(i) for i in range(0, 513, 50)},
#     ),
#     html.Div(id='output-image'),
# ])


# @app.callback(
#     Output('nrrd-store', 'data'),
#     Input('upload-image', 'contents'),
#     State('upload-image', 'filename')
# )
# def load_nrrd(contents, filename):
#     if contents is not None:
#         content_type, content_string = contents.split(',')
#         decoded = base64.b64decode(content_string)

#         with tempfile.NamedTemporaryFile(delete=True) as temp_file:
#             temp_file.write(decoded)
#             temp_file.flush()
#             temp_file.seek(0)
#             nrrd_data, header = nrrd.read(temp_file.name)

#         # Update sliders' max values based on the image dimensions
#         # app.layout['slice-slider'].max = nrrd_data.shape[0] - 1
#         # app.layout['crop-slider-x'].max = nrrd_data.shape[1] - 1
#         # app.layout['crop-slider-y'].max = nrrd_data.shape[2] - 1
#         # print(nrrd_data[0])
#         # Store data and shape
#         print('data stored')
#         return {'data': nrrd_data, 'shape': nrrd_data.shape}

#     return dash.no_update


# @app.callback(
#     [Output('output-image', 'children'),
#      Output('slice-slider', 'max'),
#      Output('crop-slider-x', 'max'),
#      Output('crop-slider-y', 'max')],
#     [Input('nrrd-store', 'data'),
#      Input('slice-slider', 'value'),
#      Input('crop-slider-x', 'value'),
#      Input('crop-slider-y', 'value')]
# )
# def update_output(stored_data, slice_index, crop_x, crop_y):
#     print(stored_data is not None, ctx.triggered_id != 'nrrd-store')
#     if stored_data is not None:
#         print('updating')
#         nrrd_data = stored_data['data'][slice_index]
#         shape = stored_data['shape']

#         # Update sliders' max values based on the image dimensions
#         max_slice = shape[0] - 1
#         max_crop_x = shape[1] - 1
#         max_crop_y = shape[2] - 1

#         # Select the slice
#         # img = nrrd_data[slice_index, :, :]

#         # Crop the image
#         img_cropped = nrrd_data[crop_x[0]:crop_x[1], crop_y[0]:crop_y[1]]

#         fig = go.Figure()
#         fig.add_trace(go.Heatmap(z=img_cropped, colorscale='gray'))
#         fig.update_layout(title=f'Slice: {slice_index}',
#                           xaxis_title='X', yaxis_title='Y',
#                           xaxis=dict(constrain='domain'),
#                           yaxis=dict(scaleanchor='x', scaleratio=1))

#         return dcc.Graph(figure=fig), max_slice, max_crop_x, max_crop_y

#     return dash.no_update


# if __name__ == '__main__':
#     app.run_server(debug=True)
