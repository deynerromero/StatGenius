#!/bin/bash
# 🚀 Installation script for StatGenius

set -e  # Exit on error

echo "╔════════════════════════════════════════╗"
echo "║   🚀 StatGenius Installation Script    ║"
echo "║   Control Estadístico de Procesos      ║"
echo "╚════════════════════════════════════════╝"
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check Python version
echo -e "${YELLOW}[1/5]${NC} Verificando Python..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 no encontrado${NC}"
    exit 1
fi
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo -e "${GREEN}✓${NC} Python ${PYTHON_VERSION} detectado"
echo ""

# Create virtual environment
echo -e "${YELLOW}[2/5]${NC} Creando entorno virtual..."
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    echo -e "${GREEN}✓${NC} Entorno virtual creado"
else
    echo -e "${YELLOW}⚠ ${NC} Entorno virtual ya existe"
fi
echo ""

# Activate virtual environment
echo -e "${YELLOW}[3/5]${NC} Activando entorno virtual..."
source .venv/bin/activate
echo -e "${GREEN}✓${NC} Entorno activado"
echo ""

# Install dependencies
echo -e "${YELLOW}[4/5]${NC} Instalando dependencias..."
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo -e "${GREEN}✓${NC} Dependencias instaladas"
echo ""

# Verify setup
echo -e "${YELLOW}[5/5]${NC} Verificando instalación..."
python verify_setup.py
echo ""

# Create .env file if not exists
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo ""
    echo -e "${YELLOW}⚠ IMPORTANTE:${NC}"
    echo "   Se creó archivo .env"
    echo "   Edita y añade tu OPENAI_API_KEY"
    echo "   (opcional, la app funciona sin IA)"
fi

echo ""
echo "╔════════════════════════════════════════╗"
echo "║         ✅ Instalación Lista           ║"
echo "╚════════════════════════════════════════╝"
echo ""
echo "🚀 Para ejecutar la aplicación:"
echo "   source .venv/bin/activate"
echo "   streamlit run app.py"
echo ""
echo "📚 Para más información:"
echo "   cat QUICKSTART.md"
echo ""
