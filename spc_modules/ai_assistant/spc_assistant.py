"""
AI-powered SPC Assistant (OpenAI or Ollama)
"""
import os
from openai import OpenAI
from typing import Optional


class SPCAssistant:
    """AI Assistant for SPC interpretations and recommendations"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize SPC Assistant
        
        Parameters:
        -----------
        api_key : str
            OpenAI API key (reads from OPENAI_API_KEY env var if not provided)
        """
        self.provider = os.getenv("AI_PROVIDER", "openai").strip().lower()

        if self.provider == "ollama":
            self.base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
            self.model = os.getenv("OLLAMA_MODEL", "llama3.2")
            # Ollama does not require a real API key, but the OpenAI client expects one.
            self.api_key = os.getenv("OLLAMA_API_KEY", "ollama")
            self.client = OpenAI(base_url=self.base_url, api_key=self.api_key)
        elif self.provider == "openai":
            self.api_key = api_key or os.getenv("OPENAI_API_KEY")
            if not self.api_key:
                raise ValueError(
                    "OPENAI_API_KEY not found. Set it in environment or pass it to __init__"
                )
            self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
            self.client = OpenAI(api_key=self.api_key)
        else:
            raise ValueError(
                "AI_PROVIDER inválido. Usa 'openai' u 'ollama'."
            )

        self.system_prompt = self._get_system_prompt()
    
    def _get_system_prompt(self) -> str:
        """Get system prompt for SPC expert"""
        return """Eres un experto en Control Estadístico de Procesos (SPC) y Estadística.
Tu rol es explicar resultados de análisis SPC en lenguaje sencillo, didáctico y profesional.

Directrices:
1. Explica conceptos complejos de forma accesible (como si enseñaras a estudiantes de ingeniería)
2. Sé específico y práctico: da ejemplos concretos y recomendaciones accionables
3. Usa analogías cuando sea útil
4. Estructura tu respuesta en párrafos cortos y fáciles de leer
5. Siempre indica el nivel de confianza o certeza (alto, medio, bajo)
6. Si hay riesgos o limitaciones, menciónalos claramente
7. Usa términos técnicos correctamente pero explícalos

Tono: Profesional pero accesible, como un profesor experimentado explicando a sus estudiantes."""
    
    def explain_normality_test(self, test_results: dict) -> str:
        """Explain normality test results"""
        prompt = f"""Explica estos resultados de prueba de normalidad (Shapiro-Wilk y Anderson-Darling):

Shapiro-Wilk: p-valor = {test_results['shapiro_wilk']['p_value']:.4f}, Pasa: {test_results['shapiro_wilk']['passes']}
Anderson-Darling: Estadístico = {test_results['anderson_darling']['statistic']:.4f}, Crítico = {test_results['anderson_darling']['critical_value']:.4f}, Pasa: {test_results['anderson_darling']['passes']}

¿Qué significa esto para el análisis del proceso? ¿Hay implicaciones prácticas si no sigue una distribución normal?
Sé conciso pero informativo (máximo 150 palabras)."""
        
        return self._call_gpt(prompt)
    
    def explain_randomness_test(self, test_results: dict) -> str:
        """Explain randomness/independence test results"""
        prompt = f"""Explica este resultado de prueba de independencia (Runs Test):

Estadístico Z: {test_results['z_statistic']:.4f}
P-valor: {test_results['p_value']:.4f}
Resultado: {test_results['interpretation']}

¿Qué implica esto para el control del proceso? ¿Hay autocorrelación problemática?
Sé conciso (máximo 100 palabras)."""
        
        return self._call_gpt(prompt)
    
    def explain_control_limits(self, control_results: dict, descriptive_stats: dict) -> str:
        """Explain control limits and stability"""
        limit_info = f"""Límites de Control Calculados:
Centro: {control_results.get('center', 'N/A')}
LCI: {control_results.get('lcl', 'N/A')}
LCS: {control_results.get('ucl', 'N/A')}
Tipo de Gráfico: {control_results.get('chart_type', 'Desconocido')}

Media del proceso: {descriptive_stats['mean']:.4f}
Desv. Est.: {descriptive_stats['std_dev']:.4f}
Coef. Variación: {descriptive_stats['cv']:.4f}"""
        
        prompt = f"""Interpreta estos límites de control para un gráfico de control:

{limit_info}

¿Es el proceso estable? ¿Hay indicios de variación anormal? ¿Qué recomendaciones harías?
Sé práctico y conciso (máximo 120 palabras)."""
        
        return self._call_gpt(prompt)
    
    def explain_power_and_arl(self, power_results: dict, sampling_freq: float) -> str:
        """Explain power and ARL results"""
        prompt = f"""Un plan de muestreo tiene estas características:

Corrimiento a detectar (δ): {power_results['delta']} sigma
Potencia (1-β): {power_results['power']:.1%}
ARL₀: {power_results['arl0']:.1f} muestras (sin cambio)
ARL₁: {power_results['arl1']:.1f} muestras (con cambio)
Frecuencia de muestreo: Cada {sampling_freq} minutos

¿Es adecuado este plan? ¿Cuál es el tiempo promedio para detectar un cambio? 
¿Qué tan probable es detectar este corrimiento?
Sé conciso (máximo 120 palabras)."""
        
        return self._call_gpt(prompt)
    
    def explain_capability(self, capability_results: dict, lsl: float, usl: float) -> str:
        """Explain process capability"""
        capk = capability_results.get('cpk', 'N/A')
        cp = capability_results.get('cp', 'N/A')
        prob_non = capability_results.get('prob_nonconforming', 'N/A')
        
        prompt = f"""Resultados de Capacidad del Proceso:

Cp (Potencial): {cp}
Cpk (Real): {capk}
LSE: {usl}, LIE: {lsl}
Probabilidad de no conformes: {prob_non}

En términos prácticos, ¿puede el proceso cumplir con las especificaciones?
¿Qué es prioritario: centrar el proceso o reducir variabilidad?
Sé directo (máximo 100 palabras)."""
        
        return self._call_gpt(prompt)
    
    def recommend_sampling_plan(self, process_info: dict) -> str:
        """Recommend optimal sampling plan"""
        prompt = f"""Basado en este proceso:

- Tamaño de subgrupo actual: {process_info.get('subgroup_size', 'N/A')}
- Desviación Estimada: {process_info.get('sigma_estimated', 'N/A')}
- Número de muestras actual: {process_info.get('observations', 'N/A')}
- Corrmientos esperados: {process_info.get('expected_shifts', 'Pequeños')}

¿Cuál sería un plan de muestreo óptimo? Considera costo vs. detección.
¿Cuál debería ser n (tamaño) y con qué frecuencia?
Sé pragmático (máximo 120 palabras)."""
        
        return self._call_gpt(prompt)
    
    def _call_gpt(self, prompt: str) -> str:
        """Call OpenAI API"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
                max_tokens=300,
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error al consultar IA: {str(e)}"
    
    def get_phase_guidance(self, phase_number: int, phase_name: str) -> str:
        """Get guidance for a specific phase"""
        phase_guidance = {
            1: "Ingreso de datos",
            2: "Validación de supuestos",
            3: "Configuración del gráfico",
            4: "Análisis de corrimiento y potencia",
            5: "Desempeño y calidad",
            6: "Optimización del muestreo",
            7: "Visualización del gráfico",
            8: "Interpretación final",
        }
        
        prompt = f"""¿Cuál es el objetivo principal de la Fase {phase_number}: {phase_name}?
Dale al usuario unas directrices claras sobre qué datos o decisiones necesita para esta fase.
De forma breve (máximo 80 palabras)."""
        
        return self._call_gpt(prompt)
