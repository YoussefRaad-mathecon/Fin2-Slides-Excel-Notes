import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import binom

# Parameters
horizon = 30
u = 1.29
d = 0.85
R = 1.04
p = 0.5

# Expected beta function
def E_beta(beta):
    return p * np.log(beta * (u - R) + R) + (1 - p) * np.log(beta * (d - R) + R)

# Calculate beta.hat
beta_hat = R * (p * u + (1 - p) * d - R) / ((u - R) * (R - d))

# Indirect utility function
def IndirectUtility(w):
    return np.log(w) + horizon * E_beta(beta_hat)

# Expected buy and hold utility function
def E_buyNhold(alpha):
    result = 0
    for i in range(horizon + 1):
        prob = binom.pmf(i, horizon, p)
        result += prob * np.log(alpha * u**i * d**(horizon - i) + (1 - alpha) * R**horizon)
    return result

# Generate y values
y = np.linspace(0, 1, 101)

# Compute the difference between buy-and-hold and best fixed-fraction dynamic
differences = [E_buyNhold(alpha) - horizon * E_beta(beta_hat) for alpha in y]

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(y, differences)
plt.ylim([-0.3, 0.1])
plt.xlabel("Fraction in stock, initially")
plt.ylabel("E(U(buy-and-hold)) - E(U(best fixed-fraction dynamic))")
plt.axhline(0, linestyle='--')

# Highlight the optimal alpha
optimal_alpha = y[np.argmax([E_buyNhold(alpha) for alpha in y])]
plt.axvline(optimal_alpha, color='r')

# Calculate and display f
f = np.exp(horizon * E_beta(beta_hat) - max([E_buyNhold(alpha) for alpha in y])) - 1
print(f"f: {f}")

plt.show()
