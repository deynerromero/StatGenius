"""
Core SPC statistical calculations
"""
import numpy as np
import pandas as pd
from scipy import stats


class SPCAnalyzer:
    """Main class for SPC analysis"""
    
    def __init__(self, data: pd.DataFrame, subgroup_size: int = 1):
        """
        Initialize SPC Analyzer
        
        Parameters:
        -----------
        data : pd.DataFrame
            Data with measurements
        subgroup_size : int
            Number of observations per subgroup (n)
        """
        self.data = data
        self.n = subgroup_size
        self.results = {}
        
    def analyze(self) -> dict:
        """Run complete SPC analysis"""
        return {
            "normality": self.test_normality(),
            "randomness": self.test_randomness(),
            "descriptive": self.get_descriptive_stats(),
        }
    
    def test_normality(self) -> dict:
        """
        Test for normality using Shapiro-Wilk and Anderson-Darling
        
        Returns:
        --------
        dict : Results with p-values and interpretations
        """
        data = self.data.iloc[:, 0].values  # Take first column
        
        # Shapiro-Wilk test
        shapiro_stat, shapiro_p = stats.shapiro(data)
        
        # Anderson-Darling test
        anderson_result = stats.anderson(data, dist='norm')
        anderson_stat = anderson_result.statistic
        anderson_crit = anderson_result.critical_values[2]  # 5% significance
        
        return {
            "shapiro_wilk": {
                "statistic": float(shapiro_stat),
                "p_value": float(shapiro_p),
                "passes": shapiro_p > 0.05,
            },
            "anderson_darling": {
                "statistic": float(anderson_stat),
                "critical_value": float(anderson_crit),
                "passes": anderson_stat < anderson_crit,
            },
            "overall_normal": shapiro_p > 0.05 and anderson_stat < anderson_crit,
        }
    
    def test_randomness(self) -> dict:
        """
        Test for randomness/independence using manual runs test implementation
        
        Returns:
        --------
        dict : Results with p-values and interpretations
        """
        data = self.data.iloc[:, 0].values
        median = np.median(data)
        
        # Count runs
        above_median = (data > median).astype(int)
        runs = np.sum(np.abs(np.diff(above_median))) + 1
        
        n1 = np.sum(above_median)  # Number above median
        n2 = len(data) - n1  # Number below median
        
        # Expected number of runs and variance
        expected_runs = (2 * n1 * n2) / (n1 + n2) + 1
        var_runs = (2 * n1 * n2 * (2 * n1 * n2 - n1 - n2)) / ((n1 + n2) ** 2 * (n1 + n2 - 1))
        
        # Z-statistic
        if var_runs > 0:
            z_stat = (runs - expected_runs) / np.sqrt(var_runs)
            p_value = 2 * (1 - stats.norm.cdf(np.abs(z_stat)))
        else:
            z_stat = 0.0
            p_value = 1.0
        
        return {
            "z_statistic": float(z_stat),
            "p_value": float(p_value),
            "passes": p_value > 0.05,
            "interpretation": "Random (independent)" if p_value > 0.05 else "Not random (dependent)",
        }
    
    def get_descriptive_stats(self) -> dict:
        """Calculate basic descriptive statistics"""
        data = self.data.iloc[:, 0].values
        
        return {
            "mean": float(np.mean(data)),
            "std_dev": float(np.std(data, ddof=1)),
            "min": float(np.min(data)),
            "max": float(np.max(data)),
            "median": float(np.median(data)),
            "cv": float(np.std(data, ddof=1) / np.mean(data) if np.mean(data) != 0 else 0),
        }


