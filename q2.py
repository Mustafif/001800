import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import norm

def theoretical_var_es_exponential(lambda_param, alpha):
    """Calculate theoretical VaR and ES for exponential distribution"""
    var = -np.log(1 - alpha) / lambda_param
    es = var + 1/lambda_param
    return var, es

# 2/3 a)
def parametric_normal_var_es(data, alpha):
    """Calculate VaR and ES assuming normal distribution"""
    mu = np.mean(data)
    sigma = np.std(data)
    var = norm.ppf(alpha, mu, sigma)
    es = mu + sigma * norm.pdf(norm.ppf(alpha)) / (1 - alpha)
    return var, es
# 2/3 b)
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

    # 2/3 c)
    # Calculate absolute errors
    # We have also calculated the absolute percentage errors as well
    param_var_error = abs(param_var - theo_var)
    param_es_error = abs(param_es - theo_es)
    emp_var_error = abs(emp_var - theo_var)
    emp_es_error = abs(emp_es - theo_es)
    param_var_error_perc = (param_var_error / theo_var) * 100
    param_es_error_perc = (param_es_error / theo_es) * 100
    emp_var_error_perc = (emp_var_error / theo_var) * 100
    emp_es_error_perc = (emp_es_error / theo_es) * 100

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
        'Empirical ES Error': emp_es_error,
        'Parametric VaR Error (%)': param_var_error_perc,
        'Parametric ES Error (%)': param_es_error_perc,
        'Empirical VaR Error (%)': emp_var_error_perc,
        'Empirical ES Error (%)': emp_es_error_perc
    }

# Plotting the results
    plt.figure(figsize=(10, 6))
    plt.hist(data, bins=30, density=True, alpha=0.6, color='skyblue', label='Data Distribution')

    plt.title(f"Distribution with VaR and ES Estimates (N={N})")
    plt.xlabel('Value')
    plt.ylabel('Density')
    plt.legend()
    plt.tight_layout()
    plt.savefig(f'var_es_plots_N_{N}.png', dpi=300, bbox_inches='tight')
    #plt.show()
    plt.close()

    return pd.DataFrame([results])

# Completing 2/3 samples sizes
# Run analysis for the different sample sizes
sample_sizes = [10**6, 10**7, 10**8]
results = pd.DataFrame()
for N in sample_sizes:
    result = run_analysis(N)
    results = pd.concat([results, result], ignore_index=True)

print("\nResults for all sample sizes:")
print(results.to_string())
