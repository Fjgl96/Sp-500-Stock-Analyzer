"""
Módulo para obtener datos de Yahoo Finance
"""

import yfinance as yf
import pandas as pd
import requests
from typing import List, Optional
import time
from datetime import datetime, timedelta
import pickle
from pathlib import Path
from ..utils.config import CACHE_DIR, DATA_CONFIG


class StockDataFetcher:
    """
    Clase para obtener datos de acciones desde Yahoo Finance
    """
    
    def __init__(self):
        self.cache_dir = CACHE_DIR
        self.cache_expiry = timedelta(hours=DATA_CONFIG["cache_expiry_hours"])
    
    def get_sp500_tickers(self) -> List[str]:
        """
        Obtiene la lista de tickers del S&P 500
        
        Returns:
            List[str]: Lista de símbolos de acciones
        """
        cache_file = self.cache_dir / "sp500_tickers.pkl"
        
        # Intentar cargar desde cache
        if cache_file.exists():
            cache_time = datetime.fromtimestamp(cache_file.stat().st_mtime)
            if datetime.now() - cache_time < timedelta(days=7):  # Cache por 7 días
                try:
                    with open(cache_file, 'rb') as f:
                        tickers = pickle.load(f)
                        # Validar que sean tickers válidos
                        if isinstance(tickers, list) and len(tickers) > 0:
                            if isinstance(tickers[0], str) and len(tickers[0]) <= 5:
                                print(f"✅ Cargados {len(tickers)} tickers desde cache")
                                return tickers
                except Exception as e:
                    print(f"⚠️ Error leyendo cache: {e}")
        
        try:
            print("📥 Descargando lista de tickers del S&P 500...")
            
            # Método 1: Usar pandas para leer directamente de Wikipedia
            url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
            tables = pd.read_html(url)
            
            # La primera tabla contiene los tickers
            df = tables[0]
            tickers = df['Symbol'].str.replace('.', '-').tolist()
            
            # Limpiar tickers
            tickers = [t.strip() for t in tickers if isinstance(t, str)]
            
            # Guardar en cache
            with open(cache_file, 'wb') as f:
                pickle.dump(tickers, f)
            
            print(f"✅ Obtenidos {len(tickers)} tickers del S&P 500")
            return tickers
            
        except Exception as e:
            print(f"⚠️ Error obteniendo tickers: {e}")
            print("📋 Usando lista predefinida...")
            
            # Lista amplia de fallback con tickers reales
            fallback_tickers = [
                # Tech Giants
                'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'NVDA', 'TSLA',
                # Finance
                'JPM', 'BAC', 'WFC', 'GS', 'MS', 'C', 'V', 'MA', 'AXP',
                # Healthcare
                'JNJ', 'UNH', 'PFE', 'ABBV', 'TMO', 'ABT', 'MRK', 'LLY',
                # Consumer
                'WMT', 'HD', 'PG', 'KO', 'PEP', 'COST', 'NKE', 'MCD',
                # Industrial
                'BA', 'CAT', 'GE', 'MMM', 'HON', 'UPS',
                # Telecom
                'T', 'VZ', 'TMUS',
                # Energy
                'XOM', 'CVX', 'COP', 'SLB',
                # Others
                'DIS', 'NFLX', 'CSCO', 'INTC', 'AMD', 'ADBE', 'CRM',
                'ORCL', 'IBM', 'QCOM', 'TXN', 'AVGO', 'PYPL'
            ]
            
            return sorted(fallback_tickers)
    
    def get_stock_data(
        self, 
        ticker: str, 
        period: str = "1y",
        interval: str = "1d"
    ) -> Optional[pd.DataFrame]:
        """
        Obtiene datos históricos de una acción
        
        Args:
            ticker: Símbolo de la acción
            period: Período de tiempo
            interval: Intervalo de datos
        
        Returns:
            DataFrame con datos históricos o None si hay error
        """
        cache_file = self.cache_dir / f"{ticker}_{period}_{interval}.pkl"
        
        # Intentar cargar desde cache
        if cache_file.exists():
            cache_time = datetime.fromtimestamp(cache_file.stat().st_mtime)
            if datetime.now() - cache_time < self.cache_expiry:
                try:
                    with open(cache_file, 'rb') as f:
                        df = pickle.load(f)
                        if not df.empty:
                            return df
                except:
                    pass
        
        try:
            print(f"📥 Descargando {ticker}...")
            
            # Descargar usando download (compatible con todas las versiones)
            df = yf.download(
                ticker,
                period=period,
                interval=interval,
                progress=False
            )
            
            if df.empty:
                print(f"⚠️ No hay datos para {ticker}")
                return None
            
            # Si el DataFrame tiene MultiIndex en columnas, aplanarlo
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
            
            # Asegurarse de que las columnas estén en el formato correcto
            expected_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
            if not all(col in df.columns for col in expected_columns):
                print(f"⚠️ Columnas inesperadas en {ticker}")
                return None
            
            # Limpiar datos
            df = df.dropna()
            
            if len(df) < 10:
                print(f"⚠️ Datos insuficientes para {ticker}")
                return None
            
            # Guardar en cache
            try:
                with open(cache_file, 'wb') as f:
                    pickle.dump(df, f)
            except:
                pass
            
            print(f"✅ {ticker}: {len(df)} filas obtenidas")
            return df
            
        except Exception as e:
            print(f"❌ Error descargando {ticker}: {str(e)[:100]}")
            return None
    
    def get_stock_info(self, ticker: str) -> dict:
        """
        Obtiene información básica de una acción
        
        Args:
            ticker: Símbolo de la acción
        
        Returns:
            Diccionario con información de la acción
        """
        default_info = {
            'name': ticker,
            'sector': 'N/A',
            'industry': 'N/A',
            'market_cap': 0,
            'pe_ratio': 0,
            'dividend_yield': 0,
            'beta': 0,
            '52_week_high': 0,
            '52_week_low': 0
        }
        
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            if not info:
                return default_info
            
            return {
                'name': info.get('longName', info.get('shortName', ticker)),
                'sector': info.get('sector', 'N/A'),
                'industry': info.get('industry', 'N/A'),
                'market_cap': info.get('marketCap', 0),
                'pe_ratio': info.get('trailingPE', 0),
                'dividend_yield': info.get('dividendYield', 0) * 100 if info.get('dividendYield') else 0,
                'beta': info.get('beta', 0),
                '52_week_high': info.get('fiftyTwoWeekHigh', 0),
                '52_week_low': info.get('fiftyTwoWeekLow', 0)
            }
        except:
            return default_info
    
    def get_multiple_stocks(
        self,
        tickers: List[str],
        period: str = "1y",
        interval: str = "1d"
    ) -> dict:
        """
        Obtiene datos de múltiples acciones
        
        Args:
            tickers: Lista de símbolos de acciones
            period: Período de tiempo
            interval: Intervalo de datos
        
        Returns:
            Diccionario con DataFrames de cada acción
        """
        data = {}
        total = len(tickers)
        
        print(f"\n📊 Descargando {total} acciones...")
        
        for i, ticker in enumerate(tickers, 1):
            print(f"[{i}/{total}] {ticker}...", end=" ")
            
            df = self.get_stock_data(ticker, period, interval)
            
            if df is not None and not df.empty:
                data[ticker] = df
                print("✅")
            else:
                print("❌")
            
            # Pausa para evitar rate limiting
            if i < total:
                time.sleep(0.3)
        
        print(f"\n✅ Cargadas: {len(data)}/{total} acciones\n")
        return data