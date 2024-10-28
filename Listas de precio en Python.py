import pandas as pd
import folium
import streamlit as st
from streamlit_folium import st_folium
import plotly.express as px
import matplotlib.pyplot as plt
import altair as alt
import plotly.graph_objects as go


# Ruta del archivo Excel
file_path = r'Copia de lista promo del 18-31 Julio (00000002).xlsx'

# Definir la ruta del archivo Excel
ruta_archivo_excel = r'Inventarios.xlsx'



city_mapping = {
    "ARMENIA": "Armenia",
    "NEIVA": "Neiva",
    "YOPAL": "Yopal",
    "IBAGUE": "Ibagué",
    "MARIQUITA": "Mariquita",
    "BOGOTA": "Bogotá",
    "VILLANUEVA": "Villanueva",
    "SINCELEJO": "Sincelejo",
    "GRANADA": "Granada",
    "VILLAVO": "Villavicencio",
    "PTO. LOPEZ": "Puerto Lopez",
    "CHINCHINA": "Chinchiná",
    "TULUA": "Tuluá",
    "PEREIRA": "Pereira",
    "MANIZALES": "Manizales",
    "LA DORADA": "La Dorada",
    "MONTERIA": "Montería",
    "ACACIAS": "Acacías",
    "PITALITO": "Pitalito",
    "GARZON": "Garzón",
    "CERETE": "Cereté",
    "ESPINAL": "Espinal",
    "MAGANGUE": "Magangué",
}

# Leer el archivo Excel
df_inventarios = pd.read_excel(ruta_archivo_excel)

# Aplicar el mapeo para corregir los nombres de ciudades
df_inventarios['CIUDAD_CORREGIDA'] = df_inventarios['CIUDAD'].map(city_mapping)

# Leer el archivo Excel como DataFrame, estableciendo el encabezado a partir de la tercera fila (índice 4)
df = pd.read_excel(file_path, header=4)

# Filtrar el DataFrame para eliminar las filas donde 'NUEVO COSTO' esté vacía o sea igual a 0
df_filtrado = df[df['NUEVO COSTO'].notna() & (df['NUEVO COSTO'] != 0)]

# Eliminar las columnas que estén completamente vacías
df_filtrado = df_filtrado.dropna(axis=1, how='all')

# Crear un nuevo DataFrame con solo las columnas especificadas y hacer una copia explícita
columnas_seleccionadas = [
    'Categoria', 'Referencia', 'Desc. item', 'Ud', 'Si.', 'Cs.', 'Cr.', 'Vt', 'S.f', 'COSTOTAL', 
    'Cp.', 'Mc p$', 'Base Lista', 'APOYO POR UNIDAD', 'NUEVO COSTO', 'MARGEN', 'SUPER CONTADO', 
    'CLIENTE ESPECIAL 75', 'CLIENTE ESPECIAL 35', 'CLIENTE ESPECIAL 15'
]

# Filtrar las columnas seleccionadas y hacer una copia del DataFrame
df_nuevo = df_filtrado[columnas_seleccionadas].copy()

# Agregar nuevas columnas vacías al DataFrame y realizar las operaciones
df_nuevo['PROTECCIÓN'] = 0  # Inicializamos con valor 0 para realizar la operación sin errores
df_nuevo['COSTO - PROTECC'] = df_nuevo['NUEVO COSTO'] - df_nuevo['PROTECCIÓN']
df_nuevo['COSTO + IVA'] = df_nuevo['COSTO - PROTECC'] * 1.19

