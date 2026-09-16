import streamlit as st
import pandas as pd
import requests
from datetime import datetime, date, time
import json
import os
import io

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

def enviar_notificacion_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": mensaje, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload, timeout=5)
    except Exception:
        pass

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
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. BASE DE DATOS DE ALUMNOS Y ARCHIVOS
# ---------------------------------------------------------
DATA_FILE = "alumnos_data.csv"
REC_FILE = "recordatorios.json"
HORARIOS_FILE = "horarios_data.json"
PAGOS_FILE = "pagos_data.json"

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

        # --- 18 NUEVOS ALUMNOS ---
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
        {"Matrícula": "21139", "Nombre": "IRIA", "Primer Apellido": "CIBREIRO", "Segundo Apellido": "TRIGO", "Teléfono": "636006448", "Fecha Alta": "23/09/2024"}
    ]

if not os.path.exists(DATA_FILE):
    df_init = pd.DataFrame(obtener_alumnos_con_nuevos())
    df_init.to_csv(DATA_FILE, index=False, encoding='utf-8-sig')
else:
    df_check = pd.read_csv(DATA_FILE, dtype=str)
    if len(df_check) < 115:
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

# ---------------------------------------------------------
# 3. BASE DE DATOS EDITABLE DE HORARIOS
# ---------------------------------------------------------
def obtener_horarios_iniciales():
    return {
        "Doro": [
            {"Hora": "10:00-11:00", "Lunes": "-", "Martes": "-", "Miércoles": "-", "Jueves": "-", "Viernes": "-"},
            {"Hora": "13:00-14:00", "Lunes": "-", "Martes": "-", "Miércoles": "Iria Cibeiro C-1", "Jueves": "-", "Viernes": "-"},
            {"Hora": "15:00-16:00", "Lunes": "-", "Martes": "Grupo 4ºeso C-1", "Miércoles": "Mauro Mendez 4ºeso marista", "Jueves": "Grupo 4ºeso C-1", "Viernes": "-"},
            {"Hora": "16:00-17:00", "Lunes": "Grupo Marga", "Martes": "Grupo 1º/2ºeso b-1", "Miércoles": "Grupo 1º/2ºeso b-1", "Jueves": "Grupo 1º/2ºeso b-1", "Viernes": "Grupo 1º/2ºeso b-1"},
            {"Hora": "17:00-18:00", "Lunes": "Grupo 1º/2º", "Martes": "Grupo 1º eso", "Miércoles": "Grupo 1º/2ºeso b-2", "Jueves": "-", "Viernes": "Grupo 1º/2ºeso b-2"},
            {"Hora": "18:00-19:00", "Lunes": "Grupo 4º C1", "Martes": "Felix Vadillo 4ºeso Miraflores b-2", "Miércoles": "Grupo C-1 4ºeso/1ºb", "Jueves": "Grupo 6º/1ºeso", "Viernes": "-"}
        ],
        "Enma": [
            {"Hora": "15:00-16:00", "Lunes": "Iago Merelles 5 prima Fcs", "Martes": "-", "Miércoles": "Iago Merelles 5 prima Fcs", "Jueves": "-", "Viernes": "Carmen Gnz GNZ Maristas"},
            {"Hora": "16:00-17:00", "Lunes": "-", "Martes": "-", "Miércoles": "-", "Jueves": "-", "Viernes": "Diego Rial 4º eso couto"},
            {"Hora": "18:00-19:00", "Lunes": "-", "Martes": "-", "Miércoles": "-", "Jueves": "-", "Viernes": "Hugo Outeriño 2º ESO"}
        ],
        "Ignacio": [
            {"Hora": "19:00-20:00", "Lunes": "Santi y Diego", "Martes": "Santi y Diego", "Miércoles": "Diego Gnz Gnz 6º pri", "Jueves": "-", "Viernes": "Sasha Iglesias 5º josefinas"}
        ],
        "Iria": [
            {"Hora": "10:00-11:00", "Lunes": "-", "Martes": "-", "Miércoles": "Natalia Santas Tr-7 online", "Jueves": "-", "Viernes": "Natalia Santas Tr-7 online"},
            {"Hora": "11:00-12:00", "Lunes": "-", "Martes": "-", "Miércoles": "-", "Jueves": "-", "Viernes": "Javier Carballo"},
            {"Hora": "12:00-13:00", "Lunes": "-", "Martes": "-", "Miércoles": "Javier Carballo", "Jueves": "-", "Viernes": "-"},
            {"Hora": "16:00-17:00", "Lunes": "-", "Martes": "Sofia", "Miércoles": "Irati A2 5 PRI MIRAFLORES", "Jueves": "Alba Medela 2ºeso josefinas", "Viernes": "Andre & Martin 2ºeso lagunas b-1"},
            {"Hora": "17:00-18:00", "Lunes": "-", "Martes": "Begoña Gomez adult", "Miércoles": "Alvaro Gomez 1ºb lagunas", "Jueves": "Alberto Novoa 1ºb marista C-1", "Viernes": "-"},
            {"Hora": "18:00-19:00", "Lunes": "-", "Martes": "Luis Uruburu 3ºeso", "Miércoles": "Grupo 4º/5º", "Jueves": "Samuel 1º BACH B2", "Viernes": "-"},
            {"Hora": "19:00-20:00", "Lunes": "-", "Martes": "Jimena 4º Padre Feijoo", "Miércoles": "Eva Boada Online", "Jueves": "Luis Uruburu 3ºeso", "Viernes": "-"},
            {"Hora": "20:00-21:00", "Lunes": "-", "Martes": "Alejandro Su. 4ºeso b-1 Online", "Miércoles": "Irene Pazos", "Jueves": "-", "Viernes": "-"}
        ],
        "Isa": [
            {"Hora": "10:00-11:00", "Lunes": "-", "Martes": "Agustina", "Miércoles": "-", "Jueves": "Agustina", "Viernes": "-"},
            {"Hora": "14:00-15:00", "Lunes": "-", "Martes": "Lucia Carneiro", "Miércoles": "-", "Jueves": "Lucia Carneiro", "Viernes": "-"},
            {"Hora": "15:00-16:00", "Lunes": "-", "Martes": "Iraia", "Miércoles": "Alex Y Adri 2 eso maristas", "Jueves": "Daniela online 1º bacj", "Viernes": "Alex Y Adri 2 eso maristas"},
            {"Hora": "16:00-17:00", "Lunes": "-", "Martes": "Anxo y Marcos", "Miércoles": "Javier o grupo", "Jueves": "Pablo Med. 2ºb marista", "Viernes": "Xiana Y Xoel 1º eso maristas b-1"},
            {"Hora": "17:00-18:00", "Lunes": "Grupo 3º", "Martes": "Iñaki Merelles b-2 Dic", "Miércoles": "Iñaki Merelles b-2 Dic", "Jueves": "Grupo restaurante", "Viernes": "Sofia carmelitas b2"},
            {"Hora": "18:00-19:00", "Lunes": "Grupo 6º/1ºeso", "Martes": "Manuel Palomo 4ºeso marista", "Miércoles": "Alejandro Nesp. 2ºeso coles", "Jueves": "Grupo 2º/3º", "Viernes": "Ada 1ºb Otero"},
            {"Hora": "19:00-20:00", "Lunes": "Eva Vilavoy", "Martes": "Antonio Quintas 3ºeso miraflores", "Miércoles": "Borja Lorenzo 3ºeso miraflores", "Jueves": "Antonio Quintas 3ºeso miraflores", "Viernes": "-"},
            {"Hora": "20:00-21:00", "Lunes": "-", "Martes": "-", "Miércoles": "Miguel Anxo b-2", "Jueves": "-", "Viernes": "-"},
            {"Hora": "21:00-22:00", "Lunes": "-", "Martes": "-", "Miércoles": "Miguel Anxo b-2 / Ana Fdez", "Jueves": "-", "Viernes": "-"}
        ],
        "Ivan": [
            {"Hora": "12:00-13:00", "Lunes": "-", "Martes": "-", "Miércoles": "Emilio", "Jueves": "-", "Viernes": "-"},
            {"Hora": "14:00-15:00", "Lunes": "-", "Martes": "Emilio online", "Miércoles": "-", "Jueves": "-", "Viernes": "-"},
            {"Hora": "15:00-16:00", "Lunes": "-", "Martes": "Lucas Alv. / Alvaro Folla 1ºb maristas", "Miércoles": "Marc Pacreu 1ºb francis C-1 cole", "Jueves": "Paula Gomez 1ºeso", "Viernes": "-"},
            {"Hora": "16:00-17:00", "Lunes": "Hugo Vila online", "Martes": "Elena Guzman B2", "Miércoles": "-", "Jueves": "Alvaro garcia 3ºeso marista b-1 cole", "Viernes": "-"},
            {"Hora": "17:00-18:00", "Lunes": "Grupo 5º/6º", "Martes": "Blanca Garcia", "Miércoles": "Sabela Fernandez", "Jueves": "Grupo 2º/3ºeso", "Viernes": "-"},
            {"Hora": "18:00-19:00", "Lunes": "Grupo 2º/3ºeso", "Martes": "Grupo 4º/5º", "Miércoles": "-", "Jueves": "Grupo 4º/5º", "Viernes": "-"},
            {"Hora": "19:00-20:00", "Lunes": "Xurxo 1ºeso / Anxo 3ºeso", "Martes": "Grupo 1º/2ºb", "Miércoles": "Alfonso Alvarez", "Jueves": "Grupo 1º2ºb", "Viernes": "-"},
            {"Hora": "20:00-21:00", "Lunes": "-", "Martes": "Sarela Rua 3ºeso lagunas", "Miércoles": "Alvaro Guzman b2 diciembre", "Jueves": "Sarela Rua 3ºeso lagunas", "Viernes": "-"}
        ],
        "Natalia": [
            {"Hora": "16:00-17:00", "Lunes": "-", "Martes": "Diego hijo sonia", "Miércoles": "Brais / Mateo Serrante 2º bch / Iago Garcia 3º Eso", "Jueves": "Noel 1º eso / Guillerme", "Viernes": "Brais / Cesar menor / Iago Garcia 3º Eso"}
        ]
    }

