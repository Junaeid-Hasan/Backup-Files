import turtle

# # for rectangle
# wn = turtle.Screen()
# rect = turtle.Turtle()
# rect.forward(150)
# rect.left(90)
# rect.forward(75)
# rect.left(90)
# rect.forward(150)
# rect.left(90)
# rect.forward(75)
# turtle.done()

# for Square
# wn = turtle.Screen()
# rect = turtle.Turtle()
# rect.forward(150)
# rect.left(90)
# rect.forward(150)
# rect.left(90)
# rect.forward(150)
# rect.left(90)
# rect.forward(150)
# turtle.done()


# for square using loop
# wn = turtle.Screen()
# rect = turtle.Turtle()
# s=150
# for _ in range(4):
#   rect.forward(s)
#   rect.left(90)

# turtle.done()


# for triangle
# wn = turtle.Screen()
# tri = turtle.Turtle()
# tri.forward(100)
# tri.left(120)
# tri.forward(100)
# tri.left(120)
# tri.forward(100)
# turtle.done()


# for triangle using loop
# wn = turtle.Screen()
# tri = turtle.Turtle()
# for _ in range(3):

#   tri.forward(100)
#   tri.left(120)

# turtle.done()


# for triangle using loop using color
# wn = turtle.Screen()
# tri = turtle.Turtle()

# # Start filling the triangle with color
# tri.fillcolor("blue")  # Set the fill color to blue
# tri.begin_fill()       # Start the fill process

# # Draw the triangle
# for _ in range(3):
#     tri.forward(100)   # Move forward by 100 units
#     tri.left(120)      # Turn left by 120 degrees

# tri.end_fill()
# turtle.done()


# for pentagon
# wn = turtle.Screen()
# pen = turtle.Turtle()
# for _ in range(5):
#    pen.forward(100)
#    pen.left(72)
# turtle.done()


# for whole
# wn = turtle.Screen()

# # Function to draw a square
# def draw_square(t, side_length):
#     t.fillcolor("red")
#     t.begin_fill()
#     for _ in range(4):
#         t.forward(side_length)
#         t.left(90)
#     t.end_fill()

# # Function to draw a triangle
# def draw_triangle(t, side_length):
#     t.fillcolor("blue")
#     t.begin_fill()
#     for _ in range(3):
#         t.forward(side_length)
#         t.left(120)
#     t.end_fill()

# # Function to draw a circle
# def draw_circle(t, radius):
#     t.fillcolor("green")
#     t.begin_fill()
#     t.circle(radius)
#     t.end_fill()

# # Create a turtle for drawing
# shape_turtle = turtle.Turtle()

# # Draw a square
# draw_square(shape_turtle, 100)

# # Move the turtle to a new position
# shape_turtle.penup()
# shape_turtle.goto(-150, 0)
# shape_turtle.pendown()

# # Draw a triangle
# draw_triangle(shape_turtle, 100)

# # Move the turtle to another position
# shape_turtle.penup()
# shape_turtle.goto(220, 0)
# shape_turtle.pendown()

# # Draw a circle
# draw_circle(shape_turtle, 50)

# turtle.done()