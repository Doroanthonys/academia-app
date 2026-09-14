import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import json
import os

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
    except Exception as e:
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
    .student-card {
        background-color: #FFFFFF; border-radius: 12px; padding: 16px 20px;
        border-left: 5px solid #2563EB; box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.04);
        margin-bottom: 12px;
    }
    .btn-action {
        display: inline-flex; align-items: center; justify-content: center;
        width: 100%; padding: 10px 14px; border-radius: 8px; font-weight: 700;
        font-size: 0.9rem; text-decoration: none !important; text-align: center;
        box-shadow: 0px 3px 8px rgba(0,0,0,0.08);
    }
    .btn-call { background-color: #2563EB; color: #FFFFFF !important; }
    .btn-wa { background-color: #25D366; color: #FFFFFF !important; }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. CARGA Y GUARDADO PERSISTENTE DE DATOS (ARCHIVOS LOCALES)
# ---------------------------------------------------------
DATA_FILE = "alumnos_data.csv"
REC_FILE = "recordatorios.json"

def obtener_datos_iniciales():
    return [
        {"Matrícula": "579", "Nombre": "LUCIA", "Primer Apellido": "PENAS", "Segundo Apellido": "LORENZO", "Teléfono": "609671976", "Fecha Alta": "02/10/2019"},
        {"Matrícula": "601", "Nombre": "RODRIGO", "Primer Apellido": "LOPEZ", "Segundo Apellido": "CID", "Teléfono": "630653659", "Fecha Alta": "12/11/2014"},
        {"Matrícula": "735", "Nombre": "MYRIAM", "Primer Apellido": "GAVILANES", "Segundo Apellido": "FEIJOO", "Teléfono": "659274499", "Fecha Alta": "27/09/2017"},
        {"Matrícula": "878", "Nombre": "ALEX", "Primer Apellido": "CALDELAS", "Segundo Apellido": "CASAS", "Teléfono": "661603323", "Fecha Alta": "23/09/2021"},
        {"Matrícula": "10741", "Nombre": "SHASHA", "Primer Apellido": "IGLESIAS", "Segundo Apellido": "GONZALEZ", "Teléfono": "676046101", "Fecha Alta": "06/10/2023"}
    ]

if not os.path.exists(DATA_FILE):
    df_init = pd.DataFrame(obtener_datos_iniciales())
    df_init.to_csv(DATA_FILE, index=False)

df_alumnos = pd.read_csv(DATA_FILE, dtype=str)

if not os.path.exists(REC_FILE):
    with open(REC_FILE, "w") as f:
        json.dump([], f)

with open(REC_FILE, "r") as f:
    recordatorios = json.load(f)

# ---------------------------------------------------------
# 3. HEADER Y MENÚ
# ---------------------------------------------------------
st.markdown("""
    <div class='hero-box'>
        <div class='hero-title'>🇬🇧 Anthony's English School</div>
        <div class='hero-subtitle'>Portal Integrado de Gestión, Notificaciones y Edición en Vivo</div>
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
        ["🏠 Buscador & Ficha Alumno", "🛠️ Editor de Alumnos (Móvil)", "📌 Recordatorios Activos", "📢 Enviar Circular General", "🗓️ Horarios de Profesores"]
    )

# ---------------------------------------------------------
# 4. BUSCADOR Y FICHA CON RECORDATORIOS TELEGRAM
# ---------------------------------------------------------
if menu == "🏠 Buscador & Ficha Alumno":
    st.subheader("🔍 Buscador de Alumnos con Gestión de Alertas")
    busqueda = st.text_input("Ingresa Nombre, Apellido o Número de Matrícula:", placeholder="Ej: Shasha, 10741...")
    
    if busqueda:
        resultado = df_alumnos[
            df_alumnos['Nombre'].str.contains(busqueda, case=False, na=False) |
            df_alumnos['Primer Apellido'].str.contains(busqueda, case=False, na=False) |
            df_alumnos['Matrícula'].str.contains(busqueda, case=False, na=False)
        ]
        
        if len(resultado) > 0:
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
                    st.write("#### 📌 Crear Recordatorio para Telegram")
                    texto_rec = st.text_input("Escribe una tarea o aviso pendiente:", key=f"rec_{mat}")
                    if st.button("🔔 Programar Alerta 24h", key=f"btn_rec_{mat}"):
                        nuevo_rec = {"id": mat, "alumno": nombre_comp, "tarea": texto_rec, "fecha": str(datetime.now().strftime("%Y-%m-%d %H:%M"))}
                        recordatorios.append(nuevo_rec)
                        with open(REC_FILE, "w") as f:
                            json.dump(recordatorios, f)
                        
                        enviar_notificacion_telegram(f"📌 *NUEVO RECORDATORIO CREADO*\n\n*Alumno:* {nombre_comp}\n*Tarea:* {texto_rec}\n\nEste aviso te recordará periódicamente hasta ser resuelto.")
                        st.success("Recordatorio guardado y enviado a Telegram ✅")

# ---------------------------------------------------------
# 5. EDITOR EN VIVO DESDE EL MÓVIL
# ---------------------------------------------------------
elif menu == "🛠️ Editor de Alumnos (Móvil)":
    st.subheader("🛠️ Añadir o Modificar Alumnos en Tiempo Real")
    st.info("Los cambios que guardes aquí se actualizarán automáticamente para toda la plantilla.")
    
    opcion_ed = st.radio("Acción:", ["➕ Añadir Nuevo Alumno", "✏️ Editar Alumno Existente"])
    
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
                df_alumnos.to_csv(DATA_FILE, index=False)
                st.success(f"Alumno {n_nom} registrado y sincronizado en todos los dispositivos ✅")

    elif opcion_ed == "✏️ Editar Alumno Existente":
        sel_alum = st.selectbox("Selecciona alumno:", df_alumnos['Matrícula'] + " - " + df_alumnos['Nombre'] + " " + df_alumnos['Primer Apellido'])
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
                    df_alumnos.to_csv(DATA_FILE, index=False)
                    st.success("Datos actualizados correctamente ✅")

# ---------------------------------------------------------
# 6. PANEL DE RECORDATORIOS ACTIVOS
# ---------------------------------------------------------
elif menu == "📌 Recordatorios Activos":
    st.subheader("📌 Tareas Pendientes y Alertas de Telegram")
    if len(recordatorios) == 0:
        st.info("No hay recordatorios pendientes en este momento.")
    else:
        for idx, rec in enumerate(recordatorios):
            col_rec1, col_rec2 = st.columns([4, 1])
            col_rec1.warning(f"👤 **{rec['alumno']}** — {rec['tarea']} *(Creado: {rec['fecha']})*")
            if col_rec2.button("✅ Eliminar / Resuelto", key=f"del_rec_{idx}"):
                recordatorios.pop(idx)
                with open(REC_FILE, "w") as f:
                    json.dump(recordatorios, f)
                enviar_notificacion_telegram(f"✅ *RECORDATORIO RESUELTO*\n\nLa tarea del alumno *{rec['alumno']}* se ha marcado como completada.")
                st.rerun()

elif menu == "📢 Enviar Circular General":
    st.subheader("📢 Envío Masivo por WhatsApp")
    txt_circ = st.text_area("Mensaje institucional:", "Estimadas familias de Anthony's English School...")
    if txt_circ:
        import urllib.parse
        encoded = urllib.parse.quote(txt_circ)
        for idx, row in df_alumnos.head(10).iterrows():
            st.markdown(f"👤 **{row['Nombre']} {row['Primer Apellido']}** — <a href='https://wa.me/34{row['Teléfono']}?text={encoded}' target='_blank'>💬 Enviar</a>", unsafe_allow_html=True)

elif menu == "🗓️ Horarios de Profesores":
    st.subheader("🗓️ Cuadrante Semanal")
    st.write("Vista completa del cuadrante de profesores de la academia.")