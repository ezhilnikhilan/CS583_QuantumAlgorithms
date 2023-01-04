import seaborn as sns
import matplotlib.pyplot as plt

rec = {0: 100.0, 1: 100.0, 2: 55.90, 3: 35.88, 4: 23.93, 5: 22.58, 6: 23.69, 7: 26.61, 8: 26.49, 9: 20.47}
qubs = {0: 35980, 1: 36005, 2: 35912, 3: 36063, 4: 36092, 5: 36011, 6: 36177, 7: 36050, 8: 35823}
probs_9 = {0.000: 100.0, 0.025: 99.3, 0.050: 96.5, 0.075: 93.0, 0.100: 88.6, 0.125: 84.2, 0.150: 80.0, 0.175: 72.1, 0.2: 71.0, 0.225: 64.4, 0.250: 58.3, 0.275: 53.9, 0.300: 51.2}
probs_7 = {0.0: 100.0, 0.025: 99.4, 0.05: 97.7, 0.075: 94.8, 0.1: 94.8, 0.125: 90.9, 0.15: 83.89999999999999, 0.175: 80.2, 0.2: 78.4, 0.225: 73.9, 0.25: 69.1, 0.275: 67.80000000000001, 0.3: 63.3}
probs_5 = {0.0: 100.0, 0.025: 99.6, 0.05: 99.1, 0.075: 98.0, 0.1: 96.39999999999999, 0.125: 94.69999999999999, 0.15: 92.4, 0.175: 88.4, 0.2: 88.0, 0.225: 85.0, 0.25: 82.19999999999999, 0.275: 78.60000000000001, 0.3: 75.9}

plt.xlabel("Probability of error on individual qubit")
plt.ylabel("% of corrected errors")
plt.title("p vs % of corrected errors")
plt.plot(probs_9.keys(), probs_9.values())
plt.plot(probs_7.keys(), probs_7.values())
plt.plot(probs_5.keys(), probs_5.values())
plt.legend(["Error acting on 9 qubits", "Error acting on 7 qubits", "Error acting on 5 qubits"])
#plt.xticks(probs.keys())
plt.show()