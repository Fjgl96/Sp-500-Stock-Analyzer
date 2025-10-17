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

# Configuración de yfinance con headers personalizados
import yfinance as yf
import requests

# Configura sesión con headers personalizados para evitar bloqueos
session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
})

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
    "INTC", "VZ", "NKE", "TMO", "ABT", "CVX", "MRK", "ACN", "COST", "DHR",
    "LLY", "MDT", "ORCL", "TXN", "NEE", "PM", "HON", "UNP", "RTX", "LOW",
    "QCOM", "BMY", "SBUX", "IBM", "INTU", "AMD", "AMGN", "CAT", "GE",
    "BA", "MMM", "GS", "BKNG", "BLK", "AXP", "DE", "LMT", "SPGI", "SYK",
    "GILD", "ADP", "MO", "TGT", "MDLZ", "CI", "CVS", "ISRG", "ZTS", "USB",
    "PLD", "C", "DUK", "SO", "MMC", "TJX", "BDX", "CB", "EOG", "CL",
    "NSC", "ITW", "BSX", "HCA", "EQIX", "SHW", "PNC", "CME", "SCHW"
]

# Colores para gráficos
CHART_COLORS = {
    'primary': '#1f77b4',
    'secondary': '#ff7f0e',
    'success': '#2ca02c',
    'danger': '#d62728',
    'warning': '#ff9800',
    'info': '#17a2b8',
    'bullish': '#26a69a',
    'bearish': '#ef5350',
    'volume': '#78909c',
    'ma_short': '#ff6b6b',
    'ma_long': '#4ecdc4',
    'rsi_oversold': '#26a69a',
    'rsi_overbought': '#ef5350',
    'macd': '#2196f3',
    'signal': '#ff9800',
    'bb_upper': '#9e9e9e',
    'bb_middle': '#607d8b',
    'bb_lower': '#9e9e9e'
}

# Configuración de indicadores técnicos
INDICATORS_CONFIG = {
    'sma': {
        'periods': [20, 50, 200],
        'default_period': 50
    },
    'ema': {
        'periods': [12, 26, 50],
        'default_period': 20
    },
    'rsi': {
        'period': 14,
        'overbought': 70,
        'oversold': 30
    },
    'macd': {
        'fast': 12,
        'slow': 26,
        'signal': 9
    },
    'bollinger_bands': {
        'period': 20,
        'std_dev': 2
    },
    'stochastic': {
        'k_period': 14,
        'd_period': 3,
        'overbought': 80,
        'oversold': 20
    },
    'atr': {
        'period': 14
    }
}

# Períodos de tiempo disponibles
TIME_PERIODS = {
    '1 Día': '1d',
    '5 Días': '5d',
    '1 Mes': '1mo',
    '3 Meses': '3mo',
    '6 Meses': '6mo',
    '1 Año': '1y',
    '2 Años': '2y',
    '5 Años': '5y',
    '10 Años': '10y',
    'Año hasta la fecha': 'ytd',
    'Máximo': 'max'
}

# Intervalos disponibles
TIME_INTERVALS = {
    '1 Minuto': '1m',
    '2 Minutos': '2m',
    '5 Minutos': '5m',
    '15 Minutos': '15m',
    '30 Minutos': '30m',
    '1 Hora': '1h',
    '1 Día': '1d',
    '5 Días': '5d',
    '1 Semana': '1wk',
    '1 Mes': '1mo',
    '3 Meses': '3mo'
}

# Configuración de cache
CACHE_CONFIG = {
    'stock_data_ttl': 3600,  # 1 hora
    'market_data_ttl': 1800,  # 30 minutos
    'stock_info_ttl': 7200,   # 2 horas
    'sp500_list_ttl': 86400   # 24 horas
}

# Configuración de la aplicación
APP_SETTINGS = {
    'max_stocks_comparison': 10,
    'default_chart_height': 600,
    'enable_animations': True,
    'theme': 'plotly_white'
}