"""
Verification script for StatGenius modules
"""
import sys
import pandas as pd
import numpy as np

print("🔍 Verificando módulos de StatGenius...\n")

try:
    # Test imports
    print("✓ Importando módulos estadísticos...")
    from spc_modules.statistics import SPCAnalyzer, calculate_control_limits
    print("  ✓ Módulo de estadística importado")
    
    print("✓ Importando visualización...")
    from spc_modules.visualization import SPCPlotter
    print("  ✓ Módulo de visualización importado")
    
    print("✓ Importando generador de datos...")
    from data.sample_data_generator import generate_subgrouped_data
    print("  ✓ Generador de datos importado")
    
    # Test basic calculations
    print("\n🧮 Probando cálculos...")
    data = generate_subgrouped_data(n_subgroups=10, subgroup_size=5)
    print(f"  ✓ Datos generados: {len(data)} filas")
    
    analyzer = SPCAnalyzer(data, subgroup_size=5)
    normality = analyzer.test_normality()
    print(f"  ✓ Prueba de normalidad: p-valor = {normality['shapiro_wilk']['p_value']:.4f}")
    
    limits = calculate_control_limits(
        data['Valor'].values,
        chart_type="xbar-r",
        subgroup_size=5
    )
    print(f"  ✓ Límites de control calculados (LCI: {limits['xbar']['lcl']:.2f}, LCS: {limits['xbar']['ucl']:.2f})")
    
    # Try importing AI (might fail if no API key)
    print("\n🤖 Verificando IA...")
    try:
        from spc_modules.ai_assistant import SPCAssistant
        print("  ✓ Módulo IA disponible")
        try:
            assistant = SPCAssistant()
            print("  ✓ Asistente IA inicializado (API key configurada)")
        except ValueError as e:
            print(f"  ⚠️ Asistente IA no disponible: {str(e)}")
            print("    → Configura OPENAI_API_KEY para habilitar IA")
    except Exception as e:
        print(f"  ❌ Error importando IA: {e}")
    
    print("\n✅ VERIFICACIÓN COMPLETADA")
    print("\n📝 Próximos pasos:")
    print("1. Configura tu clave de OpenAI:")
    print("   export OPENAI_API_KEY=sk-your-key-here")
    print("\n2. Ejecuta la aplicación:")
    print("   streamlit run app.py")
    print("\n3. La app se abrirá en:  http://localhost:8501")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
