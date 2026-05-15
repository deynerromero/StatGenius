"""
StatGenius - Interactive SPC Analysis Application
Built with Streamlit
"""
import os
import io
import json
import pandas as pd
import numpy as np
import streamlit as st
from dotenv import load_dotenv
from datetime import datetime

# Import SPC modules
from spc_modules.statistics import SPCAnalyzer, calculate_control_limits, calculate_power_and_arl
from spc_modules.visualization import SPCPlotter
from spc_modules.ai_assistant import SPCAssistant
from data.sample_data_generator import generate_subgrouped_data

# Load environment variables from .env file at startup.
load_dotenv()

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="StatGenius - SPC Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown(
    """
    <style>
    .main {
        padding-top: 1rem;
    }
    .phase-header {
        background: linear-gradient(to right, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .ai-response {
        background-color: #f0f4ff;
        border-left: 4px solid #667eea;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .success-box {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .error-box {
        background-color: #f8d7da;
        border-left: 4px solid #dc3545;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .metric-card {
        background: white;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 10px 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

if "phase" not in st.session_state:
    st.session_state.phase = 1

if "data" not in st.session_state:
    st.session_state.data = None

if "analysis_results" not in st.session_state:
    st.session_state.analysis_results = {}

if "ai_assistant" not in st.session_state:
    try:
        st.session_state.ai_assistant = SPCAssistant()
        st.session_state.ai_available = True
    except ValueError as e:
        st.session_state.ai_available = False
        st.session_state.ai_error = str(e)

if "config" not in st.session_state:
    st.session_state.config = {
        "chart_type": "xbar-r",
        "subgroup_size": 5,
        "alpha": 0.0027,
        "delta": 1.5,
        "sampling_freq": 1.0,  # hours
    }

# ============================================================================
# SIDEBAR - PHASE SELECTOR AND NAVIGATION
# ============================================================================

with st.sidebar:
    st.title("📊 StatGenius")
    st.markdown("### Control Estadístico de Procesos")
    
    st.divider()
    
    st.markdown("**Fases de Análisis**")
    
    phases = {
        1: "📥 Ingreso de datos",
        2: "✅ Validación de supuestos",
        3: "⚙️ Configuración del gráfico",
        4: "📈 Análisis de corrimiento",
        5: "🎯 Desempeño y calidad",
        6: "🔧 Optimización del muestreo",
        7: "📉 Visualización",
        8: "🤖 Interpretación Final",
    }
    
    # Phase navigation buttons
    cols = st.columns(4)
    for i in range(1, 9):
        col = cols[(i - 1) % 4]
        with col:
            if st.button(
                f"Fase {i}",
                key=f"phase_btn_{i}",
                use_container_width=True,
                disabled=i > 1 and st.session_state.data is None,
            ):
                st.session_state.phase = i
                st.rerun()
    
    st.divider()
    
    # Status indicator
    if st.session_state.data is not None:
        st.success(f"✓ Datos cargados: {len(st.session_state.data)} observaciones")
    else:
        st.info("ℹ️ Carga datos para comenzar")
    
    # AI Status
    st.divider()
    if st.session_state.ai_available:
        st.success("✓ Asistente IA disponible")
    else:
        st.warning(f"⚠️ IA no disponible: {st.session_state.ai_error}")
    
    # Download results
    st.divider()
    if st.session_state.analysis_results:
        results_json = json.dumps(st.session_state.analysis_results, indent=2, default=str)
        st.download_button(
            label="📥 Descargar resultados",
            data=results_json,
            file_name=f"spc_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
        )

# ============================================================================
# MAIN CONTENT AREA
# ============================================================================

def ai_explain(explanation_text: str, label: str = "Explicación IA"):
    """Display AI explanation in styled box"""
    if st.session_state.ai_available:
        with st.container():
            st.markdown(f"<div class='ai-response'><strong>{label}:</strong><br>{explanation_text}</div>", 
                       unsafe_allow_html=True)


# ============================================================================
# PHASE 1: DATA INPUT
# ============================================================================

def phase_1_data_input():
    """Phase 1: Data Input"""
    st.markdown(
        "<div class='phase-header'><h2>📥 Fase 1: Ingreso de Datos</h2></div>",
        unsafe_allow_html=True,
    )
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### Opciones de carga de datos")
        
        data_source = st.radio(
            "Selecciona la fuente de datos:",
            ["Cargar archivo CSV/Excel", "Datos de ejemplo", "Ingreso manual"],
            label_visibility="collapsed",
        )
        
        if data_source == "Cargar archivo CSV/Excel":
            uploaded_file = st.file_uploader(
                "Sube tu archivo",
                type=["csv", "xlsx"],
                help="Archivos CSV o Excel con datos de proceso",
            )
            if uploaded_file:
                if uploaded_file.name.endswith(".csv"):
                    st.session_state.data = pd.read_csv(uploaded_file)
                else:
                    st.session_state.data = pd.read_excel(uploaded_file)
                st.success("✓ Archivo cargado correctamente")
        
        elif data_source == "Datos de ejemplo":
            if st.button("Cargar datos de ejemplo", key="load_sample"):
                st.session_state.data = generate_subgrouped_data()
                st.success("✓ Datos de ejemplo cargados (20 subgrupos, n=5, con corrimiento en muestra 15)")
        
        else:  # Manual input
            n_rows = st.number_input("Número de observaciones:", min_value=5, max_value=500, value=20)
            if st.button("Crear tabla vacía", key="create_table"):
                st.session_state.data = pd.DataFrame({"Valor": [100.0] * n_rows})
                st.rerun()
    
    with col2:
        st.markdown("### Vista previa")
        if st.session_state.data is not None:
            st.info(f"📊 {len(st.session_state.data)} filas encontradas")
            st.dataframe(
                st.session_state.data.head(10),
                use_container_width=True,
                height=300,
            )
    
    # Data preview and column selection
    if st.session_state.data is not None:
        st.divider()
        st.markdown("### Preparación de datos")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            value_column = st.selectbox(
                "Columna con valores del proceso:",
                st.session_state.data.columns,
                key="value_col",
            )
            st.session_state.value_column = value_column
        
        with col2:
            st.session_state.config["subgroup_size"] = st.number_input(
                "Tamaño de subgrupo (n):",
                min_value=1,
                max_value=20,
                value=st.session_state.config["subgroup_size"],
                help="Número de observaciones por subgrupo. n=1 para individuos",
            )
        
        with col3:
            if st.button("Visualizar datos", key="preview_data"):
                st.session_state.show_preview = True
        
        # Show data preview plot
        if st.session_state.data is not None:
            data_array = st.session_state.data[value_column].values
            fig = SPCPlotter.plot_histogram_with_normal(
                data_array,
                np.mean(data_array),
                np.std(data_array, ddof=1),
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Navigation button
        if st.button("→ Siguiente: Validación de supuestos", key="next_phase1"):
            st.session_state.phase = 2
            st.rerun()


# ============================================================================
# PHASE 2: ASSUMPTIONS VALIDATION
# ============================================================================

def phase_2_assumptions():
    """Phase 2: Assumptions Validation"""
    st.markdown(
        "<div class='phase-header'><h2>✅ Fase 2: Validación de Supuestos</h2></div>",
        unsafe_allow_html=True,
    )
    
    if "value_column" not in st.session_state:
        st.error("❌ Primero debes cargar datos en Fase 1")
        return
    
    data_array = st.session_state.data[st.session_state.value_column].values
    
    if st.button("Ejecutar pruebas", key="run_tests"):
        with st.spinner("Realizando pruebas estadísticas..."):
            analyzer = SPCAnalyzer(st.session_state.data, st.session_state.config["subgroup_size"])
            
            # Normality test
            normality_results = analyzer.test_normality()
            descriptive = analyzer.get_descriptive_stats()
            randomness_results = analyzer.test_randomness()
            
            st.session_state.analysis_results["normality"] = normality_results
            st.session_state.analysis_results["descriptive"] = descriptive
            st.session_state.analysis_results["randomness"] = randomness_results
    
    # Display results
    if "normality" in st.session_state.analysis_results:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Prueba de Normalidad")
            
            normality = st.session_state.analysis_results["normality"]
            shapiro_p = normality["shapiro_wilk"]["p_value"]
            anderson_passes = normality["anderson_darling"]["passes"]
            overall = normality["overall_normal"]
            
            # Traffic light
            if overall:
                st.markdown("<div class='success-box'><strong>✓ Distribución Normal</strong><br>Los datos siguen una distribución normal (α=0.05)</div>", 
                          unsafe_allow_html=True)
            else:
                st.markdown("<div class='warning-box'><strong>⚠️ No es Normal</strong><br>Los datos NO siguen distribución normal. Considera transformación.</div>", 
                          unsafe_allow_html=True)
            
            with st.expander("Detalles técnicos"):
                st.write(f"**Shapiro-Wilk p-valor:** {shapiro_p:.4f}")
                st.write(f"**Anderson-Darling pasa:** {anderson_passes}")
            
            # AI explanation
            if st.session_state.ai_available:
                explanation = st.session_state.ai_assistant.explain_normality_test(normality)
                ai_explain(explanation, "🤖 Análisis IA")
        
        with col2:
            st.subheader("🎲 Prueba de Aleatoriedad")
            
            randomness = st.session_state.analysis_results["randomness"]
            passes_randomness = randomness["passes"]
            
            if passes_randomness:
                st.markdown("<div class='success-box'><strong>✓ Datos Aleatorios</strong><br>Las observaciones son independientes</div>", 
                          unsafe_allow_html=True)
            else:
                st.markdown("<div class='warning-box'><strong>⚠️ No Aleatorios</strong><br>Hay correlación entre observaciones</div>", 
                          unsafe_allow_html=True)
            
            with st.expander("Detalles técnicos"):
                st.write(f"**Z-statistic:** {randomness['z_statistic']:.4f}")
                st.write(f"**P-valor:** {randomness['p_value']:.4f}")
                st.write(f"**Interpretación:** {randomness['interpretation']}")
            
            # AI explanation
            if st.session_state.ai_available:
                explanation = st.session_state.ai_assistant.explain_randomness_test(randomness)
                ai_explain(explanation, "🤖 Análisis IA")
        
        # Descriptive statistics
        st.divider()
        st.subheader("📈 Estadísticos Descriptivos")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        descriptive = st.session_state.analysis_results["descriptive"]
        
        with col1:
            st.metric("Media", f"{descriptive['mean']:.4f}")
        with col2:
            st.metric("Desv. Est.", f"{descriptive['std_dev']:.4f}")
        with col3:
            st.metric("Mínimo", f"{descriptive['min']:.4f}")
        with col4:
            st.metric("Máximo", f"{descriptive['max']:.4f}")
        with col5:
            st.metric("Coef. Var.", f"{descriptive['cv']:.4f}")
    
    # Navigation
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Anterior: Ingreso de datos", key="prev_phase2"):
            st.session_state.phase = 1
            st.rerun()
    with col2:
        if st.button("→ Siguiente: Configuración del gráfico", key="next_phase2"):
            st.session_state.phase = 3
            st.rerun()


# ============================================================================
# PHASE 3: CHART CONFIGURATION
# ============================================================================

def phase_3_chart_config():
    """Phase 3: Chart Configuration"""
    st.markdown(
        "<div class='phase-header'><h2>⚙️ Fase 3: Configuración del Gráfico de Control</h2></div>",
        unsafe_allow_html=True,
    )
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Parámetros del gráfico")
        
        chart_type = st.selectbox(
            "Tipo de gráfico:",
            ["xbar-r", "i-mr"],
            format_func=lambda x: "Xbarra-R" if x == "xbar-r" else "Individuos-Rango Móvil",
            key="chart_type",
        )
        st.session_state.config["chart_type"] = chart_type
        
        alpha = st.number_input(
            "Riesgo de falsa alarma (α):",
            min_value=0.0001,
            max_value=0.1,
            value=st.session_state.config["alpha"],
            format="%.4f",
            help="Probabilidad de falsa alarma. Default: 0.0027 (3-sigma)",
        )
        st.session_state.config["alpha"] = alpha
    
    with col2:
        st.subheader("Límites de especificación (opcional)")
        
        col1, col2 = st.columns(2)
        with col1:
            lsl = st.number_input(
                "LIE (Límite Inferior de Especificación):",
                value=None,
                key="lsl",
            )
        with col2:
            usl = st.number_input(
                "LSE (Límite Superior de Especificación):",
                value=None,
                key="usl",
            )
        
        st.session_state.config["lsl"] = lsl
        st.session_state.config["usl"] = usl
    
    # Calculate control limits
    if st.button("Calcular límites de control", key="calc_limits"):
        with st.spinner("Calculando..."):
            data_array = st.session_state.data[st.session_state.value_column].values
            
            limits = calculate_control_limits(
                data_array,
                chart_type=st.session_state.config["chart_type"],
                alpha=st.session_state.config["alpha"],
                subgroup_size=st.session_state.config["subgroup_size"],
            )
            
            st.session_state.analysis_results["control_limits"] = limits
            st.session_state.analysis_results["descriptive"] = SPCAnalyzer(
                st.session_state.data,
                st.session_state.config["subgroup_size"],
            ).get_descriptive_stats()
    
    # Display results
    if "control_limits" in st.session_state.analysis_results:
        st.divider()
        st.subheader("📏 Límites Calculados")
        
        limits = st.session_state.analysis_results["control_limits"]
        
        if st.session_state.config["chart_type"] == "xbar-r":
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Gráfico Xbarra:**")
                st.metric("LCI", f"{limits['xbar']['lcl']:.4f}")
                st.metric("Línea Central", f"{limits['xbar']['center']:.4f}")
                st.metric("LCS", f"{limits['xbar']['ucl']:.4f}")
            
            with col2:
                st.write("**Gráfico R (Rangos):**")
                st.metric("LCI", f"{limits['r']['lcl']:.4f}")
                st.metric("Línea Central", f"{limits['r']['center']:.4f}")
                st.metric("LCS", f"{limits['r']['ucl']:.4f}")
        else:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("LCI", f"{limits['lcl']:.4f}")
            with col2:
                st.metric("Línea Central", f"{limits['center']:.4f}")
            with col3:
                st.metric("LCS", f"{limits['ucl']:.4f}")
        
        # AI explanation
        if st.session_state.ai_available:
            descriptive = st.session_state.analysis_results["descriptive"]
            explanation = st.session_state.ai_assistant.explain_control_limits(limits, descriptive)
            ai_explain(explanation, "🤖 Interpretación")
    
    # Navigation
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Anterior", key="prev_phase3"):
            st.session_state.phase = 2
            st.rerun()
    with col2:
        if st.button("→ Siguiente", key="next_phase3"):
            st.session_state.phase = 4
            st.rerun()


# ============================================================================
# PHASE 4: SHIFT AND POWER ANALYSIS
# ============================================================================

def phase_4_shift_analysis():
    """Phase 4: Shift and Power Analysis"""
    st.markdown(
        "<div class='phase-header'><h2>📈 Fase 4: Análisis de Corrimiento y Potencia</h2></div>",
        unsafe_allow_html=True,
    )

    # Ensure subgroup size is always available in this phase.
    n = int(st.session_state.config.get("subgroup_size", 1))
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Parámetros de análisis")
        
        delta = st.slider(
            "Corrimiento esperado (δ) en unidades sigma:",
            min_value=0.5,
            max_value=5.0,
            value=st.session_state.config.get("delta", 1.5),
            step=0.1,
        )
        st.session_state.config["delta"] = delta
        
        sampling_freq = st.number_input(
            "Frecuencia de muestreo (horas entre muestras):",
            min_value=0.1,
            max_value=24.0,
            value=st.session_state.config.get("sampling_freq", 1.0),
        )
        st.session_state.config["sampling_freq"] = sampling_freq
    
    with col2:
        st.subheader("Información del proceso")
        if "control_limits" in st.session_state.analysis_results:
            limits = st.session_state.analysis_results["control_limits"]
            st.metric("Sigma estimada", f"{limits.get('sigma_estimated', 'N/A'):.4f}")
            st.metric("Número de muestras", limits.get('number_of_subgroups', len(st.session_state.data)))
    
    # Calculate power and ARL
    if st.button("Calcular potencia y ARL", key="calc_power"):
        with st.spinner("Calculando..."):
            power_results = calculate_power_and_arl(
                delta=st.session_state.config["delta"],
                n=n,
                alpha=st.session_state.config["alpha"],
            )
            
            st.session_state.analysis_results["power_analysis"] = power_results
    
    # Display results
    if "power_analysis" in st.session_state.analysis_results:
        st.divider()
        st.subheader("📊 Resultados de Potencia y ARL")
        
        power_res = st.session_state.analysis_results["power_analysis"]
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Potencia (1-β)", f"{power_res['power']:.1%}")
        with col2:
            st.metric("ARL₀", f"{power_res['arl0']:.1f}")
        with col3:
            st.metric("ARL₁", f"{power_res['arl1']:.1f}")
        with col4:
            time_detection = power_res['arl1'] * st.session_state.config["sampling_freq"]
            st.metric("Tiempo medio de detección", f"{time_detection:.1f} horas")
        
        # Power curve
        st.subheader("Curva de Potencia")
        delta_range = np.linspace(0.1, 5.0, 50)
        power_values = []
        
        for d in delta_range:
            pr = calculate_power_and_arl(d, n, st.session_state.config["alpha"])
            power_values.append(pr["power"])
        
        fig_power = SPCPlotter.plot_power_curve(
            delta_range,
            np.array(power_values),
            current_delta=st.session_state.config["delta"],
        )
        st.plotly_chart(fig_power, use_container_width=True)
        
        # ARL curve
        st.subheader("Curva de ARL₁")
        arl1_values = []
        
        for d in delta_range:
            pr = calculate_power_and_arl(d, n, st.session_state.config["alpha"])
            arl1_values.append(pr["arl1"])
        
        fig_arl = SPCPlotter.plot_arl_curve(
            delta_range,
            np.array(arl1_values),
            arl0=power_res["arl0"],
        )
        st.plotly_chart(fig_arl, use_container_width=True)
        
        # AI explanation
        if st.session_state.ai_available:
            explanation = st.session_state.ai_assistant.explain_power_and_arl(
                power_res,
                st.session_state.config["sampling_freq"],
            )
            ai_explain(explanation, "🤖 Interpretación")
    
    # Navigation
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Anterior", key="prev_phase4"):
            st.session_state.phase = 3
            st.rerun()
    with col2:
        if st.button("→ Siguiente", key="next_phase4"):
            st.session_state.phase = 5
            st.rerun()


# ============================================================================
# PHASE 5: PERFORMANCE AND QUALITY
# ============================================================================

def phase_5_performance():
    """Phase 5: Performance and Quality"""
    from spc_modules.statistics import calculate_process_capability
    
    st.markdown(
        "<div class='phase-header'><h2>🎯 Fase 5: Desempeño y Calidad del Proceso</h2></div>",
        unsafe_allow_html=True,
    )
    
    # Calculate capability
    if st.button("Calcular índices de capacidad", key="calc_capability"):
        with st.spinner("Calculando..."):
            data_array = st.session_state.data[st.session_state.value_column].values
            
            sigma = None
            if "control_limits" in st.session_state.analysis_results:
                sigma = st.session_state.analysis_results["control_limits"].get("sigma_estimated")
            
            capability = calculate_process_capability(
                data_array,
                lsl=st.session_state.config.get("lsl"),
                usl=st.session_state.config.get("usl"),
                sigma=sigma,
            )
            
            st.session_state.analysis_results["capability"] = capability
    
    # Display results
    if "capability" in st.session_state.analysis_results:
        st.divider()
        
        cap = st.session_state.analysis_results["capability"]
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("Índices de Capacidad")
            
            if "cpk" in cap:
                cpk = cap["cpk"]
                if cpk > 1.33:
                    status = "✓ Excelente"
                    color = "green"
                elif cpk > 1.0:
                    status = "⚠️ Aceptable"
                    color = "orange"
                else:
                    status = "❌ No capaz"
                    color = "red"
                
                st.metric("Cpk (Capacidad Real)", f"{cpk:.4f}", delta=status)
            
            if "cp" in cap:
                st.metric("Cp (Capacidad Potencial)", f"{cap['cp']:.4f}")
        
        with col2:
            st.subheader("Probabilidad de No Conformes")
            
            if "prob_nonconforming" in cap:
                prob_non = cap["prob_nonconforming"]
                st.metric(
                    "P(no conforme)",
                    f"{prob_non:.2%}",
                    help="Probabilidad de que una pieza esté fuera de especificación",
                )
        
        # AI explanation
        if st.session_state.ai_available and st.session_state.config.get("lsl"):
            explanation = st.session_state.ai_assistant.explain_capability(
                cap,
                st.session_state.config.get("lsl"),
                st.session_state.config.get("usl"),
            )
            ai_explain(explanation, "🤖 Análisis de Capacidad")
    
    # Summary metrics
    st.divider()
    st.subheader("📊 Resumen de Desempeño")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if "analysis_results" in st.session_state and "normality" in st.session_state.analysis_results:
            passes_normal = st.session_state.analysis_results["normality"]["overall_normal"]
            st.metric("Normalidad", "✓ Sí" if passes_normal else "✗ No")
    
    with col2:
        if "analysis_results" in st.session_state and "randomness" in st.session_state.analysis_results:
            passes_random = st.session_state.analysis_results["randomness"]["passes"]
            st.metric("Aleatoriedad", "✓ Sí" if passes_random else "✗ No")
    
    with col3:
        if "capability" in st.session_state.analysis_results:
            cpk = st.session_state.analysis_results["capability"].get("cpk", 0)
            capable = "✓ Capaz" if cpk > 1.33 else "✗ No capaz"
            st.metric("Capacidad", capable)
    
    # Navigation
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Anterior", key="prev_phase5"):
            st.session_state.phase = 4
            st.rerun()
    with col2:
        if st.button("→ Siguiente", key="next_phase5"):
            st.session_state.phase = 6
            st.rerun()


# ============================================================================
# PHASE 6: SAMPLING OPTIMIZATION
# ============================================================================

def phase_6_sampling_optimization():
    """Phase 6: Sampling Optimization"""
    st.markdown(
        "<div class='phase-header'><h2>🔧 Fase 6: Optimización del Muestreo</h2></div>",
        unsafe_allow_html=True,
    )
    
    st.markdown("""
    En esta fase se calcula el plan de muestreo óptimo considerando:
    - Tamaño de subgrupo (n)
    - Frecuencia de muestreo
    - Balance entre costo y capacidad de detección
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Parámetros de optimización")
        
        min_n = st.number_input("Tamaño mínimo de subgrupo:", min_value=1, max_value=5, value=1)
        max_n = st.number_input("Tamaño máximo de subgrupo:", min_value=2, max_value=10, value=10)
        
        cost_per_sample = st.number_input("Costo por observación ($):", min_value=1.0, max_value=1000.0, value=10.0)
        cost_per_hour = st.number_input("Costo por hora de muestreo ($):", min_value=1.0, max_value=500.0, value=50.0)
    
    with col2:
        st.subheader("Objetivos")
        
        optimize_for = st.selectbox(
            "Optimizar por:",
            ["Potencia", "ARL₁", "Costo", "Balance (Potencia vs Costo)"],
        )
        
        target_power = st.slider("Potencia mínima deseada:", min_value=0.7, max_value=0.99, value=0.80, step=0.01)
    
    # Run optimization
    if st.button("Calcular plan óptimo", key="optimize_sampling"):
        with st.spinner("Optimizando plan de muestreo..."):
            results_optimization = []
            
            for n in range(int(min_n), int(max_n) + 1):
                for freq in [0.5, 1.0, 2.0, 4.0, 8.0]:  # hours
                    pr = calculate_power_and_arl(
                        st.session_state.config["delta"],
                        n=n,
                        alpha=st.session_state.config["alpha"],
                    )
                    
                    cost_per_day = (24 / freq) * n * cost_per_sample + (24 / freq) * cost_per_hour
                    
                    results_optimization.append({
                        "n": n,
                        "freq": freq,
                        "power": pr["power"],
                        "arl1": pr["arl1"],
                        "cost_per_day": cost_per_day,
                    })
            
            st.session_state.analysis_results["optimization"] = {
                "results": results_optimization,
                "target_power": target_power,
            }
    
    # Display results
    if "optimization" in st.session_state.analysis_results:
        st.divider()
        st.subheader("📊 Resultados de Optimización")
        
        results = st.session_state.analysis_results["optimization"]["results"]
        target_power = st.session_state.analysis_results["optimization"]["target_power"]
        
        # Filter by target power
        viable = [r for r in results if r["power"] >= target_power]
        
        if viable:
            df_results = pd.DataFrame(viable)
            
            # Find best options
            if optimize_for == "Potencia":
                best = max(viable, key=lambda x: x["power"])
            elif optimize_for == "ARL₁":
                best = min(viable, key=lambda x: x["arl1"])
            elif optimize_for == "Costo":
                best = min(viable, key=lambda x: x["cost_per_day"])
            else:  # Balance
                best = min(viable, key=lambda x: x["cost_per_day"] / (x["power"] + 0.1))
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Tamaño de subgrupo recomendado", int(best["n"]))
            with col2:
                st.metric("Frecuencia (horas)", f"{best['freq']:.1f}")
            with col3:
                st.metric("Potencia lograda", f"{best['power']:.1%}")
            with col4:
                st.metric("Costo diario", f"${best['cost_per_day']:.2f}")
            
            st.divider()
            st.dataframe(
                df_results.head(15),
                use_container_width=True,
                hide_index=True,
            )
            
            # AI recommendation
            if st.session_state.ai_available:
                recommendation = st.session_state.ai_assistant.recommend_sampling_plan({
                    "subgroup_size": int(best["n"]),
                    "sigma_estimated": st.session_state.analysis_results.get("control_limits", {}).get("sigma_estimated"),
                    "observations": len(st.session_state.data),
                })
                ai_explain(recommendation, "🤖 Recomendación del Plan")
        else:
            st.error(f"❌ No hay planes viables con potencia ≥ {target_power:.1%}")
    
    # Navigation
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Anterior", key="prev_phase6"):
            st.session_state.phase = 5
            st.rerun()
    with col2:
        if st.button("→ Siguiente", key="next_phase6"):
            st.session_state.phase = 7
            st.rerun()