# Crear la variable o parámetro margen (puede ser un valor fijo o un cálculo)
margen1 = 0.37  # Asignación de un valor para el margen zona 1, zona 2 y zona 3
margen2 = 0.40  # Asignación de un valor fijo para el margen zona 4
bono_pronto_pago = 0.05 # Asignación de un valor fijo para el bono pronto pago
variacion_supercontado_zona4 = 0.03 # Asignación de un valor fijo para la variacion del super_contado en zona 4
margen_credito_zona1 = 0.27 # Asignación de un valor para el margen de crédito
margen_credito_zona2 = 0.32 # Asignación de un valor para el margen de crédito
margen_credito_zona3 = 0.37 # Asignación de un valor para el margen de crédito
margen_credito_zona4 = 0.40 # Asignación de un valor para el margen de crédito
margen_convenio_y_tarjeta_zona1 = 0.27 # Asignación de un valor para el margen de crédito
margen_convenio_y_tarjeta_zona2 = 0.32 # Asignación de un valor para el margen de crédito
margen_convenio_y_tarjeta_zona3 = 0.32 # Asignación de un valor para el margen de crédito
margen_convenio_y_tarjeta_zona4 = 0.27 # Asignación de un valor para el margen de crédito

print("Leyendo el documento del departamento de Compras y definiendo parametros de margenes de la zona 1, 2, 3 y 4")

# Crear copias del DataFrame df_nuevo para calcular el precio publico 
df_final = df_nuevo.copy()
df_zona1 = df_nuevo.copy()
df_zona2 = df_nuevo.copy()
df_zona3 = df_nuevo.copy()
df_zona4 = df_nuevo.copy()

# Calcular la columna 'Precio Publico' usando la variable margen1 para zonas 1, 2 y 3
df_zona1['Precio Publico'] = df_zona1['COSTO + IVA'] / (1 - margen1) / (1 - bono_pronto_pago)
df_zona2['Precio Publico'] = df_zona2['COSTO + IVA'] / (1 - margen1) / (1 - bono_pronto_pago)
df_zona3['Precio Publico'] = df_zona3['COSTO + IVA'] / (1 - margen1) / (1 - bono_pronto_pago)

# Calcular la columna 'Precio Publico' usando la variable margen2 para zona 4
df_zona4['Precio Publico'] = df_zona4['COSTO + IVA'] / (1 - margen2) / (1 - bono_pronto_pago)

print("Calculando precios publicos de la zona 1,2,3 y 4")

# Agregar la columna 'Precio contado' a los DataFrames y asignar el valor de 'SUPER CONTADO'
df_zona1['Precio contado'] = df_zona1['SUPER CONTADO']
df_zona2['Precio contado'] = df_zona2['SUPER CONTADO']
df_zona3['Precio contado'] = df_zona3['SUPER CONTADO']

# Para zona 4, aplicar la fórmula 'SUPER CONTADO' 
df_zona4['Precio contado'] = df_zona4['SUPER CONTADO'] / (1 - variacion_supercontado_zona4)

print("Calculando los precios del super contado")

# Agregar la columna 'descuentos precio contado' a los DataFrames
df_zona1['Porcentaje descuento contado'] = (df_zona1['Precio Publico'] - df_zona1['SUPER CONTADO']) / df_zona1['Precio Publico'] * 100
df_zona1['Valor descuento contado'] = df_zona1['Precio Publico'] - df_zona1['SUPER CONTADO']
df_zona2['Porcentaje descuento contado'] = (df_zona2['Precio Publico'] - df_zona2['SUPER CONTADO']) / df_zona2['Precio Publico'] * 100
df_zona2['Valor descuento contado'] = df_zona2['Precio Publico'] - df_zona2['SUPER CONTADO']
df_zona3['Porcentaje descuento contado'] = (df_zona3['Precio Publico'] - df_zona3['SUPER CONTADO']) / df_zona3['Precio Publico'] * 100
df_zona3['Valor descuento contado'] = df_zona3['Precio Publico'] - df_zona3['SUPER CONTADO']
df_zona4['Porcentaje descuento contado'] = (df_zona4['Precio Publico'] - df_zona4['SUPER CONTADO']) / df_zona4['Precio Publico'] * 100
df_zona4['Valor descuento contado'] = df_zona4['SUPER CONTADO']

print("Calculando los porcentajes de descuento utilizados para obtener el precio super contado")

