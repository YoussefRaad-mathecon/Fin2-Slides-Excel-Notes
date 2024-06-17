import numpy as np
import matplotlib.pyplot as plt

# From ROLF
EXAMPLE = np.array([
    [1, 1.09, 1.08, 1.34],
    [1, 1.16, 1.26, 1.54],
    [1, 1.22, 1.07, 1.03],
    [1, 0.93, 0.97, 0.92],
    [1, 1.11, 1.56, 1.52],
    [1, 0.76, 0.77, 0.90],
    [1, 0.92, 0.84, 1.01],
    [1, 0.88, 1.22, 1.34]
])
paths = 8
steps = 4
strike = 1.1
startprice = 1
r = 0.06
dt = 1
disc = np.exp(dt * r * -np.arange(1, steps))
P = np.zeros((paths, steps))
S = EXAMPLE




# cashflow at T
for j in range(paths):
    P[j, steps - 1] = max(strike - S[j, steps - 1], 0)

# LSM
for h in range(steps - 2, 0, -1):
    Y = np.zeros(paths) 
    pick = strike - S[:, h] > 0
    for j in range(paths):
        Y[j] = np.sum(disc[:steps - h - 1] * P[j, h + 1:steps])
    Y = Y[pick]
    dummy = S[pick, h]
    X = np.column_stack((np.ones(len(dummy)), dummy, dummy**2)) 
    b = np.linalg.lstsq(X, Y, rcond=None)[0]
    
    for j in range(paths):
        if pick[j] and np.dot([1, S[j, h], S[j, h]**2], b) < max(strike - S[j, h], 0):
            P[j, h] = max(strike - S[j, h], 0)
            P[j, h + 1:steps] = 0

Z = np.zeros(paths)
for j in range(paths):
    Z[j] = np.sum(disc * P[j, 1:steps])
mean_Z = np.mean(Z)
print(f'Mean Value of AMR Option: {mean_Z}')




# stock prices
plt.figure(figsize=(12, 6))
for i in range(paths):
    plt.plot(range(steps), S[i], marker='o', label=f'Path {i+1}')
plt.title('Simulated Paths of Asset Prices')
plt.xlabel('Time Steps')
plt.ylabel('Asset Price')
plt.axhline(y=strike, color='r', linestyle='--', label='Strike Price')
plt.legend()
plt.grid(True)
plt.xticks([0, 1, 2, 3])
plt.show()

# cashflows
plt.figure(figsize=(12, 6))
for i in range(paths):
    plt.plot(range(steps), P[i], marker='o', label=f'Path {i+1}')
plt.title('Cashflows of AMR Option')
plt.xlabel('Time Steps')
plt.ylabel('Cashflow')
plt.grid(True)
plt.legend()
plt.xticks([0, 1, 2, 3])
plt.show()

