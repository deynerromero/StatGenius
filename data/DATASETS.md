# 📊 Datasets de Ejemplo - StatGenius

Aquí encontrarás 5 datasets CSV con 500 filas cada uno, listos para cargar en StatGenius. Cada dataset presenta diferentes patrones y características para demostrar el software.

## 🎯 Dataset Principal (RECOMENDADO)

### **spc_dataset_500_samples.csv**
**Ideal para:** Prueba completa de todas las funcionalidades

- **Filas:** 500 (con 100 por cada patrón)
- **Columnas:**
  - `Sample_Number`: ID de la muestra (1-500)
  - `Timestamp`: Fecha y hora (cada hora desde 2024-01-01)
  - `Value`: Valor del proceso (0-500) - **USAR ESTA COLUMNA**
  - `Subgroup_Position`: Posición en subgrupo (1-5)
  - `BatchID`: Identificador del lote (BATCH_001 a BATCH_010)
  - `Pattern`: Tipo de patrón detectado

**Características:**
- 🟢 Filas 1-100: **Proceso Normal** (media ≈ 100, σ ≈ 1.8)
- 📈 Filas 101-200: **Tendencia Ascendente** (gradual)
- 🔵 Filas 201-350: **Desplazamiento de Media** (media ≈ 104)
- 🔴 Filas 351-450: **Desplazamiento Mayor** (media ≈ 106, σ ≈ 1.8)
- ⚠️ Filas 451-500: **Alta Variabilidad** (σ ≈ 4.3)

**Cómo usar:**
1. Fase 1: Cargar archivo → `spc_dataset_500_samples.csv`
2. Columna: Selecciona `Value`
3. Tamaño de subgrupo: `5` (natural porque es divisor de 500)
4. Fase 2: Verás cambios en normalidad y aleatoriedad
5. Fase 7: Visualizarás claramente los 5 patrones

---

## 🏆 Dataset de Proceso de Alta Calidad

### **spc_dataset_quality_process.csv**
**Ideal para:** Demostrar procesos capaces (Cpk > 1.33)

- **Filas:** 500
- **Columnas:**
  - `Sample`: Número de muestra
  - `Measurement`: **Valor del proceso** (media ≈ 50, σ ≈ 0.8)
  - `Time`: Timestamp

**Características:**
- Baja variabilidad (~0.78)
- Media centrada
- Proceso muy estable
- Excelente capacidad

**Esperas ver:**
- ✅ Normalidad: PASA
- ✅ Aleatoriedad: PASA
- ✅ Cpk > 2.0 (proceso excelente)
- ✅ Casi 0% no conformes

---

## 🔄 Dataset con Autocorrelación

### **spc_dataset_autocorrelated_process.csv**
**Ideal para:** Violar supuestos de independencia

- **Filas:** 500
- **Columnas:**
  - `Sample`: Número de muestra
  - `Reading`: **Valor del proceso** (auto-correlacionado)
  - `DateTime`: Timestamp cada 15 minutos

**Características:**
- Violación de independencia (70% correlacionado con valor anterior)
- Patrones de "picos y valles"
- No cumple supuesto de aleatoriedad

**Esperas ver:**
- ⚠️ Normalidad: PASA
- ❌ Aleatoriedad: **NO PASA** (p-valor bajo)
- ⚠️ Necesita gráfico I-MR en lugar de Xbar-R

---

## 📊 Dataset No-Normal

### **spc_dataset_non_normal_process.csv**
**Ideal para:** Estudiar violación de normalidad

- **Filas:** 500
- **Columnas:**
  - `SampleID`: Identificador
  - `ProcessValue`: **Valor del proceso** (95% normal + 5% outliers)

**Características:**
- Distribución con colas pesadas (heavy tails)
- 5% de valores extremos
- No pasa prueba Shapiro-Wilk

**Esperas ver:**
- ❌ Normalidad: **NO PASA**
- ✅ Aleatoriedad: PASA
- ⚠️ Límites de control pueden no ser válidos
- 💡 IA recomienda transformación de datos

---

## 🌊 Dataset con Patrón Cíclico

### **spc_dataset_cyclic_process.csv**
**Ideal para:** Analizar procesos con variación periódica

