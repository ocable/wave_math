import math
import requests
import re
import matplotlib.pyplot as plt
import numpy as np

from peakDetect import peakdet


class SwellComponent:
    def __init__(self, wave_height, period, max_energy, frequency_index):
        self.wave_height = wave_height
        self.period = period
        self.max_energy = max_energy
        self.frequency_index = frequency_index

response = requests.get('https://www.ndbc.noaa.gov/data/realtime2/44007.data_spec')

if response.status_code == 200:
    #splits response by line
    raw_data = response.text.split('\n')

    # Exctracts first number with decimal point
    seperation = re.findall(r'\d+\.\d+', raw_data[1])[0]

    all_nums = re.findall(r'\d+\.\d+(?!\s*\(\d+\.\d+\))', raw_data[1])[1:]

    frequencies = re.findall(r'\(([^)]+)\)', raw_data[1])

    # seperation  = float(seperation)
    densities = []

    for i, num in enumerate(all_nums):
        if i % 2 == 0:
            densities.append(float(num))


    frequencies = [float(frequency) for frequency in frequencies]
    periods = [1 / float(frequency) for frequency in frequencies]



else:
    print(f"Request failed with status code {response.status_code}")





# Plotting the data
fig, axs = plt.subplots(1,1)               # Create a figure containing a single Axes.
plt.plot(periods, densities, color = 'c', linewidth=1.5, label = 'Period (sec)') 
axs.set_xlabel('Period (sec)')             # Set the y-axis label
axs.set_ylabel('Density (m^2 / Hz)')       # Set the y-axis label
axs.set_title('Period vs Density')         # Set the title of the plot





M0 = np.trapz(densities, frequencies)
M2 = np.trapz(densities * np.square(frequencies), frequencies)
Hm0 = 4 * np.sqrt(M0)

print(f"M0: {M0}")
print(f"M2: {M2}")  
print(f"Hm0: {Hm0}")


def wave_summary(frequencies, densities):

    max_energy_index = -1
    max_energy = -1.0
    zero_moment = 0.0

    for i in range(0, len(frequencies)):
        bandwidth = 0.01
        if i > 0:
            bandwidth = abs(frequencies[i] - frequencies[i-1])
        else:
            bandwidth = abs(frequencies[i+1] - frequencies[i])

        zero_moment += densities[i] * bandwidth

        if densities[i] > max_energy:
            max_energy = densities[i]
            max_energy_index = i

    wave_height = 4.0 * math.sqrt(zero_moment)
    period = 1.0 / frequencies[max_energy_index]
    # primary_swell.direction = self.angle[max_energy_index]
    # primary_swell.compass_direction = degree_to_direction(primary_swell.direction)

    

    return wave_height, period, zero_moment, max_energy_index





def swell_components(frequencies, densities):

    min_indexes, min_values, max_indexes, max_values = peakdet(densities, 0.05)

    print("")
    print(f"Min Indexes: {min_indexes}")
    print(f"Min Values: {min_values}")
    print(f"Max Indexes: {max_indexes}")
    print(f"Max Values: {max_values}")

    components = []
    prev_index = 0

    for i in range(0, len(max_values)):
        min_index = prev_index
        if i >= len(min_indexes):
            min_index = len(frequencies)
        else:
            min_index = min_indexes[i]

        zero_moment = 0.0
        for j in range(prev_index, min_index):
            bandwidth = 0.01
            if j > 0:
                bandwidth = abs(frequencies[j] - frequencies[j-1])
            else:
                bandwidth = abs(frequencies[j+1] - frequencies[j])

            zero_moment += densities[j] * bandwidth

        
        wave_height = 4.0 * math.sqrt(zero_moment)
        period = 1.0 / frequencies[max_indexes[i]]
        # component.direction = self.angle[max_indexes[i]]
        # component.compass_direction = degree_to_direction(component.direction)
        max_energy = max_values[i]
        frequency_index = max_indexes[i]

        component = SwellComponent(wave_height, period, max_energy, frequency_index)

        components.append(component)

        prev_index = min_index

    components.sort(key=lambda x: x.max_energy, reverse=True)
    return components




wave_height, period, zero_moment, max_energy_index = wave_summary(frequencies, densities)

components = swell_components(frequencies, densities)


# print(seperation)
# print(raw_data[1])
# print(densities)
# print(len(densities))
# print(frequencies)
# print(len(frequencies))

print("")
print(f"Wave Height: {wave_height}")
print(f"Max energy index: {max_energy_index}")
print(f"Period: {period}")
print(f"Zero Moment: {zero_moment}")
print("")

for component in components:
    print(f"Wave Height: {component.wave_height}")
    print(f"Period: {component.period}")
    # print(f"Max Energy: {component.max_energy}")
    # print(f"Frequency Index: {component.frequency_index}")

plt.show()

