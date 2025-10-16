# 📊 S&P 500 Stock Analyzer

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> Plataforma interactiva para análisis técnico y fundamental de acciones del S&P 500

[🚀 Demo en Vivo](#) | [📖 Documentación](MANUAL_USO.md) | [🎥 Video Demo](#)

## ✨ Features

- 📈 **Análisis Técnico Completo**: SMA, EMA, RSI, MACD, Bollinger Bands
- 📊 **Visualizaciones Interactivas**: Gráficos de velas, volumen y más
- 🔍 **Comparación de Acciones**: Analiza múltiples acciones simultáneamente
- 📉 **Análisis de Correlación**: Descubre relaciones entre acciones
- 💾 **Cache Inteligente**: Datos en tiempo real con optimización
- 💼 **Análisis de Portafolio**: Simula y optimiza tu cartera de inversión

## 🖼️ Screenshots

![Dashboard](docs/images/dashboard.png)
![Analysis](docs/images/analysis.png)

## 🚀 Quick Start

### Requisitos

- Python 3.9 o superior
- pip o conda

### Instalación
```bash
# Clonar repositorio
git clone https://github.com/tu-usuario/SP500-Stock-Analyzer.git
cd SP500-Stock-Analyzer

# Opción 1: Con conda (recomendado)
conda create -n stock_analyzer python=3.11 -y
conda activate stock_analyzer
pip install -r requirements.txt

# Opción 2: Con venv
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Ejecutar la aplicación
```bash
streamlit run streamlit_app/app.py
```

La aplicación se abrirá en tu navegador en `http://localhost:8501`

## 📚 Uso

### Como script de Python
```python
from src.data.data_fetcher import StockDataFetcher
from src.analysis.technical_indicators import TechnicalAnalysis

# Obtener datos
fetcher = StockDataFetcher()
data = fetcher.get_stock_data('AAPL', period='1y')

# Calcular indicadores
ta = TechnicalAnalysis(data)
data_with_indicators = ta.add_all_indicators()

# Ver señales de trading
signals = ta.get_signals()
print(signals)
```

## 🛠️ Tecnologías

- **Python 3.9+**
- **Streamlit**: Dashboard interactivo
- **Pandas**: Manipulación de datos
- **yfinance**: Datos financieros en tiempo real
- **Plotly**: Visualizaciones interactivas
- **BeautifulSoup**: Web scraping para lista S&P 500

## 📊 Indicadores Implementados

- ✅ Simple Moving Average (SMA)
- ✅ Exponential Moving Average (EMA)
- ✅ Relative Strength Index (RSI)
- ✅ MACD (Moving Average Convergence Divergence)
- ✅ Bollinger Bands
- ✅ On-Balance Volume (OBV)
- ✅ Análisis de Correlación
- ✅ Métricas de Portafolio (Sharpe Ratio, Volatilidad)

## 📁 Estructura del Proyecto
```
SP500-Stock-Analyzer/
├── data/                  # Datos y cache
├── src/                   # Código fuente
│   ├── data/             # Obtención de datos
│   ├── analysis/         # Indicadores técnicos
│   ├── visualization/    # Gráficos
│   └── utils/            # Utilidades
├── streamlit_app/         # Aplicación web
│   ├── app.py
│   └── pages/            # Páginas múltiples
├── docs/                  # Documentación
├── notebooks/             # Jupyter notebooks
└── tests/                 # Tests unitarios
```

## 🤝 Contribuir

Las contribuciones son bienvenidas! Por favor:

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT - ver [LICENSE](LICENSE)

## 👤 Autor

**Francisco Guerrero**
- GitHub: [@tu-usuario](https://github.com/Fjgl96)
- LinkedIn: [Tu Perfil](https://www.linkedin.com/in/fguerrerol01/)
- Portfolio: [tu-website.com](https://tu-website.com)

## 🙏 Agradecimientos

- Datos proporcionados por [Yahoo Finance](https://finance.yahoo.com)
- Inspirado en [Trading View](https://www.tradingview.com)
- Comunidad de Streamlit

## ⚠️ Disclaimer

Esta aplicación es solo para fines educativos y de demostración. No constituye asesoramiento financiero. Siempre consulta con un profesional antes de tomar decisiones de inversión.

---

⭐ Si te gusta este proyecto, dale una estrella en GitHub!