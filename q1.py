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
VaR99_theo = mu + sigma * norm.ppf(alpha)
ES99_theo = mu + sigma * (norm.pdf(norm.ppf(alpha)) / (1 - alpha))

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
        VaR99_param = mean + std * norm.ppf(alpha)
        ES99_param = mean + std * (norm.pdf(norm.ppf(alpha)) / (1 - alpha))
    else:
        VaR99_param = None
        ES99_param = None

    # b) Empirical estimates
    # Empirical estimates
    VaR99_emp, ES99_emp = empirical_var_es(sample, alpha)

    # c) Compute the absolute errors and compare with true values in the results
    # Compute absolute errors
    abs_error_parametric = (abs(VaR99_param - VaR99_theo), abs(ES99_param - ES99_theo)) if is_normal else (None, None)
    abs_error_param_perc = (abs_error_parametric[0] / VaR99_theo)*100, (abs_error_parametric[1] / ES99_theo)*100 if is_normal else (None, None)
    abs_error_empirical = (abs(VaR99_emp - VaR99_theo), abs(ES99_emp - ES99_theo))
    abs_error_empirical_perc = (abs_error_empirical[0] / VaR99_theo)*100, (abs_error_empirical[1] / ES99_theo)*100

    # Store results
    results[N] = {
        "data": sample,
        "VaR99_param": VaR99_param,
        "ES99_param": ES99_param,
        "VaR99_emp": VaR99_emp,
        "ES99_emp": ES99_emp,
        "abs_error_parametric": abs_error_parametric,
        "abs_error_empirical": abs_error_empirical,
        "abs_error_empirical_perc": abs_error_empirical_perc,
        "abs_error_param_perc": abs_error_param_perc,
        "is_normal": is_normal
    }

# Print results
for N, res in results.items():
    print(f"N = {N}")
    print(f"  Normality confirmed: {res['is_normal']}")
    print(f"  VaR_99 Parametric: {res['VaR99_param']:.4}, Abs Error: {res['abs_error_parametric'][0]:.2e}")
    print(f"  ES_99 Parametric: {res['ES99_param']:.4}, Abs Error: {res['abs_error_parametric'][1]:.2e}")
    print(f"  VaR_99 Empirical: {res['VaR99_emp']:.4}, Abs Error: {res['abs_error_empirical'][0]:.2e}")
    print(f"  ES_99 Empirical: {res['ES99_emp']:.4}, Abs Error: {res['abs_error_empirical'][1]:.2e}")
    print("-")
    print("Percentages:")
    print(f"  VaR_99 Parametric: {res['abs_error_param_perc'][0]:.2%}")
    print(f"  ES_99 Parametric: {res['abs_error_param_perc'][1]:.2%}")
    print(f"  VaR_99 Empirical: {res['abs_error_empirical_perc'][0]:.2%}")
    print(f"  ES_99 Empirical: {res['abs_error_empirical_perc'][1]:.2%}")

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
