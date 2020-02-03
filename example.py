import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash()

graph = dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montral'},
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            },
        },
    style={
         # turn off settings in graph container
        # 'width': '90vh',
        # 'height': '50vh'
    }

)


app.layout = html.Div(children=[
    graph
                      ], style={
                          # not respected by graph
                          'height': '10vh',
                          # respected by graph
                          'width': '50vw',
                      })

if __name__ == '__main__':
    app.run_server()
