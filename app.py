import streamlit as st
import yfinance as yf

st.set_page_config(page_title="Monitor Financiero", page_icon="📈")

st.title("🗞️ Monitor de Noticias de Acciones")

tickers_input = st.text_input("Tickers:", "AAPL, TSLA")

if tickers_input:
    tickers_list = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]
    
    for ticker in tickers_list:
        st.subheader(f"Noticias de {ticker}")
        try:
            stock = yf.Ticker(ticker)
            news = stock.news
            
            if not news:
                st.info(f"No hay noticias recientes para {ticker}.")
            else:
                for item in news[:5]:
                    # Intentamos detectar las llaves correctas dinámicamente
                    # Algunas versiones usan 'title', otras 'content', otras 'description'
                    titulo = item.get('title') or item.get('headline') or "Título no encontrado"
                    fuente = item.get('publisher') or item.get('source') or "Fuente desconocida"
                    enlace = item.get('link') or item.get('url') or "#"
                    
                    with st.expander(titulo):
                        st.write(f"**Fuente:** {fuente}")
                        st.write(f"[Leer noticia completa]({enlace})")
                        # LÍNEA DE DIAGNÓSTICO: Si el título falla, esto nos dirá por qué
                        if titulo == "Título no encontrado":
                            st.write("Datos recibidos:", item)
                        
        except Exception as e:
            st.error(f"Error técnico: {e}")

st.divider()
st.caption("Hecho con Streamlit y Yahoo Finance")
