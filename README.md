# Mi Aplicación Flask

Proyecto básico de Flask para desarrollo web con Python.

## Requisitos

- Python 3.8 o superior
- [uv](https://github.com/astral-sh/uv) (recomendado) o pip

## Instalación

### Opción 1: Con uv (Recomendado - Mucho más rápido)

1. **Instalar uv** (si no lo tienes):
   ```bash
   # En macOS/Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # En Windows
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

2. **Crear entorno virtual e instalar dependencias**:
   ```bash
   uv venv
   source .venv/bin/activate  # En macOS/Linux
   # .venv\Scripts\activate    # En Windows

   uv pip install -r requirements.txt
   ```

### Opción 2: Con pip tradicional

1. **Crear un entorno virtual**:
   ```bash
   python3 -m venv venv
   ```

2. **Activar el entorno virtual**:
   - En macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
   - En Windows:
     ```bash
     venv\Scripts\activate
     ```

3. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

## Ejecutar la aplicación

```bash
python app.py
```

La aplicación estará disponible en: `http://127.0.0.1:5000`

## Estructura del proyecto

```
remedial/
├── app.py                  # Archivo principal de la aplicación
├── requirements.txt        # Dependencias del proyecto
├── .gitignore             # Archivos ignorados por Git
├── static/                # Archivos estáticos (CSS, JS, imágenes)
│   └── css/
│       └── style.css
└── templates/             # Plantillas HTML
    ├── index.html
    └── about.html
```

## Rutas disponibles

- `/` - Página principal
- `/about` - Página "Acerca de"

## Próximos pasos

- Agregar más rutas y vistas
- Conectar una base de datos
- Implementar formularios
- Agregar autenticación de usuarios
