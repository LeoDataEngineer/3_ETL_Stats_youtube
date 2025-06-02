# 📊 ETL Estadísticas de Canales de YouTube

Este proyecto realiza un proceso **ETL** (*Extract, Transform, Load*) para recopilar, transformar y almacenar estadísticas de canales de **YouTube** utilizando la **API oficial de YouTube**.
Los datos se guardan en archivos **CSV** y también en una base de datos **MySQL** para su posterior visualización mediante **Looker**.

# 🧠 Arquitectura

- **Fuente de datos:** API de YouTube  
- **Procesamiento:** Python (Pandas)  
- **Orquestación:** GitHub Actions (Batch ETL)  
- **Destino:** MySQL Data Warehouse  
- **Visualización:** Looker Dashboard

![Arq. ETL](imagen/Arq.%20Datos%20ETL-youtube.jpeg)


# ⚙️ Tecnologías utilizadas

- **Python**
- **Pandas**
- **YouTube Data API v3**
- **MySQL**
- **SQLAlchemy**
- **GitHub Actions** (para automatización del workflow)
- **Looker** (para dashboards)

# 🚀 Cómo funciona

### 🟡 Extracción (Extract)
Se obtiene información estadística de una lista de canales de YouTube usando su `channel_id` mediante la API.

### 🔵 Transformación (Transform)
Se estructuran los datos en un **DataFrame de Pandas**, agregando:
- Fecha
- Nombre del canal
- Vistas
- Suscriptores
- Cantidad de videos

### 🟢 Carga (Load)
- Se guarda un archivo `.csv` en la carpeta `channel_files/` con los datos del día.
- También se cargan los datos en una base de datos **MySQL**, eliminando previamente los registros con la misma fecha para evitar duplicados.

### 📊 Visualización
Los datos pueden visualizarse luego en un **dashboard creado en Looker** conectado a la base **MySQL**.

# 🔐 Configuración.

Crea un archivo `config.py` con las siguientes variables:

```python
API_KEY = "TU_API_KEY"
USER = "usuario_mysql"
PASSWORD = "tu_contraseña"
HOST = "localhost"
PORT = "3306"
DATABASE = "nombre_base"
```
Si usas Github Action guarda las credenciales en la variable de entorno de Github


# 📅 Automatización

Puedes automatizar este script con **GitHub Actions** para que se ejecute diariamente y actualice la base de datos de forma automática.

# 📈 Dashboard

Los datos se pueden consumir desde **Looker**, conectando el dashboard directamente a la base de datos **MySQL** donde se almacena la tabla `youtube_stats`.

# ✅ Canales incluidos

El script analiza los siguientes canales de YouTube:

- **Marciaylanube**
- **TodoCode**
- **PeladoNerd**
- **Codigofacilito**
- **Platzi**
- **EDteam**
- **Soy Dalto**
- **midudev**
- **freeCodeCamp**
- **Valen Werle**

## Link del Dashboard en Construcción.
[Link Dashboard](https://lookerstudio.google.com/)
