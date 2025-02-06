# Copyright © 2025 Charles Theetten
# Tous droits réservés.
# Ce programme est distribué sous licence CC BY-NC-ND 4.0.

################################################################################

# pylint: disable=C0301

################################################################################

""" mandelbrot """

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
        self.nb_points  = 0
        self.bound      = 0
        self.indice     = 0
        self.matrix     = []
        self.figures    = []

    ################################################################################

    def initialize(self, x_axis, y_axis, nb_points, limit):
        """ initialize function """
        self.nb_points  = nb_points

        re              = np.linspace(x_axis[0], x_axis[1], nb_points * 2)
        im              = np.linspace(y_axis[0], y_axis[1], nb_points)
        self.points     = re[np.newaxis, :] + im[:, np.newaxis] * 1j

        self.bound      = int(limit)

    ################################################################################

    def low_compute(self, nb_iterations):
        """ low_compute function """
        z = 0
        c = self.points

        for _ in range(0, nb_iterations):
            z       = z ** 2 + c
            mask    = np.abs(z) <= self.bound
            c       = c[mask]
            z       = z[mask]

            self.matrix.append(c)

    ################################################################################

    def high_compute(self, iterations, color_mode):
        """ high_compute function """
        z = 0
        c = self.points

        if color_mode == "Binary":
            dtype   = np.uint8
            mask    = np.abs(c) <= self.bound * 2
            initial = mask.astype(np.uint8)
        elif color_mode == "Grayscale":
            dtype   = np.uint16
            mask    = np.abs(c) <= self.bound * 2
            initial = mask.astype(dtype)
        else:
            raise ValueError("Unsupported color mode")

        self.matrix.append(initial)

        for _ in range(iterations):
            z       = z ** 2 + c
            mask    = np.abs(z) <= self.bound

            if color_mode == "Binary":
                c = np.where(mask, c, 0)
                z = np.where(mask, z, 0)
                self.matrix.append((abs(c) != 0).astype(dtype))
            elif color_mode == "Grayscale":
                z = np.where(mask, z, 0)
                z = z ** 2 + c
                magnitudes  = np.clip(abs(z), 0, self.bound)
                normalized  = (magnitudes / self.bound) * 65535
                self.matrix.append(normalized.astype(dtype))

    ################################################################################

    def set_low_figures(self, iterations):
        """ set_low_figures function """
        point_size = 1000 // self.nb_points * 0.5

        fig = go.Figure()

        fig.update_layout(xaxis         = { "range" : [-2.25, 1.0], "tickmode" : "linear", "dtick" : 0.5 },
                          yaxis         = { "range" : [-2.0, 2.0], "tickmode" : "linear", "dtick" : 0.5 },
                          template      =  "plotly_dark")

        fig.add_trace(go.Scattergl(y        = self.points.imag.ravel(), x = self.points.real.ravel(),
                                   mode     = "markers",
                                   marker   = { "symbol" : "square", "color"  : "lime", "size" : point_size }))
        self.figures.append(fig)

        for i in range(0, iterations):
            fig = go.Figure()

            fig.update_layout(xaxis         = { "range" : [-2.25, 1.0], "tickmode" : "linear", "dtick" : 0.5 },
                              yaxis         = { "range" : [-2.0, 2.0], "tickmode" : "linear", "dtick" : 0.5 },
                              template      =  "plotly_dark")

            fig.add_trace(go.Scattergl(y        = self.matrix[i].imag.ravel(), x = self.matrix[i].real.ravel(),
                                       mode     = "markers",
                                       marker   = { "symbol" : "square", "color"  : "lime", "size" : point_size }))

            self.figures.append(fig)

    ################################################################################

    def set_high_figures(self, iterations, color_mode):
        """ set_high_figures function """
        fig = px.imshow(self.matrix[0], binary_string = (color_mode == "Binary"),
                        zmin = 0, zmax = 65535 if color_mode == "Grayscale" else 1,
                        color_continuous_scale = "Gray_r" if color_mode == "Grayscale" else "Viridis")

        fig.update_layout(template = "plotly_dark", paper_bgcolor = "black", plot_bgcolor = "black")
        self.figures.append(fig)

        for i in range(iterations):
            fig = px.imshow(self.matrix[i + 1], binary_string = (color_mode == "Binary"),
                            zmin = 0, zmax = 65535 if color_mode == "Grayscale" else 1,
                            color_continuous_scale = "Gray_r" if color_mode == "Grayscale" else "Viridis")

            fig.update_layout(template = "plotly_dark", paper_bgcolor = "black", plot_bgcolor = "black")
            self.figures.append(fig)

    ################################################################################
