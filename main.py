import pandas as pd
import streamlit as st
from analisis import datos, crear_grafico_torta, crear_grafico_promedios, calcular_disponibilidad


def obt_cont(bmc_dfs):
    conteos = {}
    for i, df in enumerate(bmc_dfs, start=1):
        for j in range(1, 8):
            clave = f"cont{j}_{i}"
            conteos[clave] = df[f"cont_{j}"].max()
    return conteos


def obt_acums(bmc_dfs):
    acumulado={}
    for i, df in enumerate(bmc_dfs, start=1):
        for j in range(1, 8):
            clave = f"acum{j}_{i}"
            acumulado[clave] = df[f"acum_{j}"].max()
    return acumulado

# Configurar estilo de página ------------------------------------------------------------------------------------------
st.set_page_config(page_title="Disponibilidad", layout="wide", )

st.image('./imagenes/IOT_COMPLETO.jpg')
st.divider()
st.markdown("<h1 style='text-align: center; color: #101255;'>Disponibilidad</h1>", unsafe_allow_html=True)
st.divider()

#Creacion de interfaz ------------------------------------------------

tab1, tab2, tab3, tab4 = st.tabs(["Todo","BMC","CDI","BDT"])

with tab1:
    st.title("Graficas totales")


with tab2:
    st.title("Graficas de BMC")
    bmc1,bmc2,bmc3,bmc4,bmc5 = datos()# llena los dataframes

    dfs = [bmc1, bmc2, bmc3,bmc4,bmc5]
    conteos=obt_cont(dfs)
    acumulado=obt_acums(dfs)
    st.plotly_chart(crear_grafico_torta(conteos))
    st.plotly_chart(crear_grafico_promedios(conteos,acumulado))

    bmc_opciones = [
        "bmc1", "bmc2", "bmc3", "bmc4", "bmc5", "bmc6",
        "bmc7", "bmc8", "bmc9", "bmc10", "bmc11", "bmc12"
    ]
    bmc_dict ={
        "bmc1":bmc1,
        "bmc2":bmc2,
        "bmc3":bmc3,
        "bmc4":bmc4,
        "bmc5":bmc5,
    }


    if "dfs" not in st.session_state:
        st.session_state["dfs"] = {}

    col1,col2 = st.columns(2)

    with col1:
        seleccion = st.selectbox(
            "Selecciona el bmc que quiere visualizar:",
            bmc_opciones
        )
    if seleccion not in st.session_state["dfs"]:
        st.session_state["dfs"][seleccion] = True
    if seleccion in bmc_dict:
        df = bmc_dict[seleccion]
        if df.empty:
            st.warning(f"{seleccion} está vacío.")
        else:
            st.dataframe(df, column_order=["timestamp","acum_1", "cont_1", "acum_2", "cont_2", "acum_3", "cont_3",
                                           "acum_4", "cont_4", "acum_5", "cont_5", "acum_6", "cont_6",
                                           "acum_7", "cont_7"])


    else:
        st.info("No hay ni chimbo pa mostrar.")
        calcular_disponibilidad(bmc1)





with tab3:
    st.title("Graficas de CDI")

with tab4:
    st.title("Graficas de BDT")
