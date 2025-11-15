"""
Módulo para calcular derivadas parciales usando diferencias finitas centrales
en una malla uniformemente espaciada.

Este módulo implementa el método de diferencias finitas centrales de segundo orden
para calcular las derivadas parciales ∂f/∂x y ∂f/∂y de funciones de dos variables.
"""

# ============================================================================
# IMPORTACIONES
# ============================================================================
import numpy as np


# ============================================================================
# FUNCIÓN 1: CREACIÓN DE MALLA UNIFORME
# ============================================================================
def create_uniform_mesh(x_min, x_max, y_min, y_max, nx, ny):
    """
    Crea una malla uniformemente espaciada en el dominio rectangular [x_min, x_max] × [y_min, y_max].

    Esta función usa numpy.linspace para crear vectores igualmente espaciados y
    numpy.meshgrid para generar matrices 2D de coordenadas.

    Parámetros:
    -----------
    x_min, x_max : float
        Límites del dominio en dirección x
    y_min, y_max : float
        Límites del dominio en dirección y
    nx, ny : int
        Número de puntos en cada dirección

    Retorna:
    --------
    X, Y : numpy.ndarray (2D)
        Matrices de coordenadas de forma (ny, nx)
        X[i,j] contiene la coordenada x del punto (i,j)
        Y[i,j] contiene la coordenada y del punto (i,j)
    hx, hy : float
        Espaciamientos uniformes de la malla
        hx = (x_max - x_min) / (nx - 1)
        hy = (y_max - y_min) / (ny - 1)

    Ejemplo:
    --------
    >>> X, Y, hx, hy = create_uniform_mesh(-2, 2, -1, 1, 5, 3)
    >>> print(hx, hy)
    1.0 1.0
    """
    # Crear vectores igualmente espaciados usando linspace
    x = np.linspace(x_min, x_max, nx)  # Vector de nx puntos en [x_min, x_max]
    y = np.linspace(y_min, y_max, ny)  # Vector de ny puntos en [y_min, y_max]

    # Crear matrices 2D de coordenadas usando meshgrid
    # X tiene forma (ny, nx) con valores de x repetidos en filas
    # Y tiene forma (ny, nx) con valores de y repetidos en columnas
    X, Y = np.meshgrid(x, y)

    # Calcular espaciamientos (distancia entre puntos consecutivos)
    hx = x[1] - x[0]  # Espaciamiento en x
    hy = y[1] - y[0]  # Espaciamiento en y

    return X, Y, hx, hy


# ============================================================================
# FUNCIÓN 2: EVALUACIÓN SEGURA DE FUNCIONES
# ============================================================================
def evaluate_function(func_str, X, Y):
    """
    Evalúa una función matemática (dada como string) en todos los puntos de la malla.

    Esta función usa eval() de forma segura, limitando el acceso solo a funciones
    matemáticas específicas de NumPy. Esto previene la ejecución de código malicioso.

    Parámetros:
    -----------
    func_str : str
        Función a evaluar como string
        Ejemplos: "sin(x)*cos(y)", "x**2 + y**2", "exp(-x**2 - y**2)"
    X, Y : numpy.ndarray (2D)
        Matrices de coordenadas donde evaluar la función

    Retorna:
    --------
    Z : numpy.ndarray (2D)
        Matriz con los valores de f(x,y) evaluados en cada punto
        Z[i,j] = f(X[i,j], Y[i,j])

    Excepciones:
    ------------
    ValueError
        Si la función contiene sintaxis inválida o funciones no permitidas

    Ejemplo:
    --------
    >>> X, Y, _, _ = create_uniform_mesh(0, 1, 0, 1, 3, 3)
    >>> Z = evaluate_function("x**2 + y**2", X, Y)
    """
    # Diccionario seguro: solo permite funciones matemáticas específicas
    # Esto previene ejecución de código arbitrario o malicioso
    safe_dict = {
        # Funciones trigonométricas
        'sin': np.sin,
        'cos': np.cos,
        'tan': np.tan,
        # Funciones exponenciales y logarítmicas
        'exp': np.exp,
        'log': np.log,
        # Otras funciones matemáticas
        'sqrt': np.sqrt,
        'abs': np.abs,
        # Constantes matemáticas
        'pi': np.pi,
        'e': np.e,
        # Variables de la malla
        'x': X,
        'y': Y,
        'X': X,
        'Y': Y
    }

    try:
        # Evaluar la función de forma segura
        # __builtins__ vacío previene acceso a funciones peligrosas como open(), exec(), etc.
        Z = eval(func_str, {"__builtins__": {}}, safe_dict)
        return Z
    except Exception as e:
        raise ValueError(f"Error al evaluar la función '{func_str}': {str(e)}")