# ============================================================================
# PHASE 7: VISUALIZATION
# ============================================================================

def phase_7_visualization():
    """Phase 7: Control Chart Visualization"""
    st.markdown(
        "<div class='phase-header'><h2>📉 Fase 7: Visualización del Gráfico de Control</h2></div>",
        unsafe_allow_html=True,
    )
    
    if "control_limits" not in st.session_state.analysis_results:
        st.error("Primero calcula los límites de control en Fase 3")
        return
    
    data_array = st.session_state.data[st.session_state.value_column].values
    limits = st.session_state.analysis_results["control_limits"]
    
    chart_type = st.session_state.config["chart_type"]
    
    # Generate appropriate chart
    if chart_type == "xbar-r":
        fig = SPCPlotter.plot_xbar_r_chart(
            data_array,
            st.session_state.config["subgroup_size"],
            limits,
        )
    else:  # i-mr
        fig = SPCPlotter.plot_individuals_chart(
            data_array,
            limits,
        )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Summary statistics
    st.divider()
    st.subheader("📊 Resumen Estadístico")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Observaciones fuera de control", np.sum((data_array > limits["ucl"]) | (data_array < limits["lcl"])))
    
    with col2:
        st.metric("% de variabilidad dentro de LCI-LCS", f"{100 * np.mean((data_array >= limits['lcl']) & (data_array <= limits['ucl'])):.1f}%")
    
    with col3:
        st.metric("Rango de datos", f"{data_array.max() - data_array.min():.4f}")
    
    # Navigation
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Anterior", key="prev_phase7"):
            st.session_state.phase = 6
            st.rerun()
    with col2:
        if st.button("→ Siguiente", key="next_phase7"):
            st.session_state.phase = 8
            st.rerun()


