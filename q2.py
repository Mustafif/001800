import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import pandas as pd

def theoretical_var_es_exponential(lambda_param, alpha):
    """Calculate theoretical VaR and ES for exponential distribution"""
    var = -np.log(1 - alpha) / lambda_param
    es = var + 1/lambda_param
    return var, es

def parametric_normal_var_es(data, alpha):
    """Calculate VaR and ES assuming normal distribution"""
    mu = np.mean(data)
    sigma = np.std(data)
    var = stats.norm.ppf(alpha, mu, sigma)
    es = mu + sigma * stats.norm.pdf(stats.norm.ppf(alpha)) / (1 - alpha)
    return var, es

def empirical_var_es(data, alpha):
    """Calculate empirical VaR and ES"""
    var = np.percentile(data, alpha * 100)
    es = np.mean(data[data > var])
    return var, es

def run_analysis(N, lambda_param=4, alpha=0.99):
    """Run complete analysis for a given sample size"""
    # Generate exponential data
    np.random.seed(42)  # For reproducibility
    data = np.random.exponential(scale=1/lambda_param, size=N)

    # Get theoretical values
    theo_var, theo_es = theoretical_var_es_exponential(lambda_param, alpha)

    # Get parametric estimates (assuming normal)
    param_var, param_es = parametric_normal_var_es(data, alpha)

    # Get empirical estimates
    emp_var, emp_es = empirical_var_es(data, alpha)

    # Calculate absolute errors
    param_var_error = abs(param_var - theo_var)
    param_es_error = abs(param_es - theo_es)
    emp_var_error = abs(emp_var - theo_var)
    emp_es_error = abs(emp_es - theo_es)

    results = {
        'Sample Size': N,
        'Theoretical VaR': theo_var,
        'Theoretical ES': theo_es,
        'Parametric VaR': param_var,
        'Parametric ES': param_es,
        'Empirical VaR': emp_var,
        'Empirical ES': emp_es,
        'Parametric VaR Error': param_var_error,
        'Parametric ES Error': param_es_error,
        'Empirical VaR Error': emp_var_error,
        'Empirical ES Error': emp_es_error
    }

    # Plotting the results
    plt.figure(figsize=(10, 6))

    # Histogram of data
    plt.subplot(2, 2, 1)
    plt.hist(data, bins=30, density=True, alpha=0.6, color='skyblue')
    plt.title(f"Histogram of Exponential Data (N={N})")
    plt.xlabel('Value')
    plt.ylabel('Density')

    # Theoretical VaR and ES
    plt.subplot(2, 2, 2)
    x = np.linspace(0, np.max(data), 1000)
    y_theoretical = lambda_param * np.exp(-lambda_param * x)
    plt.plot(x, y_theoretical, label="Exponential PDF", color='blue')
    plt.axvline(theo_var, color='red', linestyle='dashed', label=f'Theoretical VaR ({theo_var:.2f})')
    plt.axvline(theo_es, color='green', linestyle='dashed', label=f'Theoretical ES ({theo_es:.2f})')
    plt.title(f"Theoretical VaR and ES")
    plt.xlabel('Value')
    plt.ylabel('Density')
    plt.legend()

    # Parametric VaR and ES
    plt.subplot(2, 2, 3)
    plt.axvline(param_var, color='red', linestyle='dashed', label=f'Parametric VaR ({param_var:.2f})')
    plt.axvline(param_es, color='green', linestyle='dashed', label=f'Parametric ES ({param_es:.2f})')
    plt.hist(data, bins=30, density=True, alpha=0.6, color='skyblue')
    plt.title(f"Parametric VaR and ES")
    plt.xlabel('Value')
    plt.ylabel('Density')
    plt.legend()

    # Empirical VaR and ES
    plt.subplot(2, 2, 4)
    plt.axvline(emp_var, color='red', linestyle='dashed', label=f'Empirical VaR ({emp_var:.2f})')
    plt.axvline(emp_es, color='green', linestyle='dashed', label=f'Empirical ES ({emp_es:.2f})')
    plt.hist(data, bins=30, density=True, alpha=0.6, color='skyblue')
    plt.title(f"Empirical VaR and ES")
    plt.xlabel('Value')
    plt.ylabel('Density')
    plt.legend()

    # Adjust layout and show/save the plot
    plt.tight_layout()
    plt.savefig(f'var_es_plots_N_{N}.png', dpi=300, bbox_inches='tight')
    plt.show()
    plt.close()

    return pd.DataFrame([results])

# Run analysis for different sample sizes
sample_sizes = [10**6, 10**7, 10**8]
results = pd.DataFrame()

for N in sample_sizes:
    result = run_analysis(N)
    results = pd.concat([results, result], ignore_index=True)

print("\nResults for all sample sizes:")
print(results.to_string())
