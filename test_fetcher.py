"""
Script de prueba para data_fetcher
"""

from src.data.data_fetcher import StockDataFetcher

print('🧪 TEST DE DATA FETCHER\n')
print('=' * 50)

fetcher = StockDataFetcher()

# Test 1: Tickers
print('\n📋 Test 1: Obtener tickers')
print('-' * 50)
tickers = fetcher.get_sp500_tickers()
print(f'Tipo: {type(tickers)}')
print(f'Cantidad: {len(tickers)}')
print(f'Primeros 10: {tickers[:10]}')
print(f'Son strings?: {all(isinstance(t, str) for t in tickers[:10])}')

# Test 2: Descargar AAPL
print('\n📈 Test 2: Descargar AAPL')
print('-' * 50)
df = fetcher.get_stock_data('AAPL', period='1mo')

if df is not None:
    print('✅ Éxito!')
    print(f'Filas: {len(df)}')
    print(f'Columnas: {list(df.columns)}')
    print(f'Primeras 3 filas:')
    print(df.head(3))
    print(f'\nÚltimo precio: ${df["Close"].iloc[-1]:.2f}')
else:
    print('❌ Falló')

# Test 3: Descargar Microsoft
print('\n📊 Test 3: Descargar MSFT')
print('-' * 50)
df_msft = fetcher.get_stock_data('MSFT', period='1mo')

if df_msft is not None:
    print('✅ Éxito!')
    print(f'Último precio: ${df_msft["Close"].iloc[-1]:.2f}')
else:
    print('❌ Falló')

print('\n' + '=' * 50)
print('🏁 Tests completados\n')