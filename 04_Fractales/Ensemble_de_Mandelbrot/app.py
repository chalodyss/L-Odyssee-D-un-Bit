# Copyright © 2025 Charles Theetten
# Tous droits réservés.
# Ce programme est distribué sous licence CC BY-NC-ND 4.0.

################################################################################

# pylint: disable=C0301, W0611

################################################################################

""" app """

################################################################################

from    dash                    import callback
from    dash                    import clientside_callback
from    dash                    import dcc
from    dash                    import Dash
from    dash                    import html
from    dash                    import Input
from    dash                    import Output
from    dash                    import State

from    components.mandelbrot   import Mandelbrot

################################################################################

app         = Dash(__name__)

app.layout  = [ html.Div(id         = "options",
                         children   = [ html.H1(children = "Mandelbrot Set"),
                                        html.Br(),
                                        html.Hr(),
                                        html.H2(children = "Résolution"),
                                        dcc.Dropdown(id = "dropdown_resolution", options = [ "Low", "High" ], value = "Low"),
                                        html.Br(),
                                        html.Hr(),
                                        html.H2(children = "Nombre de points"),
                                        dcc.Dropdown(id = "dropdown_points", options = [ 10, 20, 50, 100, 250, 500 ], value = 10),
                                        html.Br(),
                                        html.Hr(),
                                        html.H2(children = "Nombre d'itérations"),
                                        dcc.Dropdown(id = "dropdown_iterations", options = [ 2, 4, 8, 16, 32, 64 ], value = 16),
                                        html.Br(),
                                        html.Hr(),
                                        html.H2(children = "Délai d'affichage"),
                                        dcc.Dropdown(id = "dropdown_delay", options = [ 1000, 500, 100, 10 ], value = 500),
                                        html.Br(),
                                        html.Hr(),
                                        html.H2(children = "Limite"),
                                        dcc.Input(id = "textbox_limit", value = 2, type = "text"),
                                        html.Br(),
                                        html.Br(),
                                        html.Hr(),
                                        html.H2(children = "Couleurs"),
                                        dcc.Dropdown(id = "dropdown_colors", options = [ "Binary", "Grayscale" ], value = "Binary"),
                                        html.Br(),
                                        html.Hr(),
                                        html.Br(),
                                        html.Br(),
                                        html.Button(children = "Init", id = "init"),
                                        html.Br(),
                                        html.Br(),
                                        html.Button(children = "Draw", id = "draw"),
                                        html.Br(),
                                        html.Br(),
                                        html.Hr() ]),

                html.Div(id         = "figure",
                         children   = [ dcc.Graph(id = "graph",
                                                  figure = {
                                                      'layout': {
                                                      'template': 'plotly_dark',
                                                      'paper_bgcolor': 'black',
                                                      'plot_bgcolor': 'black'
                                                      }
                                                  }),
                                        dcc.Interval(id = "figure_update", interval = 0, n_intervals = 0, disabled = True) ]),

                dcc.Store(id = "resolution"),
                dcc.Store(id = "nb_points"),
                dcc.Store(id = "iterations"),
                dcc.Store(id = "delay"),
                dcc.Store(id = "limit"),
                dcc.Store(id = "colors"),
                dcc.Store(id = "figures", data = []),
                dcc.Store(id = "cpt")
               ]

################################################################################

@callback(Output("resolution", "data"),
          Input("dropdown_resolution", "value"))

def update_resolution(value):
    """ update_resolution function """
    return value

################################################################################

@callback(Output("nb_points", "data"),
          Input("dropdown_points", "value"))

def update_nb_points(value):
    """ update_nb_points function """
    return value

################################################################################

@callback(Output("iterations", "data"),
          Input("dropdown_iterations", "value"))

def update_iterations(value):
    """ update_iterations function """
    return value

################################################################################

@callback(Output("figure_update", "interval"),
          Output("delay", "data"),
          Input("dropdown_delay", "value"))

def update_delay(value):
    """ update_delay function """
    return value, value

################################################################################

@callback(Output("limit", "data"),
          Input("textbox_limit", "value"))

def update_limit(value):
    """ update_limit function """
    return value

################################################################################

@callback(
    Output("colors", "data"),
    Input("dropdown_colors", "value")
)

def update_colors(value):
    """ update_colors function """
    return value

################################################################################

@callback(
    [
        Output("graph", "figure", allow_duplicate = True),
        Output("figure_update", "disabled", allow_duplicate = True),
        Output("figures", "data"),
        Output("cpt", "data", allow_duplicate = True)
    ],
    Input("init", "n_clicks"),
    [
        State("resolution", "data"),
        State("nb_points", "data"),
        State("iterations", "data"),
        State("limit", "data"),
        State("colors", "data")
    ],
    prevent_initial_call = True
)

def init(_, resolution, points, iterations, limit, colors):
    """ init function"""
    cpt         = 0
    disabled    = True

    mandelbrot = Mandelbrot()
    mandelbrot.initialize((-2, 0.5), (-1.5, 1.5), points, limit)

    if resolution == "Low":
        mandelbrot.low_compute(iterations)
        mandelbrot.set_low_figures(iterations)
    elif resolution == "High":
        mandelbrot.high_compute(iterations, colors)
        mandelbrot.set_high_figures(iterations, colors)

    return mandelbrot.figures[0], disabled, mandelbrot.figures, cpt

################################################################################

clientside_callback(
    """
    function(n_clicks, n_intervals, disabled, iterations, cpt, figures) {
        if (cpt >= iterations) {
            return [figures[figures.length - 1], true, n_intervals, iterations];
        }

        return [figures[cpt], false, n_intervals, cpt + 1];
    }
    """,
    Output("graph", "figure"),
    Output("figure_update", "disabled"),
    Output("figure_update", "n_intervals"),
    Output("cpt", "data"),
    Input("draw", "n_clicks"),
    Input("figure_update", "n_intervals"),
    State("figure_update", "disabled"),
    State("iterations", "data"),
    State("cpt", "data"),
    State("figures", "data"),
    prevent_initial_call = True)

################################################################################

if __name__ == '__main__':
    app.run(debug = True)

################################################################################