# Agregar la columna 'Precio credito' a los DataFrames y asignar el valor de 'Precio credito'
df_zona1['Precio credito'] = df_zona1['COSTO + IVA'] / (1 - margen_credito_zona1)
df_zona2['Precio credito'] = df_zona2['COSTO + IVA'] / (1 - margen_credito_zona2) / (1 - bono_pronto_pago)
df_zona3['Precio credito'] = df_zona3['COSTO + IVA'] / (1 - margen_credito_zona3) / (1 - bono_pronto_pago)
df_zona4['Precio credito'] = df_zona4['COSTO + IVA'] / (1 - margen_credito_zona4) / (1 - bono_pronto_pago)

print("Calculando los precios del crédito")

# Agregar la columna 'descuentos precio crédito' a los DataFrames
df_zona1['Porcentaje descuento credito'] = (df_zona1['Precio Publico'] - df_zona1['Precio credito']) / df_zona1['Precio Publico'] * 100
df_zona1['Valor descuento credito'] = df_zona1['Precio Publico'] - df_zona1['Precio credito']
df_zona2['Porcentaje descuento credito'] = (df_zona2['Precio Publico'] - df_zona2['Precio credito']) / df_zona2['Precio Publico'] * 100
df_zona2['Valor descuento credito'] = df_zona2['Precio Publico'] - df_zona2['Precio credito']
df_zona3['Porcentaje descuento credito'] = (df_zona3['Precio Publico'] - df_zona3['Precio credito']) / df_zona3['Precio Publico'] * 100
df_zona3['Valor descuento credito'] = df_zona3['Precio Publico'] - df_zona3['Precio credito']
df_zona4['Porcentaje descuento credito'] = (df_zona4['Precio Publico'] - df_zona4['Precio credito']) / df_zona4['Precio Publico'] * 100
df_zona4['Valor descuento credito'] = df_zona4['Precio credito']

print("Calculando los porcentajes de descuento utilizados para obtener el precio crédito")

# Agregar la columna 'Precio tarjeta' a los DataFrames y asignar el valor de 'Precio credito'
df_zona1['Precio tarjeta'] = df_zona1['COSTO + IVA'] / (1 - margen_convenio_y_tarjeta_zona1)
df_zona2['Precio tarjeta'] = df_zona2['COSTO + IVA'] / (1 - margen_convenio_y_tarjeta_zona2) / (1 - bono_pronto_pago)
df_zona3['Precio tarjeta'] = df_zona3['COSTO + IVA'] / (1 - margen_convenio_y_tarjeta_zona3) / (1 - bono_pronto_pago)
df_zona4['Precio tarjeta'] = df_zona4['COSTO + IVA'] / (1 - margen_convenio_y_tarjeta_zona4) / (1 - bono_pronto_pago)

print("Calculando los precios del credito Oportuya")

# Agregar la columna 'descuentos precio crédito' a los DataFrames
df_zona1['Porcentaje descuento credito Oportuya'] = (df_zona1['Precio Publico'] - df_zona1['Precio tarjeta']) / df_zona1['Precio Publico'] * 100
df_zona1['Valor descuento credito Oportuya'] = df_zona1['Precio Publico'] - df_zona1['Precio tarjeta']
df_zona2['Porcentaje descuento credito Oportuya'] = (df_zona2['Precio Publico'] - df_zona2['Precio tarjeta']) / df_zona2['Precio Publico'] * 100
df_zona2['Valor descuento credito Oportuya'] = df_zona2['Precio Publico'] - df_zona2['Precio tarjeta']
df_zona3['Porcentaje descuento credito Oportuya'] = (df_zona3['Precio Publico'] - df_zona3['Precio tarjeta']) / df_zona3['Precio Publico'] * 100
df_zona3['Valor descuento credito Oportuya'] = df_zona3['Precio Publico'] - df_zona3['Precio tarjeta']
df_zona4['Porcentaje descuento credito Oportuya'] = (df_zona4['Precio Publico'] - df_zona4['Precio tarjeta']) / df_zona4['Precio Publico'] * 100
df_zona4['Valor descuento credito Oportuya'] = df_zona4['Precio tarjeta']

