# Copyright © 2025 Charles Theetten
# Tous droits réservés.
# Ce programme est distribué sous licence CC BY-NC-ND 4.0.

# pylint: disable=E1101

################################################################################

""" Von Koch Flake """

################################################################################

import  argparse
import  math
import  sys
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

def check_args():
    """ check_args function """
    parser = argparse.ArgumentParser()

    parser.add_argument("ITERATIONS", help = "values in {0... 6}.", type = int)
    parser.add_argument("DELAY",  help = "values in {0... 10}.", type = int)
    parser.add_argument("TRACER",  help = "values in {0, 1}.", type = int)

    args = parser.parse_args()

    try:
        if args.ITERATIONS not in range(0, 8):
            raise argparse.ArgumentTypeError(f"ITERATIONS : {args.ITERATIONS} is an invalid value.")
        if args.DELAY not in range(0, 11):
            raise argparse.ArgumentTypeError(f"DELAY : {args.DELAY} is an invalid value.")
        if args.TRACER not in range(0, 2):
            raise argparse.ArgumentTypeError(f"TRACER : {args.TRACER} is an invalid value.")
    except argparse.ArgumentTypeError as e:
        print(f"Argument Error - {e}\n")
        parser.print_help()
        sys.exit(-1)

################################################################################

def main():
    """ main function """
    check_args()

    iterations      = int(sys.argv[1])
    speed           = int(sys.argv[2])
    tracer          = int(sys.argv[3])

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
