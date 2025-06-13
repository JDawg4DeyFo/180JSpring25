import serial
import math
import matplotlib.pyplot as plt

#define variables
Samples = 64
MaxFrequency = 480
Resolution = MaxFrequency / Samples

# Open serial port
ser = serial.Serial('/dev/ttyACM0', 115200)

# Set up plot
plt.ion()
fig, ax = plt.subplots()
line, = ax.plot([], [], 'r-')

# Add title and labels
ax.set_title("Real-Time FFT Spectrum")
ax.set_xlabel("Frequency (Hz)")
ax.set_ylabel("Magnitude")

# Vertical guide lines
# for i in range(math.floor(MaxFrequency / 60)):
# 	x_Value = (i+1) * 60
# 	ax.axvline(x_Value, linestyle='--')
	# basic_label = f"{(i+1)*60} Hz  "
	# ax.text((i+1) * 60, ax.get_ylim()[1]*0.9, basic_label, color='blue', rotation=0,
    #     verticalalignment='top', horizontalalignment='right', fontsize = 12)
	
# Dynamic THD text overlay
text_overlay = ax.text(0.95, 0.95, "", transform=ax.transAxes,
                       fontsize=10, verticalalignment='top',
                       horizontalalignment='right',
                       bbox=dict(facecolor='white', alpha=0.5))

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

		# Filter out low frequency noise
		if freq < 13:
			continue

		# if valid, add data to plots
		# Find proper index value
		Index = (freq + (Resolution / 2)) / Resolution
		math.floor(Index)

		Index = max(0, min(Index, Samples - 1))

		Index = int(Index)

		# Update plot data
		magnitudes[Index] = mag

	# Calculate THD
	## fundamental
	f_index = frequencies.index(60)
	FundamentalMag = magnitudes[f_index - 1]
	FundamentalMag += magnitudes[f_index]
	FundamentalMag += magnitudes[f_index + 1]

	## harmonics
	TotalHarmonicMag = 0
	IterationCount = 0
	for i in magnitudes:
		# Filter out low freq from 
		IterationCount += 1
		if (IterationCount <= 3):
			continue
		
		# sum
		TotalHarmonicMag += i

	# subtract fundamental from harmonics
	TotalHarmonicMag -= FundamentalMag


	if (FundamentalMag == 0):
		THD = 0
	else:
		THD = TotalHarmonicMag / FundamentalMag
	label = f"THD: {THD:.2f}%"

	# Plot newfound data
	text_overlay.set_text(label)
	line.set_xdata(frequencies)
	line.set_ydata(magnitudes)
	ax.relim()
	ax.autoscale_view()
	plt.pause(0.05)