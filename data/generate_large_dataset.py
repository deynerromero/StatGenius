"""
Generate a large realistic SPC dataset with 500 rows
Includes multiple process patterns for demonstration
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_large_spc_dataset(n_samples=500):
    """
    Generate a realistic SPC dataset with 500 samples
    
    Patterns included:
    - Normal process (rows 1-100)
    - Slight upward trend (rows 100-200)
    - Stable but shifted (rows 200-350)
    - Sudden shift (rows 350-450)
    - Increased variability (rows 450-500)
    """
    np.random.seed(42)
    
    data = []
    timestamps = []
    subgroup = []
    
    start_time = datetime(2024, 1, 1, 8, 0, 0)
    
    for i in range(n_samples):
        timestamp = start_time + timedelta(hours=i)
        
        # Different patterns by range
        if i < 100:
            # Normal stable process: mean=100, sigma=2
            value = np.random.normal(100, 2)
            pattern = "Normal"
        
        elif i < 200:
            # Subtle upward trend
            trend = (i - 100) * 0.05
            value = np.random.normal(100 + trend, 2.2)
            pattern = "Trend_Up"
        
        elif i < 350:
            # Shifted up but stable
            value = np.random.normal(104, 2)
            pattern = "Shifted_Up"
        
        elif i < 450:
            # Major shift
            value = np.random.normal(106, 1.8)
            pattern = "Major_Shift"
        
        else:
            # Increased variability (out of control)
            value = np.random.normal(102, 4)
            pattern = "High_Variability"
        
        data.append({
            'Timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'Sample_Number': i + 1,
            'Value': round(value, 4),
            'Pattern': pattern,
            'BatchID': f"BATCH_{(i // 50) + 1:03d}",
        })
        
        timestamps.append(timestamp)
        subgroup.append((i % 5) + 1)
    
    df = pd.DataFrame(data)
    df['Subgroup_Position'] = subgroup
    
    # Reorder columns
    df = df[[
        'Sample_Number',
        'Timestamp',
        'Value',
        'Subgroup_Position',
        'BatchID',
        'Pattern'
    ]]
    
    return df


def generate_additional_variants(n_samples=500):
    """
    Generate alternative datasets with different patterns
    """
    variants = {}
    np.random.seed(42)
    
    # Variant 1: High-quality process (Cpk > 2.0)
    data1 = []
    for i in range(n_samples):
        value = np.random.normal(50, 0.8)  # Low variability
        data1.append({
            'Sample': i + 1,
            'Measurement': round(value, 4),
            'Time': datetime(2024, 1, 1) + timedelta(hours=i),
        })
    variants['quality_process'] = pd.DataFrame(data1)
    
    # Variant 2: Poor process with autocorrelation
    data2 = []
    value = 100
    for i in range(n_samples):
        # Add autocorrelation
        value = 0.7 * value + 0.3 * np.random.normal(100, 3)
        data2.append({
            'Sample': i + 1,
            'Reading': round(value, 4),
            'DateTime': datetime(2024, 1, 1) + timedelta(minutes=15*i),
        })
    variants['autocorrelated_process'] = pd.DataFrame(data2)
    
    # Variant 3: Non-normal distribution (heavy tails)
    data3 = []
    for i in range(n_samples):
        if np.random.random() < 0.05:  # 5% outliers
            value = np.random.normal(100, 8)
        else:
            value = np.random.normal(100, 1.5)
        data3.append({
            'SampleID': i + 1,
            'ProcessValue': round(value, 4),
        })
    variants['non_normal_process'] = pd.DataFrame(data3)
    
    # Variant 4: Periodic variation (cyclic pattern)
    data4 = []
    for i in range(n_samples):
        # Add cyclic component
        cycle = 5 * np.sin(2 * np.pi * i / 50)
        value = 100 + cycle + np.random.normal(0, 1)
        data4.append({
            'Obs_Number': i + 1,
            'Output': round(value, 4),
            'TimePoint': i,
        })
    variants['cyclic_process'] = pd.DataFrame(data4)
    
    return variants


if __name__ == "__main__":
    print("🔧 Generando dataset principal (500 filas)...")
    
    # Generate main dataset
    df_main = generate_large_spc_dataset(500)
    df_main.to_csv(
        'data/spc_dataset_500_samples.csv',
        index=False,
    )
    print(f"✓ Guardado: data/spc_dataset_500_samples.csv ({len(df_main)} filas)")
    print(f"\nEstructura:")
    print(df_main.head(10))
    print(f"\nEstadísticos por patrón:")
    print(df_main.groupby('Pattern')['Value'].describe())
    
    # Generate variants
    print("\n" + "="*60)
    print("🔧 Generando datasets variantes...")
    variants = generate_additional_variants(500)
    
    for variant_name, df_variant in variants.items():
        filename = f'data/spc_dataset_{variant_name}.csv'
        df_variant.to_csv(filename, index=False)
        print(f"✓ {filename} ({len(df_variant)} filas)")
    
    print("\n" + "="*60)
    print("📊 RESUMEN DE DATASETS GENERADOS")
    print("="*60)
    
    datasets_info = {
        'spc_dataset_500_samples.csv': {
            'descripcion': 'Dataset principal con 5 patrones SPC',
            'filas': 500,
            'columnas': ['Sample_Number', 'Timestamp', 'Value', 'Subgroup_Position', 'BatchID', 'Pattern'],
            'patrones': ['Normal', 'Trend_Up', 'Shifted_Up', 'Major_Shift', 'High_Variability']
        },
        'spc_dataset_quality_process.csv': {
            'descripcion': 'Proceso de alta calidad (Cpk > 2.0)',
            'filas': 500,
            'columnas': ['Sample', 'Measurement', 'Time']
        },
        'spc_dataset_autocorrelated_process.csv': {
            'descripcion': 'Proceso con autocorrelación',
            'filas': 500,
            'columnas': ['Sample', 'Reading', 'DateTime']
        },
        'spc_dataset_non_normal_process.csv': {
            'descripcion': 'Proceso con distribución no-normal',
            'filas': 500,
            'columnas': ['SampleID', 'ProcessValue']
        },
        'spc_dataset_cyclic_process.csv': {
            'descripcion': 'Proceso con patrón cíclico',
            'filas': 500,
            'columnas': ['Obs_Number', 'Output', 'TimePoint']
        }
    }
    
    for filename, info in datasets_info.items():
        print(f"\n📄 {filename}")
        print(f"   Descripción: {info['descripcion']}")
        print(f"   Filas: {info['filas']}")
        print(f"   Columnas: {', '.join(info['columnas'])}")
        if 'patrones' in info:
            print(f"   Patrones: {', '.join(info['patrones'])}")
    
    print("\n" + "="*60)
    print("💡 USO EN STATGENIUS")
    print("="*60)
    print("""
1. Abre la aplicación: streamlit run app.py
2. Fase 1 → Carga archivo → Selecciona spc_dataset_500_samples.csv
3. Selecciona columna 'Value' y tamaño de subgrupo: 5
4. Ejecuta fase 2 y analiza los diferentes patrones

RECOMENDACIONES POR DATASET:
┌─────────────────────────────────────────┠─────────────────────┐
│ Dataset                                 │ Qué aprender        │
├─────────────────────────────────────────┼─────────────────────┤
│ spc_dataset_500_samples.csv             │ Todos los patrones  │
│ spc_dataset_quality_process.csv         │ Capacidad alta      │
│ spc_dataset_autocorrelated_process.csv  │ Violación supuestos │
│ spc_dataset_non_normal_process.csv      │ No normalidad       │
│ spc_dataset_cyclic_process.csv          │ Patrones periódicos │
└─────────────────────────────────────────┴─────────────────────┘
    """)
