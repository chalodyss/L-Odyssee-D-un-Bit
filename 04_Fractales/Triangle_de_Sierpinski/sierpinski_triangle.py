# Copyright © 2025 Charles Theetten
# Tous droits réservés.
# Ce programme est distribué sous licence CC BY-NC-ND 4.0.

################################################################################

""" sierpinski_triangle """

################################################################################

import  argparse

from    turtle import Turtle

################################################################################

triangle = []

################################################################################

def draw(turtle):
    """ draw function """
    i = 0

    while i < len(triangle):
        first_point = triangle[i]
        turtle.up()
        turtle.goto(first_point)
        turtle.down()
        turtle.goto(triangle[i + 1])
        turtle.goto(triangle[i + 2])
        turtle.goto(first_point)
        i += 3

################################################################################

def build(p_a, p_b, p_c, iterations):
    """build function"""
    if iterations > 0:
        new_points = [ ((p_a[0] + p_b[0]) / 2, (p_a[1] + p_b[1]) / 2),
                       ((p_a[0] + p_c[0]) / 2, (p_a[1] + p_c[1]) / 2),
                       ((p_b[0] + p_c[0]) / 2, (p_b[1] + p_c[1]) / 2) ]

        for i in range(0, 3):
            triangle.append(new_points[i])

        build(p_a, new_points[0], new_points[1], iterations - 1)
        build(new_points[0], p_b, new_points[2], iterations - 1)
        build(new_points[1], new_points[2], p_c, iterations - 1)

################################################################################

def check_iterations(value):
    """ check_iterations function """
    iteratations = int(value)

    if iteratations < 0 or iteratations > 7:
        raise argparse.ArgumentTypeError(f"ITERATIONS must be between 0 and 7, got {iteratations}.")

    return iteratations

def check_speed(value):
    """ check_speed function """
    speed = int(value)

    if speed < 0 or speed > 10:
        raise argparse.ArgumentTypeError(f"SPEED must be between 0 and 10, got {speed}.")

    return speed

def check_args():
    """ check_args function """
    parser = argparse.ArgumentParser()

    parser.add_argument("ITERATIONS", help = "Values between 0 and 7.", type = check_iterations)
    parser.add_argument("SPEED",  help = "Values between 0 and 10.", type = check_speed)

    return parser.parse_args()

################################################################################

def main():
    """ main function """
    args            = check_args()

    iterations      = args.ITERATIONS
    speed           = args.SPEED

    turtle          = Turtle()
    ws              = turtle.getscreen()

    screen_width    = ws.getcanvas().winfo_screenwidth()
    screen_height   = ws.getcanvas().winfo_screenheight()

    ws.setup(width  = screen_width / 2, height = (screen_height * 2) / 3)
    ws.title("Sierpinski Triangle")
    ws.bgcolor("#212F3C")

    turtle.speed(speed)
    turtle.ht()
    turtle.pensize(width = 2)
    turtle.pencolor("#FFFFFF")

    window_width    = ws.window_width()
    base            = window_width * 0.8
    height          = (base * 3**0.5) / 2

    p_a             = [ -base / 2, -height / 2 ]
    p_b             = [ base / 2, -height / 2 ]
    p_c             = [ 0, height / 2 ]

    triangle.extend([p_a, p_b, p_c])

    build(p_a, p_b, p_c, iterations)
    draw(turtle)

    ws.exitonclick()

################################################################################

if __name__ == "__main__":
    main()

################################################################################
