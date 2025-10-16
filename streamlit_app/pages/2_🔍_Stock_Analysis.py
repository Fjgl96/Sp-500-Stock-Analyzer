"""
Página de Análisis de Acciones Individual
"""

import streamlit as st
import sys
from pathlib import Path

# Añadir el directorio raíz al path
root_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(root_dir))

from src.data.data_fetcher import StockDataFetcher
from src.data.data_processor import DataProcessor
from src.analysis.technical_indicators import TechnicalAnalysis
from src.visualization.charts import ChartBuilder

st.set_page_config(page_title="Análisis de Acciones", page_icon="🔍", layout="wide")

@st.cache_data(ttl=3600)
def get_sp500_tickers():
    """Obtiene lista de tickers del S&P 500"""
    fetcher = StockDataFetcher()
    return fetcher.get_sp500_tickers()

@st.cache_data(ttl=3600)
def load_stock_data(ticker, period, interval):
    """Carga datos de una acción"""
    fetcher = StockDataFetcher()
    df = fetcher.get_stock_data(ticker, period, interval)
    
    if df is not None and not df.empty:
        # Procesar datos
        processor = DataProcessor()
        df = processor.clean_data(df)
        df = processor.calculate_returns(df)
        
        # Añadir indicadores técnicos
        ta = TechnicalAnalysis(df)
        df = ta.add_all_indicators()
        
        # Obtener señales
        signals = ta.get_signals()
        
        return df, signals
    
    return None, None

def display_stock_info(ticker):
    """Muestra información de la acción"""
    fetcher = StockDataFetcher()
    info = fetcher.get_stock_info(ticker)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Sector", info.get('sector', 'N/A'))
    with col2:
        st.metric("Industria", info.get('industry', 'N/A'))
    with col3:
        market_cap = info.get('market_cap', 0)
        if market_cap > 0:
            market_cap_b = market_cap / 1e9
            st.metric("Cap. Mercado", f"${market_cap_b:.2f}B")
        else:
            st.metric("Cap. Mercado", "N/A")
    with col4:
        pe_ratio = info.get('pe_ratio', 0)
        if pe_ratio > 0:
            st.metric("P/E Ratio", f"{pe_ratio:.2f}")
        else:
            st.metric("P/E Ratio", "N/A")

def display_signals(signals):
    """Muestra señales de trading"""
    st.subheader("🎯 Señales de Trading")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info(f"**RSI**\n\n{signals.get('RSI', 'N/A')}")
    with col2:
        st.info(f"**MACD**\n\n{signals.get('MACD', 'N/A')}")
    with col3:
        st.info(f"**Tendencia MA**\n\n{signals.get('MA_Trend', 'N/A')}")

