"""
Módulo para calcular indicadores técnicos
"""

import pandas as pd
import numpy as np
from typing import List, Optional
from ..utils.config import INDICATORS_CONFIG


class TechnicalAnalysis:
    """
    Clase para calcular indicadores técnicos
    """
    
    def __init__(self, df: pd.DataFrame):
        """
        Args:
            df: DataFrame con datos OHLCV
        """
        self.df = df.copy()
    
    def add_sma(self, periods: List[int] = None) -> pd.DataFrame:
        """
        Añade Simple Moving Averages
        
        Args:
            periods: Lista de períodos para SMA
        
        Returns:
            DataFrame con columnas SMA
        """
        if periods is None:
            periods = INDICATORS_CONFIG["sma_periods"]
        
        for period in periods:
            self.df[f'SMA_{period}'] = self.df['Close'].rolling(window=period).mean()
        
        return self.df
    
    def add_ema(self, periods: List[int] = None) -> pd.DataFrame:
        """
        Añade Exponential Moving Averages
        
        Args:
            periods: Lista de períodos para EMA
        
        Returns:
            DataFrame con columnas EMA
        """
        if periods is None:
            periods = INDICATORS_CONFIG["ema_periods"]
        
        for period in periods:
            self.df[f'EMA_{period}'] = self.df['Close'].ewm(span=period, adjust=False).mean()
        
        return self.df
    
    def add_rsi(self, period: int = None) -> pd.DataFrame:
        """
        Añade Relative Strength Index
        
        Args:
            period: Período para RSI
        
        Returns:
            DataFrame con columna RSI
        """
        if period is None:
            period = INDICATORS_CONFIG["rsi_period"]
        
        delta = self.df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        
        rs = gain / loss
        self.df['RSI'] = 100 - (100 / (1 + rs))
        
        return self.df
    
    def add_macd(
        self,
        fast: int = None,
        slow: int = None,
        signal: int = None
    ) -> pd.DataFrame:
        """
        Añade MACD (Moving Average Convergence Divergence)
        
        Args:
            fast: Período rápido
            slow: Período lento
            signal: Período de señal
        
        Returns:
            DataFrame con columnas MACD
        """
        if fast is None:
            fast = INDICATORS_CONFIG["macd_fast"]
        if slow is None:
            slow = INDICATORS_CONFIG["macd_slow"]
        if signal is None:
            signal = INDICATORS_CONFIG["macd_signal"]
        
        ema_fast = self.df['Close'].ewm(span=fast, adjust=False).mean()
        ema_slow = self.df['Close'].ewm(span=slow, adjust=False).mean()
        
        self.df['MACD'] = ema_fast - ema_slow
        self.df['MACD_Signal'] = self.df['MACD'].ewm(span=signal, adjust=False).mean()
        self.df['MACD_Hist'] = self.df['MACD'] - self.df['MACD_Signal']
        
        return self.df
    
    def add_bollinger_bands(
        self,
        period: int = None,
        std_dev: int = None
    ) -> pd.DataFrame:
        """
        Añade Bandas de Bollinger
        
        Args:
            period: Período para la media móvil
            std_dev: Número de desviaciones estándar
        
        Returns:
            DataFrame con columnas de Bollinger
        """
        if period is None:
            period = INDICATORS_CONFIG["bollinger_period"]
        if std_dev is None:
            std_dev = INDICATORS_CONFIG["bollinger_std"]
        
        self.df['BB_Middle'] = self.df['Close'].rolling(window=period).mean()
        std = self.df['Close'].rolling(window=period).std()
        
        self.df['BB_Upper'] = self.df['BB_Middle'] + (std * std_dev)
        self.df['BB_Lower'] = self.df['BB_Middle'] - (std * std_dev)
        
        return self.df
    
    def add_volume_indicators(self) -> pd.DataFrame:
        """
        Añade indicadores de volumen
        
        Returns:
            DataFrame con indicadores de volumen
        """
        # Volumen promedio
        self.df['Volume_SMA_20'] = self.df['Volume'].rolling(window=20).mean()
        
        # On-Balance Volume (OBV)
        obv = [0]
        for i in range(1, len(self.df)):
            if self.df['Close'].iloc[i] > self.df['Close'].iloc[i-1]:
                obv.append(obv[-1] + self.df['Volume'].iloc[i])
            elif self.df['Close'].iloc[i] < self.df['Close'].iloc[i-1]:
                obv.append(obv[-1] - self.df['Volume'].iloc[i])
            else:
                obv.append(obv[-1])
        
        self.df['OBV'] = obv
        
        return self.df
    
    def add_all_indicators(self) -> pd.DataFrame:
        """
        Añade todos los indicadores técnicos
        
        Returns:
            DataFrame con todos los indicadores
        """
        self.add_sma()
        self.add_ema()
        self.add_rsi()
        self.add_macd()
        self.add_bollinger_bands()
        self.add_volume_indicators()
        
        return self.df
    
    def get_signals(self) -> dict:
        """
        Genera señales de trading basadas en indicadores
        
        Returns:
            Diccionario con señales
        """
        signals = {}
        
        # Señal RSI
        last_rsi = self.df['RSI'].iloc[-1]
        if last_rsi < 30:
            signals['RSI'] = '🟢 SOBREVENDIDO - Señal de COMPRA'
        elif last_rsi > 70:
            signals['RSI'] = '🔴 SOBRECOMPRADO - Señal de VENTA'
        else:
            signals['RSI'] = '🟡 NEUTRAL'
        
        # Señal MACD
        last_macd = self.df['MACD'].iloc[-1]
        last_signal = self.df['MACD_Signal'].iloc[-1]
        if last_macd > last_signal:
            signals['MACD'] = '🟢 ALCISTA - Señal de COMPRA'
        else:
            signals['MACD'] = '🔴 BAJISTA - Señal de VENTA'
        
        # Señal Moving Averages
        last_close = self.df['Close'].iloc[-1]
        last_sma_50 = self.df['SMA_50'].iloc[-1]
        last_sma_200 = self.df['SMA_200'].iloc[-1]
        
        if last_close > last_sma_50 and last_sma_50 > last_sma_200:
            signals['MA_Trend'] = '🟢 TENDENCIA ALCISTA FUERTE'
        elif last_close < last_sma_50 and last_sma_50 < last_sma_200:
            signals['MA_Trend'] = '🔴 TENDENCIA BAJISTA FUERTE'
        else:
            signals['MA_Trend'] = '🟡 TENDENCIA MIXTA'
        
        return signals