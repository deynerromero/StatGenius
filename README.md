# StatGenius 📊

**StatGenius** es una aplicación web interactiva para **Control Estadístico de Procesos (SPC)** que ayuda a interpretar gráficos de control con un asistente de IA que explica los resultados en lenguaje sencillo.

## 🎯 Características Principales

### ✅ 8 Fases de Análisis Interactivo (Interfaz Tipo Wizard)

1. **Fase 1: Ingreso de Datos**
   - Cargar archivo CSV/Excel o ingresar datos manualmente
   - Vista previa y selección de columnas
   - Definir tamaño de subgrupo (n)

2. **Fase 2: Validación de Supuestos**
   - Pruebas de normalidad (Shapiro-Wilk, Anderson-Darling)
   - Pruebas de aleatoriedad (Runs Test)
   - Indicadores visuales (semáforo: verde/rojo)
   - Explicaciones IA automáticas

3. **Fase 3: Configuración del Gráfico**
   - Elegir tipo: Xbarra-R, Xbarra-S, o I-MR
   - Definir α (riesgo de falsa alarma)
   - Límites de especificación opcionales (LIE, LSE)
   - Cálculo automático de límites de control

4. **Fase 4: Análisis de Corrimiento y Potencia**
   - Calcular potencia (1-β) para detectar corrimientos
   - Calcular ARL₀ y ARL₁ (Longitud Promedio de Secuencia)
   - Tiempo promedio de detección
   - Curvas interactivas de potencia vs. corrimiento

5. **Fase 5: Desempeño y Calidad**
   - Índices de capacidad (Cp, Cpk, Pp, Ppk)
   - Probabilidad de productos no conformes
   - Resumen de estabilidad del proceso

6. **Fase 6: Optimización del Muestreo**
   - Cálculo de plan de muestreo óptimo
   - Tamaño de subgrupo recomendado
   - Frecuencia de muestreo
   - Análisis de costo vs. potencia

7. **Fase 7: Visualización del Gráfico**
   - Gráficos interactivos con Plotly
   - Datos, línea central, límites de control
   - Puntos fuera de control resaltados
   - Límites de especificación (si aplica)

8. **Fase 8: Interpretación con IA**
   - Síntesis automática de hallazgos
   - Recomendaciones concretas en lenguaje natural
   - Explicaciones didácticas de resultados

### 🤖 Asistente IA Integrado

- Explicaciones en lenguaje sencillo con tono profesional y didáctico
- Interpretación automática de pruebas estadísticas
- Recomendaciones prácticas y accionables
- Powered by **OpenAI GPT-4o-mini**

### 📊 Visualizaciones Interactivas

- Gráficos de control (Xbarra-R, I-MR)
- Curvas de potencia y ARL
- Histogramas con distribución normal
- Análisis de capacidad

## 📋 Requisitos Técnicos

- **Python**: 3.8+
- **Frameworks**: Streamlit, Pandas, NumPy, SciPy, Statsmodels
- **Visualización**: Plotly
- **IA**: OpenAI API (clave requerida)

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone <repository-url>
cd StatGenius
```

### 2. Crear entorno virtual (recomendado)

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\\Scripts\\activate   # Windows
```

### 3. Instalar dependencias

```bash
3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configuración de IA (OpenAI u Ollama)

Crea un archivo .env en la raíz del proyecto:

```bash
cp .env.example .env
```

Opción A: OpenAI

```bash
AI_PROVIDER=openai
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4o-mini
```

Opción B: Ollama local (gratis)

```bash
AI_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434/v1
OLLAMA_MODEL=llama3.2
```

Si usas Ollama, asegúrate de tener el servicio activo y el modelo descargado.

### 5. Ejecutar la aplicación

```bash
streamlit run app.py
```

La aplicación se abrirá en `http://localhost:8501`

## 📁 Estructura de carpetas

```
StatGenius/
├── .streamlit/
│   └── config.toml              # Configuración de Streamlit
├── data/
│   └── sample_data_generator.py # Generador de datos de ejemplo
├── spc_modules/
│   ├── __init__.py
│   ├── statistics/              # Cálculos estadísticos
│   │   ├── __init__.py
│   │   └── spc_calculations.py
│   ├── ai_assistant/            # Asistente IA con OpenAI
│   │   ├── __init__.py
│   │   └── spc_assistant.py
│   └── visualization/           # Gráficos interactivos
│       ├── __init__.py
│       └── spc_plotter.py
├── app.py                       # Aplicación principal Streamlit
├── requirements.txt             # Dependencias del proyecto
├── .env.example                 # Ejemplo de configuración
├── README.md                    # Este archivo
└── .gitignore
```

## 🔧 Uso de la Aplicación

### Flujo típico de análisis

1. **Carga de datos**: Usa datos de ejemplo o carga tu propio archivo
2. **Validación**: Verifica que los datos cumplen supuestos estadísticos
3. **Configuración**: Define tipo de gráfico y parámetros
4. **Análisis**: Calcula potencia, ARL y capacidad
5. **Optimización**: Determina plan de muestreo óptimo
6. **Visualización**: Explora gráficos interactivos
7. **Interpretación**: Lee recomendaciones de IA

