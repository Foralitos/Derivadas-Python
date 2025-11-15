"""
Aplicación web Flask para visualizar derivadas parciales usando diferencias finitas.

Este módulo implementa una aplicación web que:
1. Pre-calcula derivadas parciales para 4 funciones de ejemplo
2. Valida resultados numéricos contra derivadas analíticas
3. Sirve una interfaz web interactiva con visualizaciones Plotly
"""

# ============================================================================
# IMPORTACIONES
# ============================================================================
from flask import Flask, render_template
from derivatives import calculate_derivatives
import json

# ============================================================================
# CONFIGURACIÓN DE LA APLICACIÓN FLASK
# ============================================================================
app = Flask(__name__)

# ============================================================================
# EJEMPLOS PREDEFINIDOS DE FUNCIONES
# ============================================================================
# Cada ejemplo incluye:
# - Función f(x,y)
# - Derivadas analíticas ∂f/∂x y ∂f/∂y
# - Dominio y parámetros de malla
EXAMPLES = [
    # Ejemplo 1: Ondas Sinusoidales
    {
        'id': 1,
        'name': 'Ondas Sinusoidales',
        'function': 'sin(x)*cos(y)',                    # f(x,y)
        'analytical_dx': 'cos(x)*cos(y)',               # ∂f/∂x analítica
        'analytical_dy': '-sin(x)*sin(y)',              # ∂f/∂y analítica
        'description': 'Producto de funciones trigonométricas que crean un patrón ondulatorio en 2D.',
        'domain': {'x_min': -2, 'x_max': 2, 'y_min': -2, 'y_max': 2},
        'mesh': {'nx': 100, 'ny': 100}
    },
    # Ejemplo 2: Paraboloide
    {
        'id': 2,
        'name': 'Paraboloide',
        'function': 'x**2 + y**2',                      # f(x,y)
        'analytical_dx': '2*x',                         # ∂f/∂x analítica
        'analytical_dy': '2*y',                         # ∂f/∂y analítica
        'description': 'Superficie parabólica que se abre hacia arriba, común en problemas de optimización.',
        'domain': {'x_min': -3, 'x_max': 3, 'y_min': -3, 'y_max': 3},
        'mesh': {'nx': 100, 'ny': 100}
    },
    # Ejemplo 3: Silla de Montar (Punto Silla)
    {
        'id': 3,
        'name': 'Silla de Montar',
        'function': 'x**2 - y**2',                      # f(x,y)
        'analytical_dx': '2*x',                         # ∂f/∂x analítica
        'analytical_dy': '-2*y',                        # ∂f/∂y analítica
        'description': 'Punto silla con curvatura positiva en una dirección y negativa en la otra.',
        'domain': {'x_min': -2, 'x_max': 2, 'y_min': -2, 'y_max': 2},
        'mesh': {'nx': 100, 'ny': 100}
    },
    # Ejemplo 4: Gaussiana Modificada
    {
        'id': 4,
        'name': 'Gaussiana',
        'function': 'x*exp(-x**2 - y**2)',              # f(x,y)
        'analytical_dx': '(1 - 2*x**2)*exp(-x**2 - y**2)',  # ∂f/∂x analítica
        'analytical_dy': '-2*x*y*exp(-x**2 - y**2)',    # ∂f/∂y analítica
        'description': 'Función con forma de campana multiplicada por x, típica en estadística y física.',
        'domain': {'x_min': -3, 'x_max': 3, 'y_min': -3, 'y_max': 3},
        'mesh': {'nx': 100, 'ny': 100}
    }
]

# ============================================================================
# FUNCIÓN: PRE-CÁLCULO DE EJEMPLOS
# ============================================================================
def generate_examples():
    """
    Pre-calcula las derivadas parciales para todos los ejemplos predefinidos.

    Esta función se ejecuta al iniciar la aplicación para:
    1. Calcular derivadas numéricas de cada función de ejemplo
    2. Validar contra derivadas analíticas
    3. Preparar datos para visualización web

    Retorna:
    --------
    results : list
        Lista de diccionarios, cada uno con los resultados de un ejemplo
        Incluye: datos de malla, derivadas, estadísticas y validación
    """
    results = []

    # Procesar cada ejemplo predefinido
    for example in EXAMPLES:
        print(f"Generando ejemplo: {example['name']}...")

        # Calcular derivadas parciales usando diferencias finitas
        result = calculate_derivatives(
            func_str=example['function'],
            x_min=example['domain']['x_min'],
            x_max=example['domain']['x_max'],
            y_min=example['domain']['y_min'],
            y_max=example['domain']['y_max'],
            nx=example['mesh']['nx'],
            ny=example['mesh']['ny'],
            analytical_dx=example['analytical_dx'],  # Para validación
            analytical_dy=example['analytical_dy']   # Para validación
        )

        # Agregar información adicional del ejemplo
        result['name'] = example['name']
        result['analytical_dx'] = example['analytical_dx']
        result['analytical_dy'] = example['analytical_dy']
        result['description'] = example['description']
        result['id'] = example['id']

        results.append(result)

        # Mostrar métricas de validación en consola (si están disponibles)
        if result.get('validation'):
            val = result['validation']
            print(f"  ✓ Completado - Validación:")
            print(f"    ∂f/∂x: Error máx = {val['df_dx']['max_error_abs']:.2e}, RMSE = {val['df_dx']['rmse']:.2e}")
            print(f"    ∂f/∂y: Error máx = {val['df_dy']['max_error_abs']:.2e}, RMSE = {val['df_dy']['rmse']:.2e}")
        else:
            print(f"  ✓ Completado")

    return results

# ============================================================================
# INICIALIZACIÓN: Pre-calcular ejemplos al iniciar el servidor
# ============================================================================
print("\n🧮 Generando ejemplos de derivadas parciales...")
examples_results = generate_examples()
print("✅ Todos los ejemplos generados\n")

@app.route('/')
def index():
    """Página principal con ejemplos predefinidos"""
    # Convertir los datos a JSON para pasarlos al template
    # allow_nan=False asegura que valores NaN/Infinity causen error en vez de JSON inválido
    # En caso de error, se usa ignore_nan=True como fallback
    try:
        examples_json = json.dumps(examples_results, allow_nan=False)
    except ValueError:
        examples_json = json.dumps(examples_results, ignore_nan=True)

    return render_template('index.html', examples=examples_results, examples_json=examples_json)

@app.route('/about')
def about():
    """Página con información sobre el proyecto"""
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