- **Filas:** 500
- **Columnas:**
  - `Obs_Number`: Número de observación
  - `Output`: **Valor del proceso** (patrón sinusoidal)
  - `TimePoint`: Punto de tiempo (0-499)

**Características:**
- Patrón sine wave con amplitud de ±5
- Ciclo de 50 observaciones
- Apariencia de "fuera de control" pero con patrón predecible

**Esperas ver:**
- ⚠️ Normalidad: Baja (patrón no Gaussiano puro)
- ❌ Aleatoriedad: **NO PASA** (correlación seria)
- 📈 Gráfico mostrará patrón sistemático
- 💡 Sugiere investigar causa de ciclicidad

---

## 🚀 Cómo Usar Cada Dataset

### **Caso 1: Aprendizaje Rápido** (5 min)
```
1. spc_dataset_500_samples.csv
2. Columna: Value, Subgrupo: 5
3. Fase 2-3, luego Fase 7 para ver gráfico
```

### **Caso 2: Validar Capacidad** (10 min)
```
1. spc_dataset_quality_process.csv
2. Columna: Measurement, Subgrupo: 1
3. Fase 3 (Define LIE=48, LSE=52)
4. Fase 5 para ver índices
```

### **Caso 3: Entender Violaciones** (15 min)
```
1. Carga: spc_dataset_non_normal_process.csv
2. Comenta: Nota Fase 2 ("NO PASA")
3. Luego: spc_dataset_autocorrelated_process.csv
4. Compara: Cómo difieren los resultados
```

### **Caso 4: Investigación Avanzada** (20 min)
```
1. Fase 1: spc_dataset_cyclic_process.csv
2. Fase 2-3: Observa los supuestos violados
3. Fase 4-8: Analiza con IA cómo interpretar
```

---

## 📈 Estadísticas Rápidas

| Dataset | Media | Desv.Est | Min | Max | Patrón |
|---------|-------|----------|-----|-----|--------|
| **Principal** | 99-106 | 1.8-4.3 | 95 | 110 | 5 patrones |
| **Calidadad** | 50.0 | 0.8 | 47.4 | 53.1 | Estable |
| **Autocorr.** | 100.1 | 1.2 | 96.1 | 103.3 | Correlado |
| **No-Normal** | 99.9 | 2.2 | 86.1 | 114.5 | Outliers |
| **Cíclico** | Varía | Variable | -5 | +5 | Sinusoidal |

---

## 💾 Generar Nuevos Datasets

Si necesitas más datos o varaciones, puedes ejecutar:

```bash
python data/generate_large_dataset.py
```

O modificar el script `data/generate_large_dataset.py` para crear tus propios patrones.

---

## 📝 Formato de Importación

Todos los datasets están en formato **CSV estándar**:
- Separador: Coma (,)
- Encoding: UTF-8
- Encabezado: Incluido en primera fila
- Decimales: Punto (.)

Puedes abrirlos en:
- ✅ StatGenius
- ✅ Excel
- ✅ Python/Pandas
- ✅ R
- ✅ Cualquier herramienta que lea CSV

---

## 🎓 Preguntas Comunes

**P: ¿Puedo usar mis propios datos?**
R: Sí, cópialos a la carpeta `data/` y cárgalos en Fase 1.

**P: ¿Qué columna selecciono?**
R: La que contenga **valores de medición** (numérica). La documentación anterior te guía.

**P: ¿Puedo cambiar el tamaño de subgrupo?**
R: Sí, pero algunos datasets están diseñados para n=5 o n=1. Experimenta.

**P: ¿Estos datos son realistas?**
R: Sí, generados con patrones estadísticos comunes en procesos reales.

---

## 🔗 Próximos Pasos

1. ✅ Cargó datasets → Verifica que aparezcan en `data/`
2. 🚀 Ejecuta: `streamlit run app.py`
3. 📊 Fase 1: Carga `spc_dataset_500_samples.csv`
4. 🎓 Experimenta con todos los datasets
5. 💾 Descarga resultados (.json) después de cada análisis

---

**Versión:** 1.0  
**Fecha:** May 15, 2024  
**Generado automaticamente para StatGenius**
