import streamlit as st
import yfinance as yf

# Configuración de la página
st.set_page_config(page_title="Resumen de Noticias Financieras", page_icon="📈")

st.title("🗞️ Monitor de Noticias de Acciones")
st.write("Introduce los tickers de las empresas que te interesan (separados por comas).")

# Entrada de usuario
tickers_input = st.text_input("Ejemplo: AAPL, TSLA, MSFT, GOOGL", "AAPL, TSLA")

# Procesamiento de los tickers
if tickers_input:
    tickers_list = [t.strip().upper() for t in tickers_input.split(",")]
    
    for ticker in tickers_list:
        st.subheader(f"Noticias de {ticker}")
        try:
            # Obtener datos del ticker
            stock = yf.Ticker(ticker)
            news = stock.news
            
            if not news:
                st.warning(f"No se encontraron noticias recientes para {ticker}.")
            else:
                # Mostrar las primeras 5 noticias
                for item in news[:5]:
                    with st.expander(item['title']):
                        st.write(f"**Fuente:** {item['publisher']}")
                        st.write(f"**Fecha:** {item['type']}") # O usa timestamp si prefieres procesarlo
                        st.write(f"[Leer noticia completa]({item['link']})")
        except Exception as e:
            st.error(f"Error al buscar {ticker}: {e}")

st.divider()
st.caption("Datos obtenidos a través de la API de Yahoo Finance via yfinance.")