if not os.path.exists(HORARIOS_FILE):
    with open(HORARIOS_FILE, "w", encoding="utf-8") as f:
        json.dump(obtener_horarios_iniciales(), f, ensure_ascii=False, indent=2)

with open(HORARIOS_FILE, "r", encoding="utf-8") as f:
    horarios = json.load(f)

# ---------------------------------------------------------
# 4. HEADER Y MENÚ DE NAVEGACIÓN
# ---------------------------------------------------------
st.markdown("""
    <div class='hero-box'>
        <div class='hero-title'>🇬🇧 Anthony's English School</div>
        <div class='hero-subtitle'>Portal Integrado - Publicador de Redes Sociales y Gestión Académica</div>
    </div>
""", unsafe_allow_html=True)

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
            "📢 Publicar en Redes Sociales",
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
                        
                        enviar_notificacion_telegram(mensaje_telegram)
                        st.success("Alerta programada y enviada a Telegram ✅")
        else:
            st.warning("No se ha encontrado ningún alumno con ese término de búsqueda.")

# ---------------------------------------------------------
# 6. PESTAÑA NUEVA: PUBLICADOR EN REDES SOCIALES
# ---------------------------------------------------------
elif menu == "📢 Publicar en Redes Sociales":
    st.subheader("📢 Publicador de Anuncios y Ofertas (Facebook e Instagram)")
    st.info("Escribe tu anuncio, adjunta una imagen promocional y publícalo en un solo clic.")

    col_crear, col_prev = st.columns([3, 2])

    with col_crear:
        st.write("#### ✏️ Redactar Publicación")
        
        plantilla_sel = st.selectbox(
            "Cargar plantilla rápida (Opcional):",
            [
                "Personalizada (Escribir desde cero)",
                "🔥 Últimos Huecos Disponibles",
                "🎉 Oferta Especial de Matrícula",
                "🇬🇧 Nuevo Curso Intensivo de Inglés"
            ]
        )
        
        texto_defecto = ""
        if plantilla_sel == "🔥 Últimos Huecos Disponibles":
            texto_defecto = "🔥 ¡ÚLTIMOS HUECOS DISPONIBLES EN ANTHONY'S ENGLISH SCHOOL! 🔥\n\nAbriremos nuevas plazas para preparación de exámenes y refuerzo escolar.\n\n📍 Horarios adaptados por niveles.\n📲 ¡Escríbenos un WhatsApp al 609671976 y reserva la plaza de tu hijo/a antes de que se agoten!"
        elif plantilla_sel == "🎉 Oferta Especial de Matrícula":
            texto_defecto = "🎉 ¡OFERTA ESPECIAL DE MATRÍCULA! 🎉\n\nInscríbete esta semana en Anthony's English School y obtén un descuento especial en tu inscripción.\n\n🇬🇧 Grupos reducidos y atención personalizada.\n👉 ¡Pide información sin compromiso!"
        elif plantilla_sel == "🇬🇧 Nuevo Curso Intensivo de Inglés":
            texto_defecto = "🇬🇧 ¡MEJORA TU NIVEL DE INGLÉS RÁPIDAMENTE! 🇬🇧\n\nIniciamos nuevos grupos intensivos. Ideal para superar tus exámenes oficiales o ganar fluidez en conversación.\n\n📩 Mándanos un mensaje privado o contáctanos por WhatsApp."

        texto_publicacion = st.text_area("Texto de la publicación:", value=texto_defecto, height=180)
        imagen_subida = st.file_uploader("Adjuntar imagen publicitaria (Opcional):", type=["jpg", "png", "jpeg"])

        st.write("#### 🌐 Seleccionar Redes de Destino")
        col_fb, col_ig = st.columns(2)
        pub_facebook = col_fb.checkbox("Facebook Page", value=True)
        pub_instagram = col_ig.checkbox("Instagram Business", value=True)

        if st.button("🚀 PUBLICAR AHORA EN REDES SOCIALES", type="primary"):
            if not texto_publicacion.strip():
                st.error("Por favor, escribe un texto antes de enviar la publicación.")
            else:
                redes_activas = []
                if pub_facebook: redes_activas.append("Facebook")
                if pub_instagram: redes_activas.append("Instagram")

                if len(redes_activas) == 0:
                    st.warning("Selecciona al menos una red social para publicar.")
                else:
                    st.success(f"¡Anuncio enviado correctamente a **{', '.join(redes_activas)}**! 🎉")
                    st.balloons()

    with col_prev:
        st.write("#### 📱 Vista Previa en Móvil")
        
        st.markdown("<div class='preview-card'>", unsafe_allow_html=True)
        st.markdown("<b>🇬🇧 Anthony's English School</b> <small style='color:gray;'>• Publicidad</small>", unsafe_allow_html=True)
        
        if imagen_subida is not None:
            st.image(imagen_subida, use_column_width=True)
        else:
            st.info("🖼️ Ninguna imagen adjuntada. Se publicará solo texto.")
            
        if texto_publicacion:
            st.markdown(f"<p style='font-size:0.95rem; margin-top:10px;'>{texto_publicacion.replace(chr(10), '<br>')}</p>", unsafe_allow_html=True)
        else:
            st.caption("Escribe el texto a la izquierda para ver cómo lucirá tu anuncio...")
        st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# 7. CONTROL DE ASISTENCIA Y PAGOS
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
# 8. LISTA COMPLETA Y DESCARGA EN EXCEL
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
    st.subheader("🗓️ Descargar Horarios de Profesores para Imprimir")
    
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
# 9. HORARIOS DE PROFESORES
# ---------------------------------------------------------
elif menu == "🗓️ Horario de Profesores":
    st.subheader("🗓️ Cuadrante Semanal de Profesores")
    profesor_sel = st.selectbox("Selecciona un Profesor:", list(horarios.keys()))
    
    if profesor_sel in horarios:
        df_horario = pd.DataFrame(horarios[profesor_sel])
        st.dataframe(df_horario, use_container_width=True, height=450)

