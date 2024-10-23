import numpy as np

class GeometricBrownianMotion:
    def __init__(self, mu, sigma, T=50, steps=1000):
        self.mu = mu
        self.sigma = sigma
        self.T = T
        self.steps = steps

    def simulate_paths(self):
        dt = 1  # step size (1 year)
        S = np.zeros((self.steps, self.T + 1))
        S[:, 0] = 1  # start with initial investment of 1 unit
        for t in range(1, self.T + 1):
            Z = np.random.standard_normal(self.steps)  # random noise
            S[:, t] = S[:, t - 1] * np.exp((self.mu - 0.5 * self.sigma ** 2) * dt + self.sigma * np.sqrt(dt) * Z)
        return S

    def estimate_loss_probability(self):
        paths = self.simulate_paths()
        loss_probabilities = []
        for t in range(5, self.T + 1):
            losses = paths[:, t] < paths[:, t - 5]
            loss_probability = np.mean(losses)
            loss_probabilities.append(loss_probability)
        return loss_probabilities

def main():
    # Portfolio A
    portfolio_A = GeometricBrownianMotion(mu=0.06, sigma=0.10)
    loss_prob_A = portfolio_A.estimate_loss_probability()

    # Portfolio B
    portfolio_B = GeometricBrownianMotion(mu=0.08, sigma=0.16)
    loss_prob_B = portfolio_B.estimate_loss_probability()

    return loss_prob_A, loss_prob_B


loss_probabilities_A, loss_probabilities_B = main()

total_sumA = sum(loss_probabilities_A)
total_sumB = sum(loss_probabilities_B)
# Calculate average
averageA = total_sumA / len(loss_probabilities_A)
averageB = total_sumB / len(loss_probabilities_B)

print("Portfolio A Loss Probabilities:", loss_probabilities_A)
print("Portfolio B Loss Probabilities:", loss_probabilities_B)
print(averageA)
print(averageB)


import matplotlib.pyplot as plt

# Data
years = range(5, 51)  # Assuming you start from year 5
array1 = loss_probabilities_A
array2 = loss_probabilities_B

# Plotting
plt.plot(years, array1, label='Array 1')
plt.plot(years, array2, label='Array 2')

# Add labels and title
plt.xlabel('Year')
plt.ylabel('Values')
plt.title('Arrays Over Time')

# Set x-axis ticks with a step of 1
plt.xticks(range(5, 51, 5))

# Add legend
plt.legend()

# Show the plot
plt.show()


















