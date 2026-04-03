import streamlit as st
import yfinance as yf
import feedparser
import urllib.parse

# Configuración de página
st.set_page_config(page_title="Monitor Financiero 360", page_icon="📈", layout="wide")

# --- ESTILOS CSS ---
st.markdown("""
    <style>
    .fecha-noticia { font-size: 0.7rem !important; font-weight: bold; color: #6b7280; margin-bottom: 5px; }
    .card-noticia { 
        background-color: #ffffff; padding: 12px; border-radius: 8px; border: 1px solid #e9ecef; 
        height: 100%; display: flex; flex-direction: column; justify-content: space-between;
    }
    .titulo-seccion { color: #1f1f1f; border-bottom: 2px solid #007bff; padding-bottom: 5px; margin-top: 30px; margin-bottom: 15px; }
    .ticker-header { background-color: #f0f2f6; padding: 10px; border-radius: 5px; margin-bottom: 10px; border-left: 5px solid #007bff; }
    .catalizador-pos { color: #155724; background-color: #d4edda; padding: 10px; border-radius: 5px; border-left: 5px solid #28a745; margin-bottom: 5px; font-size: 0.9rem; }
    .catalizador-neg { color: #721c24; background-color: #f8d7da; padding: 10px; border-radius: 5px; border-left: 5px solid #dc3545; margin-bottom: 5px; font-size: 0.9rem; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNCIONES ---
def obtener_noticias(query, limite=6):
    query_codificada = urllib.parse.quote(query)
    url = f"https://news.google.com/rss/search?q={query_codificada}&hl=es-419&gl=US&ceid=US:es-419"
    return feedparser.parse(url).entries[:limite]

def filtrar_catalizadores(noticias, keywords_pos, keywords_neg):
    pos_encontradas = []
    neg_encontradas = []
    
    for n in noticias:
        titular = n.title.lower()
        # Verificar positivos
        if any(k.lower() in titular for k in keywords_pos):
            pos_encontradas.append(n)
        # Verificar negativos
        elif any(k.lower() in titular for k in keywords_neg):
            neg_encontradas.append(n)
            
    return pos_encontradas[:3], neg_encontradas[:3]

# --- SIDEBAR ---
with st.sidebar:
    st.title("⚙️ Configuración")
    tickers_input = st.text_input("Mis Tickers:", "AAPL, GGAL, WMT")

# --- CUERPO PRINCIPAL ---
st.title("📊 Monitor Financiero Estratégico")

# --- SECCIONES DE CONTEXTO (Global y Nacional) ---
col_g, col_n = st.columns(2)
with col_g:
    st.markdown("<h2 class='titulo-seccion'>🌐 Global</h2>", unsafe_allow_html=True)
    for n in obtener_noticias("Economía Mundial", 2):
        st.markdown(f"**{n.title}** \n<small>{n.published[:16]}</small> [Link]({n.link})", unsafe_allow_html=True)
with col_n:
    st.markdown("<h2 class='titulo-seccion'>🇦🇷 Nacional</h2>", unsafe_allow_html=True)
    for n in obtener_noticias("Economía Argentina", 2):
        st.markdown(f"**{n.title}** \n<small>{n.published[:16]}</small> [Link]({n.link})", unsafe_allow_html=True)

# --- NUEVA SECCIÓN: NOTICIAS POR SECTOR ---
st.markdown("<h2 class='titulo-seccion'>🏬 Noticias por Sector: Comercio Minorista (Retail)</h2>", unsafe_allow_html=True)

# Definición de criterios
keywords_retail_pos = ["ventas", "alza", "navidad", "black friday", "expansión", "logística", "consumo favorable"]
keywords_retail_neg = ["caída", "baja", "inventario", "inflación", "suministro", "hábitos consumo"]

noticias_sector = obtener_noticias("sector retail comercio minorista noticias", limite=15)
pos, neg = filtrar_catalizadores(noticias_sector, keywords_retail_pos, keywords_retail_neg)

col_pos, col_neg = st.columns(2)

with col_pos:
    st.subheader("✅ Catalizadores Positivos (Subas)")
    if pos:
        for p in pos:
            st.markdown(f"<div class='catalizador-pos'><strong>{p.title}</strong><br><a href='{p.link}' target='_blank' style='color: #155724; font-size: 0.75rem;'>Ver noticia</a></div>", unsafe_allow_html=True)
    else:
        st.info("No hay información reciente")

with col_neg:
    st.subheader("❌ Catalizadores Negativos (Bajas)")
    if neg:
        for n in neg:
            st.markdown(f"<div class='catalizador-neg'><strong>{n.title}</strong><br><a href='{n.link}' target='_blank' style='color: #721c24; font-size: 0.75rem;'>Ver noticia</a></div>", unsafe_allow_html=True)
    else:
        st.info("No hay información reciente")

# --- SECCIÓN 3: TICKERS ELEGIDOS ---
st.markdown("<h2 class='titulo-seccion'>📈 Análisis de Tickers Elegidos</h2>", unsafe_allow_html=True)

if tickers_input:
    tickers_list = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]
    for ticker in tickers_list:
        try:
            stock_data = yf.Ticker(ticker)
            nombre = stock_data.info.get('longName', ticker)
            st.markdown(f"<div class='ticker-header'><strong>Acción: {nombre} ({ticker})</strong></div>", unsafe_allow_html=True)
            
            c1, c2, c3, c4 = st.columns([1, 1.5, 1.5, 1.5])
            with c1:
                precio = stock_data.history(period="1d")['Close'].iloc[-1]
                st.metric("Precio", f"${precio:.2f}")
            
            noticias_t = obtener_noticias(f"{ticker} acciones", 3)
            for j, nt in enumerate(noticias_t):
                with [c2, c3, c4][j]:
                    st.markdown(f"<div class='card-noticia'><p class='fecha-noticia'>{nt.published[:16]}</p><p style='font-size: 0.8rem;'>{nt.title}</p><a href='{nt.link}' style='font-size: 0.7rem;'>Fuente →</a></div>", unsafe_allow_html=True)
        except:
            st.error(f"Error cargando {ticker}")
