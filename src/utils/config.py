"""
Configuraciones globales del proyecto
"""

import os
from pathlib import Path

# Paths del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
CACHE_DIR = DATA_DIR / "cache"

# Crear directorios si no existen
for directory in [RAW_DATA_DIR, PROCESSED_DATA_DIR, CACHE_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Configuración de la aplicación
APP_CONFIG = {
    "page_title": "S&P 500 Stock Analyzer",  # ← Cambiar 'title' por 'page_title'
    "page_icon": "📈",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# Configuración de datos
DATA_CONFIG = {
    "default_period": "1y",
    "default_interval": "1d",
    "cache_expiry_hours": 24
}

# Colores para gráficos
CHART_COLORS = {
    "primary": "#1f77b4",
    "secondary": "#ff7f0e",
    "success": "#2ca02c",
    "danger": "#d62728",
    "warning": "#ff9800",
    "info": "#17a2b8"
}

# Indicadores técnicos - Configuración por defecto
INDICATORS_CONFIG = {
    "sma_periods": [20, 50, 200],
    "ema_periods": [12, 26],
    "rsi_period": 14,
    "macd_fast": 12,
    "macd_slow": 26,
    "macd_signal": 9,
    "bollinger_period": 20,
    "bollinger_std": 2
}