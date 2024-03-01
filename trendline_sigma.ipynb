import numpy as np
from scipy.stats import linregress
import matplotlib.pyplot as plt

# Generate some synthetic data
np.random.seed(0)  
x = np.arange(1, 101)
y = 2.5 * x + np.random.normal(0, 20, 100)  # y = mx + b + noise

# Perform linear regression
slope, intercept, r_value, p_value, std_err = linregress(x, y)

# Calculate the regression line "predictions"
y_pred = slope * x + intercept

# Calculate residuals
residuals = y - y_pred

# Calculate the standard deviation of the residuals
residuals_std = np.std(residuals)

# Calculate the 3 sigma lines
y_pred_plus_3sigma = y_pred + 3 * residuals_std
y_pred_minus_3sigma = y_pred - 3 * residuals_std

# Re-plotting the data, regression line, and now the 3 sigma lines
plt.figure(figsize=(6, 4))
plt.scatter(x, y, label='Data Points')
plt.plot(x, y_pred, color='red', label=f'Trendline\ny={slope:.2f}x+{intercept:.2f}')
plt.plot(x, y_pred_plus_3sigma, 'g--', label='+3 Sigma')
plt.plot(x, y_pred_minus_3sigma, 'b--', label='-3 Sigma')

# Customize plot
plt.title('Linear Regression with 3 Sigma Borders')
plt.xlabel('X')
plt.ylabel('Y')
plt.legend()
plt.grid(True)

# Show plot
plt.show()

# Display the standard deviation of the residuals
residuals_std