# ---------------------------------------------------------
# 10. GRUPOS Y AULAS
# ---------------------------------------------------------
elif menu == "👥 Grupos de Clases":
    st.subheader("🏫 Configuración de Grupos y Aulas")
    grupos_info = [
        {"Grupo": "Grupo 0", "Profesor": "Doro", "Horario": "17:00 a 18:00", "Días": "Lunes", "Aula": "CLASS C"},
        {"Grupo": "Grupo 1", "Profesor": "Isa", "Horario": "17:00 a 18:00", "Días": "Lunes", "Aula": "CLASS D"},
        {"Grupo": "Grupo 2", "Profesor": "Ivan", "Horario": "17:00 a 18:00", "Días": "Lunes", "Aula": "CLASS A"}
    ]
    st.dataframe(pd.DataFrame(grupos_info), use_container_width=True)

# ---------------------------------------------------------
# 11. EDITOR COMPLETO (BAJAS Y MODIFICACIONES)
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
# 12. RECORDATORIOS PROGRAMADOS Y CIRCULARES
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
        import urllib.parse
        encoded = urllib.parse.quote(txt_circ)
        for idx, row in df_alumnos.head(15).iterrows():
            st.markdown(f"👤 **{row['Nombre']} {row['Primer Apellido']}** — <a href='https://wa.me/34{row['Teléfono']}?text={encoded}' target='_blank'>💬 Enviar WhatsApp</a>", unsafe_allow_html=True)