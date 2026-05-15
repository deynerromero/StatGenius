"""
Sample data generator for SPC application
"""
import numpy as np
import pandas as pd


def generate_sample_data():
    """Generate sample SPC data with shift at sample 15"""
    np.random.seed(42)
    
    # Process: mean = 100, sigma = 2
    # First 14 samples: normal
    # Samples 15-20: shifted up by 3 sigma
    
    data = []
    for i in range(20):
        if i < 14:
            # Normal process
            value = np.random.normal(100, 2)
        else:
            # Process shift
            value = np.random.normal(103, 2)  # Shift of 3 sigma
        data.append(value)
    
    return np.array(data)


def generate_subgrouped_data(n_subgroups: int = 20, subgroup_size: int = 5):
    """Generate data with subgroups"""
    np.random.seed(42)
    
    data = []
    for i in range(n_subgroups):
        if i < 14:
            # Normal process
            subgroup = np.random.normal(100, 2, subgroup_size)
        else:
            # Process shift
            subgroup = np.random.normal(103, 2, subgroup_size)
        data.extend(subgroup)
    
    df = pd.DataFrame({
        "Muestra": np.arange(1, len(data) + 1),
        "Subgrupo": np.repeat(np.arange(1, n_subgroups + 1), subgroup_size),
        "Valor": data,
    })
    
    return df


def save_sample_csv():
    """Save sample data to CSV"""
    df = generate_subgrouped_data()
    df.to_csv(
        "/workspaces/StatGenius/data/sample_process_data.csv",
        index=False,
    )
    print("Sample data saved to data/sample_process_data.csv")


if __name__ == "__main__":
    save_sample_csv()
