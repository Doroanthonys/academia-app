import streamlit as st
import pandas as pd
import requests
from datetime import datetime, date, time
import json
import os
import io
import urllib.parse

# ---------------------------------------------------------
# 1. CONFIGURACIÓN DE PÁGINA Y BOT TELEGRAM
# ---------------------------------------------------------
st.set_page_config(
    page_title="Anthony's English School",
    page_icon="🇬🇧",
    layout="wide",
    initial_sidebar_state="expanded"
)

TELEGRAM_TOKEN = "8811202788:AAF3mWm2tCVUkZe9mg5XhLuxuogEMK3pNlU"
TELEGRAM_CHAT_ID = "8954494227"

try:
    if "TELEGRAM_TOKEN" in st.secrets:
        TELEGRAM_TOKEN = st.secrets["TELEGRAM_TOKEN"]
    if "TELEGRAM_CHAT_ID" in st.secrets:
        TELEGRAM_CHAT_ID = st.secrets["TELEGRAM_CHAT_ID"]
except Exception:
    pass

def enviar_notificacion_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": mensaje, "parse_mode": "Markdown"}
    try:
        res = requests.post(url, json=payload, timeout=5)
        return res.status_code == 200
    except Exception:
        return False

def enviar_foto_telegram(foto_bytes, caption):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
    files = {"photo": ("anuncio.jpg", foto_bytes, "image/jpeg")}
    data = {"chat_id": TELEGRAM_CHAT_ID, "caption": caption, "parse_mode": "Markdown"}
    try:
        res = requests.post(url, files=files, data=data, timeout=10)
        return res.status_code == 200
    except Exception:
        return False

