Ciencia de redes en mineria visible 

Este proyecto analiza datos de explotación de minerales en Colombia mediante redes bipartitas y de coocurrencia. Genera visualizaciones y exporta los resultados en formato `GraphML`.

---

## Requisitos previos

Asegúrese de tener instalado lo siguiente en su sistema:

1. **Python** (versión 3.7 o superior)
2. **pip** (administrador de paquetes de Python)
3. **virtualenv** (opcional, para entornos virtuales)

---

## Configuración del entorno virtual

### 1. Crear un entorno virtual

1. Navegue al directorio del proyecto.
2. Ejecute el siguiente comando para crear un entorno virtual:

   ```bash
   python -m venv venv
   ```

3. Active el entorno virtual:
   - En Windows:
     ```bash
     venv\Scripts\activate
     ```
   - En macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

### 2. Instalar dependencias

Con el entorno virtual activado, instale las dependencias requeridas:

```bash
pip install -r requirements.txt
```

---

## Estructura del proyecto

- `notebook.ipynb`: Jupyter Notebook principal con el análisis.
- `datos/raw/`: Carpeta que contiene los datos sin procesar.
- `datos/processed/`: Carpeta donde se guardan los resultados procesados.
- `requirements.txt`: Lista de dependencias necesarias para ejecutar el proyecto.

---

## Ejecución del proyecto

### 1. Preparar los datos

Coloque el archivo de datos en la carpeta `datos/raw/`. El archivo esperado debe tener un formato CSV con columnas como:
- `municipio`
- `recurso_natural`
- `valor_contraprestacion`
- `cantidad_produccion`

### 2. Ejecutar el análisis

Abra el archivo Jupyter Notebook en su navegador:

```bash
jupyter notebook
```

Navegue al archivo `notebook.ipynb` y ejecúte las celdas paso a paso.

### 3. Guardar y exportar resultados

Los resultados se guardarán en `datos/processed/`:
- `red_bipartita_municipios_recursos.graphml`
- `coocurrencia_recursos.graphml`
- `coocurrencia_municipios.graphml`
