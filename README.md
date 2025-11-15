# 🧮 Calculadora de Derivadas Parciales

Aplicación web interactiva para visualizar el cálculo numérico de derivadas parciales usando el método de **diferencias finitas centrales de segundo orden**.

## 📋 Descripción

Este proyecto implementa una calculadora web que permite visualizar y entender cómo funcionan las derivadas parciales ∂f/∂x y ∂f/∂y para funciones de dos variables f(x,y). Utiliza métodos numéricos para aproximar las derivadas y valida los resultados contra derivadas analíticas exactas.

### ✨ Características Principales

- 🔢 **Método Numérico Robusto**: Diferencias finitas centrales O(h²)
- 📊 **Visualizaciones Interactivas 3D**: Gráficos de contorno, superficies 3D y campos vectoriales usando Plotly
- ✅ **Validación Automática**: Compara resultados numéricos con derivadas analíticas
- 🎯 **4 Ejemplos Predefinidos**: Ondas sinusoidales, paraboloide, silla de montar y gaussiana
- 📱 **Diseño Responsive**: Interfaz adaptable a móviles, tablets y desktop
- 🧪 **Suite de Tests**: Testing automatizado con verificación de requisitos

## 🚀 Inicio Rápido

### Requisitos del Sistema

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Navegador web moderno (Chrome, Firefox, Safari, Edge)

### Instalación

1. **Clonar o descargar el proyecto**
   ```bash
   cd remedial
   ```

2. **Crear entorno virtual (recomendado)**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # En Windows: .venv\Scripts\activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecutar la aplicación**
   ```bash
   python3 app.py
   ```

5. **Abrir en el navegador**
   ```
   http://127.0.0.1:5000
   ```

¡Listo! La aplicación pre-calculará los 4 ejemplos al iniciar y estará lista para usar.

## 📖 Uso

### Navegación

- **Sidebar**: Haz clic en cualquier ejemplo del menú lateral
- **Tabs**: Usa las pestañas superiores para cambiar entre ejemplos
- **Gráficos Interactivos**:
  - Zoom: Rueda del mouse
  - Rotar (3D): Arrastrar con el mouse
  - Pan: Shift + arrastrar

### Interpretación de Resultados

Cada ejemplo muestra:

1. **Función Original** - Expresión matemática f(x,y)
2. **Derivadas Analíticas** - Fórmulas exactas de ∂f/∂x y ∂f/∂y
3. **Parámetros de Malla** - Dominio, número de puntos y espaciamiento
4. **Tres Visualizaciones**:
   - Gráficas de contorno de f, ∂f/∂x y ∂f/∂y
   - Superficies 3D interactivas
   - Campo vectorial del gradiente ∇f = (∂f/∂x, ∂f/∂y)

## 📁 Estructura del Proyecto

```
remedial/
├── app.py                    # Aplicación Flask principal
├── derivatives.py            # Módulo de cálculo matemático
├── test_derivatives.py       # Suite de tests automatizados
├── requirements.txt          # Dependencias del proyecto
├── README.md                 # Este archivo
├── templates/
│   └── index.html           # Página principal con interfaz interactiva
├── static/
│   ├── css/
│   │   └── style.css        # Estilos responsive (1047 líneas)
│   └── js/
│       └── main.js          # Lógica de tabs y visualizaciones Plotly
└── .venv/                   # Entorno virtual (no versionado)
```

## 🔬 Método Matemático

### Diferencias Finitas Centrales de Segundo Orden

El proyecto calcula las derivadas parciales usando aproximaciones numéricas con precisión O(h²):

**Para puntos interiores:**

```
∂f/∂x ≈ (f[i, j+1] - f[i, j-1]) / (2·hx)
∂f/∂y ≈ (f[i+1, j] - f[i-1, j]) / (2·hy)
```

**Para puntos de borde:**
- Los valores se duplican del vecino inmediato
- No se usan diferencias forward/backward

### Pipeline de Cálculo

1. **Crear Malla** - Generación de puntos uniformemente espaciados con `numpy.meshgrid`
2. **Evaluar Función** - Evaluación segura de f(x,y) en todos los puntos
3. **Calcular Derivadas** - Aplicación de diferencias finitas centrales
4. **Validar** - Comparación con derivadas analíticas (métricas de error)
5. **Preparar Datos** - Serialización JSON para visualización web

## 📚 Ejemplos Incluidos

| # | Nombre | Función f(x,y) | ∂f/∂x | ∂f/∂y | Dominio | Puntos |
|---|--------|----------------|-------|-------|---------|--------|
| 1 | Ondas Sinusoidales | sin(x)·cos(y) | cos(x)·cos(y) | -sin(x)·sin(y) | [-2,2]² | 100×100 |
| 2 | Paraboloide | x²+y² | 2x | 2y | [-3,3]² | 100×100 |
| 3 | Silla de Montar | x²-y² | 2x | -2y | [-2,2]² | 100×100 |
| 4 | Gaussiana | x·exp(-x²-y²) | (1-2x²)·exp(-x²-y²) | -2xy·exp(-x²-y²) | [-3,3]² | 100×100 |

### Métricas de Validación

Para cada ejemplo se calculan automáticamente:

- **Error Absoluto**: máximo y promedio |numérico - exacto|
- **Error Relativo**: máximo y promedio |error| / |exacto|
- **RMSE**: Raíz del error cuadrático medio
- **Norma L2**: Magnitud del vector de error

Ejemplo de salida en consola:
```
Generando ejemplo: Ondas Sinusoidales...
  ✓ Completado - Validación:
    ∂f/∂x: Error máx = 3.72e-02, RMSE = 3.34e-03
    ∂f/∂y: Error máx = 1.58e-02, RMSE = 1.74e-03
```

## 🛠️ Funciones Principales

