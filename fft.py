import serial
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

XMAX=2000
# Function to initialize the plot
def init_plot():
    ax.set_xlim(0, 0.5)
    ax.set_ylim(0, 2550)
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
    
    # Perform FFT on the received data
    fft_values = np.fft.fft(values)
    fft_values = np.abs(fft_values)  # Take the absolute value for magnitude spectrum
    
    # Generate x-axis values for the FFT plot
    freq = np.fft.fftfreq(len(values))
    
    # Update the plot with the FFT data
    line.set_data(freq, fft_values)
    
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