# Estilos CSS Modernos
st.markdown("""
    <style>
    .stApp { background-color: #F8FAFC; }
    .hero-box {
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
        padding: 22px; border-radius: 16px; color: white;
        text-align: center; box-shadow: 0px 8px 20px rgba(30, 58, 138, 0.15);
        margin-bottom: 20px;
    }
    .hero-title { font-size: 2.1rem; font-weight: 800; margin: 0; }
    .hero-subtitle { font-size: 1rem; opacity: 0.9; margin-top: 4px; }
    .btn-action {
        display: inline-flex; align-items: center; justify-content: center;
        width: 100%; padding: 10px 14px; border-radius: 8px; font-weight: 700;
        font-size: 0.9rem; text-decoration: none !important; text-align: center;
        box-shadow: 0px 3px 8px rgba(0,0,0,0.08);
    }
    .btn-call { background-color: #2563EB; color: #FFFFFF !important; }
    .btn-wa { background-color: #25D366; color: #FFFFFF !important; }
    .preview-card {
        background-color: #FFFFFF; border: 1px solid #E2E8F0;
        border-radius: 12px; padding: 16px; margin-top: 10px;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.05);
    }
    .kpi-card {
        background-color: #FFFFFF; border-radius: 12px; padding: 16px;
        border: 1px solid #E2E8F0; text-align: center;
        box-shadow: 0px 2px 6px rgba(0,0,0,0.04);
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. BASE DE DATOS DE ALUMNOS Y ARCHIVOS LOCALES
# ---------------------------------------------------------
DATA_FILE = "alumnos_data.csv"
REC_FILE = "recordatorios.json"
HORARIOS_FILE = "horarios_data.json"
PAGOS_FILE = "pagos_data.json"
CAJA_FILE = "caja_data.json"

GSHEET_ID = "1Yz_QgCn9Amfurxa5YWDgJYuN3HB-d5tVqGRcvWYjEiE"
GSHEET_CSV_URL = f"https://docs.google.com/spreadsheets/d/{GSHEET_ID}/gviz/tq?tqx=out:csv"

def obtener_movimientos_caja_gsheets():
    try:
        df_caja = pd.read_csv(GSHEET_CSV_URL)
        df_caja.columns = [str(c).strip() for c in df_caja.columns]
        return df_caja
    except Exception:
        if os.path.exists(CAJA_FILE):
            with open(CAJA_FILE, "r") as f:
                caja_local = json.load(f)
            return pd.DataFrame(caja_local.get("movimientos", []))
        return pd.DataFrame(columns=["Fecha", "Hora", "Tipo", "Monto", "Motivo"])

def obtener_alumnos_con_nuevos():
    return [
        {"Matrícula": "579", "Nombre": "LUCIA", "Primer Apellido": "PENAS", "Segundo Apellido": "LORENZO", "Teléfono": "609671976", "Fecha Alta": "02/10/2019"},
        {"Matrícula": "601", "Nombre": "RODRIGO", "Primer Apellido": "LOPEZ", "Segundo Apellido": "CID", "Teléfono": "630653659", "Fecha Alta": "12/11/2014"},
        {"Matrícula": "735", "Nombre": "MYRIAM", "Primer Apellido": "GAVILANES", "Segundo Apellido": "FEIJOO", "Teléfono": "659274499", "Fecha Alta": "27/09/2017"},
        {"Matrícula": "878", "Nombre": "ALEX", "Primer Apellido": "CALDELAS", "Segundo Apellido": "CASAS", "Teléfono": "661603323", "Fecha Alta": "23/09/2021"},
        {"Matrícula": "936", "Nombre": "AIMAR", "Primer Apellido": "CID", "Segundo Apellido": "BLANCO", "Teléfono": "645979057", "Fecha Alta": "22/09/2022"},
        {"Matrícula": "942", "Nombre": "ORLINDES", "Primer Apellido": "MONTES", "Segundo Apellido": "NOYA", "Teléfono": "66647073", "Fecha Alta": "22/09/2022"},
        {"Matrícula": "943", "Nombre": "MARIA", "Primer Apellido": "HERMIDA", "Segundo Apellido": "CARBALLO", "Teléfono": "649052393", "Fecha Alta": "22/09/2022"},
        {"Matrícula": "971", "Nombre": "NOEL", "Primer Apellido": "CID", "Segundo Apellido": "BLANCO", "Teléfono": "645979057", "Fecha Alta": "12/09/2023"},
        {"Matrícula": "972", "Nombre": "BRUNO", "Primer Apellido": "DORRIBO", "Segundo Apellido": "ALBA", "Teléfono": "626212544", "Fecha Alta": "29/09/2023"},
        {"Matrícula": "973", "Nombre": "MARA", "Primer Apellido": "DORRIBO", "Segundo Apellido": "ALBA", "Teléfono": "626212544", "Fecha Alta": "29/09/2023"},
        {"Matrícula": "975", "Nombre": "JAVIER", "Primer Apellido": "CANEIRO", "Segundo Apellido": "SENIN", "Teléfono": "617494511", "Fecha Alta": "29/09/2023"},
        {"Matrícula": "983", "Nombre": "ALEXANDRE", "Primer Apellido": "RODRIGUEZ", "Segundo Apellido": "CAMPO", "Teléfono": "619099126", "Fecha Alta": "24/10/2025"},
        {"Matrícula": "984", "Nombre": "ESTELA", "Primer Apellido": "RODRIGUEZ", "Segundo Apellido": "CAMPO", "Teléfono": "619099126", "Fecha Alta": "24/10/2025"},
        {"Matrícula": "989", "Nombre": "ALEJANDRO", "Primer Apellido": "SERANTES", "Segundo Apellido": "PARDO", "Teléfono": "646805466", "Fecha Alta": "29/09/2023"},
        {"Matrícula": "992", "Nombre": "EREA", "Primer Apellido": "FERNANDEZ", "Segundo Apellido": "MARTINEZ", "Teléfono": "696400663", "Fecha Alta": "02/11/2023"},
        {"Matrícula": "994", "Nombre": "SARA", "Primer Apellido": "DIAZ", "Segundo Apellido": "MENDEZ", "Teléfono": "630077532", "Fecha Alta": "02/02/2024"},
        {"Matrícula": "1000", "Nombre": "ADRIAN", "Primer Apellido": "ALVAREZ", "Segundo Apellido": "ENRIQUEZ", "Teléfono": "651527730", "Fecha Alta": "07/10/2024"},
        {"Matrícula": "1001", "Nombre": "YOEL", "Primer Apellido": "PEREZ", "Segundo Apellido": "PEREZ", "Teléfono": "670825582", "Fecha Alta": "02/10/2024"},
        {"Matrícula": "1002", "Nombre": "EVA", "Primer Apellido": "TIERNO", "Segundo Apellido": "PEREZ", "Teléfono": "649610750", "Fecha Alta": "02/10/2024"},
        {"Matrícula": "1003", "Nombre": "INES", "Primer Apellido": "TIERNO", "Segundo Apellido": "PEREZ", "Teléfono": "649610750", "Fecha Alta": "02/10/2024"},
        {"Matrícula": "1004", "Nombre": "HECTOR", "Primer Apellido": "FERNANDEZ", "Segundo Apellido": "GIL", "Teléfono": "630450122", "Fecha Alta": "02/10/2024"},
        {"Matrícula": "1010", "Nombre": "BELTRAN", "Primer Apellido": "RODRIGUEZ", "Segundo Apellido": "VASALLO", "Teléfono": "661603749", "Fecha Alta": "13/10/2025"},
        {"Matrícula": "1027", "Nombre": "LUCA", "Primer Apellido": "GOMEZ", "Segundo Apellido": "TELLERIA", "Teléfono": "651326675", "Fecha Alta": "25/09/2024"},
        {"Matrícula": "1028", "Nombre": "BRUNO", "Primer Apellido": "GOMEZ", "Segundo Apellido": "TELLERIA", "Teléfono": "651326675", "Fecha Alta": "25/09/2024"},
        {"Matrícula": "1029", "Nombre": "DIEGO", "Primer Apellido": "FERNANDEZ", "Segundo Apellido": "FUENTEFRIA", "Teléfono": "687418829", "Fecha Alta": "22/10/2024"},
        {"Matrícula": "1033", "Nombre": "ALVARO", "Primer Apellido": "DOMINGUEZ", "Segundo Apellido": "GUZMAN", "Teléfono": "630876429", "Fecha Alta": "25/09/2024"},
        {"Matrícula": "1035", "Nombre": "HUGO", "Primer Apellido": "ARMESTO", "Segundo Apellido": "OTERO", "Teléfono": "679217341", "Fecha Alta": "25/09/2024"},
        {"Matrícula": "1042", "Nombre": "UXIA", "Primer Apellido": "MARTINEZ", "Segundo Apellido": "MORAL", "Teléfono": "619868077", "Fecha Alta": "25/09/2024"},
        {"Matrícula": "1047", "Nombre": "EMILY", "Primer Apellido": "PARDO", "Segundo Apellido": "COSTAS", "Teléfono": "682736955", "Fecha Alta": "25/09/2024"},
        {"Matrícula": "1054", "Nombre": "MARTA", "Primer Apellido": "GARCIA", "Segundo Apellido": "RODRIGUEZ", "Teléfono": "609873706", "Fecha Alta": "25/09/2024"},
        {"Matrícula": "1056", "Nombre": "MARTIN", "Primer Apellido": "BRANDIN", "Segundo Apellido": "SALGADO", "Teléfono": "677332663", "Fecha Alta": "25/09/2024"},
        {"Matrícula": "1058", "Nombre": "ANXO", "Primer Apellido": "DE LA IGLESIA", "Segundo Apellido": "MARTINEZ", "Teléfono": "606087419", "Fecha Alta": "25/09/2024"},
        {"Matrícula": "1059", "Nombre": "FERNANDO", "Primer Apellido": "VALBUENA", "Segundo Apellido": "VAZQUEZ", "Teléfono": "665089859", "Fecha Alta": "03/10/2024"},
        {"Matrícula": "1060", "Nombre": "JORGE", "Primer Apellido": "FERNANDEZ", "Segundo Apellido": "DACAL", "Teléfono": "686264241", "Fecha Alta": "25/09/2024"},
        {"Matrícula": "1061", "Nombre": "ALEJANDRO", "Primer Apellido": "LOPEZ", "Segundo Apellido": "BARREIROS", "Teléfono": "658633496", "Fecha Alta": "25/09/2024"},
        {"Matrícula": "1063", "Nombre": "MARTIN", "Primer Apellido": "SALGADO", "Segundo Apellido": "D ALTO", "Teléfono": "617634229", "Fecha Alta": "25/09/2024"},
        {"Matrícula": "1070", "Nombre": "ALVARO", "Primer Apellido": "PENIN", "Segundo Apellido": "BLANCO", "Teléfono": "600407372", "Fecha Alta": "25/09/2024"},
        {"Matrícula": "1072", "Nombre": "LAURA", "Primer Apellido": "ALVAREZ", "Segundo Apellido": "RAMA", "Teléfono": "602683194", "Fecha Alta": "25/09/2024"},
        {"Matrícula": "1078", "Nombre": "DANIELLA", "Primer Apellido": "GUTIERREZ", "Segundo Apellido": "FERNANDEZ", "Teléfono": "661378913", "Fecha Alta": "23/10/2025"},
        {"Matrícula": "1083", "Nombre": "IRIA", "Primer Apellido": "RODRIGUEZ", "Segundo Apellido": "FERNANDEZ", "Teléfono": "676884647", "Fecha Alta": "25/09/2024"},
        {"Matrícula": "1095", "Nombre": "HUGO", "Primer Apellido": "RODRIGUEZ", "Segundo Apellido": "LASTRA", "Teléfono": "626184546", "Fecha Alta": "27/09/2024"},
        {"Matrícula": "1096", "Nombre": "BRAIS", "Primer Apellido": "CID", "Segundo Apellido": "GALLEGO", "Teléfono": "637303133", "Fecha Alta": "04/10/2024"},
        {"Matrícula": "1118", "Nombre": "XIAN", "Primer Apellido": "VAZQUEZ", "Segundo Apellido": "BLANCO", "Teléfono": "670825409", "Fecha Alta": "06/10/2025"},
        {"Matrícula": "1119", "Nombre": "COVA", "Primer Apellido": "VAZQUEZ", "Segundo Apellido": "BLANCO", "Teléfono": "670825409", "Fecha Alta": "06/10/2025"},
        {"Matrícula": "1121", "Nombre": "NEREA", "Primer Apellido": "VILARCHAO", "Segundo Apellido": "SOTO", "Teléfono": "647990884", "Fecha Alta": "07/10/2025"},
        {"Matrícula": "1123", "Nombre": "SARA", "Primer Apellido": "SOUTO", "Segundo Apellido": "GOMEZ", "Teléfono": "616502050", "Fecha Alta": "07/10/2025"},
        {"Matrícula": "1128", "Nombre": "FERNANDA", "Primer Apellido": "CASTRO", "Segundo Apellido": "ANAYA", "Teléfono": "683622272", "Fecha Alta": "26/09/2025"},
        {"Matrícula": "1129", "Nombre": "IZAN", "Primer Apellido": "RODRIGUEZ", "Segundo Apellido": "RAAB", "Teléfono": "667743950", "Fecha Alta": "26/09/2025"},
        {"Matrícula": "1130", "Nombre": "MARTIN", "Primer Apellido": "SALGADO", "Segundo Apellido": "CARBALLO", "Teléfono": "650179009", "Fecha Alta": "26/09/2025"},
        {"Matrícula": "1131", "Nombre": "MARIO", "Primer Apellido": "SALGADO", "Segundo Apellido": "CARBALLO", "Teléfono": "650179009", "Fecha Alta": "26/09/2025"},
        {"Matrícula": "1133", "Nombre": "SARA", "Primer Apellido": "GONZALEZ", "Segundo Apellido": "PENA", "Teléfono": "666576651", "Fecha Alta": "26/09/2025"},
        {"Matrícula": "1134", "Nombre": "ALDARA", "Primer Apellido": "FERNANDEZ", "Segundo Apellido": "RODRIGUEZ", "Teléfono": "679212158", "Fecha Alta": "26/09/2025"},
        {"Matrícula": "1135", "Nombre": "ELENA", "Primer Apellido": "GUZMAN", "Segundo Apellido": "DOMINGUEZ", "Teléfono": "630876429", "Fecha Alta": "26/09/2025"},
        {"Matrícula": "1137", "Nombre": "CANDELA", "Primer Apellido": "MENDEZ", "Segundo Apellido": "REGUERA", "Teléfono": "667863029", "Fecha Alta": "01/10/2025"},
        {"Matrícula": "1138", "Nombre": "CARLOTA", "Primer Apellido": "MENDEZ", "Segundo Apellido": "REGUERA", "Teléfono": "667863029", "Fecha Alta": "01/10/2025"},
        {"Matrícula": "1141", "Nombre": "OLAIA", "Primer Apellido": "BOTTI", "Segundo Apellido": "SOUTO", "Teléfono": "696749261", "Fecha Alta": "14/11/2025"},
        {"Matrícula": "1142", "Nombre": "GANNI", "Primer Apellido": "IGLESIAS", "Segundo Apellido": "BOTTI", "Teléfono": "663064797", "Fecha Alta": "14/11/2025"},
        {"Matrícula": "1143", "Nombre": "BRAIS", "Primer Apellido": "GOMEZ", "Segundo Apellido": "BREA", "Teléfono": "652895437", "Fecha Alta": "28/11/2025"},
        {"Matrícula": "1145", "Nombre": "VERA", "Primer Apellido": "FERNANDEZ", "Segundo Apellido": "VARELAS", "Teléfono": "616321463", "Fecha Alta": "09/12/2025"},
        {"Matrícula": "1148", "Nombre": "ALEJANDRO", "Primer Apellido": "CHAO", "Segundo Apellido": "FERRADAS", "Teléfono": "636765415", "Fecha Alta": "01/06/2026"},
        {"Matrícula": "10239", "Nombre": "HUGO", "Primer Apellido": "SANMARTIN", "Segundo Apellido": "DACOSTA", "Teléfono": "626562540", "Fecha Alta": "04/10/2012"},
        {"Matrícula": "10444", "Nombre": "AGUSTINA", "Primer Apellido": "RUIBAL", "Segundo Apellido": "SAGASTI", "Teléfono": "620962055", "Fecha Alta": "26/10/2016"},
        {"Matrícula": "10616", "Nombre": "ALEJANDRO", "Primer Apellido": "VAZQUEZ", "Segundo Apellido": "SEVILLANO", "Teléfono": "682172225", "Fecha Alta": "26/10/2020"},
        {"Matrícula": "10639", "Nombre": "PAULA", "Primer Apellido": "LASTRA", "Segundo Apellido": "RIGUELA", "Teléfono": "656669035", "Fecha Alta": "14/09/2021"},
        {"Matrícula": "10644", "Nombre": "LUCAS", "Primer Apellido": "RODRIGUEZ", "Segundo Apellido": "LOPEZ", "Teléfono": "677822693", "Fecha Alta": "25/10/2021"},
        {"Matrícula": "10645", "Nombre": "ALVARO", "Primer Apellido": "RODRIGUEZ", "Segundo Apellido": "FOLLA", "Teléfono": "660990063", "Fecha Alta": "28/10/2021"},
        {"Matrícula": "10649", "Nombre": "SAMUEL", "Primer Apellido": "RODRIGUEZ", "Segundo Apellido": "MIRA", "Teléfono": "676035976", "Fecha Alta": "07/10/2021"},
        {"Matrícula": "10660", "Nombre": "ADA", "Primer Apellido": "PEREZ", "Segundo Apellido": "TABOADA", "Teléfono": "696324742", "Fecha Alta": "07/10/2021"},
        {"Matrícula": "10668", "Nombre": "LUIS", "Primer Apellido": "URUBURU", "Segundo Apellido": "AIRAS", "Teléfono": "670640793", "Fecha Alta": "15/12/2021"},
        {"Matrícula": "10671", "Nombre": "XABIER", "Primer Apellido": "IGLESIAS", "Segundo Apellido": "LOPEZ", "Teléfono": "609752454", "Fecha Alta": "10/03/2022"},
        {"Matrícula": "10677", "Nombre": "MARTIN", "Primer Apellido": "LOPEZ", "Segundo Apellido": "ARIAS", "Teléfono": "626109986", "Fecha Alta": "07/09/2022"},
        {"Matrícula": "10694", "Nombre": "ANDRE", "Primer Apellido": "FERNANDEZ", "Segundo Apellido": "MACEIRAS", "Teléfono": "610942238", "Fecha Alta": "06/10/2022"},
        {"Matrícula": "10696", "Nombre": "NOEL", "Primer Apellido": "RODRIGUEZ", "Segundo Apellido": "GONZALEZ", "Teléfono": "607591682", "Fecha Alta": "29/09/2022"},
        {"Matrícula": "10702", "Nombre": "MATEO", "Primer Apellido": "PARDO", "Segundo Apellido": "SERANTES", "Teléfono": "646805466", "Fecha Alta": "06/10/2022"},
        {"Matrícula": "10706", "Nombre": "JOSE", "Primer Apellido": "GARCIA", "Segundo Apellido": "VILA", "Teléfono": "620836164", "Fecha Alta": "25/11/2022"},
        {"Matrícula": "10713", "Nombre": "PAULA", "Primer Apellido": "GOMEZ", "Segundo Apellido": "GONZALEZ", "Teléfono": "647646793", "Fecha Alta": "25/09/2023"},
        {"Matrícula": "10734", "Nombre": "HUGO", "Primer Apellido": "FERNANDEZ", "Segundo Apellido": "SALGADO", "Teléfono": "657014918", "Fecha Alta": "29/09/2023"},
        {"Matrícula": "10735", "Nombre": "MARC", "Primer Apellido": "PACREU", "Segundo Apellido": "ESTEVEZ", "Teléfono": "670443414", "Fecha Alta": "29/09/2023"},
        {"Matrícula": "10736", "Nombre": "ALVARO", "Primer Apellido": "GOMEZ", "Segundo Apellido": "RAMOS", "Teléfono": "646772435", "Fecha Alta": "29/09/2023"},
        {"Matrícula": "10737", "Nombre": "IAGO", "Primer Apellido": "GONZALEZ", "Segundo Apellido": "GARCIA", "Teléfono": "654247396", "Fecha Alta": "29/09/2023"},
        {"Matrícula": "10741", "Nombre": "SHASHA", "Primer Apellido": "IGLESIAS", "Segundo Apellido": "GONZALEZ", "Teléfono": "676046101", "Fecha Alta": "06/10/2023"},
        {"Matrícula": "10746", "Nombre": "NOE", "Primer Apellido": "RIVERO", "Segundo Apellido": "RIVERO", "Teléfono": "630652131", "Fecha Alta": "10/11/2023"},
        {"Matrícula": "10748", "Nombre": "ALEJANDRO", "Primer Apellido": "NESPEREIRA", "Segundo Apellido": "VALADARES", "Teléfono": "678638702", "Fecha Alta": "17/01/2024"},
        {"Matrícula": "10758", "Nombre": "FELIX", "Primer Apellido": "LEYES", "Segundo Apellido": "VADILLO", "Teléfono": "606111008", "Fecha Alta": "01/10/2024"},
        {"Matrícula": "10760", "Nombre": "ANTONIO", "Primer Apellido": "DE LAS CUEVAS", "Segundo Apellido": "QUINTAS", "Teléfono": "645830475", "Fecha Alta": "27/09/2024"},
        {"Matrícula": "10764", "Nombre": "MANUEL", "Primer Apellido": "PALOMO", "Segundo Apellido": "GOMEZ", "Teléfono": "687759598", "Fecha Alta": "27/09/2024"},
        {"Matrícula": "10766", "Nombre": "INES", "Primer Apellido": "DOMINGUEZ", "Segundo Apellido": "GUZMAN", "Teléfono": "630876429", "Fecha Alta": "25/09/2024"},
        {"Matrícula": "10770", "Nombre": "MARCOS", "Primer Apellido": "MARTINEZ", "Segundo Apellido": "DE LA IGLESIA", "Teléfono": "606387419", "Fecha Alta": "03/10/2024"},
        {"Matrícula": "10774", "Nombre": "MARTIN", "Primer Apellido": "VARELA", "Segundo Apellido": "DA CUÑA", "Teléfono": "666222608", "Fecha Alta": "18/10/2024"},
        {"Matrícula": "10778", "Nombre": "ALBA", "Primer Apellido": "DAPENA", "Segundo Apellido": "MEDELA", "Teléfono": "629622391", "Fecha Alta": "13/01/2025"},
        {"Matrícula": "10779", "Nombre": "PABLO", "Primer Apellido": "DAPENA", "Segundo Apellido": "MEDELA", "Teléfono": "629622391", "Fecha Alta": "13/01/2025"},
        {"Matrícula": "10780", "Nombre": "DANIELA", "Primer Apellido": "RODRIGUEZ", "Segundo Apellido": "REGUART", "Teléfono": "693644339", "Fecha Alta": "15/01/2025"},
        {"Matrícula": "10785", "Nombre": "XIANA XOEL", "Primer Apellido": "POZO", "Segundo Apellido": "CID", "Teléfono": "636358438", "Fecha Alta": "18/09/2025"},
        {"Matrícula": "10786", "Nombre": "SARELA", "Primer Apellido": "PEREZ", "Segundo Apellido": "RUA", "Teléfono": "669706783", "Fecha Alta": "18/09/2025"},
        {"Matrícula": "10796", "Nombre": "ALVARO", "Primer Apellido": "GARCIA", "Segundo Apellido": "RODRIGUEZ", "Teléfono": "661423773", "Fecha Alta": "30/01/2026"},
        {"Matrícula": "20030", "Nombre": "EMILIO", "Primer Apellido": "GONZALEZ", "Segundo Apellido": "PAZOS", "Teléfono": "669365020", "Fecha Alta": "14/10/2009"},
        {"Matrícula": "21077", "Nombre": "JAVIER", "Primer Apellido": "GARCIA", "Segundo Apellido": "CARBALLO", "Teléfono": "662049766", "Fecha Alta": "08/11/2022"},
        {"Matrícula": "21100", "Nombre": "NATALIA", "Primer Apellido": "SANTAS", "Segundo Apellido": "SEARA", "Teléfono": "6262251295", "Fecha Alta": "04/10/2023"},
        {"Matrícula": "21119", "Nombre": "BEATRIZ", "Primer Apellido": "GONTAD", "Segundo Apellido": "CURROS", "Teléfono": "653070592", "Fecha Alta": "11/09/2024"},
        {"Matrícula": "21146", "Nombre": "EVA", "Primer Apellido": "ALVITE", "Segundo Apellido": "VILABOY", "Teléfono": "620372394", "Fecha Alta": "17/10/2024"},
        {"Matrícula": "21166", "Nombre": "HUGO", "Primer Apellido": "VAZQUEZ", "Segundo Apellido": "VILA", "Teléfono": "626150544", "Fecha Alta": "01/10/2025"},
        {"Matrícula": "21173", "Nombre": "PALOMA", "Primer Apellido": "UGARTE", "Segundo Apellido": "GARCIA", "Teléfono": "673525726", "Fecha Alta": "04/06/2026"},

        # --- 18 NUEVOS ANTERIORES ---
        {"Matrícula": "1008", "Nombre": "RUBEN", "Primer Apellido": "CASADO", "Segundo Apellido": "FERNANDEZ", "Teléfono": "626546199", "Fecha Alta": "22/09/2024"},
        {"Matrícula": "1043", "Nombre": "ALEJANDRA", "Primer Apellido": "CANAL", "Segundo Apellido": "DOMINGUEZ", "Teléfono": "606353218", "Fecha Alta": "24/09/2024"},
        {"Matrícula": "1055", "Nombre": "MAURO", "Primer Apellido": "DIAZ", "Segundo Apellido": "FERNANDEZ", "Teléfono": "666563610", "Fecha Alta": "24/09/2024"},
        {"Matrícula": "1080", "Nombre": "LUANA EN", "Primer Apellido": "BAO", "Segundo Apellido": "XIA", "Teléfono": "618643807", "Fecha Alta": "24/09/2024"},
        {"Matrícula": "1081", "Nombre": "LUKE", "Primer Apellido": "BAO", "Segundo Apellido": "XIA", "Teléfono": "618643807", "Fecha Alta": "24/09/2024"},
        {"Matrícula": "1082", "Nombre": "LUCA", "Primer Apellido": "BAO", "Segundo Apellido": "XIA", "Teléfono": "618643807", "Fecha Alta": "24/09/2024"},
        {"Matrícula": "1092", "Nombre": "LIA", "Primer Apellido": "MIGUEZ", "Segundo Apellido": "GOMEZ", "Teléfono": "687912772", "Fecha Alta": "24/09/2024"},
        {"Matrícula": "1101", "Nombre": "ZOE", "Primer Apellido": "PARK", "Segundo Apellido": "DO", "Teléfono": "988064432", "Fecha Alta": "27/09/2024"},
        {"Matrícula": "1117", "Nombre": "ADRIAN", "Primer Apellido": "ALVAREZ", "Segundo Apellido": "CARBALLAL", "Teléfono": "607387571", "Fecha Alta": "23/09/2025"},
        {"Matrícula": "1126", "Nombre": "MARCO", "Primer Apellido": "GABRIEL", "Segundo Apellido": "CID", "Teléfono": "609854509", "Fecha Alta": "24/09/2025"},
        {"Matrícula": "1144", "Nombre": "MIKEL", "Primer Apellido": "GOMEZ", "Segundo Apellido": "BREA", "Teléfono": "652895437", "Fecha Alta": "21/11/2025"},
        {"Matrícula": "1146", "Nombre": "ANDREA", "Primer Apellido": "PEREZ", "Segundo Apellido": "", "Teléfono": "6163321463", "Fecha Alta": "11/12/2025"},
        {"Matrícula": "1147", "Nombre": "CLOE", "Primer Apellido": "RODRIGUEZ", "Segundo Apellido": "PALLA", "Teléfono": "661467904", "Fecha Alta": "13/04/2026"},
        {"Matrícula": "10492", "Nombre": "MARIO", "Primer Apellido": "SARMIENTO", "Segundo Apellido": "", "Teléfono": "636220698", "Fecha Alta": "27/09/2017"},
        {"Matrícula": "10642", "Nombre": "IÑAKI", "Primer Apellido": "MERELLES", "Segundo Apellido": "IGLESIAS", "Teléfono": "697326165", "Fecha Alta": "30/09/2021"},
        {"Matrícula": "10658", "Nombre": "ALBERTO", "Primer Apellido": "NOVOA", "Segundo Apellido": "ALVAREZ", "Teléfono": "647251628", "Fecha Alta": "30/09/2021"},
        {"Matrícula": "21050", "Nombre": "BEGOÑA", "Primer Apellido": "TEJERO", "Segundo Apellido": "MIGUEZ", "Teléfono": "678892964", "Fecha Alta": "30/09/2021"},
        {"Matrícula": "21139", "Nombre": "IRIA", "Primer Apellido": "CIBREIRO", "Segundo Apellido": "TRIGO", "Teléfono": "636006448", "Fecha Alta": "23/09/2024"},

        # --- 17 NUEVOS ALUMNOS ---
        {"Matrícula": "1016", "Nombre": "XINHUI", "Primer Apellido": "XIA", "Segundo Apellido": "", "Teléfono": "618643807", "Fecha Alta": "22/09/2024"},
        {"Matrícula": "10751", "Nombre": "IAGO", "Primer Apellido": "MERELLES", "Segundo Apellido": "IGLESIAS", "Teléfono": "687683242", "Fecha Alta": "05/02/2024"},
        {"Matrícula": "10756", "Nombre": "CESAR", "Primer Apellido": "MENOR", "Segundo Apellido": "FERNANDEZ", "Teléfono": "676050069", "Fecha Alta": "14/09/2024"},
        {"Matrícula": "10759", "Nombre": "XURXO ANXO", "Primer Apellido": "ROJAS", "Segundo Apellido": "MANUEL", "Teléfono": "659102441", "Fecha Alta": "22/09/2024"},
        {"Matrícula": "10765", "Nombre": "JIMENA MARIA", "Primer Apellido": "FERNANDEZ", "Segundo Apellido": "CONDE", "Teléfono": "637852079", "Fecha Alta": "22/09/2024"},
        {"Matrícula": "10781", "Nombre": "BORJA", "Primer Apellido": "LORENZO", "Segundo Apellido": "GRANDE", "Teléfono": "637598042", "Fecha Alta": "14/01/2025"},
        {"Matrícula": "10782", "Nombre": "LUCIA", "Primer Apellido": "CANEIRO", "Segundo Apellido": "BASALO", "Teléfono": "630917160", "Fecha Alta": "25/02/2025"},
        {"Matrícula": "10788", "Nombre": "DIEGO", "Primer Apellido": "RIAL", "Segundo Apellido": "ROMAN", "Teléfono": "637353599", "Fecha Alta": "19/09/2025"},
        {"Matrícula": "10789", "Nombre": "IRATI", "Primer Apellido": "MIRANDA", "Segundo Apellido": "GARCIA", "Teléfono": "627630170", "Fecha Alta": "19/09/2025"},
        {"Matrícula": "10791", "Nombre": "DUNIA", "Primer Apellido": "LOPEZ", "Segundo Apellido": "SILVA", "Teléfono": "696624077", "Fecha Alta": "23/09/2025"},
        {"Matrícula": "10792", "Nombre": "MAURO", "Primer Apellido": "MENDEZ", "Segundo Apellido": "LORENZO", "Teléfono": "605311903", "Fecha Alta": "24/09/2025"},
        {"Matrícula": "10794", "Nombre": "ALEJANDRO", "Primer Apellido": "ADRIAN CARBALLEDA", "Segundo Apellido": "OGANDO", "Teléfono": "659690505", "Fecha Alta": "26/11/2025"},
        {"Matrícula": "10795", "Nombre": "HUGO", "Primer Apellido": "OUTEIRIÑO", "Segundo Apellido": "MOURE", "Teléfono": "636898067", "Fecha Alta": "02/12/2025"},
        {"Matrícula": "10802", "Nombre": "JAVIER", "Primer Apellido": "GARRIDO", "Segundo Apellido": "FERNANDEZ", "Teléfono": "647070082", "Fecha Alta": "30/04/2026"},
        {"Matrícula": "10808", "Nombre": "SOFIA", "Primer Apellido": "GONALEZ", "Segundo Apellido": "VAZQUEZ", "Teléfono": "667567900", "Fecha Alta": "10/11/2024"},
        {"Matrícula": "10809", "Nombre": "DIEGO", "Primer Apellido": "GONZALEZ", "Segundo Apellido": "VAZQUEZ", "Teléfono": "667567900", "Fecha Alta": "10/11/2024"},
        {"Matrícula": "21122", "Nombre": "ALFONSO", "Primer Apellido": "ALVAREZ", "Segundo Apellido": "RODRIGUEZ", "Teléfono": "639165754", "Fecha Alta": "22/09/2024"},

        # --- 30 ALUMNOS PENDIENTES DE FICHA/MATRÍCULA ---
        {"Matrícula": "PEND-1", "Nombre": "JINCHENG", "Primer Apellido": "SIN FICHA", "Segundo Apellido": "", "Teléfono": "PENDIENTE", "Fecha Alta": "01/10/2026"},
        {"Matrícula": "PEND-2", "Nombre": "SARA", "Primer Apellido": "CALVO", "Segundo Apellido": "", "Teléfono": "PENDIENTE", "Fecha Alta": "01/10/2026"},
        {"Matrícula": "PEND-3", "Nombre": "ANDREA", "Primer Apellido": "CALVO", "Segundo Apellido": "ANDRADE", "Teléfono": "PENDIENTE", "Fecha Alta": "01/10/2026"},
        {"Matrícula": "PEND-4", "Nombre": "NEREA", "Primer Apellido": "QUINTAS", "Segundo Apellido": "", "Teléfono": "PENDIENTE", "Fecha Alta": "01/10/2026"},
        {"Matrícula": "PEND-5", "Nombre": "ALEX", "Primer Apellido": "CASAS", "Segundo Apellido": "CALDELAS", "Teléfono": "PENDIENTE", "Fecha Alta": "01/10/2026"},
        {"Matrícula": "PEND-6", "Nombre": "XULIANA", "Primer Apellido": "SIN FICHA", "Segundo Apellido": "", "Teléfono": "PENDIENTE", "Fecha Alta": "01/10/2026"},
        {"Matrícula": "PEND-7", "Nombre": "RUTH", "Primer Apellido": "CADAH", "Segundo Apellido": "", "Teléfono": "PENDIENTE", "Fecha Alta": "01/10/2026"},
        {"Matrícula": "PEND-8", "Nombre": "MARA", "Primer Apellido": "DORRIBO", "Segundo Apellido": "", "Teléfono": "PENDIENTE", "Fecha Alta": "01/10/2026"},
        {"Matrícula": "PEND-9", "Nombre": "IRENE", "Primer Apellido": "CUENCA", "Segundo Apellido": "", "Teléfono": "PENDIENTE", "Fecha Alta": "01/10/2026"},
        {"Matrícula": "PEND-10", "Nombre": "HELENA", "Primer Apellido": "VIEIRA", "Segundo Apellido": "GONZ", "Teléfono": "PENDIENTE", "Fecha Alta": "01/10/2026"},
        {"Matrícula": "PEND-11", "Nombre": "MANUEL", "Primer Apellido": "GONZ", "Segundo Apellido": "GONZ", "Teléfono": "PENDIENTE", "Fecha Alta": "01/10/2026"},
        {"Matrícula": "PEND-12", "Nombre": "NICO", "Primer Apellido": "PALACIO", "Segundo Apellido": "LUENGOS", "Teléfono": "PENDIENTE", "Fecha Alta": "01/10/2026"},
        {"Matrícula": "PEND-13", "Nombre": "ALBA", "Primer Apellido": "CARBAJALES", "Segundo Apellido": "OTERO", "Teléfono": "PENDIENTE", "Fecha Alta": "01/10/2026"},
        {"Matrícula": "PEND-14", "Nombre": "MYRIAM", "Primer Apellido": "FEIJOO", "Segundo Apellido": "GAVILANES", "Teléfono": "PENDIENTE", "Fecha Alta": "01/10/2026"},
        {"Matrícula": "PEND-15", "Nombre": "DIEGO", "Primer Apellido": "GONZ", "Segundo Apellido": "", "Teléfono": "PENDIENTE", "Fecha Alta": "01/10/2026"},
        {"Matrícula": "PEND-16", "Nombre": "BRUNO", "Primer Apellido": "DORRIBO", "Segundo Apellido": "", "Teléfono": "PENDIENTE", "Fecha Alta": "01/10/2026"},
        {"Matrícula": "PEND-17", "Nombre": "DIEGO", "Primer Apellido": "CACHALDORA", "Segundo Apellido": "CARBALLO", "Teléfono": "PENDIENTE", "Fecha Alta": "01/10/2026"},
        {"Matrícula": "PEND-18", "Nombre": "EREA", "Primer Apellido": "MART", "Segundo Apellido": "FERNÁNDEZ", "Teléfono": "PENDIENTE", "Fecha Alta": "01/10/2026"},
        {"Matrícula": "PEND-19", "Nombre": "IAGO", "Primer Apellido": "GARC", "Segundo Apellido": "GONZ", "Teléfono": "PENDIENTE", "Fecha Alta": "01/10/2026"},
        {"Matrícula": "PEND-20", "Nombre": "MARCO", "Primer Apellido": "PALACIO", "Segundo Apellido": "LUENGOS", "Teléfono": "PENDIENTE", "Fecha Alta": "01/10/2026"},
        {"Matrícula": "PEND-21", "Nombre": "ADRIANA", "Primer Apellido": "BATAN", "Segundo Apellido": "", "Teléfono": "PENDIENTE", "Fecha Alta": "01/10/2026"},
        {"Matrícula": "PEND-22", "Nombre": "RODRIGO", "Primer Apellido": "TORRALBA", "Segundo Apellido": "PADR", "Teléfono": "PENDIENTE", "Fecha Alta": "01/10/2026"},
        {"Matrícula": "PEND-23", "Nombre": "ALEJANDRO", "Primer Apellido": "BARREIROS", "Segundo Apellido": "", "Teléfono": "PENDIENTE", "Fecha Alta": "01/10/2026"},
        {"Matrícula": "PEND-24", "Nombre": "ÁLVARO", "Primer Apellido": "BLANCO", "Segundo Apellido": "", "Teléfono": "PENDIENTE", "Fecha Alta": "01/10/2026"},
        {"Matrícula": "PEND-25", "Nombre": "BORJA", "Primer Apellido": "MARTIN", "Segundo Apellido": "", "Teléfono": "PENDIENTE", "Fecha Alta": "01/10/2026"},
        {"Matrícula": "PEND-26", "Nombre": "BORJA", "Primer Apellido": "LUCAS", "Segundo Apellido": "", "Teléfono": "PENDIENTE", "Fecha Alta": "01/10/2026"},
        {"Matrícula": "PEND-27", "Nombre": "PENAS", "Primer Apellido": "LORENZO", "Segundo Apellido": "", "Teléfono": "PENDIENTE", "Fecha Alta": "01/10/2026"},
        {"Matrícula": "PEND-28", "Nombre": "RAQUEL XING", "Primer Apellido": "SIN FICHA", "Segundo Apellido": "", "Teléfono": "PENDIENTE", "Fecha Alta": "01/10/2026"},
        {"Matrícula": "PEND-29", "Nombre": "AINHOA", "Primer Apellido": "ÁLVAREZ", "Segundo Apellido": "FERNÁNDEZ", "Teléfono": "PENDIENTE", "Fecha Alta": "01/10/2026"},
        {"Matrícula": "PEND-30", "Nombre": "JUAN", "Primer Apellido": "FERNÁNDEZ", "Segundo Apellido": "SEARA", "Teléfono": "PENDIENTE", "Fecha Alta": "01/10/2026"}
    ]

df_init = pd.DataFrame(obtener_alumnos_con_nuevos())
df_init.to_csv(DATA_FILE, index=False, encoding='utf-8-sig')
df_alumnos = pd.read_csv(DATA_FILE, dtype=str)

if not os.path.exists(REC_FILE):
    with open(REC_FILE, "w") as f:
        json.dump([], f)

with open(REC_FILE, "r") as f:
    recordatorios = json.load(f)

if not os.path.exists(PAGOS_FILE):
    pagos_init = {mat: True for mat in df_alumnos['Matrícula'].tolist()}
    with open(PAGOS_FILE, "w") as f:
        json.dump(pagos_init, f)

with open(PAGOS_FILE, "r") as f:
    estado_pagos = json.load(f)

if not os.path.exists(CAJA_FILE):
    caja_init = {"fondo_inicial": 0.0, "movimientos": []}
    with open(CAJA_FILE, "w") as f:
        json.dump(caja_init, f)

with open(CAJA_FILE, "r") as f:
    caja_data = json.load(f)

# ---------------------------------------------------------
# 3. BASE DE DATOS DE HORARIOS Y GRUPOS OFICIALES 2026
# ---------------------------------------------------------
def obtener_horarios_iniciales():
    return {
        "Doro": [
            {"Hora": "15:00-16:00", "Lunes": "-", "Martes": "Grupo 8 (Uxía, Carmen, Irene, Marcos)", "Miércoles": "-", "Jueves": "Grupo 8 (Uxía, Carmen, Irene, Marcos)", "Viernes": "-"},
            {"Hora": "16:00-17:00", "Lunes": "Grupo 11 (Tierno, Yoel, Tierno, Ainhoa)", "Martes": "Grupo 9 (Helena, Daniela, Manuel, Nico, Laura, Mauro, Alba, Marta, Myriam)", "Miércoles": "Grupo 15 (Luca, Valbuena, Jorge, Hugo, Casado, Marta, Martin, Alba, Ganni, Olaia)", "Jueves": "Grupo 9 (Helena, Daniela, Manuel, Nico, Laura, Mauro, Alba, Marta, Myriam)", "Viernes": "Grupo 15 (Luca, Valbuena, Jorge, Hugo, Casado, Marta, Martin, Alba, Ganni, Olaia)"},
            {"Hora": "17:00-18:00", "Lunes": "Doro (Jincheng, Cova, Candela, Carlota, Vera, Luana)", "Martes": "Grupo 13 (Luke, Luca, Alejandro Chao, Alejandro Serantes, Adriana Batan)", "Miércoles": "Grupo 16 (Alejandro, Álvaro, Borja Martin, Borja Lucas)", "Jueves": "Grupo 13 (Luke, Luca, Alejandro Chao, Alejandro Serantes, Adriana Batan)", "Viernes": "Grupo 16 (Alejandro, Álvaro, Borja Martin, Borja Lucas)"},
            {"Hora": "19:00-20:00", "Lunes": "Grupo 17 (Brais, Zoe, Fernanda, Vadillo, Adri, Zamora, Penas Lorenzo, Raquel Xing)", "Martes": "-", "Miércoles": "Grupo 17 (Brais, Zoe, Fernanda, Vadillo, Adri, Zamora, Penas Lorenzo, Raquel Xing)", "Jueves": "-", "Viernes": "-"}
        ],
        "Iza": [
            {"Hora": "17:00-18:00", "Lunes": "Grupo 1 (Hugo, Marco, Andrea, Cloe, Sara Calvo, Xian)", "Martes": "-", "Miércoles": "-", "Jueves": "Grupo 10 (Álvarez, Diego Gonz, Bruno Dorribo)", "Viernes": "-"},
            {"Hora": "18:00-19:00", "Lunes": "Grupo 4 (Estela, Alexandre, Aldara, Adrián, Ruth Cadah)", "Martes": "-", "Miércoles": "-", "Jueves": "Iza (Jincheng, Xinhui, Luana Xia)", "Viernes": "-"}
        ],
        "Ivan": [
            {"Hora": "17:00-18:00", "Lunes": "Grupo 2 (Luke, Xian, Alejandro Serantes, Javier Caneiro)", "Martes": "-", "Miércoles": "-", "Jueves": "Grupo 3 (Rodrigo, Maria, Andrea, Nerea, Alex, Sara, Zamora, Xuliana)", "Viernes": "-"},
            {"Hora": "18:00-19:00", "Lunes": "Grupo 3 (Rodrigo, Maria, Andrea, Nerea, Alex, Sara, Zamora, Xuliana)", "Martes": "Grupo 12 (Diego Cachaldora, Erea, Iago, Héctor, Izan, Emily, Marco)", "Miércoles": "-", "Jueves": "Grupo 12 (Diego Cachaldora, Erea, Iago, Héctor, Izan, Emily, Marco)", "Viernes": "-"},
            {"Hora": "19:00-20:00", "Lunes": "-", "Martes": "-", "Miércoles": "-", "Jueves": "Ivan (Beatriz, Ainhoa, Nerea, Juan Fernández)", "Viernes": "-"}
        ],
        "Ignacio": [
            {"Hora": "18:00-19:00", "Lunes": "-", "Martes": "-", "Miércoles": "Grupo 6 (Alba, Mara Dorribo, Bruno, Sara Pena, Vera)", "Jueves": "-", "Viernes": "-"}
        ],
        "Martha": [
            {"Hora": "16:00-17:00", "Lunes": "-", "Martes": "-", "Miércoles": "Grupo 14 (Álvaro, Sergio, Rodrigo Torralba, Alejandra, Olaia)", "Jueves": "-", "Viernes": "Grupo 14 (Álvaro, Sergio, Rodrigo Torralba, Alejandra, Olaia)"}
        ]
    }

if not os.path.exists(HORARIOS_FILE):
    with open(HORARIOS_FILE, "w", encoding="utf-8") as f:
        json.dump(obtener_horarios_iniciales(), f, ensure_ascii=False, indent=2)

with open(HORARIOS_FILE, "r", encoding="utf-8") as f:
    horarios = json.load(f)

# ---------------------------------------------------------
# 4. HEADER Y CONTADORES EN LA PORTADA
# ---------------------------------------------------------
st.markdown("""
    <div class='hero-box'>
        <div class='hero-title'>🇬🇧 Anthony's English School</div>
        <div class='hero-subtitle'>Portal Integrado - Diseñador de Anuncios y Gestión General</div>
    </div>
""", unsafe_allow_html=True)

# Cálculo de contadores
total_alumnos = len(df_alumnos)
alumnos_pendientes = len(df_alumnos[df_alumnos['Matrícula'].str.startswith('PEND-', na=False)])
alumnos_oficiales = total_alumnos - alumnos_pendientes

# Mostrar Tarjetas KPI en la Portada Principal
col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)
col_kpi1.markdown(f"<div class='kpi-card'><b>👨‍🎓 Total Alumnos Activos</b><br><h2 style='color:#1E3A8A; margin:0;'>{total_alumnos}</h2></div>", unsafe_allow_html=True)
col_kpi2.markdown(f"<div class='kpi-card'><b>✅ Matriculados con Ficha</b><br><h2 style='color:#16A34A; margin:0;'>{alumnos_oficiales}</h2></div>", unsafe_allow_html=True)
col_kpi3.markdown(f"<div class='kpi-card'><b>⏳ Pendientes de Ficha</b><br><h2 style='color:#EAB308; margin:0;'>{alumnos_pendientes}</h2></div>", unsafe_allow_html=True)
col_kpi4.markdown(f"<div class='kpi-card'><b>💰 Saldo Caja Hoy (Sincronizado)</b><br><h2 style='color:#2563EB; margin:0;'>{saldo_caja:.2f} €</h2></div>", unsafe_allow_html=True)

st.markdown("---")

with st.sidebar:
    try:
        st.image("logo.webp", width=180)
    except:
        st.write("🇬🇧 **Anthony's English School**")
    
    st.markdown("### 📌 Navegación")
    menu = st.radio(
        "",
        [
            "🏠 Buscador & Ficha Alumno",
            "📢 Diseñar Anuncio (Enviar a Telegram)",
            "📄 Enviar Formulario LOPD (WhatsApp)",
            "💵 Control de Caja Diario (Cloud)",
            "✅ Asistencia y Pagos",
            "📋 Lista Completa & Descargas",
            "🗓️ Horario de Profesores",
            "👥 Grupos de Clases",
            "🛠️ Editor (Bajas y Modificaciones)",
            "📌 Recordatorios Activos",
            "📢 Enviar Circular General"
        ]
    )

# ---------------------------------------------------------
# 5. BUSCADOR Y FICHA CON RECORDATORIOS
# ---------------------------------------------------------
if menu == "🏠 Buscador & Ficha Alumno":
    st.subheader("🔍 Buscador de Alumnos")
    busqueda = st.text_input("Ingresa Nombre, Apellido o Número de Matrícula:", placeholder="Ej: Alejandro, Shasha, 10741...")
    
    if busqueda:
        resultado = df_alumnos[
            df_alumnos['Nombre'].str.contains(busqueda, case=False, na=False) |
            df_alumnos['Primer Apellido'].str.contains(busqueda, case=False, na=False) |
            df_alumnos['Segundo Apellido'].str.contains(busqueda, case=False, na=False) |
            df_alumnos['Matrícula'].str.contains(busqueda, case=False, na=False)
        ]
        
        if len(resultado) > 0:
            st.success(f"Se han encontrado **{len(resultado)}** coincidencia(s):")
            for idx, row in resultado.iterrows():
                mat = str(row['Matrícula'])
                nombre_comp = f"{row['Nombre']} {row['Primer Apellido']} {row['Segundo Apellido']}".strip()
                telf = str(row['Teléfono']).replace(" ", "")
                
                link_llamada = f"tel:{telf}"
                link_wa = f"https://wa.me/34{telf}?text=Hola%20{row['Nombre']},%20te%20escribimos%20desde%20Anthony's%20English%20School:"
                
                with st.expander(f"👤 {nombre_comp} (Matrícula: {mat})", expanded=True):
                    st.markdown(f"📱 **Teléfono:** {telf} | 📅 **Alta:** {row['Fecha Alta']}")
                    
                    b_col1, b_col2 = st.columns(2)
                    b_col1.markdown(f'<a href="{link_llamada}" target="_blank" class="btn-action btn-call">📞 Llamar</a>', unsafe_allow_html=True)
                    b_col2.markdown(f'<a href="{link_wa}" target="_blank" class="btn-action btn-wa">💬 WhatsApp Directo</a>', unsafe_allow_html=True)
                    
                    st.markdown("---")
                    st.write("#### 📌 Programar Aviso Personalizado por Fecha y Hora")
                    
                    texto_rec = st.text_input("Tarea o aviso pendiente:", placeholder="Ej: Llamar a la madre de Juan", key=f"rec_{mat}")
                    col_f, col_h = st.columns(2)
                    fecha_aviso = col_f.date_input("📅 Fecha del aviso:", min_value=date.today(), key=f"f_{mat}")
                    hora_aviso = col_h.time_input("⏰ Hora del aviso:", value=time(17, 0), key=f"h_{mat}")
                    
                    if st.button("🔔 Confirmar Alerta Programada", key=f"btn_rec_{mat}"):
                        f_str = fecha_aviso.strftime("%d/%m/%Y")
                        h_str = hora_aviso.strftime("%H:%M")
                        mensaje_telegram = f"📌 *RECORDATORIO PROGRAMADO:*\n{texto_rec} del alumno/a *{nombre_comp}* a las {h_str} el {f_str}"
                        
                        nuevo_rec = {
                            "id": mat,
                            "alumno": nombre_comp,
                            "tarea": texto_rec,
                            "fecha_aviso": f_str,
                            "hora_aviso": h_str,
                            "creado": str(datetime.now().strftime("%d/%m/%Y %H:%M"))
                        }
                        recordatorios.append(nuevo_rec)
                        with open(REC_FILE, "w") as f:
                            json.dump(recordatorios, f)
                        
                        if enviar_notificacion_telegram(mensaje_telegram):
                            st.success("Alerta programada y enviada a Telegram ✅")
                        else:
                            st.error("Error al conectar con Telegram. Revisa la conexión.")
        else:
            st.warning("No se ha encontrado ningún alumno con ese término de búsqueda.")

# ---------------------------------------------------------
# 6. DISEÑADOR DE ANUNCIOS Y ENVÍO A TELEGRAM
# ---------------------------------------------------------
elif menu == "📢 Diseñar Anuncio (Enviar a Telegram)":
    st.subheader("📢 Diseñador de Anuncios y Ofertas")
    st.info("Crea el post de tu preferencia, adjunta la foto real de las instalaciones y recíbelo maquetado en tu Telegram listo para copiar a Instagram/Facebook.")

    col_crear, col_prev = st.columns([3, 2])

    with col_crear:
        st.write("#### ✏️ Elegir Plantilla o Redactar")
        
        plantilla_sel = st.selectbox(
            "Cargar plantilla basada en tus aulas e instalaciones:",
            [
                "Personalizada (Escribir desde cero)",
                "🔥 Plantilla 1: Últimos Huecos (Foto Oficina)",
                "🎓 Plantilla 2: Aulas Equipadas / Exámenes",
                "🇺🇸 Plantilla 3: Enfoque Práctico (Aula Route 66)",
                "🧸 Plantilla 4: Refuerzo Primaria y ESO"
            ]
        )
        
        texto_defecto = ""
        if plantilla_sel == "🔥 Plantilla 1: Últimos Huecos (Foto Oficina)":
            texto_defecto = "🔥 ¡ÚLTIMOS HUECOS DISPONIBLES EN ANTHONY'S ENGLISH SCHOOL! 🔥\n\n¿Buscas un centro de inglés moderno, cercano y donde realmente se aprenda?\n\nVen a conocer nuestras instalaciones y encuentra el grupo perfecto para ti o para tus hijos.\n\n📍 Grupos reducidos y atención personalizada.\n📲 ¡Escríbenos un WhatsApp al 609671976 y reserva tu prueba de nivel gratuita!"
        elif plantilla_sel == "🎓 Plantilla 2: Aulas Equipadas / Exámenes":
            texto_defecto = "🎓 PREPARA TU TÍTULO OFICIAL DE CAMBRIDGE (B1, B2, C1)\n\nEn Anthony's English School preparamos a nuestros alumnos en aulas adaptadas, cómodas y con la última tecnología.\n\n📚 Exámenes PET, FCE y Advanced\n🏫 Simulacros reales y material actualizado\n🗣️ Clases con profesores expertos\n\n📩 ¡Consúltanos horarios y reserva tu plaza!"
        elif plantilla_sel == "🇺🇸 Plantilla 3: Enfoque Práctico (Aula Route 66)":
            texto_defecto = "🇺🇸 ¡SUMÉRGETE EN EL INGLÉS SIN SALIR DE OURENSE!\n\nNo solo enseñamos gramática; creamos un entorno interactivo y estimulante para que hablar inglés sea natural.\n\n💡 Clases dinámicas con tecnología en el aula\n🗣️ Enfoque 100% práctico y conversacional\n🎯 Grupos específicos por niveles\n\n📲 ¡Pídenos información sin compromiso!"
        elif plantilla_sel == "🧸 Plantilla 4: Refuerzo Primaria y ESO":
            texto_defecto = "🧸 EL MEJOR REFUERZO ESCOLAR PARA LOS MÁS PEQUEÑOS\n\nAyudamos a tus hijos a ganar confianza con el inglés desde el primer día, en un ambiente divertido y acogedor.\n\n🏫 Apoyo para Primaria, ESO y Bachillerato\n👥 Grupos reducidos para una atención real\n📈 Seguimiento continuo e información a las familias\n\n📲 Contacta por WhatsApp al 609671976."

        texto_publicacion = st.text_area("Texto maquetado para el anuncio:", value=texto_defecto, height=200)
        imagen_subida = st.file_uploader("Adjuntar foto de la academia (Opcional):", type=["jpg", "png", "jpeg"])

        if st.button("📲 ENVIAR PUBLICACIÓN A MI TELEGRAM", type="primary"):
            if not texto_publicacion.strip():
                st.error("Por favor, escribe un texto antes de enviar la publicación.")
            else:
                exito = False
                if imagen_subida is not None:
                    foto_bytes = imagen_subida.getvalue()
                    exito = enviar_foto_telegram(foto_bytes, texto_publicacion)
                else:
                    exito = enviar_notificacion_telegram(texto_publicacion)
                
                if exito:
                    st.success("¡Anuncio enviado con éxito a tu Telegram! 📱 Abre Telegram, copia el texto y la foto y publícalo en tu Instagram o Facebook.")
                    st.balloons()
                else:
                    st.error("Hubo un problema al enviar el mensaje a Telegram. Verifica la conexión.")

    with col_prev:
        st.write("#### 📱 Vista Previa del Anuncio")
        
        st.markdown("<div class='preview-card'>", unsafe_allow_html=True)
        st.markdown("<b>🇬🇧 Anthony's English School</b> <small style='color:gray;'>• Vista Previa</small>", unsafe_allow_html=True)
        
        if imagen_subida is not None:
            st.image(imagen_subida, use_container_width=True)
        else:
            st.info("🖼️ Ninguna foto adjuntada. Se enviará solo el mensaje de texto.")
            
        if texto_publicacion:
            st.markdown(f"<p style='font-size:0.95rem; margin-top:10px;'>{texto_publicacion.replace(chr(10), '<br>')}</p>", unsafe_allow_html=True)
        else:
            st.caption("Escribe el texto a la izquierda para simular el anuncio...")
        st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# 7. ENVIAR FORMULARIO LOPD POR WHATSAPP
# ---------------------------------------------------------
elif menu == "📄 Enviar Formulario LOPD (WhatsApp)":
    st.subheader("📄 Autorización para el Tratamiento de Datos (LOPD / RGPD)")
    st.info("Envía el enlace al formulario digital de AYC ORENSE, S.L. a un alumno registrado o a una persona no guardada en la base de datos.")

    tipo_destinatario = st.radio(
        "Seleccionar Destinatario:",
        ["👤 Alumno Registrado en Base de Datos", "📱 Nuevo Contacto / No Registrado (Urgente)"]
    )

    telefono_destino = ""
    nombre_destinatario = ""

    if tipo_destinatario == "👤 Alumno Registrado en Base de Datos":
        alumno_sel = st.selectbox(
            "Selecciona el alumno:",
            df_alumnos['Matrícula'] + " - " + df_alumnos['Nombre'] + " " + df_alumnos['Primer Apellido']
        )
        if alumno_sel:
            mat_sel = alumno_sel.split(" - ")[0]
            idx_sel = df_alumnos[df_alumnos['Matrícula'] == mat_sel].index[0]
            nombre_destinatario = df_alumnos.at[idx_sel, 'Nombre']
            telefono_destino = str(df_alumnos.at[idx_sel, 'Teléfono']).replace(" ", "").replace("-", "")

    else:
        col_n1, col_n2 = st.columns(2)
        nombre_destinatario = col_n1.text_input("Nombre de la persona / tutor legal:", placeholder="Ej: Maria Perez")
        telefono_destino = col_n2.text_input("Número de Teléfono (móvil):", placeholder="Ej: 600123456")

    st.markdown("---")
    st.write("#### 📝 Enlace y Mensaje Oficial para WhatsApp")

    link_formulario = st.text_input(
        "Enlace del formulario / documento LOPD:",
        value="https://docs.google.com/document/d/1uGiLkQrsrpciaywvqVa0wa5zlg0GD59CbtXpfkTlLF0/edit?usp=sharing"
    )

    mensaje_plantilla = f"""Hola {nombre_destinatario if nombre_destinatario else ''}, te damos la bienvenida a *Anthony's English School* 🇬🇧.

Para cumplir con la normativa de Protección de Datos (RGPD) de AYC ORENSE, S.L., te solicitamos completar/revisar brevemente el formulario de autorización de tratamiento de datos desde tu teléfono (se completa en 1 minuto):

👇 *Haz clic en el enlace para acceder:*
{link_formulario}

¡Muchas gracias por tu colaboración!"""

    mensaje_editado = st.text_area("Mensaje que se enviará por WhatsApp:", value=mensaje_plantilla, height=180)

    if st.button("💬 Abrir WhatsApp y Enviar Formulario", type="primary"):
        tel_clean = ''.join(filter(str.isdigit, telefono_destino))
        
        if len(tel_clean) < 9:
            st.error("Por favor, introduce o selecciona un número de teléfono válido.")
        else:
            if not tel_clean.startswith("34") and len(tel_clean) == 9:
                tel_clean = "34" + tel_clean
            
            texto_encoded = urllib.parse.quote(mensaje_editado)
            wa_url = f"https://wa.me/{tel_clean}?text={texto_encoded}"
            
            st.success("¡Enlace generado con éxito!")
            st.markdown(
                f'<a href="{wa_url}" target="_blank" class="btn-action btn-wa" style="text-decoration:none; padding:12px; font-size:1.1rem;">📲 Hacer Clic Para Abrir WhatsApp</a>', 
                unsafe_allow_html=True
            )

# ---------------------------------------------------------
# 8. CONTROL DE CAJA DIARIO (SINCRONIZADO EN NUBE)
# ---------------------------------------------------------
elif menu == "💵 Control de Caja Diario (Cloud)":
    st.subheader("💵 Control Diario de Caja (Sincronizado en la Nube)")
    st.info("Todas las operaciones guardadas aquí se verán al instante tanto en tu teléfono como en el ordenador de la academia.")

    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(f"<div class='kpi-card'><b>🏦 Fondo Inicial:</b><br><h3 style='color:#2563EB;'>{caja_data.get('fondo_inicial', 0.0):.2f} €</h3></div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='kpi-card'><b>🟢 Entradas Hoy:</b><br><h3 style='color:#16A34A;'>+{total_entradas:.2f} €</h3></div>", unsafe_allow_html=True)
    c3.markdown(f"<div class='kpi-card'><b>🔴 Salidas / Gastos:</b><br><h3 style='color:#DC2626;'>-{total_salidas:.2f} €</h3></div>", unsafe_allow_html=True)
    c4.markdown(f"<div class='kpi-card'><b>💰 Saldo Actual en Caja:</b><br><h3 style='color:#1E3A8A;'>{saldo_caja:.2f} €</h3></div>", unsafe_allow_html=True)

    st.markdown("---")
    col_cj1, col_cj2 = st.columns(2)

    hoy_str = datetime.now().strftime("%d/%m/%Y")

    with col_cj1:
        st.write("#### ➕ / ➖ Registrar Movimiento de Efectivo")
        tipo_mov = st.selectbox("Tipo de Movimiento:", ["🟢 Entrada / Cobro en Efectivo", "🔴 Salida / Retiro de Dinero (Gasto)"])
        monto_mov = st.number_input("Importe (€):", min_value=0.01, value=10.00, step=1.0)
        motivo_mov = st.text_input("Motivo / Concepto del movimiento:", placeholder="Ej: Compra folios, Tinta impresora, Cobro cuota...")

        if st.button("💾 Guardar Movimiento en Caja", type="primary"):
            if not motivo_mov.strip():
                st.error("Por favor, especifica el motivo o concepto del movimiento.")
            else:
                tipo_final = "Entrada" if "Entrada" in tipo_mov else "Salida"
                hora_actual = datetime.now().strftime("%H:%M")
                
                nuevo_mov = {"fecha": hoy_str, "hora": hora_actual, "tipo": tipo_final, "monto": float(monto_mov), "motivo": motivo_mov.strip()}
                caja_data["movimientos"].append(nuevo_mov)
                with open(CAJA_FILE, "w") as f:
                    json.dump(caja_data, f, indent=2)
                
                enviar_notificacion_telegram(f"💵 *NUEVO MOVIMIENTO DE CAJA ({tipo_final.upper()}):*\nImporte: *{monto_mov:.2f} €*\nMotivo: {motivo_mov}\nFecha: {hoy_str} {hora_actual}")
                
                st.success(f"Movimiento de {monto_mov:.2f} € registrado correctamente ✅")
                st.markdown(f"🔗 [Abrir Tu Hoja en Google Sheets](https://docs.google.com/spreadsheets/d/{GSHEET_ID}/edit)")
                st.rerun()

    with col_cj2:
        st.write("#### ⚙️ Fondo Inicial de Caja")
        nuevo_fondo = st.number_input("Establecer nuevo Fondo Inicial (€):", min_value=0.0, value=float(caja_data.get('fondo_inicial', 0.0)), step=10.0)
        if st.button("🔄 Actualizar Fondo Inicial"):
            caja_data["fondo_inicial"] = float(nuevo_fondo)
            with open(CAJA_FILE, "w") as f:
                json.dump(caja_data, f, indent=2)
            st.success("Fondo inicial actualizado correctamente ✅")
            st.rerun()

    st.markdown("---")
    st.write("#### 📋 Historial de Movimientos & Descarga en Excel")

    if not df_caja_gsheet.empty:
        buffer_caja = io.BytesIO()
        df_caja_gsheet.to_csv(buffer_caja, index=False, sep=';', encoding='utf-8-sig')
        buffer_caja.seek(0)
        
        st.download_button(
            label="📥 Descargar Registro de Caja Completo (Para Filtrar por Semanas/Meses en Excel)",
            data=buffer_caja,
            file_name=f"Caja_Anthonys_School_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
        st.dataframe(df_caja_gsheet, use_container_width=True)
    else:
        st.info("Aún no hay movimientos registrados en la hoja de cálculo de Google Sheets.")

# ---------------------------------------------------------
# 9. CONTROL DE ASISTENCIA Y PAGOS
# ---------------------------------------------------------
elif menu == "✅ Asistencia y Pagos":
    st.subheader("✅ Control Diario de Asistencia y Gestión de Pagos")
    sub_tab1, sub_tab2 = st.tabs(["🔴 Registro de Faltas de Asistencia", "💳 Confirmación de Pagos (Verde por Defecto)"])
    
    with sub_tab1:
        st.write("#### Registrar Falta de Asistencia")
        col_as1, col_as2 = st.columns(2)
        fecha_falta = col_as1.date_input("Fecha de la falta:", value=date.today())
        alumno_falta_sel = col_as2.selectbox("Selecciona el alumno que ha faltado:", df_alumnos['Matrícula'] + " - " + df_alumnos['Nombre'] + " " + df_alumnos['Primer Apellido'])
        
        marca_falta = st.checkbox("❌ Marcar Falta de Asistencia")
        
        if st.button("💾 Guardar Falta y Crear Recordatorio Automatico"):
            if marca_falta and alumno_falta_sel:
                mat_f = alumno_falta_sel.split(" - ")[0]
                idx_f = df_alumnos[df_alumnos['Matrícula'] == mat_f].index[0]
                nom_f = f"{df_alumnos.at[idx_f, 'Nombre']} {df_alumnos.at[idx_f, 'Primer Apellido']}"
                f_str = fecha_falta.strftime("%d/%m/%Y")
                hora_actual = datetime.now().strftime("%H:%M")
                
                texto_tarea = f"Llamar a la familia por falta de asistencia el {f_str}"
                
                nuevo_rec = {
                    "id": mat_f,
                    "alumno": nom_f,
                    "tarea": texto_tarea,
                    "fecha_aviso": f_str,
                    "hora_aviso": hora_actual,
                    "creado": str(datetime.now().strftime("%d/%m/%Y %H:%M"))
                }
                recordatorios.append(nuevo_rec)
                with open(REC_FILE, "w") as f:
                    json.dump(recordatorios, f)
                
                msg_tele = f"📌 *RECORDATORIO AUTOMÁTICO (FALTA DE ASISTENCIA):*\nLlamar a la familia de *{nom_f}* por falta de asistencia el {f_str}."
                enviar_notificacion_telegram(msg_tele)
                st.success(f"Falta registrada y recordatorio generado para {nom_f} ✅")

    with sub_tab2:
        st.write("#### Estado Mensual de Pagos")
        st.info("Todos los alumnos están marcados en **Verde (Pagado)** por defecto. Desmarca la casilla solo si el pago no ha entrado.")
        
        alumno_pago_sel = st.selectbox("Buscar Alumno para revisar pago:", df_alumnos['Matrícula'] + " - " + df_alumnos['Nombre'] + " " + df_alumnos['Primer Apellido'])
        
        if alumno_pago_sel:
            mat_p = alumno_pago_sel.split(" - ")[0]
            idx_p = df_alumnos[df_alumnos['Matrícula'] == mat_p].index[0]
            nom_p = f"{df_alumnos.at[idx_p, 'Nombre']} {df_alumnos.at[idx_p, 'Primer Apellido']}"
            
            pago_ok = estado_pagos.get(mat_p, True)
            pago_check = st.checkbox("🟢 Pago Recibido / Confirmado", value=pago_ok)
            
            if pago_check != pago_ok:
                estado_pagos[mat_p] = pago_check
                with open(PAGOS_FILE, "w") as f:
                    json.dump(estado_pagos, f)
                
                if not pago_check:
                    texto_pago = f"Reclamar cuota mensual pendiente"
                    nuevo_rec = {
                        "id": mat_p,
                        "alumno": nom_p,
                        "tarea": texto_pago,
                        "fecha_aviso": datetime.now().strftime("%d/%m/%Y"),
                        "hora_aviso": datetime.now().strftime("%H:%M"),
                        "creado": str(datetime.now().strftime("%d/%m/%Y %H:%M"))
                    }
                    recordatorios.append(nuevo_rec)
                    with open(REC_FILE, "w") as f:
                        json.dump(recordatorios, f)
                    
                    enviar_notificacion_telegram(f"🔴 *ALERTA DE PAGO PENDIENTE:*\nEl alumno/a *{nom_p}* ha sido marcado con pago pendiente.")
                    st.error(f"El estado de {nom_p} ha cambiado a PENDIENTE DE PAGO. Se ha generado la alerta en Telegram.")
                else:
                    st.success(f"El estado de {nom_p} ha vuelto a PAGADO 🟢")

# ---------------------------------------------------------
# 10. LISTA COMPLETA Y DESCARGA EN EXCEL
# ---------------------------------------------------------
elif menu == "📋 Lista Completa & Descargas":
    st.subheader(f"📋 Registro Oficial de Alumnos ({len(df_alumnos)} Alumnos)")
    
    buffer_alumnos = io.BytesIO()
    df_alumnos.to_csv(buffer_alumnos, index=False, sep=';', encoding='utf-8-sig')
    buffer_alumnos.seek(0)
    
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        st.download_button(
            label="📥 Descargar Lista Completa (Excel / CSV Perfecto)",
            data=buffer_alumnos,
            file_name=f"Alumnos_Anthonys_School_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    
    st.dataframe(df_alumnos, height=350, use_container_width=True)
    
    st.markdown("---")
    st.subheader("🗓️️ Descargar Horarios de Profesores para Imprimir")
    
    prof_descarga = st.selectbox("Selecciona Profesor para exportar horario:", list(horarios.keys()))
    if prof_descarga in horarios:
        df_hor_descarga = pd.DataFrame(horarios[prof_descarga])
        
        buffer_horario = io.BytesIO()
        df_hor_descarga.to_csv(buffer_horario, index=False, sep=';', encoding='utf-8-sig')
        buffer_horario.seek(0)
        
        st.download_button(
            label=f"🖨️ Descargar Horario de {prof_descarga} (Listo para Imprimir)",
            data=buffer_horario,
            file_name=f"Horario_{prof_descarga}_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
        st.dataframe(df_hor_descarga, use_container_width=True)

# ---------------------------------------------------------
# 11. HORARIOS DE PROFESORES
# ---------------------------------------------------------
elif menu == "🗓️ Horario de Profesores":
    st.subheader("🗓️ Cuadrante Semanal de Profesores")
    profesor_sel = st.selectbox("Selecciona un Profesor:", list(horarios.keys()))
    
    if profesor_sel in horarios:
        df_horario = pd.DataFrame(horarios[profesor_sel])
        st.dataframe(df_horario, use_container_width=True, height=450)

# ---------------------------------------------------------
# 12. GRUPOS Y AULAS OFICIALES 2026
# ---------------------------------------------------------
elif menu == "👥 Grupos de Clases":
    st.subheader("🏫 Configuración Oficial de Grupos y Aulas")
    grupos_info = [
        {"Grupo": "Grupo Doro (L 17:00)", "Profesor": "Doro", "Horario": "17:00 - 18:00", "Días": "Lunes", "Aula": "CLASS C", "Alumnos": "Jincheng, Cova, Candela, Carlota, Vera, Luana Xia"},
        {"Grupo": "Grupo 1", "Profesor": "Iza", "Horario": "17:00 - 18:00", "Días": "Lunes", "Aula": "CLASS D", "Alumnos": "Hugo, Marco, Andrea, Cloe, Sara Calvo, Xian"},
        {"Grupo": "Grupo 2", "Profesor": "Ivan", "Horario": "17:00 - 18:00", "Días": "Lunes", "Aula": "CLASS A", "Alumnos": "Luke, Xian, Alejandro Serantes, Javier Caneiro"},
        {"Grupo": "Grupo 3", "Profesor": "Ivan", "Horario": "L 18:00 / J 17:00", "Días": "Lunes y Jueves", "Aula": "CLASS A", "Alumnos": "Rodrigo, Maria, Andrea, Nerea, Alex, Sara, Zamora, Xuliana"},
        {"Grupo": "Grupo 4", "Profesor": "Iza", "Horario": "18:00 - 19:00", "Días": "Lunes", "Aula": "CLASS D", "Alumnos": "Estela, Alexandre, Aldara, Adrián, Ruth Cadah"},
        {"Grupo": "Grupo 6", "Profesor": "Ignacio", "Horario": "18:00 - 19:00", "Días": "Miércoles", "Aula": "CLASS B", "Alumnos": "Alba, Mara Dorribo, Bruno, Sara Pena, Vera"},
        {"Grupo": "Grupo 8", "Profesor": "Doro", "Horario": "15:00 - 16:00", "Días": "Martes y Jueves", "Aula": "CLASS A", "Alumnos": "Uxía, Carmen, Irene, Marcos"},
        {"Grupo": "Grupo 9", "Profesor": "Doro", "Horario": "16:00 - 17:00", "Días": "Martes y Jueves", "Aula": "CLASS A", "Alumnos": "Helena, Daniela, Manuel, Nico, Laura, Mauro, Alba, Marta, Myriam"},
        {"Grupo": "Grupo 10", "Profesor": "Iza", "Horario": "18:00 - 19:00", "Días": "Jueves", "Aula": "CLASS C", "Alumnos": "Álvarez, Diego Gonz, Bruno Dorribo"},
        {"Grupo": "Grupo 11", "Profesor": "Doro", "Horario": "16:00 - 17:00", "Días": "Lunes", "Aula": "CLASS A", "Alumnos": "Tierno, Yoel, Tierno, Ainhoa"},
        {"Grupo": "Grupo 12", "Profesor": "Ivan", "Horario": "18:00 - 19:00", "Días": "Martes y Jueves", "Aula": "CLASS A", "Alumnos": "Diego Cachaldora, Erea, Iago, Héctor, Izan, Emily, Marco"},
        {"Grupo": "Grupo 13", "Profesor": "Doro", "Horario": "17:00 - 18:00", "Días": "Martes y Jueves", "Aula": "CLASS D", "Alumnos": "Luke, Luca, Alejandro Chao, Alejandro Serantes, Adriana Batan"},
        {"Grupo": "Grupo 14", "Profesor": "Martha", "Horario": "16:00 - 17:00", "Días": "Miércoles y Viernes", "Aula": "CLASS D", "Alumnos": "Álvaro, Sergio, Rodrigo Torralba, Alejandra, Olaia"},
        {"Grupo": "Grupo 15", "Profesor": "Doro", "Horario": "16:00 - 17:00", "Días": "Miércoles y Viernes", "Aula": "CLASS A", "Alumnos": "Luca, Valbuena, Jorge, Hugo, Casado, Marta, Martin, Alba, Ganni, Olaia"},
        {"Grupo": "Grupo 16", "Profesor": "Doro", "Horario": "17:00 - 18:00", "Días": "Miércoles y Viernes", "Aula": "CLASS A", "Alumnos": "Alejandro, Álvaro, Borja Martin, Borja Lucas"},
        {"Grupo": "Grupo 17", "Profesor": "Doro", "Horario": "19:00 - 20:00", "Días": "Lunes y Miércoles", "Aula": "CLASS A", "Alumnos": "Brais, Zoe, Fernanda, Vadillo, Adri, Zamora, Penas Lorenzo, Raquel Xing"},
        {"Grupo": "Grupo Ivan Jueves", "Profesor": "Ivan", "Horario": "19:00 - 20:00", "Días": "Jueves", "Aula": "CLASS A", "Alumnos": "Beatriz, Ainhoa, Nerea, Juan Fernández"},
        {"Grupo": "Grupo Iza Jueves", "Profesor": "Iza", "Horario": "18:00 - 19:00", "Días": "Jueves", "Aula": "CLASS C", "Alumnos": "Jincheng, Xinhui, Luana Xia"}
    ]
    st.dataframe(pd.DataFrame(grupos_info), use_container_width=True)

# ---------------------------------------------------------
# 13. EDITOR COMPLETO (BAJAS Y MODIFICACIONES)
# ---------------------------------------------------------
elif menu == "🛠️ Editor (Bajas y Modificaciones)":
    st.subheader("🛠️ Panel de Modificación y Dar de Baja")
    pestana = st.tabs(["👨‍🎓 Gestión de Alumnos (Editar / Dar de Baja)", "🗓️ Modificar Horarios"])
    
    with pestana[0]:
        opcion_ed = st.radio("Acción:", ["➕ Añadir Nuevo Alumno", "✏️ Editar Alumno Existente", "❌ Dar de Baja / Eliminar Alumno"])
        
        if opcion_ed == "➕ Añadir Nuevo Alumno":
            with st.form("form_nuevo"):
                n_mat = st.text_input("Número de Matrícula:")
                n_nom = st.text_input("Nombre:")
                n_ap1 = st.text_input("Primer Apellido:")
                n_ap2 = st.text_input("Segundo Apellido:")
                n_tel = st.text_input("Teléfono móvil:")
                btn_guardar = st.form_submit_button("💾 Guardar Alumno")
                
                if btn_guardar:
                    nueva_fila = {"Matrícula": n_mat, "Nombre": n_nom.upper(), "Primer Apellido": n_ap1.upper(), "Segundo Apellido": n_ap2.upper(), "Teléfono": n_tel, "Fecha Alta": datetime.now().strftime("%d/%m/%Y")}
                    df_alumnos = pd.concat([df_alumnos, pd.DataFrame([nueva_fila])], ignore_index=True)
                    df_alumnos.to_csv(DATA_FILE, index=False, encoding='utf-8-sig')
                    
                    estado_pagos[n_mat] = True
                    with open(PAGOS_FILE, "w") as f:
                        json.dump(estado_pagos, f)
                        
                    st.success(f"Alumno {n_nom} registrado correctamente ✅")
                    st.rerun()

        elif opcion_ed == "✏️ Editar Alumno Existente":
            sel_alum = st.selectbox("Selecciona alumno a editar:", df_alumnos['Matrícula'] + " - " + df_alumnos['Nombre'] + " " + df_alumnos['Primer Apellido'])
            if sel_alum:
                mat_sel = sel_alum.split(" - ")[0]
                idx_alum = df_alumnos[df_alumnos['Matrícula'] == mat_sel].index[0]
                
                with st.form("form_edit"):
                    e_nom = st.text_input("Nombre:", value=df_alumnos.at[idx_alum, 'Nombre'])
                    e_ap1 = st.text_input("Primer Apellido:", value=df_alumnos.at[idx_alum, 'Primer Apellido'])
                    e_tel = st.text_input("Teléfono:", value=df_alumnos.at[idx_alum, 'Teléfono'])
                    btn_mod = st.form_submit_button("🔄 Actualizar Datos")
                    
                    if btn_mod:
                        df_alumnos.at[idx_alum, 'Nombre'] = e_nom.upper()
                        df_alumnos.at[idx_alum, 'Primer Apellido'] = e_ap1.upper()
                        df_alumnos.at[idx_alum, 'Teléfono'] = e_tel
                        df_alumnos.to_csv(DATA_FILE, index=False, encoding='utf-8-sig')
                        st.success("Datos actualizados correctamente ✅")
                        st.rerun()

        elif opcion_ed == "❌ Dar de Baja / Eliminar Alumno":
            sel_baja = st.selectbox("Selecciona alumno que se da de BAJA:", df_alumnos['Matrícula'] + " - " + df_alumnos['Nombre'] + " " + df_alumnos['Primer Apellido'])
            if sel_baja:
                mat_baja = sel_baja.split(" - ")[0]
                idx_baja = df_alumnos[df_alumnos['Matrícula'] == mat_baja].index[0]
                nom_baja = f"{df_alumnos.at[idx_baja, 'Nombre']} {df_alumnos.at[idx_baja, 'Primer Apellido']}"
                
                st.warning(f"⚠️ ¿Estás seguro de que quieres dar de baja a **{nom_baja}** (Matrícula: {mat_baja})?")
                if st.button("❌ Confirmar Baja Definitiva"):
                    df_alumnos = df_alumnos.drop(idx_baja).reset_index(drop=True)
                    df_alumnos.to_csv(DATA_FILE, index=False, encoding='utf-8-sig')
                    st.error(f"El alumno {nom_baja} ha sido dado de baja correctamente ✅")
                    st.rerun()

    with pestana[1]:
        st.write("#### ✏️ Modificar Cuadrante de Clases")
        prof_edit = st.selectbox("Selecciona Profesor a editar:", list(horarios.keys()), key="prof_edit_sel")
        
        if prof_edit:
            df_prof = pd.DataFrame(horarios[prof_edit])
            franja_sel = st.selectbox("Selecciona la Franja Horaria:", df_prof['Hora'].tolist())
            dia_sel = st.selectbox("Selecciona el Día de la Semana:", ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"])
            
            idx_franja = df_prof[df_prof['Hora'] == franja_sel].index[0]
            val_actual = df_prof.at[idx_franja, dia_sel]
            
            nuevo_valor_clase = st.text_input(f"Clase/Alumno asignado para el {dia_sel} a las {franja_sel}:", value=val_actual)
            
            if st.button("💾 Guardar Cambio en el Horario"):
                horarios[prof_edit][idx_franja][dia_sel] = nuevo_valor_clase
                with open(HORARIOS_FILE, "w", encoding="utf-8") as f:
                    json.dump(horarios, f, ensure_ascii=False, indent=2)
                st.success(f"¡Horario de {prof_edit} actualizado con éxito! ✅")
                st.rerun()

# ---------------------------------------------------------
# 14. RECORDATORIOS PROGRAMADOS Y CIRCULARES
# ---------------------------------------------------------
elif menu == "📌 Recordatorios Activos":
    st.subheader("📌 Agenda de Alertas Programadas")
    if len(recordatorios) == 0:
        st.info("No hay recordatorios programados en este momento.")
    else:
        for idx, rec in enumerate(recordatorios):
            col_rec1, col_rec2 = st.columns([4, 1])
            f_txt = rec.get('fecha_aviso', 'Pendiente')
            h_txt = rec.get('hora_aviso', '')
            col_rec1.warning(f"📌 **{rec['tarea']}** — 👤 *{rec['alumno']}* \n📅 **Programado para:** {h_txt} el {f_txt}")
            
            if col_rec2.button("✅ Marcar como Resuelto", key=f"del_rec_{idx}"):
                recordatorios.pop(idx)
                with open(REC_FILE, "w") as f:
                    json.dump(recordatorios, f)
                enviar_notificacion_telegram(f"✅ *RECORDATORIO RESUELTO*\n\nSe ha completado el aviso programado del alumno *{rec['alumno']}*.")
                st.rerun()

elif menu == "📢 Enviar Circular General":
    st.subheader("📢 Envío Masivo por WhatsApp")
    txt_circ = st.text_area("Mensaje institucional:", "Estimadas familias de Anthony's English School...")
    if txt_circ:
        encoded = urllib.parse.quote(txt_circ)
        for idx, row in df_alumnos.head(15).iterrows():
            st.markdown(f"👤 **{row['Nombre']} {row['Primer Apellido']}** — <a href='https://wa.me/34{row['Teléfono']}?text={encoded}' target='_blank'>💬 Enviar WhatsApp</a>", unsafe_allow_html=True)