import serial
import math
import matplotlib.pyplot as plt

#define variables
Samples = 128
MaxFrequency = 400
Resolution = MaxFrequency / Samples

# Open serial port
ser = serial.Serial('/dev/ttyACM0', 115200)

# Set up plot
plt.ion()
fig, ax = plt.subplots()
line, = ax.plot([], [], 'r-')

# Define and populate plot data
frequencies = []
magnitudes = []
for i in range(Samples):
	frequencies.append(Resolution * i)
	magnitudes.append(0)

# Main loop to get plot data and update plot
while True:
	# Read serial data
	line_data = ser.readline().decode().strip()
	items = line_data.split(',')

	print(items)
	# Read thru serial data pairs
	for i in items:
		try:
			freq, mag = i.split(' ')
		except:
			continue
		# Check that data is valid
		try:
			freq = float(freq)
			mag = float(mag)
		except:
			continue

		# if valid, add data to plots
		# Find proper index value
		Index = (freq + (Resolution / 2)) / Resolution
		math.floor(Index)

		Index = max(0, min(Index, Samples))

		Index = int(Index)

		# Update plot data
		magnitudes[Index] = mag
	
	# Plot newfound data
	line.set_xdata(frequencies)
	line.set_ydata(magnitudes)
	ax.relim()
	ax.autoscale_view()
	plt.pause(0.05)
		