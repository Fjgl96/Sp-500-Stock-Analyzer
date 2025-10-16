"""
Página de Comparación de Múltiples Acciones
"""

import streamlit as st
import sys
from pathlib import Path
import pandas as pd
import numpy as np

# Añadir el directorio raíz al path
root_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(root_dir))

from src.data.data_fetcher import StockDataFetcher
from src.data.data_processor import DataProcessor
from src.visualization.charts import ChartBuilder

st.set_page_config(page_title="Comparación", page_icon="📈", layout="wide")

@st.cache_data(ttl=3600)
def get_sp500_tickers():
    """Obtiene lista de tickers del S&P 500"""
    fetcher = StockDataFetcher()
    return fetcher.get_sp500_tickers()

@st.cache_data(ttl=3600)
def load_multiple_stocks(tickers, period):
    """Carga datos de múltiples acciones"""
    fetcher = StockDataFetcher()
    data = fetcher.get_multiple_stocks(tickers, period=period)
    
    # Procesar datos
    processor = DataProcessor()
    processed_data = {}
    
    for ticker, df in data.items():
        if df is not None and not df.empty:
            df = processor.clean_data(df)
            df = processor.calculate_returns(df)
            processed_data[ticker] = df
    
    return processed_data

def calculate_correlation_matrix(data_dict):
    """Calcula matriz de correlación entre acciones"""
    # Crear DataFrame con precios de cierre
    close_prices = pd.DataFrame()
    
    for ticker, df in data_dict.items():
        close_prices[ticker] = df['Close']
    
    # Calcular correlación
    correlation = close_prices.corr()
    
    return correlation

def calculate_portfolio_stats(data_dict, weights=None):
    """Calcula estadísticas del portafolio"""
    if weights is None:
        # Pesos iguales
        weights = {ticker: 1/len(data_dict) for ticker in data_dict.keys()}
    
    # Calcular retornos del portafolio
    portfolio_returns = []
    
    for ticker, weight in weights.items():
        if ticker in data_dict:
            df = data_dict[ticker]
            if 'Returns' in df.columns:
                weighted_returns = df['Returns'] * weight
                portfolio_returns.append(weighted_returns)
    
    if portfolio_returns:
        portfolio_returns = pd.concat(portfolio_returns, axis=1).sum(axis=1)
        
        # Estadísticas
        total_return = (1 + portfolio_returns).prod() - 1
        avg_daily_return = portfolio_returns.mean()
        volatility = portfolio_returns.std()
        sharpe_ratio = (avg_daily_return / volatility) * np.sqrt(252) if volatility > 0 else 0
        
        return {
            'total_return': total_return * 100,
            'avg_daily_return': avg_daily_return * 100,
            'annual_volatility': volatility * np.sqrt(252) * 100,
            'sharpe_ratio': sharpe_ratio
        }
    
    return None

