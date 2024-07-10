import base64
import dash
from dash import dcc, html, Input, Output, State

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
    html.Div(id='output-image'),
])


@app.callback(
    Output('output-image', 'children'),
    [Input('upload-image', 'contents')],
    [State('upload-image', 'filename')]
)
def update_output(contents, filename):
    if contents is not None:
        print(f"Uploaded file name: {filename}")

        # Split the content into metadata and the base64 encoded image
        _, content_string = contents.split(',')
        # Decode the base64 string
        decoded = base64.b64decode(content_string)
        # Convert the bytes object to a string suitable for HTML
        src_str = 'data:image/png;base64,' + base64.b64encode(decoded).decode()
        # Display the image in an html.Img component
        return html.Img(src=src_str, style={'maxWidth': '500px', 'maxHeight': '500px'})

    return "Please upload a file."


if __name__ == '__main__':
    app.run_server(debug=True)
