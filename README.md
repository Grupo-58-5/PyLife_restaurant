# PyLife Group - Restaurant Project 🍝🍕🍔

API para la gestión de restaurantes, reservas y usuarios, desarrollada con FastAPI, Alembic y SQLModel.

## Características

- Registro y autenticación de usuarios (JWT)
- Gestión de usuarios (admin y cliente)
- CRUD de restaurantes
- Reservas de mesas con validaciones de disponibilidad
- Base de datos PostgreSQL (configurable por variables de entorno)s
- Migraciones con Alembic
- Tests automáticos con pytest

## Instalación

1. **Clona el repositorio**
```
git clone <https://github.com/Grupo-58-5/PyLife_restaurant.git>
cd PyLife_restaurant
```

2. **Configura las variables de entorno**
-  Copia [`.env.template`](.env.template) a `.env` y completa los valores requeridos.

3. **Instala las Dependencias**
- En tu ambiente virtual instala las dependencias
   ```
   pip install -r requirements.txt
4. **Ejecuta las migraciones**
   ```
   alembic upgrade head
5. **Docker Setup**
- Una vez ajustado las variables de entono en el `.env`
- Levanta los servicios
   ```
   docker-compose up --build -d
6. **Inicia la aplicación**
con uno de los 2 sig comandos
   - `uvicorn src.main:app --reload`
   - `fastapi dev src\main.py`

