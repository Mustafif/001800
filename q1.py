from scipy.stats import norm
import numpy as np
from scipy.stats import shapiro, kstest
import matplotlib.pyplot as plt

# Given parameters
mu = 2
sigma = 3
alpha = 0.99
# we will loop through all sample sizes provided 2-3)
sample_sizes = [10**6, 10**7, 10**8]

# Theoretical values as calculated in 1)
VaR_99_theoretical = mu + sigma * norm.ppf(alpha)
ES_99_theoretical = mu + sigma * (norm.pdf(norm.ppf(alpha)) / (1 - alpha))

# Function to compute empirical VaR and ES
# As defined in Lecture 5, the empiricial Var
# is defined by the 99th percentile of the sample
# The empirical ES is defined by the average of the values
# greater than or equal to the empirical Var
def empirical_var_es(data, alpha=0.99):
    var = np.percentile(data, alpha * 100)
    es = np.mean(data[data >= var])
    return var, es

# Run simulations
results = {}
for N in sample_sizes:
    np.random.seed(42)  # For reproducibility
    sample = np.random.normal(mu, sigma, N)

    # a) Standardizing the data and Testing for normality
    # Standardize the data
    mean = np.mean(sample)
    std = np.std(sample)
    standardized_sample = (sample - mean) / std

    # Test for normality
    stat1, p_value1 = kstest(standardized_sample, 'norm')
    stat2, p_value2 = shapiro(standardized_sample[:5000])  # Using subset due to Shapiro limit

    is_normal = p_value1 > 0.05 and p_value2 > 0.05

    # Parametric estimates (if normal)
    if is_normal:
        VaR_99_parametric = mean + std * norm.ppf(alpha)
        ES_99_parametric = mean + std * (norm.pdf(norm.ppf(alpha)) / (1 - alpha))
    else:
        VaR_99_parametric = None
        ES_99_parametric = None

    # b) Empirical estimates
    # Empirical estimates
    VaR_99_empirical, ES_99_empirical = empirical_var_es(sample, alpha)

    # c) Compute the absolute errors and compare with true values in the results
    # Compute absolute errors
    abs_error_parametric = (abs(VaR_99_parametric - VaR_99_theoretical), abs(ES_99_parametric - ES_99_theoretical)) if is_normal else (None, None)
    abs_error_empirical = (abs(VaR_99_empirical - VaR_99_theoretical), abs(ES_99_empirical - ES_99_theoretical))

    # Store results
    results[N] = {
        "data": sample,
        "VaR_99_parametric": VaR_99_parametric,
        "ES_99_parametric": ES_99_parametric,
        "VaR_99_empirical": VaR_99_empirical,
        "ES_99_empirical": ES_99_empirical,
        "abs_error_parametric": abs_error_parametric,
        "abs_error_empirical": abs_error_empirical,
        "is_normal": is_normal
    }

# Print results
for N, res in results.items():
    print(f"N = {N}")
    print(f"  Normality confirmed: {res['is_normal']}")
    print(f"  VaR_99 Parametric: {res['VaR_99_parametric']}, Abs Error: {res['abs_error_parametric'][0]}")
    print(f"  ES_99 Parametric: {res['ES_99_parametric']}, Abs Error: {res['abs_error_parametric'][1]}")
    print(f"  VaR_99 Empirical: {res['VaR_99_empirical']}, Abs Error: {res['abs_error_empirical'][0]}")
    print(f"  ES_99 Empirical: {res['ES_99_empirical']}, Abs Error: {res['abs_error_empirical'][1]}")
    print("-")

    # Normality check with histograms
    sample = results[N]['data']

    # Create the plot
    plt.figure(figsize=(8, 4))
    plt.hist(sample, bins=30, density=True, alpha=0.6, color='skyblue')
    plt.title(f'Normality Check for N={N}')
    plt.xlabel('Value')
    plt.ylabel('Density')
    plt.grid(True)
    plt.tight_layout()

    # Save the plot first
    plt.savefig(f'normality_check_{N}.png', dpi=300, bbox_inches='tight')

    # Show the plot
    plt.show()
    plt.close()

# Create figure with subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 12))

# Plot 1: VaR Comparison
var_empirical = [results[N]['VaR_99_empirical'] for N in sample_sizes]
var_parametric = [results[N]['VaR_99_parametric'] for N in sample_sizes]
var_theoretical = [VaR_99_theoretical] * len(sample_sizes)

x_pos = np.arange(len(sample_sizes))
width = 0.25

ax1.bar(x_pos - width, var_empirical, width, label='Empirical VaR', color='skyblue')
ax1.bar(x_pos, var_parametric, width, label='Parametric VaR', color='lightcoral')
ax1.bar(x_pos + width, var_theoretical, width, label='Theoretical VaR', color='lightgreen')

ax1.set_xticks(x_pos)
ax1.set_xticklabels([f'N=10^{int(np.log10(N))}' for N in sample_sizes])
ax1.set_title('VaR₀.₉₉ Comparison Across Sample Sizes')
ax1.set_ylabel('Value at Risk (VaR)')
ax1.legend()
ax1.grid(True)

# Plot 2: Absolute Errors
# This will help us visualize the effect on absolute errors as sample size increases
var_errors_empirical = [results[N]['abs_error_empirical'][0] for N in sample_sizes]
var_errors_parametric = [results[N]['abs_error_parametric'][0] for N in sample_sizes]
es_errors_empirical = [results[N]['abs_error_empirical'][1] for N in sample_sizes]
es_errors_parametric = [results[N]['abs_error_parametric'][1] for N in sample_sizes]

x_pos = np.arange(len(sample_sizes))
width = 0.2

ax2.bar(x_pos - 1.5*width, var_errors_empirical, width, label='VaR Empirical Error', color='skyblue')
ax2.bar(x_pos - 0.5*width, var_errors_parametric, width, label='VaR Parametric Error', color='lightcoral')
ax2.bar(x_pos + 0.5*width, es_errors_empirical, width, label='ES Empirical Error', color='lightgreen')
ax2.bar(x_pos + 1.5*width, es_errors_parametric, width, label='ES Parametric Error', color='lightpink')

ax2.set_xticks(x_pos)
ax2.set_xticklabels([f'N=10^{int(np.log10(N))}' for N in sample_sizes])
ax2.set_title('Absolute Errors Comparison')
ax2.set_ylabel('Absolute Error')
ax2.legend()
ax2.grid(True)
ax2.set_yscale('log')  # Using log scale to better show error differences

plt.tight_layout()

# Save the figure
filename = 'var_es_comparison.png'
plt.savefig(filename, dpi=300, bbox_inches='tight')
print(f"Plot saved as: {filename}")
