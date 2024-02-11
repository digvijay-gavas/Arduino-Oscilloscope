import serial
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import time

rSampleSize = 512
rSamples = np.empty(rSampleSize)

def init_plot():
    ax_time.set_xlim(0, rSampleSize)
    ax_time.set_ylim(0, 255)
    line_time.set_data([], [])
    
    ax_freq.set_xlim(0, 4500)  # Adjust x-axis limit based on Nyquist frequency
    ax_freq.set_ylim(0, 255)  # Adjust y-axis limit as needed
    line_freq.set_data([], [])
    
    return line_time, line_freq

def update_plot(frame):
    ser.write(b'10')
    time.sleep(0.15)
    print(ser.in_waiting)
    if ser.in_waiting < (rSampleSize + 5):
        print('ser.readall()')
        ser.readall()
        line_time.set_data(range(0, rSampleSize), rSamples)
        return line_time, line_freq
    
    rSamplesByte = ser.read(rSampleSize)
    rSampleMicros = int(ser.readline().decode().strip())
    ser.readall()
    print(1000000.0 / (rSampleMicros / rSampleSize))

    for i, rSampleByte in enumerate(rSamplesByte):
        rSamples[i] = rSampleByte
    
    # Perform FFT on the received data
    fft_values = np.fft.fft(rSamples)
    fft_values = np.abs(fft_values)  # Take the absolute value for magnitude spectrum
    
    # Generate x-axis values for the FFT plot
    freq = np.fft.fftfreq(len(rSamples),  (rSampleMicros / rSampleSize) / 1000000.0 )
    
    # Update the plots
    line_time.set_data(range(0, rSampleSize), rSamples)
    line_freq.set_data(freq[:rSampleSize//2], fft_values[:rSampleSize//2])
    
    return line_time, line_freq

# Serial port configuration
port = 'COM7'  # Modify this according to your Arduino serial port
baudrate = 115200
ser = serial.Serial(port, baudrate, timeout=0.01)

# Create a figure and subplots
fig, (ax_time, ax_freq) = plt.subplots(2, 1)

# Time domain plot
line_time, = ax_time.plot([], [], lw=2)
ax_time.set_title('Time Domain')
ax_time.set_xlabel('Sample')
ax_time.set_ylabel('Amplitude')

# Frequency domain plot
line_freq, = ax_freq.plot([], [], lw=2)
ax_freq.set_title('Frequency Domain')
ax_freq.set_xlabel('Frequency (Hz)')
ax_freq.set_ylabel('Magnitude')

# Create the animation
ani = FuncAnimation(fig, update_plot, frames=30, init_func=init_plot, blit=True)

# Show the plot
plt.show()

# Close the serial connection
ser.close()
