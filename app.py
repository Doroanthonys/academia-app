import streamlit as st
import pandas as pd

# ---------------------------------------------------------
# 1. CONFIGURACIÓN DE PÁGINA Y TEMA VISUAL PREMIUM
# ---------------------------------------------------------
st.set_page_config(
    page_title="Anthony's English School",
    page_icon="🇬🇧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS Personalizados (Diseño Elegante y Moderno)
st.markdown("""
    <style>
    /* Fondo general */
    .stApp {
        background-color: #F8FAFC;
    }
    
    /* Hero Header */
    .hero-box {
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
        padding: 22px;
        border-radius: 16px;
        color: white;
        text-align: center;
        box-shadow: 0px 8px 20px rgba(30, 58, 138, 0.15);
        margin-bottom: 20px;
    }
    .hero-title {
        font-size: 2.1rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .hero-subtitle {
        font-size: 1rem;
        opacity: 0.9;
        margin-top: 4px;
    }

    /* Tarjetas de Alumno */
    .student-card {
        background-color: #FFFFFF;
        border-radius: 12px;
        padding: 16px 20px;
        border-left: 5px solid #2563EB;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.04);
        margin-bottom: 12px;
    }

    /* Botones Interactivos de Llamada y WhatsApp */
    .btn-action {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 100%;
        padding: 10px 14px;
        border-radius: 8px;
        font-weight: 700;
        font-size: 0.9rem;
        text-decoration: none !important;
        text-align: center;
        box-shadow: 0px 3px 8px rgba(0,0,0,0.08);
        transition: all 0.2s ease;
    }
    .btn-call {
        background-color: #2563EB;
        color: #FFFFFF !important;
    }
    .btn-wa {
        background-color: #25D366;
        color: #FFFFFF !important;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. BASE DE DATOS DE ALUMNOS (102 Alumnos Oficiales)
# ---------------------------------------------------------
@st.cache_data
def cargar_alumnos():
    data = [
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
        {"Matrícula": "21173", "Nombre": "PALOMA", "Primer Apellido": "UGARTE", "Segundo Apellido": "GARCIA", "Teléfono": "673525726", "Fecha Alta": "04/06/2026"}
    ]
    return pd.DataFrame(data)

df_alumnos = cargar_alumnos()

# Horarios de Profesores
horarios = {
    "Doro": [
        {"Hora": "15:00 - 16:00", "Lunes": "-", "Martes": "Mama vera (online)", "Miércoles": "Iria Cibeiro (C-1)", "Jueves": "Grupo 4ºeso (C-1)", "Viernes": "Brais"},
        {"Hora": "16:00 - 17:00", "Lunes": "Marcos de la Iglesia (b-2)", "Martes": "Grupo 4ºeso (C-1)", "Miércoles": "Brais / Mauro Mendez (4ºeso marista)", "Jueves": "Grupo 1º/2ºeso (b-1)", "Viernes": "Cesar menor / Grupo 1º/2ºeso (b-1)"},
        {"Hora": "17:00 - 18:00", "Lunes": "Grupo 1º/2º", "Martes": "Sofia hija sonia", "Miércoles": "Grupo 1º/2ºeso (b-2)", "Jueves": "Felix Vadillo (4ºeso Miraflores b-2)", "Viernes": "Grupo 1º/2ºeso (b-2)"},
        {"Hora": "18:00 - 19:00", "Lunes": "Grupo 4º", "Martes": "Felix Vadillo (4ºeso Miraflores b-2)", "Miércoles": "Beatriz Alva. / Adriana Vieria (1ºb C-1)", "Jueves": "Grupo 6º/1ºeso", "Viernes": "-"},
        {"Hora": "19:00 - 20:00", "Lunes": "C1", "Martes": "-", "Miércoles": "Grupo C-1 (4ºeso/1ºb)", "Jueves": "-", "Viernes": "-"}
    ],
    "Iria": [
        {"Hora": "10:00 - 11:00", "Lunes": "-", "Martes": "Natalia Santas (Tr-7 online)", "Miércoles": "-", "Jueves": "Natalia Santas (Tr-7 online)", "Viernes": "-"},
        {"Hora": "11:00 - 12:00", "Lunes": "-", "Martes": "Lara", "Miércoles": "-", "Jueves": "Javier Carballo", "Viernes": "-"},
        {"Hora": "12:00 - 13:00", "Lunes": "-", "Martes": "Javier Carballo", "Miércoles": "-", "Jueves": "-", "Viernes": "-"},
        {"Hora": "16:00 - 17:00", "Lunes": "Irati A2 5 PRI / Samuel 1º BACH B2", "Martes": "Alba Medela (2ºeso josefinas)", "Miércoles": "Andre & Martin (2ºeso lagunas b-1)", "Jueves": "-", "Viernes": "-"},
        {"Hora": "17:00 - 18:00", "Lunes": "-", "Martes": "Begoña Gomez (adult) / Alvaro Gomez (1ºb lagunas)", "Miércoles": "Alberto Novoa (1ºb marista C-1)", "Jueves": "-", "Viernes": "-"},
        {"Hora": "18:00 - 19:00", "Lunes": "-", "Martes": "Grupo 4º/5º / Luis Uruburu (3ºeso)", "Miércoles": "-", "Jueves": "Hugo da Costa (1ºb C-1)", "Viernes": "-"},
        {"Hora": "19:00 - 20:00", "Lunes": "-", "Martes": "Jimena (4º Padre Feijoo)", "Miércoles": "Luis Uruburu (3ºeso)", "Jueves": "-", "Viernes": "-"},
        {"Hora": "20:00 - 21:00", "Lunes": "-", "Martes": "Alejandro Su. / Noe Rivero (4ºeso b-1 / 1ºb marista)", "Miércoles": "-", "Jueves": "Sasha Iglesias (5º josefinas)", "Viernes": "-"}
    ],
    "Isa": [
        {"Hora": "10:00 - 11:00", "Lunes": "-", "Martes": "Agustina", "Miércoles": "Agustina", "Jueves": "-", "Viernes": "Alex y Adri (2ºeso maristas)"},
        {"Hora": "14:00 - 15:00", "Lunes": "-", "Martes": "Lucia Carneiro", "Miércoles": "Lucia Carneiro", "Jueves": "-", "Viernes": "-"},
        {"Hora": "15:00 - 16:00", "Lunes": "-", "Martes": "Alex y Adri / Iraia", "Miércoles": "-", "Jueves": "Daniela online (1º bach)", "Viernes": "-"},
        {"Hora": "16:00 - 17:00", "Lunes": "-", "Martes": "Anxo y Marcos / Javier o grupo", "Miércoles": "Pablo Med. (2ºb marista)", "Jueves": "Xiana y Xoel (1ºeso maristas b-1)", "Viernes": "-"},
        {"Hora": "17:00 - 18:00", "Lunes": "Grupo 3º", "Martes": "Iñaki Merelles (b-2 Dic)", "Miércoles": "Iñaki Merelles (b-2 Dic)", "Jueves": "-", "Viernes": "Sofia carmelitas (b2)"},
        {"Hora": "18:00 - 19:00", "Lunes": "Grupo 6º/1ºeso", "Martes": "Manuel Palomo / Alejandro Nesp.", "Miércoles": "Grupo 2º/3º", "Jueves": "Ada (1ºb Otero)", "Viernes": "-"},
        {"Hora": "19:00 - 20:00", "Lunes": "Eva Vilavoy", "Martes": "Antonio Quintas / Borja Lorenzo (3ºeso)", "Miércoles": "Antonio Quintas (3ºeso)", "Jueves": "-", "Viernes": "-"},
        {"Hora": "20:00 - 21:00", "Lunes": "-", "Martes": "Miguel Anxo (b-2)", "Miércoles": "-", "Jueves": "-", "Viernes": "-"},
        {"Hora": "21:00 - 22:00", "Lunes": "-", "Martes": "Miguel Anxo (b-2)", "Miércoles": "Ana Fdez", "Jueves": "-", "Viernes": "-"}
    ],
    "Ivan": [
        {"Hora": "12:00 - 13:00", "Lunes": "-", "Martes": "-", "Miércoles": "Emilio", "Jueves": "-", "Viernes": "-"},
        {"Hora": "14:00 - 15:00", "Lunes": "-", "Martes": "Emilio (online)", "Miércoles": "-", "Jueves": "-", "Viernes": "-"},
        {"Hora": "15:00 - 16:00", "Lunes": "-", "Martes": "Lucas Alv. / Alvaro Folla (1ºb maristas)", "Miércoles": "Marc Pacreu (1ºb C-1 cole)", "Jueves": "Paula Gomez (1ºeso)", "Viernes": "-"},
        {"Hora": "16:00 - 17:00", "Lunes": "Hugo Vila (online)", "Martes": "-", "Miércoles": "Mario Sarmiento (4ºeso marista)", "Jueves": "Alvaro Garcia (3ºeso marista b-1)", "Viernes": "-"},
        {"Hora": "17:00 - 18:00", "Lunes": "Grupo 5º/6º", "Martes": "Blanca Garcia / Grupo 4º/5º", "Miércoles": "Pablo, Dunia, Carlota", "Jueves": "Grupo 2º/3ºeso / Grupo 4º/5º", "Viernes": "-"},
        {"Hora": "18:00 - 19:00", "Lunes": "Grupo 2º/3ºeso", "Martes": "-", "Miércoles": "-", "Jueves": "-", "Viernes": "-"},
        {"Hora": "19:00 - 20:00", "Lunes": "Xurxo (1ºeso) / Anxo (3ºeso)", "Martes": "Grupo 1º/2ºb", "Miércoles": "Alfonso Alvarez", "Jueves": "Grupo 1º/2ºb", "Viernes": "-"},
        {"Hora": "20:00 - 21:00", "Lunes": "-", "Martes": "Sarela Rua (3ºeso lagunas)", "Miércoles": "Alvaro Guzman (b2 dic)", "Jueves": "Sarela Rua (3ºeso lagunas)", "Viernes": "-"}
    ]
}

# ---------------------------------------------------------
# 3. ENCABEZADO Y MENÚ DE NAVEGACIÓN
# ---------------------------------------------------------
st.markdown("""
    <div class='hero-box'>
        <div class='hero-title'>🇬🇧 Anthony's English School</div>
        <div class='hero-subtitle'>Portal Integrado de Gestión de Alumnos, Horarios y Contacto Directo</div>
    </div>
""", unsafe_allow_html=True)

# Barra Lateral (Sidebar)
with st.sidebar:
    try:
        st.image("logo.webp", width=180)
    except:
        st.write("🇬🇧 **Anthony's English School**")
    
    st.markdown("### 📌 Navegación")
    menu = st.radio(
        "",
        ["🏠 Inicio & Buscador", "👨‍🎓 Directorio de Alumnos", "🗓️ Horario de Profesores", "👥 Grupos de Clases"]
    )

# ---------------------------------------------------------
# 4. PANTALLA 1: INICIO & BUSCADOR CON BOTONES DE ACCIÓN
# ---------------------------------------------------------
if menu == "🏠 Inicio & Buscador":
    st.subheader("📊 Resumen General de la Academia")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Alumnos Totales", len(df_alumnos))
    c2.metric("Profesores Activos", len(horarios))
    c3.metric("Grupos de Clase", "20")
    c4.metric("Estado del Sistema", "En línea ✅")

    st.markdown("---")
    st.subheader("🔍 Buscador de Alumnos con Contacto Directo")
    busqueda = st.text_input("Ingresa Nombre, Apellido o Número de Matrícula:", placeholder="Ej: Shasha, 10741, Perez...")
    
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
                nombre_comp = f"{row['Nombre']} {row['Primer Apellido']} {row['Segundo Apellido']}".strip()
                telf = str(row['Teléfono']).replace(" ", "")
                
                # Creación de enlaces interactivos
                link_llamada = f"tel:{telf}"
                link_wa = f"https://wa.me/34{telf}?text=Hola%20{row['Nombre']},%20te%20escribimos%20desde%20Anthony's%20English%20School:"
                
                with st.container():
                    st.markdown(f"""
                        <div class='student-card'>
                            <div style='font-size: 1.15rem; font-weight: 700; color: #1E3A8A;'>👤 {nombre_comp}</div>
                            <div style='color: #64748B; font-size: 0.9rem; margin-top:2px;'>
                                🆔 <b>Matrícula:</b> {row['Matrícula']} &nbsp;|&nbsp; 📱 <b>Teléfono:</b> {telf} &nbsp;|&nbsp; 📅 <b>Alta:</b> {row['Fecha Alta']}
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    b_col1, b_col2 = st.columns(2)
                    with b_col1:
                        st.markdown(f'<a href="{link_llamada}" target="_blank" class="btn-action btn-call">📞 Llamar al Alumno</a>', unsafe_allow_html=True)
                    with b_col2:
                        st.markdown(f'<a href="{link_wa}" target="_blank" class="btn-action btn-wa">💬 Enviar WhatsApp Directo</a>', unsafe_allow_html=True)
                    st.write("")
        else:
            st.warning("No se ha encontrado ningún alumno con ese término de búsqueda.")

# ---------------------------------------------------------
# 5. PANTALLA 2: DIRECTORIO COMPLETO DE ALUMNOS
# ---------------------------------------------------------
elif menu == "👨‍🎓 Directorio de Alumnos":
    st.subheader("📋 Listado Oficial de Alumnos (102 Alumnos)")
    
    col_f1, col_f2 = st.columns([3, 1])
    with col_f1:
        filtro = st.text_input("Filtrar lista de alumnos:")
    
    if filtro:
        df_mostrar = df_alumnos[
            df_alumnos['Nombre'].str.contains(filtro, case=False, na=False) |
            df_alumnos['Primer Apellido'].str.contains(filtro, case=False, na=False) |
            df_alumnos['Segundo Apellido'].str.contains(filtro, case=False, na=False)
        ]
    else:
        df_mostrar = df_alumnos

    st.dataframe(df_mostrar, height=450, use_container_width=True)

# ---------------------------------------------------------
# 6. PANTALLA 3: HORARIOS DE PROFESORES
# ---------------------------------------------------------
elif menu == "🗓️ Horario de Profesores":
    st.subheader("🗓️ Cuadrante Semanal de Profesores")
    profesor_sel = st.selectbox("Selecciona un Profesor:", ["Doro", "Iria", "Isa", "Ivan"])
    
    if profesor_sel in horarios:
        df_horario = pd.DataFrame(horarios[profesor_sel])
        st.dataframe(df_horario, use_container_width=True, height=400)

# ---------------------------------------------------------
# 7. PANTALLA 4: GRUPOS Y AULAS
# ---------------------------------------------------------
elif menu == "👥 Grupos de Clases":
    st.subheader("🏫 Configuración de Grupos y Aulas")
    grupos_info = [
        {"Grupo": "Grupo 0", "Profesor": "Doro", "Horario": "17:00 a 18:00", "Días": "Lunes", "Aula": "CLASS C"},
        {"Grupo": "Grupo 1", "Profesor": "Iza", "Horario": "17:00 a 18:00", "Días": "Lunes", "Aula": "CLASS D"},
        {"Grupo": "Grupo 2", "Profesor": "Ivan", "Horario": "17:00 a 18:00", "Días": "Lunes", "Aula": "CLASS A"},
        {"Grupo": "Grupo 3", "Profesor": "Ivan", "Horario": "Lun 18:00 / Jue 17:00", "Días": "Lunes y Jueves", "Aula": "CLASS A"},
        {"Grupo": "Grupo 4", "Profesor": "Iza", "Horario": "18:00 a 19:00", "Días": "Lunes", "Aula": "CLASS D"},
        {"Grupo": "Grupo 5", "Profesor": "Doro", "Horario": "18:00 a 19:00", "Días": "Lunes", "Aula": "CLASS C"},
        {"Grupo": "Grupo 6", "Profesor": "Eve", "Horario": "18:00 a 19:00", "Días": "Miércoles", "Aula": "CLASS B"},
        {"Grupo": "Grupo 7", "Profesor": "Doro", "Horario": "15:00 a 16:00", "Días": "Viernes", "Aula": "CLASS A"},
        {"Grupo": "Grupo 8", "Profesor": "Doro", "Horario": "15:00 a 16:00", "Días": "Martes y Jueves", "Aula": "CLASS A"},
        {"Grupo": "Grupo 9", "Profesor": "Doro", "Horario": "16:00 a 17:00", "Días": "Martes y Jueves", "Aula": "CLASS A"}
    ]
    st.dataframe(pd.DataFrame(grupos_info), use_container_width=True)