"""
Módulo para obtener datos de acciones usando yfinance
"""

import yfinance as yf
import pandas as pd
import time
from typing import Dict, List, Optional
import streamlit as st

class StockDataFetcher:
    """Clase para obtener datos de acciones con manejo robusto de errores"""
    
    def __init__(self):
        """Inicializa el fetcher"""
        self.max_retries = 5
        self.retry_delay = 2
    
    def get_stock_data(
        self, 
        ticker: str, 
        period: str = '1y',
        interval: str = '1d'
    ) -> Optional[pd.DataFrame]:
        """
        Obtiene datos históricos de una acción con retry logic
        
        Args:
            ticker: Símbolo de la acción
            period: Período ('1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max')
            interval: Intervalo ('1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo')
        
        Returns:
            DataFrame con datos históricos o None
        """
        for attempt in range(self.max_retries):
            try:
                # Delay entre reintentos
                if attempt > 0:
                    time.sleep(self.retry_delay * attempt)
                
                # Descarga datos
                stock = yf.Ticker(ticker)
                df = stock.history(
                    period=period,
                    interval=interval,
                    timeout=15,
                    raise_errors=False
                )
                
                # Verifica que tenga datos
                if df is not None and not df.empty and len(df) > 0:
                    return df
                
                # Si está vacío, continúa al siguiente intento
                if attempt < self.max_retries - 1:
                    continue
                    
            except Exception as e:
                if attempt == self.max_retries - 1:
                    try:
                        st.error(f"❌ Error al cargar {ticker}: {str(e)}")
                    except:
                        pass
                    return None
                continue
        
        try:
            st.warning(f"⚠️ No se pudieron obtener datos para {ticker}")
        except:
            pass
        return None
    
    def get_multiple_stocks(
        self, 
        tickers: List[str], 
        period: str = '1y',
        interval: str = '1d'
    ) -> Dict[str, pd.DataFrame]:
        """
        Obtiene datos de múltiples acciones con delays
        
        Args:
            tickers: Lista de símbolos
            period: Período de tiempo
            interval: Intervalo
        
        Returns:
            Diccionario {ticker: DataFrame}
        """
        data_dict = {}
        total = len(tickers)
        
        # Progress bar (intenta mostrar, si falla continúa sin progress)
        try:
            progress_bar = st.progress(0)
            status_text = st.empty()
            show_progress = True
        except:
            show_progress = False
        
        for i, ticker in enumerate(tickers):
            # Actualiza progreso
            if show_progress:
                try:
                    progress = (i + 1) / total
                    progress_bar.progress(progress)
                    status_text.text(f"Cargando {ticker}... ({i+1}/{total})")
                except:
                    pass
            
            # Delay entre requests
            if i > 0:
                time.sleep(1.5)
            
            # Descarga datos
            df = self.get_stock_data(ticker, period, interval)
            if df is not None and not df.empty:
                data_dict[ticker] = df
        
        # Limpia UI
        if show_progress:
            try:
                progress_bar.empty()
                status_text.empty()
            except:
                pass
        
        return data_dict
    
    def get_stock_info(self, ticker: str) -> Dict:
        """
        Obtiene información de la empresa
        
        Args:
            ticker: Símbolo de la acción
        
        Returns:
            Diccionario con información de la empresa
        """
        for attempt in range(3):
            try:
                if attempt > 0:
                    time.sleep(2)
                
                stock = yf.Ticker(ticker)
                info = stock.info
                
                if info and len(info) > 0:
                    # Estandariza nombres de campos
                    standardized_info = {
                        'sector': info.get('sector', 'N/A'),
                        'industry': info.get('industry', 'N/A'),
                        'market_cap': info.get('marketCap', 0),
                        'pe_ratio': info.get('trailingPE', 0),
                        'forward_pe': info.get('forwardPE', 0),
                        'dividend_yield': info.get('dividendYield', 0),
                        'beta': info.get('beta', 0),
                        'website': info.get('website', ''),
                        'description': info.get('longBusinessSummary', '')
                    }
                    return standardized_info
                    
            except Exception as e:
                if attempt == 2:
                    try:
                        st.warning(f"⚠️ No se pudo obtener información de {ticker}")
                    except:
                        pass
                    return {}
                continue
        
        return {}
    
    def get_sp500_tickers(self) -> List[str]:
        """
        Obtiene lista de tickers del S&P 500
        
        Returns:
            Lista de símbolos del S&P 500
        """
        # Lista hardcodeada de tickers populares del S&P 500
        tickers = [
            'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'TSLA', 'BRK.B',
            'V', 'JNJ', 'WMT', 'JPM', 'MA', 'PG', 'UNH', 'HD', 'DIS', 'BAC',
            'ADBE', 'CRM', 'NFLX', 'CMCSA', 'XOM', 'KO', 'PEP', 'CSCO', 'AVGO',
            'INTC', 'VZ', 'NKE', 'TMO', 'ABT', 'CVX', 'MRK', 'ACN', 'COST', 'DHR',
            'LLY', 'MDT', 'ORCL', 'TXN', 'NEE', 'PM', 'HON', 'UNP', 'RTX', 'LOW',
            'QCOM', 'BMY', 'SBUX', 'IBM', 'INTU', 'AMD', 'AMGN', 'CAT', 'GE',
            'BA', 'MMM', 'GS', 'BKNG', 'BLK', 'AXP', 'DE', 'LMT', 'SPGI', 'SYK',
            'GILD', 'ADP', 'MO', 'TGT', 'MDLZ', 'CI', 'CVS', 'ISRG', 'ZTS', 'USB',
            'PLD', 'C', 'DUK', 'SO', 'MMC', 'TJX', 'BDX', 'CB', 'EOG', 'CL',
            'NSC', 'ITW', 'BSX', 'HCA', 'EQIX', 'SHW', 'PNC', 'CME', 'SCHW'
        ]
        
        return sorted(tickers)