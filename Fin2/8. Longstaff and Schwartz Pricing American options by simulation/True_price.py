import numpy as np

# Parameters
S0 = 40
capT = 1
r = 0.06
sigma = 0.20
strike = 1.1

n = int(capT * 50)
m = 1
dt = capT / n

u = np.exp(sigma * np.sqrt(dt))
d = np.exp(-sigma * np.sqrt(dt))
R = np.exp(r * dt)
q = (R - d) / (u - d)

# Payoff for put option at maturity
PutB = np.maximum(strike - S0 * u ** np.arange(n + 1) * d ** np.arange(n, -1, -1), 0)

# Backward induction
for i in range(n, 0, -1):
    St = S0 * u ** np.arange(i) * d ** np.arange(i - 1, -1, -1)
    dummy = np.maximum(strike - St, 0) * (i % m == 0)
    temp = np.maximum((q * PutB[1:i+1] + (1 - q) * PutB[:i]) / R, dummy)
    PutB = temp

print(round(PutB[0], 5))
print(dt)