def calculate_control_limits(
    data: np.ndarray,
    chart_type: str = "xbar-r",
    alpha: float = 0.0027,
    subgroup_size: int = None,
) -> dict:
    """
    Calculate control limits for different chart types
    
    Parameters:
    -----------
    data : np.ndarray
        Process measurements
    chart_type : str
        Type of chart: 'xbar-r', 'xbar-s', 'i-mr'
    alpha : float
        Risk of false alarm (default: 0.0027 ≈ 3-sigma)
    subgroup_size : int
        Size of subgroups
        
    Returns:
    --------
    dict : Control limits and related statistics
    """
    z_critical = stats.norm.ppf(1 - alpha / 2)
    
    if chart_type == "i-mr":
        # Individual-Moving Range chart
        individuals = data
        moving_range = np.abs(np.diff(individuals))
        
        mr_bar = np.mean(moving_range)
        d2 = 1.128  # Constant for n=2
        sigma_hat = mr_bar / d2
        
        xbar = np.mean(individuals)
        
        lcl = xbar - z_critical * sigma_hat
        ucl = xbar + z_critical * sigma_hat
        
        return {
            "lcl": float(lcl),
            "center": float(xbar),
            "ucl": float(ucl),
            "sigma_estimated": float(sigma_hat),
            "observations": len(individuals),
            "chart_type": "I-MR",
        }
    
    elif chart_type == "xbar-r" and subgroup_size:
        # Xbar-R chart
        n_subgroups = len(data) // subgroup_size
        reshaped = data[: n_subgroups * subgroup_size].reshape(-1, subgroup_size)
        
        xbar_vals = np.mean(reshaped, axis=1)
        r_vals = np.max(reshaped, axis=1) - np.min(reshaped, axis=1)
        
        xbar_bar = np.mean(xbar_vals)
        r_bar = np.mean(r_vals)
        
        # Constants for Xbar-R
        d2_dict = {2: 1.128, 3: 1.693, 4: 2.059, 5: 2.326, 6: 2.534}
        d2 = d2_dict.get(subgroup_size, 1.128)
        d3_dict = {2: 0.853, 3: 0.888, 4: 0.880, 5: 0.864, 6: 0.848}
        d3 = d3_dict.get(subgroup_size, 0.853)
        
        sigma_hat = r_bar / d2
        a2_dict = {2: 1.880, 3: 1.023, 4: 0.729, 5: 0.577, 6: 0.483}
        a2 = a2_dict.get(subgroup_size, 1.880)
        
        xbar_lcl = xbar_bar - a2 * r_bar
        xbar_ucl = xbar_bar + a2 * r_bar
        
        r_lcl = max(0, d3 * r_bar)
        r_ucl = (2 - d3) * r_bar
        
        return {
            "xbar": {
                "lcl": float(xbar_lcl),
                "center": float(xbar_bar),
                "ucl": float(xbar_ucl),
            },
            "r": {
                "lcl": float(r_lcl),
                "center": float(r_bar),
                "ucl": float(r_ucl),
            },
            "sigma_estimated": float(sigma_hat),
            "subgroup_size": subgroup_size,
            "number_of_subgroups": n_subgroups,
            "chart_type": "Xbar-R",
        }
    
    return {}


def calculate_process_capability(
    data: np.ndarray,
    lsl: float = None,
    usl: float = None,
    sigma: float = None,
) -> dict:
    """
    Calculate process capability indices (Cp, Cpk, Pp, Ppk)
    
    Parameters:
    -----------
    data : np.ndarray
        Process measurements
    lsl : float
        Lower specification limit
    usl : float
        Upper specification limit
    sigma : float
        Process standard deviation (if None, estimated from data)
        
    Returns:
    --------
    dict : Capability indices and metrics
    """
    if sigma is None:
        sigma = np.std(data, ddof=1)
    
    mean = np.mean(data)
    
    results = {"mean": float(mean), "sigma": float(sigma)}
    
    if lsl is not None and usl is not None:
        # Cp - potential capability
        cp = (usl - lsl) / (6 * sigma)
        results["cp"] = float(cp)
        
        # Cpk - actual capability
        cpk_lower = (mean - lsl) / (3 * sigma) if mean != lsl else 0
        cpk_upper = (usl - mean) / (3 * sigma) if usl != mean else 0
        cpk = min(cpk_lower, cpk_upper)
        results["cpk"] = float(cpk)
        
        # Probability of non-conformance
        if cpk > 0:
            p_lower = stats.norm.cdf((lsl - mean) / sigma)
            p_upper = 1 - stats.norm.cdf((usl - mean) / sigma)
            p_nonconform = p_lower + p_upper
            results["prob_nonconforming"] = float(p_nonconform)
        
    # Pp and Ppk (using sample std for overall performance)
    pp = (usl - lsl) / (6 * sigma) if (lsl and usl) else None
    if pp:
        results["pp"] = float(pp)
    
    return results


def calculate_power_and_arl(
    delta: float,
    n: int = 1,
    alpha: float = 0.0027,
    chart_type: str = "individuals",
) -> dict:
    """
    Calculate power, ARL₀, ARL₁ for shift detection
    
    Parameters:
    -----------
    delta : float
        Shift size in sigma units
    n : int
        Sample size
    alpha : float
        Type I error rate
    chart_type : str
        Type of control chart
        
    Returns:
    --------
    dict : Power, ARL₀, ARL₁, and time to detection
    """
    # For individuals chart (n=1)
    z_critical = stats.norm.ppf(1 - alpha / 2)
    
    # Power calculation: P(detect shift)
    # Non-centrality parameter
    lambda_nc = abs(delta) * np.sqrt(n)
    
    # Power ≈ P(Z > z_critical - lambda_nc) + P(Z < -z_critical - lambda_nc)
    power = 2 * (1 - stats.norm.cdf(z_critical - lambda_nc))
    
    # ARL₀ (no shift)
    arl0 = 1 / alpha
    
    # ARL₁ (with shift)
    if power > 0 and power < 1:
        arl1 = 1 / power
    else:
        arl1 = 1  # Perfect detection
    
    return {
        "delta": float(delta),
        "power": float(power),
        "arl0": float(arl0),
        "arl1": float(arl1),
        "z_critical": float(z_critical),
        "n": int(n),
    }