# ============================================================================
# PHASE 8: FINAL INTERPRETATION
# ============================================================================

def phase_8_interpretation():
    """Phase 8: Final Interpretation"""
    st.markdown(
        "<div class='phase-header'><h2>🤖 Fase 8: Interpretación Final con IA</h2></div>",
        unsafe_allow_html=True,
    )
    
    st.markdown("""
    En esta fase final, el asistente IA sintetiza todos los hallazgos del análisis 
    y proporciona recomendaciones concretas para mejorar el proceso.
    """)
    
    if not st.session_state.ai_available:
        st.error("⚠️ Asistente IA no disponible. Confirma tu clave de API en variables de entorno.")
        return
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Resumen del análisis")
        
        # Checklist of completed analyses
        st.markdown("### Análisis realizados:")
        
        analyses_done = {
            "Normality": "✓" if "normality" in st.session_state.analysis_results else "□",
            "Randomness": "✓" if "randomness" in st.session_state.analysis_results else "□",
            "Control Limits": "✓" if "control_limits" in st.session_state.analysis_results else "□",
            "Power Analysis": "✓" if "power_analysis" in st.session_state.analysis_results else "□",
            "Capability": "✓" if "capability" in st.session_state.analysis_results else "□",
        }
        
        for analysis, status in analyses_done.items():
            st.write(f"{status} {analysis}")
    
    with col2:
        st.subheader("Métricas clave")
        capability_data = st.session_state.analysis_results.get("capability") or {}
        power_data = st.session_state.analysis_results.get("power_analysis") or {}
        
        if capability_data:
            cpk = capability_data.get("cpk")
            if cpk:
                if cpk > 1.33:
                    st.success(f"Cpk = {cpk:.4f} (Proceso capaz)")
                else:
                    st.warning(f"Cpk = {cpk:.4f} (Proceso no capaz)")
        
        if power_data and "power" in power_data:
            power = power_data["power"]
            st.info(f"Potencia de detección: {power:.1%}")
    
    # Generate comprehensive interpretation
    st.divider()
    
    if st.button("🤖 Generar interpretación con IA", key="gen_interpretation"):
        with st.spinner("El asistente IA está analizando..."):
            # Build comprehensive prompt
            interpretation_data = {
                "normality": st.session_state.analysis_results.get("normality") or {},
                "randomness": st.session_state.analysis_results.get("randomness") or {},
                "capability": st.session_state.analysis_results.get("capability") or {},
                "power": st.session_state.analysis_results.get("power_analysis") or {},
            }
            
            prompt = f"""Proporciona una interpretación COMPLETA y PROFESIONAL del análisis SPC:

DATOS DEL PROCESO:
- Número de observaciones: {len(st.session_state.data)}
- Media: {st.session_state.analysis_results.get('descriptive', {}).get('mean', 'N/A')}
- Desviación estándar: {st.session_state.analysis_results.get('descriptive', {}).get('std_dev', 'N/A')}

RESULTADOS:
- Normalidad: {interpretation_data.get('normality', {}).get('overall_normal', 'N/A')}
- Aleatoriedad: {interpretation_data.get('randomness', {}).get('passes', 'N/A')}
- Cpk: {interpretation_data.get('capability', {}).get('cpk', 'N/A')}
- Potencia: {interpretation_data.get('power', {}).get('power', 'N/A')}

PREGUNTAS A RESPONDER:
1. ¿Es el proceso estable? ¿Por qué?
2. ¿Es el proceso capaz de cumplir con especificaciones?
3. ¿Cuáles son los principales problemas o riesgos?
4. ¿Qué recomendaciones concretas haces para mejorar?
5. ¿Cuál debería ser el siguiente paso?

Sé conciso pero informativo (máximo 500 palabras)."""
            
            if st.session_state.ai_assistant:
                response = st.session_state.ai_assistant._call_gpt(prompt)
                st.markdown("<div class='ai-response'>" + response + "</div>", unsafe_allow_html=True)
    
    # Download report
    st.divider()
    st.subheader("📥 Descargar Reporte")
    
    if st.button("Generar PDF (próximamente)"):
        st.info("Funcionalidad en desarrollo")
    
    # Navigation
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Anterior", key="prev_phase8"):
            st.session_state.phase = 7
            st.rerun()
    with col2:
        if st.button("🏠 Inicio", key="home"):
            st.session_state.phase = 1
            st.rerun()


# ============================================================================
# MAIN APP LOGIC
# ============================================================================

def main():
    """Main application"""
    
    # Display current phase
    phases = {
        1: phase_1_data_input,
        2: phase_2_assumptions,
        3: phase_3_chart_config,
        4: phase_4_shift_analysis,
        5: phase_5_performance,
        6: phase_6_sampling_optimization,
        7: phase_7_visualization,
        8: phase_8_interpretation,
    }
    
    phase_func = phases[st.session_state.phase]
    phase_func()


if __name__ == "__main__":
    main()
