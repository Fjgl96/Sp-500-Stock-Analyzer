"""
Módulo para descargar datos de Yahoo Finance con manejo robusto de errores
"""

import yfinance as yf
import streamlit as st
import time
import pandas as pd
from typing import Dict, Optional

@st.cache_data(ttl=3600, show_spinner="📊 Cargando datos...")
def get_stock_data(ticker: str, period: str = "1y", interval: str = "1d") -> Optional[pd.DataFrame]:
    """
    Descarga datos de una acción con retry logic
    
    Args:
        ticker: Símbolo de la acción (ej: 'AAPL')
        period: Período de tiempo ('1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max')
        interval: Intervalo ('1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo')
    
    Returns:
        DataFrame con datos históricos o None si falla
    """
    max_retries = 5
    retry_delay = 2
    
    for attempt in range(max_retries):
        try:
            # Delay progresivo entre reintentos
            if attempt > 0:
                wait_time = retry_delay * attempt
                time.sleep(wait_time)
            
            # Descarga con timeout
            stock = yf.Ticker(ticker)
            data = stock.history(
                period=period,
                interval=interval,
                timeout=15,
                raise_errors=False
            )
            
            # Verifica que tenga datos
            if data is not None and not data.empty and len(data) > 0:
                return data
            
            # Si está vacío pero no es el último intento, continúa
            if attempt < max_retries - 1:
                continue
                
        except Exception as e:
            if attempt == max_retries - 1:
                st.error(f"❌ Error al cargar {ticker}: {str(e)}")
                return None
            continue
    
    st.warning(f"⚠️ No se pudieron obtener datos para {ticker}")
    return None


@st.cache_data(ttl=1800, show_spinner="📈 Cargando múltiples acciones...")
def get_multiple_stocks(tickers: list, period: str = "1y") -> Dict[str, pd.DataFrame]:
    """
    Descarga datos de múltiples acciones con delays
    
    Args:
        tickers: Lista de símbolos ['AAPL', 'GOOGL', 'MSFT']
        period: Período de tiempo
    
    Returns:
        Diccionario {ticker: DataFrame}
    """
    data_dict = {}
    total = len(tickers)
    
    # Progress bar
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i, ticker in enumerate(tickers):
        # Actualiza progreso
        progress = (i + 1) / total
        progress_bar.progress(progress)
        status_text.text(f"Cargando {ticker}... ({i+1}/{total})")
        
        # Delay entre requests para evitar rate limiting
        if i > 0:
            time.sleep(1.5)
        
        # Descarga datos
        data = get_stock_data(ticker, period)
        if data is not None and not data.empty:
            data_dict[ticker] = data
    
    # Limpia UI
    progress_bar.empty()
    status_text.empty()
    
    return data_dict


@st.cache_data(ttl=1800)
def get_stock_info(ticker: str) -> Optional[dict]:
    """
    Obtiene información de la empresa
    
    Args:
        ticker: Símbolo de la acción
    
    Returns:
        Diccionario con info de la empresa o None
    """
    max_retries = 3
    
    for attempt in range(max_retries):
        try:
            if attempt > 0:
                time.sleep(2)
            
            stock = yf.Ticker(ticker)
            info = stock.info
            
            if info and len(info) > 0:
                return info
                
        except Exception as e:
            if attempt == max_retries - 1:
                st.warning(f"⚠️ No se pudo obtener información de {ticker}")
                return None
            continue
    
    return None