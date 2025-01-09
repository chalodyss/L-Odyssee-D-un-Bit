# Copyright © 2025 Charles Theetten
# Tous droits réservés.
# Ce programme est distribué sous licence CC BY-NC-ND 4.0.

# pylint: disable=C0301

""" Mandelbrot set """

################################################################################

import  numpy                   as np

import  plotly.graph_objects    as go
import  plotly.express          as px

################################################################################

class Mandelbrot():
    """ Mandelbrot Class """

    def __init__(self):
        """ constructor """
        self.points     = None
        self.bound      = 0
        self.indice     = 0
        self.point_size = 0
        self.steps      = []
        self.matrix     = []
        self.figures    = []

    ################################################################################

    def initialize(self, x_axis, y_axis, nb_points, limit):
        """ initialize function """
        re              = np.linspace(x_axis[0], x_axis[1], nb_points * 2)
        im              = np.linspace(y_axis[0], y_axis[1], nb_points)

        self.points     = re[np.newaxis, :] + im[:, np.newaxis] * 1j

        self.point_size = 1000 // nb_points * 0.5
        self.bound      = int(limit)

    ################################################################################

    def low_compute(self, nb_iterations):
        """ low_compute function """
        z = 0
        c = self.points

        for _ in range(0, nb_iterations):
            z = z ** 2 + c
            c = c[abs(z) <= self.bound]
            z = z[abs(z) <= self.bound]

            self.steps.append(c)

    ################################################################################

    def high_compute_binary(self, iterations):
        """ high_compute_binary function """  
        z = 0
        c = self.points

        self.matrix.append((abs(c) <= self.bound * 2).astype(np.uint8))

        for _ in range(0, iterations):
            z = z ** 2 + c
            c = np.where(abs(z) <= self.bound, c, 0)
            z = np.where(abs(z) <= self.bound, z, 0)

            self.matrix.append(abs(c) != 0)

    ################################################################################

    def high_compute_grayscale(self, iterations):
        """ high_compute_grayscale function """  
        z = 0
        c = self.points

        self.matrix.append((abs(self.points) <= self.bound).astype(np.uint16))

        for _ in range(0, iterations):
            z           = np.where(abs(z) <= self.bound, z, 0)
            z           = z ** 2 + c

            magnitudes  = np.clip(abs(z), 0, self.bound)
            normalized  = (magnitudes / self.bound) * 65535
            self.matrix.append(normalized.astype(np.uint16))

    ################################################################################

    def set_low_figures(self, iterations):
        """ set_low_figures function """
        fig = go.Figure()

        fig.update_layout(xaxis         = { "range" : [-2.25, 1.0], "tickmode" : "linear", "dtick" : 0.5 },
                          yaxis         = { "range" : [-2.0, 2.0], "tickmode" : "linear", "dtick" : 0.5 },
                          template      =  "plotly_dark")

        fig.add_trace(go.Scattergl(y        = self.points.imag.ravel(), x = self.points.real.ravel(),
                                   mode     = "markers",
                                   marker   = { "symbol" : "square", "color"  : "lime", "size" : self.point_size }))
        self.figures.append(fig)

        for i in range(0, iterations):
            fig = go.Figure()

            fig.update_layout(xaxis         = { "range" : [-2.25, 1.0], "tickmode" : "linear", "dtick" : 0.5 },
                              yaxis         = { "range" : [-2.0, 2.0], "tickmode" : "linear", "dtick" : 0.5 },
                              template      =  "plotly_dark")

            fig.add_trace(go.Scattergl(y        = self.steps[i].imag.ravel(), x = self.steps[i].real.ravel(),
                                       mode     = "markers",
                                       marker   = { "symbol" : "square", "color"  : "lime", "size" : self.point_size }))

            self.figures.append(fig)

    ################################################################################

    def set_high_figures_binary(self, iterations):
        """ set_high_figures_binary function """
        fig = px.imshow(self.matrix[0], binary_string = True, zmin = 0, zmax = 1)

        fig.update_layout(template = "plotly_dark", paper_bgcolor = "black", plot_bgcolor = "black")
        self.figures.append(fig)

        for i in range(0, iterations):
            fig = px.imshow(self.matrix[i + 1], binary_string = True, zmin = 0, zmax = 1)

            fig.update_layout(template = "plotly_dark", paper_bgcolor = "black", plot_bgcolor = "black")
            self.figures.append(fig)

    ################################################################################

    def set_high_figures_grayscale(self, iterations):
        """ set_high_figures_grayscale function """
        fig = px.imshow(self.matrix[0], binary_string = False, zmin = 0, zmax = 65535, color_continuous_scale = "gray_r")

        fig.update_layout(template = "plotly_dark", paper_bgcolor = "black", plot_bgcolor = "black")
        self.figures.append(fig)

        for i in range(0, iterations):
            fig = px.imshow(self.matrix[i + 1], binary_string = False, zmin = 0, zmax = 65535, color_continuous_scale = "gray_r")

            fig.update_layout(template = "plotly_dark", paper_bgcolor = "black", plot_bgcolor = "black")
            self.figures.append(fig)
