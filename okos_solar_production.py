import numpy as np
import random

def simulate_cloudy_periods(solar_production, total_samples, num_periods=3, max_drop_percentage=0.5):
    """
    Simulates random cloudy periods by reducing the solar production randomly
    for a specified number of periods and by a maximum drop percentage.
    """
    modified_production = solar_production.copy()
    for _ in range(num_periods):
        # Randomly choose a start time for the cloudy period
        start_sample = random.randint(0, total_samples - 1)
        # Randomly determine the duration of the cloudy period (in samples)
        duration = random.randint(total_samples // 20, total_samples // 10)
        # Randomly determine the drop percentage for this cloudy period
        drop_percentage = random.uniform(0.1, max_drop_percentage)
        # Apply the drop in production for the duration of the cloudy period
        end_sample = min(start_sample + duration, total_samples)
        modified_production[start_sample:end_sample] *= (1 - drop_percentage)
    return modified_production

# # Apply random cloudy periods to the solar production
# solar_production_with_clouds = simulate_cloudy_periods(solar_production_normalized, total_samples)

def adjust_for_sunrise_sunset(time, production, sunrise, sunset):
    """
    Adjusts the solar production to be zero before sunrise and after sunset.
    """
    adjusted_production = production.copy()
    for i, t in enumerate(time):
        if t < sunrise or t > sunset:
            adjusted_production[i] = 0
    return adjusted_production

def get_solar_production_with_clouds_absolute(sunrise=6, sunset=21, hours=24, samples_per_hour=4, total_capacity_pv=10):
	total_samples = hours * samples_per_hour

	# Time array representing each sample in the day
	time = np.linspace(0, hours, total_samples)

	# Parameters for the Gaussian function
	mean = hours / 2  # Peak production at midday
	std_dev = hours / 6  # Standard deviation to control the "width" of the sunlight hours

	# Gaussian function to simulate solar production
	solar_production = np.exp(-((time - mean) ** 2) / (2 * std_dev ** 2))

	# Normalize to simulate a maximum production capacity (e.g., 100%)
	solar_production_normalized = solar_production / max(solar_production)

	# Original solar production without cloudy periods for reference
	solar_production = np.exp(-((time - mean) ** 2) / (2 * std_dev ** 2))
	solar_production_normalized = solar_production / max(solar_production)
	solar_production_adjusted = adjust_for_sunrise_sunset(time, solar_production_normalized, sunrise, sunset)

	# Apply random cloudy periods to the adjusted solar production
	solar_production_with_clouds_adjusted = simulate_cloudy_periods(solar_production_adjusted, total_samples)
	lost_capacity = (solar_production_adjusted - solar_production_with_clouds_adjusted) * 100

	# Adjust solar production to absolute values based on total capacity
	solar_production_absolute = solar_production_adjusted * total_capacity_pv
	solar_production_with_clouds_absolute = solar_production_with_clouds_adjusted * total_capacity_pv
	# Calculate the lost capacity due to cloudy periods in absolute values (kW)
	lost_capacity_absolute = solar_production_absolute - solar_production_with_clouds_absolute
	return solar_production_with_clouds_absolute



def plot_absolute():
	import matplotlib.pyplot as plt
	# Plot the adjusted solar production curve with cloudy periods in absolute values
	plt.figure(figsize=(12, 7))
	plt.subplot(2, 1, 1)  # First plot
	plt.plot(time, solar_production_absolute, label='Adjusted Solar Production without Clouds (kW)', alpha=0.5)
	plt.plot(time, solar_production_with_clouds_absolute, label='Adjusted Solar Production with Clouds (kW)', color='red')
	plt.axvline(x=sunrise, color='grey', linestyle='--', label='Sunrise')
	plt.axvline(x=sunset, color='grey', linestyle='--', label='Sunset')
	plt.xlabel('Time of Day (Hours)')
	plt.ylabel('Production Capacity (kW)')
	plt.title('Simulated Solar Production over One Day with Sunrise and Sunset (Absolute Values)')
	plt.grid(True)
	plt.legend()

	# Plot showing only the lost capacity due to cloudy periods in absolute values
	plt.subplot(2, 1, 2)  # Second plot
	plt.fill_between(time, 0, lost_capacity_absolute, color='orange', label='Lost Capacity due to Clouds (kW)')
	plt.xlabel('Time of Day (Hours)')
	plt.ylabel('Lost Capacity (kW)')
	plt.title('Lost Solar Production Capacity due to Cloudy Periods (Absolute Values)')
	plt.grid(True)
	plt.legend()

	plt.tight_layout()
	plt.show()