print("Calculando los porcentajes de descuento utilizados para obtener el precio crédito Oportuya")

# Agregar la columna 'Precio convenio' a los DataFrames y asignar el valor de 'Precio credito'
df_zona1['Precio convenio'] = df_zona1['COSTO + IVA'] / (1 - margen_convenio_y_tarjeta_zona1)
df_zona2['Precio convenio'] = df_zona2['COSTO + IVA'] / (1 - margen_convenio_y_tarjeta_zona2)
df_zona3['Precio convenio'] = df_zona3['COSTO + IVA'] / (1 - margen_convenio_y_tarjeta_zona3)
df_zona4['Precio convenio'] = df_zona4['COSTO + IVA'] / (1 - margen_convenio_y_tarjeta_zona4)

# Agregar la columna 'descuentos precio crédito' a los DataFrames
df_zona1['Porcentaje descuento credito Convenio'] = (df_zona1['Precio Publico'] - df_zona1['Precio convenio']) / df_zona1['Precio Publico'] * 100
df_zona1['Valor descuento credito Convenio'] = df_zona1['Precio Publico'] - df_zona1['Precio convenio']
df_zona2['Porcentaje descuento credito Convenio'] = (df_zona2['Precio Publico'] - df_zona2['Precio convenio']) / df_zona2['Precio Publico'] * 100
df_zona2['Valor descuento credito Convenio'] = df_zona2['Precio Publico'] - df_zona2['Precio convenio']
df_zona3['Porcentaje descuento credito Convenio'] = (df_zona3['Precio Publico'] - df_zona3['Precio convenio']) / df_zona3['Precio Publico'] * 100
df_zona3['Valor descuento credito Convenio'] = df_zona3['Precio Publico'] - df_zona3['Precio convenio']
df_zona4['Porcentaje descuento credito Convenio'] = (df_zona4['Precio Publico'] - df_zona4['Precio convenio']) / df_zona4['Precio Publico'] * 100
df_zona4['Valor descuento credito Convenio'] = df_zona4['Precio convenio']

print("Calculando los porcentajes de descuento utilizados para obtener el precio crédito Convenio")

#Filtro de los Dataframes para visualizar lo realmente importante

# Definir las columnas relevantes para los DataFrames
columnas_relevantes = [
    'Referencia', 'Desc. item', 'Precio Publico', 'Porcentaje descuento contado', 
    'Precio contado', 'Porcentaje descuento credito', 'Precio credito', 
    'Porcentaje descuento credito Oportuya', 'Precio tarjeta', 'Precio convenio', 
    'Porcentaje descuento credito Convenio', 'CLIENTE ESPECIAL 75', 'CLIENTE ESPECIAL 35', 'CLIENTE ESPECIAL 15'
]

columnas_a_formatear = [
    'Precio Publico', 'Precio contado', 'Precio credito', 'Precio tarjeta', 'Precio convenio', 
    'CLIENTE ESPECIAL 75', 'CLIENTE ESPECIAL 35', 'CLIENTE ESPECIAL 15'
]

# Función para formatear los números con separador de miles y sin decimales
def formatear_valor(valor):
    if pd.notna(valor):  # Verificar que el valor no sea NaN
        return f"{valor:,.0f}".replace(",", ".")
    return valor

# Aplicar el formato a las columnas relevantes de cada DataFrame
df_zona1[columnas_a_formatear] = df_zona1[columnas_a_formatear].applymap(formatear_valor)
df_zona2[columnas_a_formatear] = df_zona2[columnas_a_formatear].applymap(formatear_valor)
df_zona3[columnas_a_formatear] = df_zona3[columnas_a_formatear].applymap(formatear_valor)
df_zona4[columnas_a_formatear] = df_zona4[columnas_a_formatear].applymap(formatear_valor)

# Aplicar el filtro de columnas a cada DataFrame
df_zona1 = df_zona1[columnas_relevantes]
df_zona2 = df_zona2[columnas_relevantes]
df_zona3 = df_zona3[columnas_relevantes]
df_zona4 = df_zona4[columnas_relevantes]

