import serial
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

XMAX=2000
# Function to initialize the plot
def init_plot():
    ax.set_xlim(0, XMAX)
    ax.set_ylim(0, 255)
    line.set_data([], [])
    return line,

# Function to update the plot
def update_plot(frame):
    values = []
    for _ in range(XMAX):
        data = ser.read(1)  # Read one byte from serial
        if data:
            value = ord(data)
            values.append(value)
    
    xdata=range(0, XMAX)
    ydata=values
    line.set_data(xdata, ydata)
    
    
    return line,

# Serial port configuration
port = 'COM7'  # Modify this according to your Arduino serial port
baudrate = 115200
ser = serial.Serial(port, baudrate)

# Create a figure and axis
fig, ax = plt.subplots()
line, = ax.plot([], [], lw=2)
xdata, ydata = [], []

# Create the animation
ani = FuncAnimation(fig, update_plot, frames=30, init_func=init_plot, blit=True)

# Show the plot
plt.show()

# Close the serial connection
ser.close()