# ============================================================================
# FUNCIÓN 3: CÁLCULO DE DERIVADAS PARCIALES (DIFERENCIAS FINITAS CENTRALES)
# ============================================================================
def partial_derivatives_central(f, hx, hy):
    """
    Calcula las derivadas parciales ∂f/∂x y ∂f/∂y usando diferencias finitas centrales de segundo orden.

    MÉTODO:
    -------
    - Puntos INTERIORES: Usa diferencias centrales de segundo orden (O(h²))
      ∂f/∂x ≈ (f[i, j+1] - f[i, j-1]) / (2*hx)
      ∂f/∂y ≈ (f[i+1, j] - f[i-1, j]) / (2*hy)

    - Puntos BORDE: Duplica el valor del vecino inmediato
      Primer punto = Segundo punto
      Último punto = Penúltimo punto

    IMPORTANTE:
    -----------
    Este método NO usa diferencias forward/backward en los bordes.
    Los bordes se manejan copiando el valor ya calculado del vecino.

    Parámetros:
    -----------
    f : numpy.ndarray (2D)
        Valores de la función f(x,y) en la malla
        Forma: (ny, nx)
    hx, hy : float
        Espaciamientos de la malla en x e y respectivamente

    Retorna:
    --------
    df_dx : numpy.ndarray (2D)
        Derivada parcial ∂f/∂x en cada punto
        Forma: (ny, nx), igual que f
    df_dy : numpy.ndarray (2D)
        Derivada parcial ∂f/∂y en cada punto
        Forma: (ny, nx), igual que f

    Ejemplo:
    --------
    >>> X, Y, hx, hy = create_uniform_mesh(-1, 1, -1, 1, 5, 5)
    >>> f = X**2 + Y**2  # Función f(x,y) = x² + y²
    >>> df_dx, df_dy = partial_derivatives_central(f, hx, hy)
    >>> # df_dx ≈ 2x, df_dy ≈ 2y
    """
    # Inicializar matrices vacías con las mismas dimensiones que f
    df_dx = np.zeros_like(f)  # Para almacenar ∂f/∂x
    df_dy = np.zeros_like(f)  # Para almacenar ∂f/∂y

    # Obtener dimensiones de la malla
    ny, nx = f.shape  # ny = número de filas, nx = número de columnas

    # ========================================================================
    # CÁLCULO DE ∂f/∂x (derivada respecto a x)
    # ========================================================================
    # Trabajamos por COLUMNAS (variación en dirección x)

    # PUNTOS INTERIORES (columnas 1 hasta nx-2)
    # Fórmula: ∂f/∂x ≈ (f[i, j+1] - f[i, j-1]) / (2*hx)
    # Slicing: [:, 1:-1] selecciona todas las filas, columnas interiores
    #          [:, 2:]   selecciona f[i, j+1] (desplazamiento a la derecha)
    #          [:, :-2]  selecciona f[i, j-1] (desplazamiento a la izquierda)
    df_dx[:, 1:-1] = (f[:, 2:] - f[:, :-2]) / (2 * hx)

    # BORDES EN X
    # Borde izquierdo (columna 0): duplicar del vecino (columna 1)
    # NO usamos diferencias finitas aquí, solo copiamos el valor
    df_dx[:, 0] = df_dx[:, 1]  # Primer columna = Segunda columna

    # Borde derecho (columna nx-1): duplicar del vecino (columna nx-2)
    df_dx[:, -1] = df_dx[:, -2]  # Última columna = Penúltima columna

    # ========================================================================
    # CÁLCULO DE ∂f/∂y (derivada respecto a y)
    # ========================================================================
    # Trabajamos por FILAS (variación en dirección y)

    # PUNTOS INTERIORES (filas 1 hasta ny-2)
    # Fórmula: ∂f/∂y ≈ (f[i+1, j] - f[i-1, j]) / (2*hy)
    # Slicing: [1:-1, :] selecciona filas interiores, todas las columnas
    #          [2:, :]   selecciona f[i+1, j] (desplazamiento hacia abajo)
    #          [:-2, :]  selecciona f[i-1, j] (desplazamiento hacia arriba)
    df_dy[1:-1, :] = (f[2:, :] - f[:-2, :]) / (2 * hy)

    # BORDES EN Y
    # Borde inferior (fila 0): duplicar del vecino (fila 1)
    df_dy[0, :] = df_dy[1, :]  # Primera fila = Segunda fila

    # Borde superior (fila ny-1): duplicar del vecino (fila ny-2)
    df_dy[-1, :] = df_dy[-2, :]  # Última fila = Penúltima fila

    return df_dx, df_dy


