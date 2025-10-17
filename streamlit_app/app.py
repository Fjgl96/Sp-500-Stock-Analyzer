"""
Aplicación principal de Streamlit
"""

import streamlit as st
import sys
from pathlib import Path

# Añadir el directorio raíz al path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from src.utils.config import APP_CONFIG
from src.utils.data_fetcher import get_stock_data, get_multiple_stocks

# Configuración de la página
st.set_page_config(**APP_CONFIG)

# CSS personalizado
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stAlert {
        padding: 1rem;
        margin: 1rem 0;
    }
    h1 {
        color: #1f77b4;
        padding-bottom: 1rem;
        border-bottom: 2px solid #e0e0e0;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)

def main():
    """Función principal de la aplicación"""
    
    # Título principal
    st.title("📊 S&P 500 Stock Analyzer")
    
    st.markdown("""
    ### 🎯 Bienvenido al Analizador de Acciones del S&P 500
    
    Esta aplicación te permite analizar acciones del índice S&P 500 con:
    - 📈 **Indicadores Técnicos**: SMA, EMA, RSI, MACD, Bollinger Bands
    - 📊 **Visualizaciones Interactivas**: Gráficos de velas, volumen y más
    - 🔍 **Análisis Comparativo**: Compara múltiples acciones
    - 💹 **Señales de Trading**: Basadas en indicadores técnicos
    
    ---
    
    ### 🚀 Comienza seleccionando una página en el menú lateral:
    
    """)
    
    # Columnas para características
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("""
        **📊 Dashboard**
        
        Vista general del mercado
        y métricas principales
        """)
    
    with col2:
        st.success("""
        **🔍 Análisis de Acciones**
        
        Análisis detallado con
        indicadores técnicos
        """)
    
    with col3:
        st.warning("""
        **📈 Comparación**
        
        Compara múltiples acciones
        y encuentra correlaciones
        """)
    
    st.markdown("---")
    
    # Demo de carga de datos
    with st.expander("🧪 Prueba de Conexión con Yahoo Finance"):
        st.write("Verifica que la conexión funcione correctamente:")
        
        if st.button("🔄 Probar carga de datos"):
            with st.spinner("Probando conexión..."):
                # Intenta cargar AAPL
                data = get_stock_data("AAPL", period="5d")
                
                if data is not None and not data.empty:
                    st.success("✅ Conexión exitosa!")
                    st.dataframe(data.tail(), use_container_width=True)
                else:
                    st.error("❌ Error al conectar. Intenta de nuevo en unos segundos.")
    
    # Información adicional
    with st.expander("ℹ️ Acerca de esta aplicación"):
        st.markdown("""
        **Desarrollado por:** Tu Nombre
        
        **Tecnologías utilizadas:**
        - Python 3.11
        - Streamlit
        - Pandas & NumPy
        - Plotly
        - yfinance
        
        **Fuente de datos:** Yahoo Finance
        
        **Versión:** 1.0.0
        
        ---
        
        ⚠️ **Disclaimer:** Esta aplicación es solo para fines educativos. 
        No constituye asesoramiento financiero. Siempre consulta con un 
        profesional antes de tomar decisiones de inversión.
        """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: gray; padding: 1rem;'>
        📊 S&P 500 Stock Analyzer | Desarrollado con ❤️ usando Streamlit
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()