def main():
    st.title("📈 Comparación de Acciones")
    st.markdown("### Analiza y Compara Múltiples Acciones")
    
    # Sidebar - Configuración
    with st.sidebar:
        st.header("⚙️ Configuración")
        
        # Obtener tickers
        all_tickers = get_sp500_tickers()
        
        # Selección múltiple de acciones
        default_tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN']
        default_selection = [t for t in default_tickers if t in all_tickers]
        
        selected_tickers = st.multiselect(
            "Selecciona acciones (máx. 10)",
            options=all_tickers,
            default=default_selection,
            max_selections=10
        )
        
        # Período de tiempo
        period = st.selectbox(
            "Período de tiempo",
            options=['1mo', '3mo', '6mo', '1y', '2y', '5y'],
            index=3
        )
        
        st.markdown("---")
        
        # Tipo de análisis
        analysis_type = st.radio(
            "Tipo de análisis",
            options=['Comparación de Precios', 'Correlación', 'Portafolio'],
            index=0
        )
        
        st.markdown("---")
        
        # Botón de análisis
        compare_button = st.button("📊 Comparar", type="primary", use_container_width=True)
    
    # Validación
    if not selected_tickers:
        st.info("👆 Selecciona al menos una acción en el menú lateral para comenzar")
        return
    
    # Cargar y analizar datos
    if compare_button or 'last_comparison' in st.session_state:
        st.session_state['last_comparison'] = selected_tickers
        
        with st.spinner(f"Cargando datos de {len(selected_tickers)} acciones..."):
            stock_data = load_multiple_stocks(selected_tickers, period)
        
        if not stock_data:
            st.error("❌ No se pudieron cargar datos")
            return
        
        # Mostrar número de acciones cargadas
        st.success(f"✅ Datos cargados para {len(stock_data)} acciones")
        
        st.markdown("---")
        
        # Análisis según tipo seleccionado
        if analysis_type == 'Comparación de Precios':
            st.subheader("📊 Comparación de Precios")
            
            # Opciones de visualización
            col1, col2 = st.columns([3, 1])
            
            with col2:
                normalize = st.checkbox("Normalizar precios", value=True)
                show_returns = st.checkbox("Mostrar retornos", value=False)
            
            # Gráfico de comparación
            chart_builder = ChartBuilder(pd.DataFrame(), "Comparación")
            
            if show_returns:
                # Crear DataFrame de retornos acumulados
                returns_data = {}
                for ticker, df in stock_data.items():
                    if 'Cumulative_Returns' in df.columns:
                        returns_data[ticker] = df[['Cumulative_Returns']].rename(
                            columns={'Cumulative_Returns': 'Close'}
                        )
                
                if returns_data:
                    fig = chart_builder.create_comparison_chart(returns_data, normalize=False)
                    st.plotly_chart(fig, use_container_width=True)
            else:
                fig = chart_builder.create_comparison_chart(stock_data, normalize=normalize)
                st.plotly_chart(fig, use_container_width=True)
            
            # Tabla de rendimiento
            st.markdown("---")
            st.subheader("📋 Rendimiento en el Período")
            
            performance_data = []
            
            for ticker, df in stock_data.items():
                first_price = df['Close'].iloc[0]
                last_price = df['Close'].iloc[-1]
                change = last_price - first_price
                change_pct = (change / first_price) * 100
                
                high = df['High'].max()
                low = df['Low'].min()
                volatility = df['Close'].pct_change().std() * np.sqrt(252) * 100
                
                performance_data.append({
                    'Ticker': ticker,
                    'Precio Inicial': f"${first_price:.2f}",
                    'Precio Final': f"${last_price:.2f}",
                    'Cambio': f"${change:.2f}",
                    'Cambio %': f"{change_pct:.2f}%",
                    'Máximo': f"${high:.2f}",
                    'Mínimo': f"${low:.2f}",
                    'Volatilidad Anual': f"{volatility:.2f}%"
                })
            
            df_performance = pd.DataFrame(performance_data)
            st.dataframe(df_performance, use_container_width=True, hide_index=True)
            
        elif analysis_type == 'Correlación':
            st.subheader("🔄 Análisis de Correlación")
            
            # Calcular matriz de correlación
            correlation_matrix = calculate_correlation_matrix(stock_data)
            
            # Mostrar mapa de calor
            chart_builder = ChartBuilder(pd.DataFrame(), "Correlación")
            fig_corr = chart_builder.create_correlation_heatmap(correlation_matrix)
            st.plotly_chart(fig_corr, use_container_width=True)
            
            # Interpretación
            st.markdown("---")
            st.info("""
            **Interpretación de la Correlación:**
            - **1.0**: Correlación positiva perfecta (se mueven juntas)
            - **0.0**: Sin correlación
            - **-1.0**: Correlación negativa perfecta (se mueven en direcciones opuestas)
            
            📊 Una correlación alta (>0.7) indica que las acciones tienden a moverse juntas.
            """)
            
            # Tabla de correlación
            st.markdown("---")
            st.subheader("📊 Matriz de Correlación Detallada")
            st.dataframe(
                correlation_matrix.style.background_gradient(cmap='RdBu', vmin=-1, vmax=1),
                use_container_width=True
            )
            
        elif analysis_type == 'Portafolio':
            st.subheader("💼 Análisis de Portafolio")
            
            # Configuración de pesos
            st.markdown("#### ⚖️ Asignación de Pesos")
            
            weights = {}
            cols = st.columns(min(len(stock_data), 4))
            
            for i, ticker in enumerate(stock_data.keys()):
                with cols[i % 4]:
                    weight = st.slider(
                        f"{ticker}",
                        min_value=0.0,
                        max_value=1.0,
                        value=1.0/len(stock_data),
                        step=0.01,
                        key=f"weight_{ticker}"
                    )
                    weights[ticker] = weight
            
            # Validar que sumen 1.0
            total_weight = sum(weights.values())
            
            if abs(total_weight - 1.0) > 0.01:
                st.warning(f"⚠️ Los pesos deben sumar 1.0 (actualmente: {total_weight:.2f})")
            else:
                st.success(f"✅ Pesos válidos (total: {total_weight:.2f})")
            
            # Calcular estadísticas del portafolio
            st.markdown("---")
            portfolio_stats = calculate_portfolio_stats(stock_data, weights)
            
            if portfolio_stats:
                st.markdown("#### 📊 Estadísticas del Portafolio")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric(
                        "Retorno Total",
                        f"{portfolio_stats['total_return']:.2f}%"
                    )
                
                with col2:
                    st.metric(
                        "Retorno Diario Promedio",
                        f"{portfolio_stats['avg_daily_return']:.4f}%"
                    )
                
                with col3:
                    st.metric(
                        "Volatilidad Anual",
                        f"{portfolio_stats['annual_volatility']:.2f}%"
                    )
                
                with col4:
                    st.metric(
                        "Ratio de Sharpe",
                        f"{portfolio_stats['sharpe_ratio']:.2f}"
                    )
                
                # Gráfico de composición del portafolio
                st.markdown("---")
                st.markdown("#### 🥧 Composición del Portafolio")
                
                import plotly.express as px
                
                weights_df = pd.DataFrame({
                    'Ticker': list(weights.keys()),
                    'Peso': list(weights.values())
                })
                weights_df = weights_df[weights_df['Peso'] > 0]
                
                fig_pie = px.pie(
                    weights_df,
                    values='Peso',
                    names='Ticker',
                    title='Distribución de Pesos'
                )
                
                fig_pie.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig_pie, use_container_width=True)
            
            # Evolución del portafolio
            st.markdown("---")
            st.markdown("#### 📈 Evolución del Portafolio")
            
            # Calcular valor del portafolio normalizado
            portfolio_value = pd.DataFrame()
            
            for ticker, weight in weights.items():
                if ticker in stock_data and weight > 0:
                    df = stock_data[ticker]
                    normalized = (df['Close'] / df['Close'].iloc[0]) * weight
                    portfolio_value[ticker] = normalized
            
            if not portfolio_value.empty:
                portfolio_value['Total'] = portfolio_value.sum(axis=1)
                
                # Crear gráfico
                import plotly.graph_objects as go
                
                fig = go.Figure()
                
                # Línea del portafolio total
                fig.add_trace(go.Scatter(
                    x=portfolio_value.index,
                    y=portfolio_value['Total'],
                    name='Portafolio Total',
                    line=dict(color='blue', width=3)
                ))
                
                # Líneas individuales
                for ticker in weights.keys():
                    if ticker in portfolio_value.columns and ticker != 'Total':
                        fig.add_trace(go.Scatter(
                            x=portfolio_value.index,
                            y=portfolio_value[ticker],
                            name=ticker,
                            line=dict(width=1),
                            opacity=0.6
                        ))
                
                fig.update_layout(
                    title='Evolución del Portafolio (Base 1.0)',
                    xaxis_title='Fecha',
                    yaxis_title='Valor Normalizado',
                    template='plotly_white',
                    hovermode='x unified',
                    height=500
                )
                
                st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()