# ============================================================================
# FUNCIÓN 4: VALIDACIÓN CON DERIVADAS ANALÍTICAS
# ============================================================================
def validate_against_analytical(X, Y, df_dx_num, df_dy_num, analytical_dx_str, analytical_dy_str):
    """
    Valida las derivadas numéricas comparándolas con las derivadas analíticas exactas.

    Esta función calcula varias métricas de error para cuantificar la precisión
    del método de diferencias finitas:
    - Error absoluto: |numérico - exacto|
    - Error relativo: |numérico - exacto| / |exacto|
    - Norma L2: √(Σ error²)
    - RMSE: Raíz del error cuadrático medio

    Parámetros:
    -----------
    X, Y : numpy.ndarray (2D)
        Matrices de coordenadas de la malla
    df_dx_num, df_dy_num : numpy.ndarray (2D)
        Derivadas parciales calculadas numéricamente
    analytical_dx_str, analytical_dy_str : str
        Expresiones de las derivadas analíticas exactas
        Ejemplo: Para f(x,y) = sin(x)*cos(y)
                 analytical_dx_str = "cos(x)*cos(y)"
                 analytical_dy_str = "-sin(x)*sin(y)"

    Retorna:
    --------
    validation : dict
        Diccionario con 2 claves ('df_dx', 'df_dy'), cada una con:
        - 'max_error_abs': Error absoluto máximo
        - 'mean_error_abs': Error absoluto promedio
        - 'max_error_rel': Error relativo máximo
        - 'mean_error_rel': Error relativo promedio
        - 'l2_norm': Norma L2 del error
        - 'rmse': Raíz del error cuadrático medio

    Ejemplo:
    --------
    >>> val = validate_against_analytical(X, Y, df_dx, df_dy, "2*x", "2*y")
    >>> print(f"Error máximo en ∂f/∂x: {val['df_dx']['max_error_abs']:.2e}")
    """
    # Evaluar las derivadas analíticas exactas en todos los puntos de la malla
    df_dx_exact = evaluate_function(analytical_dx_str, X, Y)
    df_dy_exact = evaluate_function(analytical_dy_str, X, Y)

    # ========================================================================
    # CÁLCULO DE ERRORES ABSOLUTOS
    # ========================================================================
    # Error absoluto = |valor_numérico - valor_exacto|
    error_dx = np.abs(df_dx_num - df_dx_exact)
    error_dy = np.abs(df_dy_num - df_dy_exact)

    # ========================================================================
    # CÁLCULO DE ERRORES RELATIVOS
    # ========================================================================
    # Error relativo = |error_absoluto| / |valor_exacto|
    # Sumamos 1e-10 para evitar división por cero cuando el valor exacto es muy pequeño
    error_rel_dx = error_dx / (np.abs(df_dx_exact) + 1e-10)
    error_rel_dy = error_dy / (np.abs(df_dy_exact) + 1e-10)

    # ========================================================================
    # GENERAR MÉTRICAS DE VALIDACIÓN
    # ========================================================================
    validation = {
        'df_dx': {
            'max_error_abs': float(np.max(error_dx)),      # Máximo error absoluto
            'mean_error_abs': float(np.mean(error_dx)),    # Promedio de errores absolutos
            'max_error_rel': float(np.max(error_rel_dx)),  # Máximo error relativo
            'mean_error_rel': float(np.mean(error_rel_dx)),# Promedio de errores relativos
            'l2_norm': float(np.linalg.norm(error_dx)),    # Norma L2 del error
            'rmse': float(np.sqrt(np.mean(error_dx**2)))   # Raíz del error cuadrático medio
        },
        'df_dy': {
            'max_error_abs': float(np.max(error_dy)),
            'mean_error_abs': float(np.mean(error_dy)),
            'max_error_rel': float(np.max(error_rel_dy)),
            'mean_error_rel': float(np.mean(error_rel_dy)),
            'l2_norm': float(np.linalg.norm(error_dy)),
            'rmse': float(np.sqrt(np.mean(error_dy**2)))
        }
    }

    return validation


