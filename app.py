# CÓDIGO ACTUALIZADO PARA LA DESCARGA LIMPIA EN EXCEL / CSV

elif menu == "📋 Lista Completa & Descargas":
    st.subheader(f"📋 Registro Oficial de Alumnos ({len(df_alumnos)} Alumnos)")
    
    # 1. Exportación optimizada de Alumnos para Excel (UTF-8 con BOM)
    buffer_alumnos = io.BytesIO()
    df_alumnos.to_csv(buffer_alumnos, index=False, sep=';', encoding='utf-8-sig')
    buffer_alumnos.seek(0)
    
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        st.download_button(
            label="📥 Descargar Alumnos (Excel / CSV Perfecto)",
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
        
        # 2. Exportación optimizada de Horarios (evita caracteres raros como MiÃ©rcoles o 4ºeso)
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