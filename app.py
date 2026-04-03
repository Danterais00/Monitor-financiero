import streamlit as st
import yfianance as yf

st.set_page_config(page_title="Monitor Financiero", page_icon="📈")

st.title("🗞️ Monitor de Noticias de Acciones")
st.write("Introduce los tickers separados por comas (ej: AAPL, TSLA, MSFT).")

tickers_input = st.text_input("Tickers:", "AAPL, TSLA")

if tickers_input:
    tickers_list = [t.strip().upper() for t in tickers_input.split(",")]
    
    for ticker in tickers_list:
        st.subheader(f"Noticias de {ticker}")
        try:
            stock = yf.Ticker(ticker)
            news = stock.news
            
            if not news:
                st.info(f"No hay noticias recientes para {ticker}.")
            else:
                for item in news[:5]:
                    # Usamos .get() para evitar el error si la 'key' no existe
                    titulo = item.get('title', 'Título no disponible')
                    fuente = item.get('publisher', 'Fuente desconocida')
                    enlace = item.get('link', '#')
                    
                    with st.expander(titulo):
                        st.write(f"**Fuente:** {fuente}")
                        st.write(f"[Leer noticia completa]({enlace})")
                        
        except Exception as e:
            st.error(f"Hubo un problema al cargar {ticker}. Intenta de nuevo en unos minutos.")