# Guardar los DataFrames en archivos Excel en la ruta especificada
ruta_base = r"D:\DATOS JUAN\Desktop\LISTAS DE PRECIO"

# Guardar cada DataFrame como un archivo Excel utilizando la cadena raw para evitar errores de escape
df_zona1.to_excel(rf"{ruta_base}\df_zona1.xlsx", index=False)
df_zona2.to_excel(rf"{ruta_base}\df_zona2.xlsx", index=False)
df_zona3.to_excel(rf"{ruta_base}\df_zona3.xlsx", index=False)
df_zona4.to_excel(rf"{ruta_base}\df_zona4.xlsx", index=False)

print("Los archivos Excel para zona1, zona2, zona3 y zona 4 se han guardado exitosamente en la ruta especificada.")

#_________________________________Visualizador__________________________________________________________

import streamlit as st
import pandas as pd

# Definir las claves aleatorias para cada zona
zonas_claves = {
    "Zona 1": "clave123",
    "Zona 2": "clave456",
    "Zona 3": "clave789",
    "Zona 4": "clave012"
}

# Estilo CSS para ajustar el diseño
st.markdown(
    """
    <style>
        
.main-title {
    font-size: 48px;
    font-weight: bold;
    text-align: center;
    color: #000000;
}

/* Cambiar el color de fondo de la barra lateral */
[data-testid="stSidebar"] {
    background-color: #01bcf3;
}

/* Estilo del texto de bienvenida justificado */
.welcome-text {
    font-size: 20px;
    font-weight: normal;
    text-align: justify;
    margin: 20px auto;
    color: #333333;
    line-height: 1.5;
    width: 60%; /* Ajustar el ancho */
}

/* Estilo del label con flecha centrado y separación */
.info-label {
    background-color: #01bcf3;
    color: #ffffff;
    border-radius: 25px;
    padding: 10px;
    margin: 30px auto;
    text-align: center;
    font-size: 18px;
    font-weight: normal;
    width: fit-content;
    white-space: nowrap; /* Asegurar que el texto ocupe un solo renglón */
    position: relative;
    padding-left: 30px; /* Separación entre flecha y texto */
}

.info-label:before {
    content: "←";
    font-size: 24px;
    position: absolute;
    left: 10px;
    top: 50%;
    transform: translateY(-50%);
}

/* Estilo ajustado y centrado del encabezado del producto seleccionado */
.product-header {
    background-color: #01bcf3;
    color: #ffffff;
    font-size: 20px; /* Reducir el tamaño del texto */
    font-weight: bold;
    display: inline-block; /* Ajustar para un solo renglón */
    padding: 15px;
    border-radius: 20px; /* Aplicar el mismo diseño de las tarjetas */
    margin: 10px auto;
    text-align: center;
    width: fit-content;
    box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2); /* Sombra similar a las tarjetas */
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.product-header:hover {
    transform: translateY(-5px);
    box-shadow: 0px 8px 12px rgba(0, 0, 0, 0.3);
}

/* Contenedor para centrar el label de PRODUCTO SELECCIONADO */
.product-container {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    margin-top: 25px;
}

/* Estilo para la referencia y descripción en un solo renglón */
.product-details-inline {
    text-align: center;
    font-size: 19px;
    font-weight: bold;
    font-family: 'Arial', sans-serif; /* Cambiar la fuente a Berlin Sans */
    color: #000000;
    margin: 25px 0;
}

.product-details-inline span {
    display: inline-block;
    margin: 0 20px; /* Separar los elementos de texto */
}

/* Contenedor para asegurar que las tarjetas estén centradas */
.price-container {
    display: flex;
    margin: 0 auto; /* Centrar horizontalmente */
}

/* Mejora en el diseño de las cajas de precios */
.price-box {
    display: flex;
    flex-direction: column;
    align-items: center;
    background-color: #01bcf3;
    color: #ffffff;
    padding: 25px;
    margin: 10px;
    border-radius: 30px;
    box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.price-box:hover {
    transform: translateY(-5px);
    box-shadow: 0px 8px 12px rgba(0, 0, 0, 0.3);
}

.price-box .label {
    font-size: 24px;
    border-bottom: 2px solid #ffffff;
    font-weight: bold;
    width: 106%;
    text-align: center; /* Asegurarse de que el label esté centrado */
}

.price-box .value {
    font-size: 25px;
    font-weight: bold;
    text-align: center; /* Centrar el precio */
}

/* Contenedor para el área azul que contiene el texto "Disponibilidad" */
.availability-container {
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: #01bcf3; /* Color azul claro */
    border-radius: 3px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
    width: 100%;
    height: 40px;
    margin: 0 auto; /* Centrar horizontalmente */
}

/* Estilo del texto "Disponibilidad" */
.availability-label {
    font-size: 19px;
    font-weight: bold;
    color: white; /* Texto en blanco */
    text-align: center;
}

    </style>
    """, 
    unsafe_allow_html=True
)

