import numpy as np
import matplotlib.pyplot as plt

""" # Define the sigmoid function
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

# Generate x values
x = np.linspace(-10, 10, 100)

# Compute y values using the sigmoid function
y = sigmoid(x)

# Plot the sigmoid function with thicker line and customized grid
plt.figure(figsize=(8, 6))
plt.plot(x, y, label='Sigmoid Function', color='blue', linewidth=3)  # Increase line width
plt.xlabel('x')
plt.ylabel('sigmoid(x)')
plt.title('Sigmoid Function')
#plt.grid(True, linestyle='--', alpha=0.7)  # Customized grid with dashed lines and transparency
plt.legend()
plt.show()
 """

# Define the step function
def step_function(x):
    return np.heaviside(x, 0.5)

# Generate x values
x = np.linspace(-5, 5, 100)

# Compute y values using the step function
y = step_function(x)

# Plot the step function
plt.figure(figsize=(8, 6))
plt.plot(x, y, label='Step Function', color='blue', linewidth=4)
plt.xlabel('x')
plt.ylabel('step_function(x)')
plt.title('Step Function')
#plt.grid(True)
plt.legend()
plt.show()