def main():
    st.title("🔍 Análisis de Acciones")
    st.markdown("### Análisis Técnico Detallado")
    
    # Sidebar - Configuración
    with st.sidebar:
        st.header("⚙️ Configuración")
        
        # Obtener tickers
        tickers = get_sp500_tickers()
        
        # Selección de acción
        selected_ticker = st.selectbox(
            "Selecciona una acción",
            options=tickers,
            index=tickers.index('AAPL') if 'AAPL' in tickers else 0
        )
        
        # Período de tiempo
        period = st.selectbox(
            "Período de tiempo",
            options=['1mo', '3mo', '6mo', '1y', '2y', '5y'],
            index=3
        )
        
        # Intervalo
        interval = st.selectbox(
            "Intervalo",
            options=['1d', '1wk', '1mo'],
            index=0
        )
        
        st.markdown("---")
        
        # Botón de análisis
        analyze_button = st.button("📊 Analizar", type="primary", use_container_width=True)
    
    # Cargar y mostrar datos
    if analyze_button or 'last_ticker' in st.session_state:
        # Guardar última acción analizada
        st.session_state['last_ticker'] = selected_ticker
        
        with st.spinner(f"Analizando {selected_ticker}..."):
            df, signals = load_stock_data(selected_ticker, period, interval)
        
        if df is None:
            st.error(f"❌ No se pudieron cargar datos para {selected_ticker}")
            return
        
        # Información de la acción
        st.markdown("---")
        display_stock_info(selected_ticker)
        
        # Métricas principales
        st.markdown("---")
        col1, col2, col3, col4 = st.columns(4)
        
        current_price = df['Close'].iloc[-1]
        first_price = df['Close'].iloc[0]
        change = current_price - first_price
        change_pct = (change / first_price) * 100
        
        max_price = df['High'].max()
        min_price = df['Low'].min()
        avg_volume = df['Volume'].mean()
        
        with col1:
            st.metric(
                "Precio Actual",
                f"${current_price:.2f}",
                f"{change_pct:+.2f}%"
            )
        with col2:
            st.metric("Máximo", f"${max_price:.2f}")
        with col3:
            st.metric("Mínimo", f"${min_price:.2f}")
        with col4:
            st.metric("Vol. Promedio", f"{avg_volume/1e6:.2f}M")
        
        # Señales de trading
        st.markdown("---")
        if signals:
            display_signals(signals)
        
        # Gráficos
        st.markdown("---")
        
        chart_builder = ChartBuilder(df, selected_ticker)
        
        # Pestañas para diferentes análisis
        tab1, tab2, tab3, tab4 = st.tabs([
            "📈 Precio y Volumen",
            "📊 Indicadores",
            "📉 Retornos",
            "📋 Datos"
        ])
        
        with tab1:
            st.subheader("Gráfico de Precios")
            fig_price = chart_builder.create_candlestick_chart()
            st.plotly_chart(fig_price, use_container_width=True)
            
            st.subheader("Bandas de Bollinger")
            fig_bb = chart_builder.create_bollinger_bands_chart()
            st.plotly_chart(fig_bb, use_container_width=True)
        
        with tab2:
            st.subheader("RSI (Relative Strength Index)")
            fig_rsi = chart_builder.create_rsi_chart()
            st.plotly_chart(fig_rsi, use_container_width=True)
            
            st.subheader("MACD")
            fig_macd = chart_builder.create_macd_chart()
            st.plotly_chart(fig_macd, use_container_width=True)
        
        with tab3:
            st.subheader("Retornos Acumulados")
            fig_returns = chart_builder.create_returns_chart()
            st.plotly_chart(fig_returns, use_container_width=True)
            
            # Estadísticas de retornos
            col1, col2, col3 = st.columns(3)
            
            if 'Returns' in df.columns:
                import numpy as np
                daily_return = df['Returns'].mean() * 100
                volatility = df['Returns'].std() * 100
                sharpe = (daily_return / volatility) * (252 ** 0.5) if volatility > 0 else 0
                
                with col1:
                    st.metric("Retorno Diario Promedio", f"{daily_return:.4f}%")
                with col2:
                    st.metric("Volatilidad Diaria", f"{volatility:.4f}%")
                with col3:
                    st.metric("Ratio de Sharpe (aprox)", f"{sharpe:.2f}")
        
        with tab4:
            st.subheader("Datos Históricos")
            
            # Selector de columnas
            all_columns = df.columns.tolist()
            selected_columns = st.multiselect(
                "Selecciona columnas a mostrar",
                options=all_columns,
                default=['Open', 'High', 'Low', 'Close', 'Volume']
            )
            
            if selected_columns:
                st.dataframe(
                    df[selected_columns].tail(100),
                    use_container_width=True,
                    height=400
                )
                
                # Botón de descarga
                csv = df[selected_columns].to_csv()
                st.download_button(
                    label="📥 Descargar CSV",
                    data=csv,
                    file_name=f"{selected_ticker}_data.csv",
                    mime="text/csv"
                )

if __name__ == "__main__":
    main()