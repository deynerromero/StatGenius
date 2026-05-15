# StatGenius

StatGenius es una aplicación web inicial construida con **Python** y **Flask**, preparada para evolucionar hacia funcionalidades de análisis y visualización estadística.

## Propósito inicial del proyecto

- Establecer una base limpia y modular para una aplicación de estadísticas.
- Contar con una interfaz web profesional y simple como punto de partida.
- Facilitar la evolución hacia servicios de análisis de datos y reportes.

## Estructura de carpetas

```text
StatGenius/
├─ .github/
│  └─ copilot-instructions.md
├─ app/
│  ├─ __init__.py
│  ├─ routes.py
│  ├─ services/
│  │  └─ __init__.py
│  ├─ templates/
│  │  ├─ base.html
│  │  └─ index.html
│  └─ static/
│     ├─ css/
│     │  └─ styles.css
│     └─ js/
│        └─ main.js
├─ tests/
│  ├─ __init__.py
│  └─ test_app.py
├─ run.py
├─ requirements.txt
└─ .gitignore
```

## Instalación

1. Crear entorno virtual (recomendado):

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\\Scripts\\activate   # Windows
```

2. Instalar dependencias:

```bash
pip install -r requirements.txt
```

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
