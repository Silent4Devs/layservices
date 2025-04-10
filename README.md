
# LayServices 

Este proyecto constituye el backend principal para la inteligencia artificial dentro de la empresa. Se encarga del procesamiento, almacenamiento y monitoreo de datos utilizados por los modelos de IA, para la orquestación de tareas automatizadas y el análisis de información en tiempo real.

## Tabla de Contenidos 📖

- [Stack](#stack)
	- [UV (Gestor de Dependencias)](#uv)
	- [Alembic (Migraciones)](#alembic)
	- [Prefect (Orquestación)](#prefect)
	- [Langchain (Framework IA)](#langchain)
	- [Qdrant (Vector DB)](#qdrant)
	- [FastAPI](#fastapi)
	- [FastMCP (MCP Server)](#fastmcp)

- [Despliegue Local](#despliegue-local-)

- [Despliegue en Producción](#despliegue-en-producción-)

- [Estructura del Proyecto](#estructura-del-proyecto-)

  
## Stack 🛠
### UV (Gestor de Dependencias)
[UV](https://github.com/astral-sh/uv) es un gestor de paquetes rápido escrito en Rust, compatible con el ecosistema Python.
 📦 Instalación de UV
```bash
# Instalar UV globalmente
pip install uv

# Verificar instalación
uv --version
```
Para installar las dependencias usa el comando
```bash
uv sync
```

Para más información consulta la documentación oficial https://docs.astral.sh/uv/


### Alembic (Migraciones)
Alembic es un sistema de migraciones automático. Para ejecutar cualquier comando de alembic primero debes de ir al folder /app:

```bash
cd app
alembic --version
```
Las migraciones se hacen automáticamente con los cambios de la carpeta /app/models, con el comando:
```bash
alembic revision --autogenerate -m "Mensaje de la migración"
```
Para que alembic detecte correctamente los modelos es necesario definir el Modelo de la siguiente forma:
```python
from .base  import  Base
class MyModel(Base):
```
Para ejecutar las migraciones usa el comando:
```bash
alembic upgrade head
```
Para más información consultar la documentación oficial: https://alembic.sqlalchemy.org/en/latest/

### UV 

### Prefect (Orquestación)




### Qdrant (Vector DB)


## Despliegue Local ⚙️
 
1.  **Instalar Docker**

Para Windows:
https://docs.docker.com/desktop/setup/install/windows-install/

Distribuciones Linux:
https://docs.docker.com/engine/install/


2.  **Clonar Repositorio**

```bash
git  clone  https://github.com/Silent4Devs/layservices.git
cd  layservices
```

## Despliegue en Producción 🚀
