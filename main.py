import pandas as pd
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go


# Definir la ruta del archivo Excel
ruta_archivo_excel = 'Inventarios.xlsx'

# Leer el archivo Excel
df_inventarios = pd.read_excel(ruta_archivo_excel)

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
st.sidebar.image(r"channels4_profile (1).jpg", use_column_width=True)

# Inicializar la variable de sesión para la clave correcta
if 'clave_correcta' not in st.session_state:
    st.session_state.clave_correcta = False

def cargar_datos():
    # Leer cada archivo de zona directamente desde el repositorio
    df_zona1 = pd.read_excel('df_zona1.xlsx')
    df_zona2 = pd.read_excel('df_zona2.xlsx')
    df_zona3 = pd.read_excel('df_zona3.xlsx')
    df_zona4 = pd.read_excel('df_zona4.xlsx')
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
                        f'<span>Descripción del item - {row["Desc. item"]}</span>'
                        f'<span>Código del item - {row["Referencia"]}</span>'
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
            
            # Crear el gráfico de barras horizontal
            fig, ax = plt.subplots(figsize=(8, 6))
            bars = ax.barh(df_agrupado['CIUDAD'], df_agrupado['Saldo final (cant.)'], color='#01bcf3')

            # Agregar etiquetas dentro de las barras
            for bar in bars:
                ax.text(
                    bar.get_width(),  # Ajuste para posicionar el texto dentro de la barra
                    bar.get_y() + bar.get_height() / 2,
                    f'{int(bar.get_width())}',
                    va='center',
                    ha='right',  # Alinear el texto a la derecha
                    color='white',
                    fontsize=12,
                    fontweight='bold'
                )

            # Crear el gráfico de barras horizontal con un margen ajustado
            fig.subplots_adjust(left=-0.1)  # Ajuste de margen izquierdo (0.3 es el margen extra a la izquierda)
                
            # Configurar título y eliminar ejes
            ax.set_title("DISPONIBILIDAD DE PRODUCTO POR CIUDAD", fontsize=14, fontweight='bold', color='black')
            ax.set_xlabel("UNIDADES")  # Eje X 
            ax.set_ylabel("")  # Eje Y vacío
            ax.tick_params(axis='x', colors='white')  # Ocultar las etiquetas del eje X

            # Mostrar el gráfico en Streamlit
            st.pyplot(fig)

    # Mostrar los datos según la zona seleccionada
    if st.session_state.zona_seleccionada == "Zona 1":
        visualizar_datos_por_zona(df_zona1, st.session_state.zona_seleccionada)
    elif st.session_state.zona_seleccionada == "Zona 2":
        visualizar_datos_por_zona(df_zona2, st.session_state.zona_seleccionada)
    elif st.session_state.zona_seleccionada == "Zona 3":
        visualizar_datos_por_zona(df_zona3, st.session_state.zona_seleccionada)
    elif st.session_state.zona_seleccionada == "Zona 4":
        visualizar_datos_por_zona(df_zona4, st.session_state.zona_seleccionada)
