"""
Módulo para procesar y limpiar datos
"""

import pandas as pd
import numpy as np
from typing import List


class DataProcessor:
    """
    Clase para procesar y limpiar datos de acciones
    """
    
    @staticmethod
    def clean_data(df: pd.DataFrame) -> pd.DataFrame:
        """
        Limpia el DataFrame eliminando valores nulos y duplicados
        
        Args:
            df: DataFrame con datos crudos
        
        Returns:
            DataFrame limpio
        """
        df = df.copy()
        
        # Eliminar duplicados
        df = df[~df.index.duplicated(keep='first')]
        
        # Interpolar valores faltantes
        df = df.interpolate(method='linear', limit_direction='both')
        
        # Eliminar filas con todos los valores NaN
        df = df.dropna(how='all')
        
        return df
    
    @staticmethod
    def calculate_returns(df: pd.DataFrame, column: str = 'Close') -> pd.DataFrame:
        """
        Calcula los retornos diarios
        
        Args:
            df: DataFrame con datos
            column: Columna para calcular retornos
        
        Returns:
            DataFrame con columna de retornos
        """
        df = df.copy()
        df['Returns'] = df[column].pct_change()
        df['Cumulative_Returns'] = (1 + df['Returns']).cumprod() - 1
        return df
    
    @staticmethod
    def calculate_volatility(
        df: pd.DataFrame,
        window: int = 20,
        column: str = 'Returns'
    ) -> pd.DataFrame:
        """
        Calcula la volatilidad móvil
        
        Args:
            df: DataFrame con datos
            window: Ventana para calcular volatilidad
            column: Columna para calcular volatilidad
        
        Returns:
            DataFrame con columna de volatilidad
        """
        df = df.copy()
        df['Volatility'] = df[column].rolling(window=window).std() * np.sqrt(252)
        return df
    
    @staticmethod
    def normalize_data(df: pd.DataFrame, column: str) -> pd.DataFrame:
        """
        Normaliza una columna (0-1)
        
        Args:
            df: DataFrame con datos
            column: Columna a normalizar
        
        Returns:
            DataFrame con columna normalizada
        """
        df = df.copy()
        min_val = df[column].min()
        max_val = df[column].max()
        df[f'{column}_Normalized'] = (df[column] - min_val) / (max_val - min_val)
        return df
    
    @staticmethod
    def resample_data(
        df: pd.DataFrame,
        freq: str = 'W',
        agg_dict: dict = None
    ) -> pd.DataFrame:
        """
        Remuestrea los datos a diferente frecuencia
        
        Args:
            df: DataFrame con datos
            freq: Frecuencia ('D', 'W', 'M', 'Q', 'Y')
            agg_dict: Diccionario de agregación personalizado
        
        Returns:
            DataFrame remuestreado
        """
        if agg_dict is None:
            agg_dict = {
                'Open': 'first',
                'High': 'max',
                'Low': 'min',
                'Close': 'last',
                'Volume': 'sum'
            }
        
        return df.resample(freq).agg(agg_dict).dropna()