### Datos de ejemplo precargados

La aplicación incluye un botón "Cargar datos de ejemplo" que proporciona:
- 20 subgrupos de tamaño 5 (n=5)
- Proceso normal con media 100 y σ=2
- Corrimiento de 3σ a partir de muestra 15
- Ideal para demostración del software

## 📊 Cálculos Estadísticos Soportados

### Pruebas de Supuestos
- ✅ **Shapiro-Wilk**: Normalidad
- ✅ **Anderson-Darling**: Distribución normal
- ✅ **Runs Test**: Aleatoriedad/Independencia

### Gráficos de Control
- ✅ **Xbarra-R**: Medias y rangos
- ✅ **Xbarra-S**: Medias y desv. estándar (en desarrollo)
- ✅ **I-MR**: Individuos y rango móvil

### Análisis de Potencia
- ✅ **Potencia (1-β)**: Probabilidad de detectar corrimiento
- ✅ **ARL₀**: Promedio de muestras sin cambio
- ✅ **ARL₁**: Promedio de muestras hasta detectar cambio

### Capacidad del Proceso
- ✅ **Cp**: Capacidad potencial
- ✅ **Cpk**: Capacidad real (considerando centrado)
- ✅ **P(d)**: Probabilidad de no conformidad
- ✅ **Pp, Ppk**: Capacidad general del proceso

## 🤖 Asistente IA: Capacidades

El asistente IA explica automáticamente:

1. **Resultados de pruebas**: Interpreta p-valores y estadísticos
2. **Estabilidad del proceso**: Identifica si hay problemas
3. **Capacidad**: Explica índices Cp, Cpk en términos prácticos
4. **Potencia estadística**: Qué significa la detección de cambios
5. **Recomendaciones**: Acciones concretas para mejorar

### Ejemplos de respuestas IA

> "Los datos no siguen una distribución normal (p=0.023). Esto sugiere transformar los datos usando Box-Cox o usar gráficos robustos menos sensibles a la normalidad."

> "Con Cpk=0.85, el proceso no es capaz de cumplir especificaciones. Prioriza reducir la variabilidad calibrando máquinas antes de centrar el proceso."

> "Con este plan de muestreo (n=5, cada 2 horas), tendrás 78% de probabilidad de detectar un corrimiento de $3\sigma$ en promedio 3.2 muestras después."

## 🧪 Testing (En desarrollo)

```bash
pytest tests/
```

## 📝 Ejemplo de Flujo Completo

```python
# 1. Cargar datos
data = pd.read_csv('mi_proceso.csv')

# 2. Inicializar analizador
analyzer = SPCAnalyzer(data, subgroup_size=5)

# 3. Ejecutar análisis
results = analyzer.analyze()

# 4. Visualizar
from spc_modules.visualization import SPCPlotter
plotter = SPCPlotter()
fig = plotter.plot_xbar_r_chart(data.values, 5, limits)

# 5. Obtener explicación IA
assistant = SPCAssistant()
explanation = assistant.explain_control_limits(limits, descriptive_stats)
print(explanation)
```

## 🎨 Características Visuales

- **Interfaz Clara**: División por fases con botones de navegación
- **Tarjetas de Información**: Métricas en tarjetas visuales
- **Semáforos**: Verde (✓), Amarillo (⚠️), Rojo (❌)
- **Gráficos Interactivos**: Zoom, pan, hover con Plotly
- **Responsive**: Compatible con laptop y tablet
- **Tema Profesional**: Colores suaves y legibles

## 🛠️ Tecnologías Utilizadas

| Tecnología | Propósito |
|-----------|----------|
| **Streamlit** | Framework web interactivo |
| **Pandas/NumPy** | Manipulación y cálculos datos |
| **SciPy/Statsmodels** | Análisis estadístico |
| **Plotly** | Gráficos interactivos |
| **OpenAI API** | Asistente IA inteligente |
| **Python** | Lenguaje base |

## 📚 Referencias Estadísticas

- Montgomery, D. C. (2020). "Statistical Quality Control"
- Ryan, T. P. (2011). "Statistical Methods for Quality Improvement"
- Box, G. E., & Luceno, A. (1997). "Statistical Control by Monitoring and Adjustment"

## 🤝 Contribuciones

Este proyecto está en constante evolución. Contribuciones y sugerencias son bienvenidas.

## 📄 Licencia

(Especificar licencia si corresponde)

## 👨‍💻 Autor

Desarrollado como herramienta educativa y profesional para SPC.

## 🔗 Enlaces Útiles

- [Documentación de Streamlit](https://docs.streamlit.io/)
- [SciPy Stats](https://docs.scipy.org/doc/scipy/reference/stats.html)
- [OpenAI API](https://platform.openai.com/docs/)

## Ejecución local

```bash
python run.py
```

Luego abre en tu navegador: `http://127.0.0.1:5000/`

## Próximos pasos sugeridos

- Agregar módulos de análisis estadístico en `app/services/`.
- Incorporar carga y validación de datasets.
- Diseñar dashboards con métricas y visualizaciones.
- Añadir pruebas unitarias y de integración para nuevas funcionalidades.