### `derivatives.py`

| Función | Descripción |
|---------|-------------|
| `create_uniform_mesh(x_min, x_max, y_min, y_max, nx, ny)` | Crea malla 2D uniformemente espaciada usando numpy.meshgrid |
| `evaluate_function(func_str, X, Y)` | Evalúa función matemática de forma segura (solo permite funciones NumPy) |
| `partial_derivatives_central(f, hx, hy)` | Calcula ∂f/∂x y ∂f/∂y con diferencias finitas centrales |
| `validate_against_analytical(X, Y, df_dx_num, df_dy_num, analytical_dx_str, analytical_dy_str)` | Calcula métricas de error comparando con derivadas exactas |
| `calculate_derivatives(func_str, x_min, x_max, y_min, y_max, nx, ny, analytical_dx, analytical_dy)` | Orquesta todo el pipeline de cálculo |

### Seguridad en `evaluate_function()`

La función usa `eval()` de forma segura limitando el acceso a:
- Funciones matemáticas: `sin`, `cos`, `tan`, `exp`, `log`, `sqrt`, `abs`
- Constantes: `pi`, `e`
- Variables de malla: `x`, `y`

Esto previene la ejecución de código arbitrario o malicioso.

## 🧪 Testing

### Ejecutar Tests

```bash
python3 test_derivatives.py
```

### Suite de Tests

El archivo `test_derivatives.py` incluye 5 tests:

1. ✅ **Verificación de Bordes**: Confirma que los bordes duplican valores vecinos
2. ✅ **Verificación de Dimensiones**: Valida que las derivadas tengan la misma forma que f
3. ✅ **Fórmula de Diferencias Centrales**: Verifica la implementación en puntos interiores
4. ✅ **Comparación con Analíticas**: Prueba con funciones conocidas (x², y²)
5. ✅ **Función de Validación**: Asegura que las métricas de error se calculen correctamente

Cada test proporciona mensajes detallados con símbolos visuales (✓, ✗) para facilitar el debugging.

## 💻 Tecnologías Utilizadas

### Backend
- **Python 3.11** - Lenguaje de programación
- **Flask 3.0.0** - Framework web minimalista
- **NumPy 1.26.2** - Cálculos numéricos eficientes con matrices
- **Python-dotenv 1.0.0** - Gestión de variables de entorno

### Frontend
- **HTML5** - Estructura con plantillas Jinja2
- **CSS3** - Diseño responsive con variables CSS
- **JavaScript Vanilla** - Interactividad sin dependencias externas
- **Plotly.js 2.27.0** - Visualizaciones interactivas 3D y 2D

## 🎨 Diseño y UX

### Sistema de Diseño CSS

El archivo `style.css` implementa:

- **Variables CSS**: Escalas de spacing, tipografía y colores
- **Layout Grid**: Sistema de grid moderno y flexible
- **Responsive Breakpoints**:
  - Desktop: >1024px
  - Tablet: 768px-1024px
  - Mobile: <768px
- **Componentes**: Cards, buttons, tabs, sidebar, plots
- **Animaciones**: Transiciones suaves y efecto fadeIn

### Accesibilidad

- Contraste de colores adecuado (WCAG AA)
- Navegación por teclado funcional
- Etiquetas semánticas HTML5

## 🔧 Configuración Avanzada

### Variables de Entorno

El proyecto usa `python-dotenv` para configuración. Puedes crear un archivo `.env`:

```env
FLASK_ENV=development
FLASK_DEBUG=True
```

### Personalizar Ejemplos

Para agregar tus propios ejemplos, edita el array `EXAMPLES` en `app.py`:

```python
EXAMPLES = [
    {
        'id': 5,
        'name': 'Mi Función',
        'function': 'x**3 + y**3',
        'analytical_dx': '3*x**2',
        'analytical_dy': '3*y**2',
        'description': 'Descripción de tu función',
        'domain': {'x_min': -2, 'x_max': 2, 'y_min': -2, 'y_max': 2},
        'mesh': {'nx': 100, 'ny': 100}
    }
]
```

### Ajustar Precisión de Malla

Modifica `nx` y `ny` en los ejemplos para cambiar la resolución:
- Mayor valor = más puntos = mayor precisión = más lento
- Menor valor = menos puntos = menor precisión = más rápido

## 📝 Notas Técnicas

### Manejo de JSON

El código incluye manejo robusto de valores especiales en JSON:

```python
try:
    examples_json = json.dumps(examples_results, allow_nan=False)
except ValueError:
    examples_json = json.dumps(examples_results, ignore_nan=True)
```

Esto previene errores cuando aparecen valores `NaN` o `Infinity` en los cálculos.

### Pre-cálculo al Iniciar

La aplicación pre-calcula todos los ejemplos cuando inicia el servidor Flask:

```
🧮 Generando ejemplos de derivadas parciales...
Generando ejemplo: Ondas Sinusoidales...
  ✓ Completado - Validación
...
✅ Todos los ejemplos generados
```

Esto asegura respuestas instantáneas cuando el usuario carga la página.

## 🤝 Contribuciones

Este proyecto es educativo. Si deseas contribuir:

1. Agrega más ejemplos de funciones interesantes
2. Mejora la documentación
3. Optimiza los cálculos numéricos
4. Agrega más métricas de validación
5. Mejora el diseño responsive

## 📄 Licencia

Este proyecto es de código abierto con fines educativos.

## 👨‍💻 Autor

Proyecto desarrollado como demostración de métodos numéricos para derivadas parciales.

---

**¿Preguntas o sugerencias?** Abre un issue en el repositorio.

**¿Encontraste un bug?** Los tests automatizados están en `test_derivatives.py` - úsalos para verificar.

---

Hecho con ❤️ usando Python, NumPy y Plotly
