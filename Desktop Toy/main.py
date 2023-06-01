import time
import threading
from tkinter import Tk, Label, PhotoImage

# Create the root window
root = Tk()
root.overrideredirect(True)  # Remove the border
root.wm_attributes('-topmost', 1)  # Make it stay on top
# Set the transparent color to white
root.wm_attributes('-transparentcolor', 'white')

# Load the car image
car_image = PhotoImage(file='car.png')

# Create a label to hold the car image
car_label = Label(root, image=car_image, bg='white')
car_label.pack()


def move_car():
    # Get the screen width
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Now, let's move the car from right to left
    for i in range(screen_width*2, -car_image.width(), -1):
        # Update the position of the window
        root.geometry('+{}+{}'.format(i, screen_height-car_image.height()-40))
        time.sleep(0.01)  # Pause for a moment
        root.wm_attributes('-topmost', 1)  # Make it stay on top

    # When the car has finished moving, start again
    move_car()


# Start the animation in a separate thread
animation_thread = threading.Thread(target=move_car)
animation_thread.start()

root.mainloop()
