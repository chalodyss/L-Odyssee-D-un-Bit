# Copyright © 2025 Charles Theetten
# Tous droits réservés.
# Ce programme est distribué sous licence CC BY-NC-ND 4.0.

################################################################################

# pylint: disable=E1101, R0914

################################################################################

""" von_koch_flake """

################################################################################

import  argparse
import  math
import  turtle

################################################################################

class Line:
    """ Line Class """

    def __init__(self, start, end):
        self.start  = start
        self.end    = end
        self.b      = 0
        self.d      = 0

    ################################################################################

    def koch_a(self):
        """ koch_a function """
        return self.start

    ################################################################################

    def koch_b(self):
        """ koch_b function """
        self.b = [ ((self.end[0] - self.start[0]) / 3 + self.start[0]),
                   ((self.end[1] - self.start[1]) / 3 + self.start[1]) ]

        return self.b

    ################################################################################

    def koch_c(self):
        """ koch_c function """
        angle   = 60 * (math.pi / 180)

        o       = self.b
        p       = self.d

        x       = o[0] + ((p[0] - o[0]) * math.cos(angle)) - ((p[1] - o[1]) * math.sin(angle))
        y       = o[1] + ((p[0] - o[0]) * math.sin(angle)) + ((p[1] - o[1]) * math.cos(angle))

        return [ x, y ]

    ################################################################################

    def koch_d(self):
        """ koch_d function """
        self.d = [ ((self.end[0] - self.start[0]) * (2 / 3) + self.start[0]),
                   ((self.end[1] - self.start[1]) * (2 / 3) + self.start[1]) ]

        return self.d

    ################################################################################

    def koch_e(self):
        """ koch_e function """
        return self.end

################################################################################

def koch_curve(start, end, iterations):
    """ koch_curve function """
    curve = []

    curve.append(Line(start, end))

    for _ in range(0, iterations):
        lines = []
        for l in curve:
            a = l.koch_a()
            b = l.koch_b()
            d = l.koch_d()
            c = l.koch_c()
            e = l.koch_e()

            lines.append(Line(a, b))
            lines.append(Line(b, c))
            lines.append(Line(c, d))
            lines.append(Line(d, e))

        curve = lines

    return curve

################################################################################

def check_iterations(value):
    """ check_iterations function """
    iterations = int(value)

    if iterations < 0 or iterations > 6:
        raise argparse.ArgumentTypeError(f"ITERATIONS must be between 0 and 6, got {iterations}.")

    return iterations

def check_speed(value):
    """ check_speed function """
    speed = int(value)

    if speed < 0 or speed > 10:
        raise argparse.ArgumentTypeError(f"SPEED must be between 0 and 10, got {speed}.")

    return speed

def check_tracer(value):
    """ check_tracer function """
    tracer = int(value)

    if tracer not in range(0, 2):
        raise argparse.ArgumentTypeError(f"TRACER must be 0 or 1, got {tracer}.")

    return tracer

def check_args():
    """ check_args function """
    parser = argparse.ArgumentParser()

    parser.add_argument("ITERATIONS", help = "Values between 0 and 6.", type = check_iterations)
    parser.add_argument("SPEED",  help = "Values between 0 and 10.", type = check_speed)
    parser.add_argument("TRACER",  help = "Values in {0, 1}.", type = check_tracer)

    return parser.parse_args()

################################################################################

def main():
    """ main function """
    check_args()

    args            = check_args()

    iterations      = args.ITERATIONS
    speed           = args.SPEED
    tracer          = args.TRACER

    ws              = turtle.getscreen()

    screen_width    = ws.getcanvas().winfo_screenwidth()
    screen_height   = ws.getcanvas().winfo_screenheight()

    ws.setup(width  = screen_width / 2, height = (screen_height * 2) / 3)
    ws.title("Von Koch Curve")
    ws.bgcolor("#17202A")

    turtle.pencolor("#FFFFFF")
    turtle.speed(speed)
    turtle.ht()
    turtle.pensize(width = 1)
    turtle.fillcolor("#00FFFF")

    if tracer == 1:
        turtle.tracer(0)

    window_width    = ws.window_width()
    base            = window_width * 0.6
    height          = (base * 3**0.5) / 2

    p_a             = [ -base / 2, -height / 3 ]
    p_b             = [ base / 2, -height / 3 ]
    p_c             = [ 0, height * 2/3 ]

    curves          = [ koch_curve(p_a, p_c, iterations),
                        koch_curve(p_c, p_b, iterations),
                        koch_curve(p_b, p_a, iterations) ]

    turtle.begin_fill()

    turtle.up()
    turtle.goto(p_a)
    turtle.down()

    for curve in curves:
        for line in curve:
            turtle.goto(line.end)

    turtle.end_fill()

    ws.exitonclick()

################################################################################

if __name__ == "__main__":
    main()

################################################################################