# Mostrar el logo en la parte superior de la barra lateral
st.sidebar.image(r"D:\DATOS JUAN\Downloads\channels4_profile (1).jpg", use_column_width=True)

# Inicializar la variable de sesión para la clave correcta
if 'clave_correcta' not in st.session_state:
    st.session_state.clave_correcta = False

# Función para cargar y procesar los datos
def cargar_datos():
    ruta_base = r"D:\DATOS JUAN\Desktop\LISTAS DE PRECIO"
    df_zona1 = pd.read_excel(f"{ruta_base}\\df_zona1.xlsx")
    df_zona2 = pd.read_excel(f"{ruta_base}\\df_zona2.xlsx")
    df_zona3 = pd.read_excel(f"{ruta_base}\\df_zona3.xlsx")
    df_zona4 = pd.read_excel(f"{ruta_base}\\df_zona4.xlsx")
    return df_zona1, df_zona2, df_zona3, df_zona4

# Cargar los datos
df_zona1, df_zona2, df_zona3, df_zona4 = cargar_datos()

# Selección de la zona si la clave no es correcta aún
if not st.session_state.clave_correcta:
    st.title("Acceso a Zonas")
    
    zona_seleccionada = st.selectbox("Selecciona una zona para acceder:", ["Zona 1", "Zona 2", "Zona 3", "Zona 4"])

    # Solicitar clave de acceso
    clave_ingresada = st.text_input(f"Ingresa la clave para {zona_seleccionada}:", type="password")

    # Verificar clave ingresada
    if clave_ingresada == zonas_claves[zona_seleccionada]:
        st.session_state.clave_correcta = True
        st.session_state.zona_seleccionada = zona_seleccionada
        st.success(f"Acceso permitido para {zona_seleccionada}")
    elif clave_ingresada:
        st.error("Clave incorrecta. Por favor, intenta nuevamente.")

