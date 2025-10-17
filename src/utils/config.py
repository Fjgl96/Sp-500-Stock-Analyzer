"""
Configuración de la aplicación
"""

import streamlit as st

# Configuración de la página
APP_CONFIG = {
    "page_title": "S&P 500 Stock Analyzer",
    "page_icon": "📊",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# Configuración de yfinance
import yfinance as yf
import requests

# Configura sesión con headers personalizados
session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
})

# Aplica la sesión a yfinance
yf.pdr_override()

# Índices principales
MAJOR_INDICES = {
    "S&P 500": "^GSPC",
    "Dow Jones": "^DJI",
    "NASDAQ": "^IXIC",
    "Russell 2000": "^RUT"
}

# Lista de acciones populares del S&P 500
SP500_STOCKS = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA", "BRK.B",
    "V", "JNJ", "WMT", "JPM", "MA", "PG", "UNH", "HD", "DIS", "BAC",
    "ADBE", "CRM", "NFLX", "CMCSA", "XOM", "KO", "PEP", "CSCO", "AVGO",
    "INTC", "VZ", "NKE", "TMO", "ABT", "CVX", "MRK", "ACN", "COST", "DHR"
]