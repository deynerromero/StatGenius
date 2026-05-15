# 🚀 StatGenius - Guía de Inicio Rápido

## ⚡ En 5 minutos

### 1. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

### 2. **Configurar OpenAI (opcional pero recomendado)**
```bash
# Obtén una clave en https://platform.openai.com/api-keys
export OPENAI_API_KEY=sk-your-key-here
```

### 3. **Ejecutar la aplicación**
```bash
streamlit run app.py
```

**¡Listo!** Se abrirá automáticamente en `http://localhost:8501`

---

## 📊 Flujo de uso típico

### Primera vez: Usa datos de ejemplo
1. Abre la aplicación ✓
2. Fase 1: Haz clic en **"Cargar datos de ejemplo"**
3. Fase 2: Haz clic en **"Ejecutar pruebas"**
4. Ve atravesando las fases ➡️ Siguiente en cada fase

### Con tus datos
1. Fase 1: Carga tu CSV/Excel
2. Selecciona la columna y tamaño de subgrupo
3. Continúa con los pasos

---

## 🎯 Cada fase, explicada brevemente

| Fase | Qué hace | Tiempo |
|------|----------|---------|
| **1** 📥 | Cargar datos | 1 min |
| **2** ✅ | Validar supuestos | 2 min |
| **3** ⚙️ | Configurar gráfico | 1 min |
| **4** 📈 | Calcular potencia | 2 min |
| **5** 🎯 | Analizar capacidad | 1 min |
| **6** 🔧 | Optimizar muestreo | 2 min |
| **7** 📉 | Ver gráfico | 1 min |
| **8** 🤖 | Leer recomendaciones IA | 2 min |

**Total:** ~12 minutos para análisis completo

---

## ⚠️ Soluciones a problemas comunes

### **"ModuleNotFoundError"**
```bash
# Reinstala dependencias
pip install --upgrade -r requirements.txt
```

### **"OPENAI_API_KEY not found"**
```bash
# Opción 1: Variable de entorno
export OPENAI_API_KEY=sk-...

# Opción 2: Archivo .env
# Crea archivo .env en la raíz con:
OPENAI_API_KEY=sk-...

# Sin API key: La app funciona sin IA
```

### **Puerto 8501 en uso**
```bash
# Usa otro puerto
streamlit run app.py --server.port=8502
```

### **Muere al calcular**
- Si tienes +1000 filas, intenta aumentar en 3 min el timeout
- Usa subgrupos más pequeños (n=2 en lugar de n=10)

---

## 🧮 Casos de uso

### Caso 1: Auditoría de proceso
1. Fase 1: Carga datos del mes
2. Fase 2: Verifica normalidad
3. Fase 3: Crea gráfico Xbar-R
4. Fase 7: Visualiza y exporta

**⏱️ Tiempo: 5 minutos**

### Caso 2: Diseño de plan de muestreo
1. Fases 1-3: Setup básico
2. Fase 4: Experimenta con `δ` (corrimiento)
3. Fase 6: Compara tamaños de muestra
4. Fase 8: Lee recomendación IA

**⏱️ Tiempo: 15 minutos**

### Caso 3: Análisis de capacidad
1. Fases 1-3: Setup
2. Fase 5: Calcula Cp, Cpk, P(no conforme)
3. Si Cpk < 1.33: Lee recomendación IA
4. Descarga resultados

**⏱️ Tiempo: 10 minutos**

---

## 📁 Archivos importantes

```
StatGenius/
├── app.py                    ← EJECUTA ESTO
├── requirements.txt          ← pip install
├── .env.example              ← Copia como .env
├── verify_setup.py           ← Verifica instalación
├── spc_modules/              ← Lógica estadística
├── data/                     ← Datos de ejemplo
└── README.md                 ← Documentación completa
```

---

## 🔗 Accesos rápidos

- **Documentación completa:** [README.md](README.md)
- **Verificar setup:** `python verify_setup.py`
- **Generar datos ejemplo:** `python data/sample_data_generator.py`
- **Obtener API key:** https://platform.openai.com/account/api-keys

---

## 💡 Tips

✅ **Copia tus datos a `data/` para fácil acceso**
✅ **Descarga resultados .json después de cada análisis**
✅ **La IA explica mejor con +20 muestras**
✅ **Experimenta con diferentes `α` y `δ` en Fases 3-4**
✅ **Para procesos con tendencia, usa I-MR en lugar de Xbar-R**

---

## 🎓 Aprende más

- **SPC Básico:** Libros de Montgomery o Wheeler
- **Potencia estadística:** Ejemplos en Fase 4
- **Capacidad:** https://en.wikipedia.org/wiki/Process_capability

¡Disfruta analizando procesos! 📊