# ============================================================================
# FUNCIÓN 5: FUNCIÓN PRINCIPAL - CÁLCULO COMPLETO DE DERIVADAS PARCIALES
# ============================================================================
def calculate_derivatives(func_str, x_min=-2, x_max=2, y_min=-2, y_max=2, nx=100, ny=100,
                         analytical_dx=None, analytical_dy=None):
    """
    Función principal que realiza el proceso completo de cálculo de derivadas parciales.

    Esta función orquesta todo el proceso:
    1. Crear malla uniformemente espaciada
    2. Evaluar la función f(x,y) en todos los puntos
    3. Calcular derivadas parciales con diferencias finitas centrales
    4. Validar contra derivadas analíticas (si se proporcionan)
    5. Preparar datos en formato JSON para visualización web con Plotly

    Parámetros:
    -----------
    func_str : str
        Expresión de la función f(x,y) a derivar
        Ejemplo: "sin(x)*cos(y)", "x**2 + y**2"
    x_min, x_max : float, optional
        Límites del dominio en dirección x (default: -2, 2)
    y_min, y_max : float, optional
        Límites del dominio en dirección y (default: -2, 2)
    nx, ny : int, optional
        Número de puntos en cada dirección (default: 100)
    analytical_dx, analytical_dy : str, optional
        Expresiones de las derivadas analíticas para validación
        Si se proporcionan, se calculan métricas de error

    Retorna:
    --------
    result : dict
        Diccionario con todos los resultados, listo para JSON:
        - 'function': Expresión de f(x,y)
        - 'domain': Límites del dominio
        - 'mesh': Información de la malla (nx, ny, hx, hy)
        - 'plot_data': Datos para gráficos (X, Y, Z, df_dx, df_dy, vectores)
        - 'stats': Estadísticas (min, max de f, ∂f/∂x, ∂f/∂y)
        - 'validation': Métricas de error (si se proporcionaron derivadas analíticas)

    Ejemplo:
    --------
    >>> result = calculate_derivatives("x**2 + y**2", -3, 3, -3, 3, 50, 50,
    ...                               analytical_dx="2*x", analytical_dy="2*y")
    >>> print(f"Error máximo: {result['validation']['df_dx']['max_error_abs']:.2e}")
    """
    # ========================================================================
    # PASO 1: Crear malla uniformemente espaciada
    # ========================================================================
    X, Y, hx, hy = create_uniform_mesh(x_min, x_max, y_min, y_max, nx, ny)

    # ========================================================================
    # PASO 2: Evaluar función f(x,y) en todos los puntos de la malla
    # ========================================================================
    Z = evaluate_function(func_str, X, Y)

    # ========================================================================
    # PASO 3: Calcular derivadas parciales con diferencias finitas centrales
    # ========================================================================
    df_dx, df_dy = partial_derivatives_central(Z, hx, hy)

    # ========================================================================
    # PASO 4: Validación contra derivadas analíticas (opcional)
    # ========================================================================
    validation = None
    if analytical_dx and analytical_dy:
        try:
            validation = validate_against_analytical(X, Y, df_dx, df_dy,
                                                    analytical_dx, analytical_dy)
        except Exception as e:
            # Si hay error en la validación, continuar sin ella
            print(f"Error en validación: {str(e)}")
            validation = None

    # ========================================================================
    # PASO 5: Preparar resultado en formato JSON para la aplicación web
    # ========================================================================
    # Convertir arrays de NumPy a listas de Python (JSON-serializable)
    result = {
        'function': func_str,
        'domain': {
            'x_min': x_min,
            'x_max': x_max,
            'y_min': y_min,
            'y_max': y_max
        },
        'mesh': {
            'nx': nx,
            'ny': ny,
            'hx': hx,
            'hy': hy
        },
        'plot_data': {
            # Matrices completas para visualización 3D
            'X': X.tolist(),
            'Y': Y.tolist(),
            'Z': Z.tolist(),
            'df_dx': df_dx.tolist(),
            'df_dy': df_dy.tolist(),
            # Vectores 1D para ejes de gráficos de contorno
            'x_vector': np.linspace(x_min, x_max, nx).tolist(),
            'y_vector': np.linspace(y_min, y_max, ny).tolist()
        },
        'stats': {
            # Estadísticas de la función
            'f_min': float(np.min(Z)),
            'f_max': float(np.max(Z)),
            # Estadísticas de las derivadas
            'df_dx_min': float(np.min(df_dx)),
            'df_dx_max': float(np.max(df_dx)),
            'df_dy_min': float(np.min(df_dy)),
            'df_dy_max': float(np.max(df_dy))
        },
        # Métricas de validación (None si no se proporcionaron derivadas analíticas)
        'validation': validation
    }

    return result
