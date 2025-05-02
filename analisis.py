import os
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots




def verificar_archivo(ruta):
    if not os.path.exists(ruta):
        print(f"Error: El archivo {ruta} no existe.")
    else:
        print(f"Archivo encontrado: {ruta}")

def datos():
    # Definir la ruta base
    try:
        BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    except NameError:  # Si estás en un notebook
        BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    ruta_bmc1 = os.path.join(BASE_DIR, "BMC", "paros_simulados_acumulados_1.csv")
    ruta_bmc2 = os.path.join(BASE_DIR, "BMC", "paros_simulados_acumulados_2.csv")
    ruta_bmc3 = os.path.join(BASE_DIR, "BMC", "paros_simulados_acumulados_3.csv")
    ruta_bmc4 = os.path.join(BASE_DIR, "BMC", "paros_simulados_acumulados_4.csv")
    ruta_bmc5 = os.path.join(BASE_DIR, "BMC", "paros_simulados_acumulados_5.csv")

    # Verificar si los archivos existen


    for ruta in [ruta_bmc1, ruta_bmc2, ruta_bmc3,ruta_bmc4,ruta_bmc5]:
        verificar_archivo(ruta)

    # Cargar los archivos en DataFrames
    bmc1 = pd.read_csv(ruta_bmc1)
    bmc2 = pd.read_csv(ruta_bmc2)
    bmc3 = pd.read_csv(ruta_bmc3)
    bmc4 = pd.read_csv(ruta_bmc4)
    bmc5 = pd.read_csv(ruta_bmc5)


    return bmc1,bmc2,bmc3,bmc4,bmc5


def crear_grafico_torta(conteos):
    # Agrupar por tipo de paro (cont_1 a cont_7)
    sumas_por_tipo = {}
    for j in range(1, 8):
        tipo_paro = f"cont_{j}"
        # Sumar todos los máximos de este tipo para todas las máquinas
        suma = sum(valor for clave, valor in conteos.items() if clave.startswith(f"cont{j}_"))
        sumas_por_tipo[tipo_paro] = suma

    # Nombres descriptivos para los tipos de paro (puedes modificarlos según tus datos reales)
    nombres_paros = {
        "cont_1": "Averias",
        "cont_2": "Mantenimiento",
        "cont_3": "Lavado o cambio de moldes",
        "cont_4": "Ausencia de operario",
        "cont_5": "Maquina no programada para produccion",
        "cont_6": "Servicios(Falta de agua ,aire ...)",
        "cont_7": "Procesos que impidan el inicio"
    }

    # Preparar datos para el gráfico
    tipos = list(sumas_por_tipo.keys())
    valores = list(sumas_por_tipo.values())
    etiquetas = [nombres_paros[tipo] for tipo in tipos]

    # Crear el gráfico de torta con Plotly Go
    fig = go.Figure(data=[go.Pie(
        labels=etiquetas,
        values=valores,
        hole=.2,
        textinfo='label+percent',
        insidetextorientation='radial',
        marker_colors=['#FF9999', '#66B2FF', '#99FF99', '#FFCC99', '#FF99CC', '#9999FF', '#CCFF99']
    )])

    # Personalizar el diseño
    fig.update_layout(
        title_text="Distribución de Tipos de Paro",
        title_font_size=20,
        legend_title="Tipos de Paro",
        height=600,
        width=800
    )
    fig.update_traces(hoverinfo='value+label', textinfo='label+percent',
                      marker=dict(line=dict(color='#000000', width=2)))

    return fig



def numero_fallas(conteo):
    pass



def obtener_maximos(bmc_dfs):
    conteos = {}
    for i, df in enumerate(bmc_dfs, start=1):
        for j in range(1, 8):  # cont_1 a cont_7
            clave = f"cont{j}_{i}"
            conteos[clave] = df[f"cont_{j}"].max()
    return conteos


def obt_acums(bmc_dfs):
    acumulado = {}
    for i, df in enumerate(bmc_dfs, start=1):
        for j in range(1, 8):
            clave = f"acum{j}_{i}"
            acumulado[clave] = df[f"acum_{j}"].max()
    return acumulado

def obt_acum(df):
    acumulado = {}
    for j in range(1, 8):
        clave = f"acum{j}"
        acumulado[clave] = df[f"acum_{j}"].max()
    return acumulado


def crear_grafico_promedios(conteos, acumulados):
    # Calcular los promedios por tipo
    promedios_por_tipo = {}

    for j in range(1, 8):
        # Inicializar listas para guardar conteos y acumulados de este tipo
        conteos_tipo = []
        acumulados_tipo = []

        # Recolectar todos los valores para este tipo de paro
        for i in range(1, len(conteos) // 7 + 1):  # Asumiendo que hay datos para todas las máquinas
            clave_cont = f"cont{j}_{i}"
            clave_acum = f"acum{j}_{i}"

            if clave_cont in conteos and clave_acum in acumulados:
                cont_valor = conteos[clave_cont]
                acum_valor = acumulados[clave_acum]

                if cont_valor > 0:
                    conteos_tipo.append(cont_valor)
                    acumulados_tipo.append(acum_valor)

        if sum(conteos_tipo) > 0:
            promedio = sum(acumulados_tipo) / sum(conteos_tipo)
        else:
            promedio = 0

        promedios_por_tipo[f"Tipo {j}"] = promedio

    tipos = [f"Tipo {j}" for j in range(1, 8)]
    valores = [promedios_por_tipo[tipo] for tipo in tipos]

    fig = go.Figure(data=[
        go.Bar(
            x=tipos,
            y=valores,
            text=[f"{v:.2f}" for v in valores],  # Mostrar el valor con 2 decimales
            textposition='auto',
            marker_color=['#FF9999', '#66B2FF', '#99FF99', '#FFCC99', '#FF99CC', '#9999FF', '#CCFF99'],
            hoverinfo='text',
            hovertext=[f"Tipo {j}: {promedios_por_tipo[f'Tipo {j}']:.2f}" for j in range(1, 8)]
        )
    ])

    # Personalizar el diseño
    fig.update_layout(
        title_text="Promedio de Tiempo por Tipo de Paro",
        title_font_size=20,
        xaxis_title="Tipo de Paro",
        yaxis_title="Tiempo Promedio(Seg)",
        height=600,
        width=900
    )

    return fig



def calcular_disponibilidad(df):
    acumulados=obt_acum(df)
    tiempo_perdido = sum(acumulados.values())



