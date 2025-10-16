"""
Página de Dashboard - Vista general del mercado
"""

import streamlit as st
import sys
from pathlib import Path
import pandas as pd

# Añadir el directorio raíz al path
root_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(root_dir))

from src.data.data_fetcher import StockDataFetcher
from src.visualization.charts import ChartBuilder

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")

@st.cache_data(ttl=3600)
def load_market_overview():
    """Carga vista general del mercado"""
    fetcher = StockDataFetcher()
    
    # Principales índices
    indices = {
        '^GSPC': 'S&P 500',
        '^DJI': 'Dow Jones',
        '^IXIC': 'NASDAQ',
        '^RUT': 'Russell 2000'
    }
    
    data = {}
    for symbol, name in indices.items():
        df = fetcher.get_stock_data(symbol, period='1mo')
        if df is not None and not df.empty:
            data[name] = df
    
    return data

def display_index_card(name, df):
    """Muestra tarjeta con información del índice"""
    current_price = df['Close'].iloc[-1]
    prev_price = df['Close'].iloc[-2]
    change = current_price - prev_price
    change_pct = (change / prev_price) * 100
    
    delta_color = "normal" if change >= 0 else "inverse"
    
    st.metric(
        label=name,
        value=f"${current_price:,.2f}",
        delta=f"{change_pct:+.2f}%",
        delta_color=delta_color
    )

def main():
    st.title("📊 Dashboard del Mercado")
    st.markdown("### Vista General de los Principales Índices")
    
    # Botón de actualización
    if st.button("🔄 Actualizar Datos", type="primary"):
        st.cache_data.clear()
        st.rerun()
    
    # Cargar datos
    with st.spinner("Cargando datos del mercado..."):
        market_data = load_market_overview()
    
    if not market_data:
        st.error("❌ No se pudieron cargar los datos del mercado")
        return
    
    # Mostrar métricas de índices
    st.markdown("---")
    cols = st.columns(len(market_data))
    
    for col, (name, df) in zip(cols, market_data.items()):
        with col:
            display_index_card(name, df)
    
    st.markdown("---")
    
    # Gráfico principal
    st.subheader("📈 S&P 500 - Último Mes")
    
    if 'S&P 500' in market_data:
        sp500_df = market_data['S&P 500']
        chart_builder = ChartBuilder(sp500_df, "S&P 500")
        
        # Opciones de visualización
        col1, col2 = st.columns([3, 1])
        
        with col2:
            show_volume = st.checkbox("Mostrar Volumen", value=True)
            show_ma = st.checkbox("Mostrar Medias Móviles", value=True)
        
        # Crear y mostrar gráfico
        fig = chart_builder.create_candlestick_chart(
            show_volume=show_volume,
            show_ma=show_ma,
            ma_periods=[20, 50]
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Comparación de índices
    st.markdown("---")
    st.subheader("🔄 Comparación de Índices (Normalizado)")
    
    chart_builder = ChartBuilder(pd.DataFrame(), "Índices")
    comparison_fig = chart_builder.create_comparison_chart(market_data, normalize=True)
    st.plotly_chart(comparison_fig, use_container_width=True)
    
    # Información adicional
    with st.expander("ℹ️ Información sobre los índices"):
        st.markdown("""
        **S&P 500**: Índice de las 500 empresas más grandes de EE.UU.
        
        **Dow Jones**: Índice de 30 empresas industriales importantes.
        
        **NASDAQ**: Índice centrado en empresas tecnológicas.
        
        **Russell 2000**: Índice de empresas de pequeña capitalización.
        """)

if __name__ == "__main__":
    main()