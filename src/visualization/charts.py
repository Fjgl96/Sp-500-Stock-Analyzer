"""
Módulo para crear gráficos interactivos con Plotly
"""

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from typing import List, Optional
from ..utils.config import CHART_COLORS


class ChartBuilder:
    """
    Clase para construir gráficos interactivos
    """
    
    def __init__(self, df: pd.DataFrame, ticker: str = "Stock"):
        """
        Args:
            df: DataFrame con datos y indicadores
            ticker: Nombre/símbolo de la acción
        """
        self.df = df
        self.ticker = ticker
        self.colors = CHART_COLORS
    
    def create_candlestick_chart(
        self,
        show_volume: bool = True,
        show_ma: bool = True,
        ma_periods: List[int] = [20, 50, 200]
    ) -> go.Figure:
        """
        Crea un gráfico de velas japonesas
        
        Args:
            show_volume: Mostrar volumen
            show_ma: Mostrar medias móviles
            ma_periods: Períodos de las medias móviles
        
        Returns:
            Figura de Plotly
        """
        # Crear subplots
        if show_volume:
            fig = make_subplots(
                rows=2, cols=1,
                shared_xaxes=True,
                vertical_spacing=0.03,
                row_heights=[0.7, 0.3],
                subplot_titles=(f'{self.ticker} - Precio', 'Volumen')
            )
        else:
            fig = go.Figure()
        
        # Candlestick
        candlestick = go.Candlestick(
            x=self.df.index,
            open=self.df['Open'],
            high=self.df['High'],
            low=self.df['Low'],
            close=self.df['Close'],
            name='OHLC',
            increasing_line_color=self.colors['success'],
            decreasing_line_color=self.colors['danger']
        )
        
        if show_volume:
            fig.add_trace(candlestick, row=1, col=1)
        else:
            fig.add_trace(candlestick)
        
        # Medias móviles
        if show_ma:
            colors_ma = [self.colors['primary'], self.colors['warning'], self.colors['info']]
            for i, period in enumerate(ma_periods):
                col_name = f'SMA_{period}'
                if col_name in self.df.columns:
                    ma_trace = go.Scatter(
                        x=self.df.index,
                        y=self.df[col_name],
                        name=f'SMA {period}',
                        line=dict(color=colors_ma[i % len(colors_ma)], width=2)
                    )
                    if show_volume:
                        fig.add_trace(ma_trace, row=1, col=1)
                    else:
                        fig.add_trace(ma_trace)
        
        # Volumen
        if show_volume:
            colors = [self.colors['success'] if self.df['Close'].iloc[i] >= self.df['Open'].iloc[i] 
                     else self.colors['danger'] for i in range(len(self.df))]
            
            volume_trace = go.Bar(
                x=self.df.index,
                y=self.df['Volume'],
                name='Volumen',
                marker_color=colors,
                showlegend=False
            )
            fig.add_trace(volume_trace, row=2, col=1)
        
        # Layout
        fig.update_layout(
            title=f'{self.ticker} - Análisis de Precios',
            xaxis_title='Fecha',
            yaxis_title='Precio (USD)',
            template='plotly_white',
            hovermode='x unified',
            height=600,
            showlegend=True,
            xaxis_rangeslider_visible=False
        )
        
        return fig
    
    def create_rsi_chart(self) -> go.Figure:
        """
        Crea gráfico de RSI
        
        Returns:
            Figura de Plotly
        """
        fig = go.Figure()
        
        # RSI
        fig.add_trace(go.Scatter(
            x=self.df.index,
            y=self.df['RSI'],
            name='RSI',
            line=dict(color=self.colors['primary'], width=2)
        ))
        
        # Líneas de referencia
        fig.add_hline(y=70, line_dash="dash", line_color=self.colors['danger'], 
                     annotation_text="Sobrecomprado (70)")
        fig.add_hline(y=30, line_dash="dash", line_color=self.colors['success'], 
                     annotation_text="Sobrevendido (30)")
        fig.add_hline(y=50, line_dash="dot", line_color="gray", 
                     annotation_text="Neutral (50)")
        
        fig.update_layout(
            title=f'{self.ticker} - RSI (Relative Strength Index)',
            xaxis_title='Fecha',
            yaxis_title='RSI',
            template='plotly_white',
            hovermode='x unified',
            height=300,
            yaxis=dict(range=[0, 100])
        )
        
        return fig
    
    def create_macd_chart(self) -> go.Figure:
        """
        Crea gráfico de MACD
        
        Returns:
            Figura de Plotly
        """
        fig = go.Figure()
        
        # MACD Line
        fig.add_trace(go.Scatter(
            x=self.df.index,
            y=self.df['MACD'],
            name='MACD',
            line=dict(color=self.colors['primary'], width=2)
        ))
        
        # Signal Line
        fig.add_trace(go.Scatter(
            x=self.df.index,
            y=self.df['MACD_Signal'],
            name='Signal',
            line=dict(color=self.colors['secondary'], width=2)
        ))
        
        # Histogram
        colors = [self.colors['success'] if val >= 0 else self.colors['danger'] 
                 for val in self.df['MACD_Hist']]
        
        fig.add_trace(go.Bar(
            x=self.df.index,
            y=self.df['MACD_Hist'],
            name='Histogram',
            marker_color=colors
        ))
        
        fig.update_layout(
            title=f'{self.ticker} - MACD',
            xaxis_title='Fecha',
            yaxis_title='MACD',
            template='plotly_white',
            hovermode='x unified',
            height=300
        )
        
        return fig
    
    def create_bollinger_bands_chart(self) -> go.Figure:
        """
        Crea gráfico con Bandas de Bollinger
        
        Returns:
            Figura de Plotly
        """
        fig = go.Figure()
        
        # Precio de cierre
        fig.add_trace(go.Scatter(
            x=self.df.index,
            y=self.df['Close'],
            name='Precio',
            line=dict(color=self.colors['primary'], width=2)
        ))
        
        # Banda superior
        fig.add_trace(go.Scatter(
            x=self.df.index,
            y=self.df['BB_Upper'],
            name='Banda Superior',
            line=dict(color=self.colors['danger'], width=1, dash='dash')
        ))
        
        # Banda media
        fig.add_trace(go.Scatter(
            x=self.df.index,
            y=self.df['BB_Middle'],
            name='Banda Media',
            line=dict(color='gray', width=1)
        ))
        
        # Banda inferior
        fig.add_trace(go.Scatter(
            x=self.df.index,
            y=self.df['BB_Lower'],
            name='Banda Inferior',
            line=dict(color=self.colors['success'], width=1, dash='dash'),
            fill='tonexty',
            fillcolor='rgba(127, 127, 127, 0.1)'
        ))
        
        fig.update_layout(
            title=f'{self.ticker} - Bandas de Bollinger',
            xaxis_title='Fecha',
            yaxis_title='Precio (USD)',
            template='plotly_white',
            hovermode='x unified',
            height=400
        )
        
        return fig
    
    def create_returns_chart(self) -> go.Figure:
        """
        Crea gráfico de retornos acumulados
        
        Returns:
            Figura de Plotly
        """
        fig = go.Figure()
        
        # Calcular retornos si no existen
        if 'Cumulative_Returns' not in self.df.columns:
            returns = self.df['Close'].pct_change()
            cumulative_returns = (1 + returns).cumprod() - 1
        else:
            cumulative_returns = self.df['Cumulative_Returns']
        
        fig.add_trace(go.Scatter(
            x=self.df.index,
            y=cumulative_returns * 100,
            name='Retorno Acumulado',
            line=dict(color=self.colors['primary'], width=2),
            fill='tozeroy',
            fillcolor='rgba(31, 119, 180, 0.2)'
        ))
        
        fig.add_hline(y=0, line_dash="dash", line_color="gray")
        
        fig.update_layout(
            title=f'{self.ticker} - Retornos Acumulados',
            xaxis_title='Fecha',
            yaxis_title='Retorno (%)',
            template='plotly_white',
            hovermode='x unified',
            height=400
        )
        
        return fig
    
    def create_comparison_chart(self, dfs: dict, normalize: bool = True) -> go.Figure:
        """
        Crea gráfico de comparación entre múltiples acciones
        
        Args:
            dfs: Diccionario {ticker: DataFrame}
            normalize: Normalizar precios para comparación
        
        Returns:
            Figura de Plotly
        """
        fig = go.Figure()
        
        colors = [self.colors['primary'], self.colors['secondary'], 
                 self.colors['success'], self.colors['danger'], 
                 self.colors['warning'], self.colors['info']]
        
        for i, (ticker, df) in enumerate(dfs.items()):
            if normalize:
                # Normalizar al primer valor = 100
                y_data = (df['Close'] / df['Close'].iloc[0]) * 100
                y_label = 'Precio Normalizado (Base 100)'
            else:
                y_data = df['Close']
                y_label = 'Precio (USD)'
            
            fig.add_trace(go.Scatter(
                x=df.index,
                y=y_data,
                name=ticker,
                line=dict(color=colors[i % len(colors)], width=2)
            ))
        
        fig.update_layout(
            title='Comparación de Acciones',
            xaxis_title='Fecha',
            yaxis_title=y_label,
            template='plotly_white',
            hovermode='x unified',
            height=500,
            showlegend=True
        )
        
        return fig
    
    def create_correlation_heatmap(self, correlation_matrix: pd.DataFrame) -> go.Figure:
        """
        Crea mapa de calor de correlaciones
        
        Args:
            correlation_matrix: Matriz de correlación
        
        Returns:
            Figura de Plotly
        """
        fig = go.Figure(data=go.Heatmap(
            z=correlation_matrix.values,
            x=correlation_matrix.columns,
            y=correlation_matrix.index,
            colorscale='RdBu',
            zmid=0,
            text=correlation_matrix.values.round(2),
            texttemplate='%{text}',
            textfont={"size": 10},
            colorbar=dict(title="Correlación")
        ))
        
        fig.update_layout(
            title='Matriz de Correlación',
            template='plotly_white',
            height=500,
            width=600
        )
        
        return fig