# Mostrar el contenido si la clave es correcta
if st.session_state.clave_correcta:
    def visualizar_datos_por_zona(df_zona, zona):
        referencia = st.sidebar.text_input(f"CÓDIGO DEL ITEM (Zona {zona[-1]})")
        medio_pago = st.sidebar.selectbox(
            "MEDIO DE PAGO", 
            ["Selecciona una opción", "Precio Público", "Precio Contado", "Precio Crédito", 
             "Precio Mayoreo 75", "Precio Mayoreo 35", "Precio Mayoreo 15", 
             "Precio Oportuya", "Precio Convenio"]
        )

        # Filtrar los datos según la referencia y la descripción ingresadas
        df_filtrado = df_zona[
            df_zona['Referencia'].astype(str).str.contains(referencia, case=False, na=False)
        ]

        # Filtrar los datos según la referencia en df_inventarios
        df_filtrado_inventarios = df_inventarios[
            df_inventarios['Referencia'].astype(str).str.contains(referencia, case=False, na=False)
        ]

        if not referencia :
            st.markdown('<div class="main-title">LISTAS DE PRECIO</div>', unsafe_allow_html=True)

            # Texto de bienvenida justificado
            st.markdown("""
                <div class="welcome-text">
                    <strong>¡Bienvenido, Asesor!</strong><br><br>
                    Nos alegra tenerte como parte de nuestro equipo. Aquí encontrarás todas las herramientas necesarias 
                    para consultar y actualizar los precios de nuestros productos de manera rápida y sencilla. 
                    Este espacio ha sido diseñado para brindarte acceso directo a la información más actualizada, 
                    permitiéndote ofrecer el mejor servicio a tus clientes.
                </div>
            """, unsafe_allow_html=True)

            # Label con el mensaje y flecha centrado en un solo renglón con separación
            st.markdown("""
                <div class="info-label">
                    Comienza por diligenciar el código del item. 
                </div>
            """, unsafe_allow_html=True)

            # Mostrar mensaje si no se selecciona un medio de pago
        elif medio_pago == "Selecciona una opción":
            st.warning("Por favor, selecciona un medio de pago para desplegar la información.")
            return
        else:
            # Mostrar los resultados en el formato visual tipo tarjeta si hay datos filtrados
            if df_filtrado is not None and not df_filtrado.empty:
                for _, row in df_filtrado.iterrows():
                    st.markdown("""
                    <div class="product-container">
                        <div class="product-header">PRODUCTO SELECCIONADO</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Mostrando referencia y descripción en la misma línea con letras negras
                    st.markdown(
                        f'<div class="product-details-inline">'
                        f'<span>Descripción del item 🡺 {row["Desc. item"]}</span>'
                        f'<span>Código del item 🡺 {row["Referencia"]}</span>'
                        f'</div>', unsafe_allow_html=True
                    )

                    # Añadir el contenedor que centrará las tarjetas
                    st.markdown('<div class="price-container">', unsafe_allow_html=True)

                    # Mostrar solo la tarjeta del medio de pago seleccionado
                    if medio_pago == "Precio Público":
                        st.markdown(f"""
                            <div class="price-box">
                                <div class="label">PRECIO PUBLICO</div>
                                <div class="value">${row['Precio Publico']}</div>
                            </div>
                        """, unsafe_allow_html=True)
                    elif medio_pago == "Precio Contado":
                        st.markdown(f"""
                            <div class="price-box">
                                <div class="label">PRECIO CONTADO</div>
                                <div class="value">${row['Precio contado']}</div>
                            </div>
                        """, unsafe_allow_html=True)
                    elif medio_pago == "Precio Crédito":
                        st.markdown(f"""
                            <div class="price-box">
                                <div class="label">PRECIO CREDITO</div>
                                <div class="value">
                                    <a href="https://lagobo.coxti.com/auth/login" target="_blank" style="color: #ffffff; text-decoration: none;">
                                        ${row['Precio credito']}
                                    </a>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                    # Repite la lógica para los demás medios de pago
                    elif medio_pago == "Precio Mayoreo 75":
                        st.markdown(f"""
                            <div class="price-box">
                                <div class="label">PRECIO MAYOREO 75</div>
                                <div class="value">${row['CLIENTE ESPECIAL 75']}</div>
                            </div>
                        """, unsafe_allow_html=True)
                    elif medio_pago == "Precio Mayoreo 35":
                        st.markdown(f"""
                            <div class="price-box">
                                <div class="label">PRECIO MAYOREO 35</div>
                                <div class="value">${row['CLIENTE ESPECIAL 35']}</div>
                            </div>
                        """, unsafe_allow_html=True)
                    elif medio_pago == "Precio Mayoreo 15":
                        st.markdown(f"""
                            <div class="price-box">
                                <div class="label">PRECIO MAYOREO 15</div>
                                <div class="value">${row['CLIENTE ESPECIAL 15']}</div>
                            </div>
                        """, unsafe_allow_html=True)
                    elif medio_pago == "Precio Oportuya":
                        st.markdown(f"""
                            <div class="price-box">
                                <div class="label">PRECIO OPORTUYA</div>
                                <div class="value">${row['Precio tarjeta']}</div>
                            </div>
                        """, unsafe_allow_html=True)
                    elif medio_pago == "Precio Convenio":
                        st.markdown(f"""
                            <div class="price-box">
                                <div class="label">PRECIO CONVENIO</div>
                                <div class="value">${row['Precio convenio']}</div>
                            </div>
                        """, unsafe_allow_html=True)

                    # Cerrar el contenedor que centra las tarjetas
                    st.markdown('</div>', unsafe_allow_html=True)

            # Filtrar las ciudades con saldo mayor a 0 y calcular las unidades disponibles
            df_filtrado_inventarios = df_filtrado_inventarios[df_filtrado_inventarios['Saldo final (cant.)'] > 0]

            # Agrupar por ciudad y sumar las unidades disponibles
            df_agrupado = df_filtrado_inventarios.groupby('CIUDAD', as_index=False)['Saldo final (cant.)'].sum()
            # Convertir 'Saldo final (cant.)' a numérico si es necesario
            df_agrupado['Saldo final (cant.)'] = pd.to_numeric(df_agrupado['Saldo final (cant.)'], errors='coerce')
            # Reemplazar posibles valores NaN por 0
            df_agrupado['Saldo final (cant.)'] = df_agrupado['Saldo final (cant.)'].fillna(0)

            # Crear gráfico de barras horizontal con Plotly
            fig = px.bar(
                df_agrupado,
                y='CIUDAD',  # Eje Y: Ciudades (para barras horizontales)
                x='Saldo final (cant.)',  # Eje X: Unidades
                text='Saldo final (cant.)',  # Añadir texto dentro de las barras
                orientation='h'  # Configuración para barras horizontales
            )

            # Personalizar el gráfico para mejorar el diseño
            fig.update_traces(
                textposition='inside',  # Posición del texto dentro de las barras
                marker=dict(
                    color='#01bcf3',  # Color de las barras
                ),
                width=0.8,  # Ancho relativo de las barras (reduce para parecer redondeadas)
                textfont=dict(
                size=14,  # Tamaño del texto (puedes ajustar a tus necesidades)
                color='white',  # Color del texto
                family='Arial',  # Fuente del texto, puedes cambiarla si prefieres otra
                weight='bold'  # Hacer el texto en negrita
                )
            )

            fig.update_layout(
            xaxis_title= "UNIDADES DISPONIBLES",  # Eliminar el título del eje X
            yaxis_title=None,  # Eliminar el título del eje Y
            title="DISPONIBILIDAD DEL PRODUCTO POR CIUDAD",  # Título
            plot_bgcolor='white',  # Fondo blanco para el gráfico
            yaxis=dict(
                categoryorder='total ascending',  # Ordenar las ciudades de mayor a menor
                tickfont=dict(
                    size=14,  # Tamaño del texto de las ciudades
                    color='Gray',  # Color del texto
                ),
                tickangle=0,  # Mantener el texto horizontal
                automargin=True  # Ajustar márgenes automáticamente para el texto grande
            ),
            title_font=dict(
                size=20,
                color='black',
                family='Arial',
            ),
            title_x=0.2,  # Centrar el título
        )

            # Mostrar el gráfico en Streamlit
            st.plotly_chart(fig)

    # Mostrar los datos según la zona seleccionada
    if st.session_state.zona_seleccionada == "Zona 1":
        visualizar_datos_por_zona(df_zona1, st.session_state.zona_seleccionada)
    elif st.session_state.zona_seleccionada == "Zona 2":
        visualizar_datos_por_zona(df_zona2, st.session_state.zona_seleccionada)
    elif st.session_state.zona_seleccionada == "Zona 3":
        visualizar_datos_por_zona(df_zona3, st.session_state.zona_seleccionada)
    elif st.session_state.zona_seleccionada == "Zona 4":
        visualizar_datos_por_zona(df_zona4, st.session_state.zona_seleccionada)
