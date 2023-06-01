import tkinter as tk
import math
# Initialize Tkinter
root = tk.Tk()
root.title("Car Animation")

# Set up the canvas
canvas_width = 800
canvas_height = 600
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
canvas.pack()

# Load the car image
car_image = tk.PhotoImage(file="car.png")
car_width = car_image.width()
car_height = car_image.height()

# Set initial variables for animation
amplitude = 30  # Bump amplitude
frequency = 0.1  # Bump frequency
rotation_speed = 2  # Rotation speed
angle = 0

# Create the car on the canvas
car = canvas.create_image(
    canvas_width // 2, canvas_height // 2, image=car_image)

# Animation function


def animate():
    global angle

    # Update car position
    car_y = (canvas_height // 2) + amplitude * math.sin(angle)
    canvas.coords(car, canvas_width // 2 - car_width //
                  2, car_y - car_height // 2)

    # Update car rotation
    angle += rotation_speed

    # Repeat the animation
    canvas.after(10, animate)


# Start the animation
animate()

# Run the Tkinter event loop
root.mainloop()
