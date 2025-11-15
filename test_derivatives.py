"""
Tests de verificación para el módulo de derivadas parciales.
Verifica que la implementación cumple con los requisitos de la tarea.
"""

import numpy as np
from derivatives import (
    create_uniform_mesh,
    evaluate_function,
    partial_derivatives_central,
    validate_against_analytical
)


def test_border_duplication():
    """
    Verifica que los bordes estén duplicados correctamente.
    REQUISITO: Bordes deben duplicar valor del vecino, no usar diferencias finitas.
    """
    print("\n" + "="*70)
    print("TEST 1: Verificación de duplicación de bordes")
    print("="*70)

    # Crear malla de prueba
    f = np.random.rand(10, 10)
    hx, hy = 0.1, 0.1

    # Calcular derivadas
    df_dx, df_dy = partial_derivatives_central(f, hx, hy)

    # Verificar duplicación en x (columnas)
    border_left_ok = np.allclose(df_dx[:, 0], df_dx[:, 1])
    border_right_ok = np.allclose(df_dx[:, -1], df_dx[:, -2])

    # Verificar duplicación en y (filas)
    border_bottom_ok = np.allclose(df_dy[0, :], df_dy[1, :])
    border_top_ok = np.allclose(df_dy[-1, :], df_dy[-2, :])

    # Resultados
    print(f"  Borde izquierdo (∂f/∂x):  {'✅ CORRECTO' if border_left_ok else '❌ FALLO'}")
    print(f"  Borde derecho (∂f/∂x):    {'✅ CORRECTO' if border_right_ok else '❌ FALLO'}")
    print(f"  Borde inferior (∂f/∂y):   {'✅ CORRECTO' if border_bottom_ok else '❌ FALLO'}")
    print(f"  Borde superior (∂f/∂y):   {'✅ CORRECTO' if border_top_ok else '❌ FALLO'}")

    all_ok = border_left_ok and border_right_ok and border_bottom_ok and border_top_ok

    if all_ok:
        print("\n  ✅ TEST PASADO: Todos los bordes duplicados correctamente")
    else:
        print("\n  ❌ TEST FALLIDO: Algunos bordes no están duplicados")

    assert all_ok, "Los bordes no están duplicados correctamente"

    return all_ok


def test_dimensions():
    """
    Verifica que las dimensiones de las matrices sean correctas.
    REQUISITO: Las derivadas deben tener las mismas dimensiones que f.
    """
    print("\n" + "="*70)
    print("TEST 2: Verificación de dimensiones")
    print("="*70)

    # Probar varias dimensiones
    test_cases = [(10, 10), (20, 30), (50, 40), (100, 100)]
    all_ok = True

    for ny, nx in test_cases:
        f = np.random.rand(ny, nx)
        hx, hy = 0.1, 0.1

        df_dx, df_dy = partial_derivatives_central(f, hx, hy)

        dim_ok = (df_dx.shape == f.shape) and (df_dy.shape == f.shape)
        status = "✅ CORRECTO" if dim_ok else "❌ FALLO"

        print(f"  Malla {ny}×{nx}: {status}")

        if not dim_ok:
            print(f"    f.shape = {f.shape}")
            print(f"    df_dx.shape = {df_dx.shape}")
            print(f"    df_dy.shape = {df_dy.shape}")

        all_ok = all_ok and dim_ok

    if all_ok:
        print("\n  ✅ TEST PASADO: Todas las dimensiones correctas")
    else:
        print("\n  ❌ TEST FALLIDO: Algunas dimensiones incorrectas")

    assert all_ok, "Las dimensiones de las derivadas son incorrectas"

    return all_ok


def test_central_differences_formula():
    """
    Verifica que la fórmula de diferencias centrales sea correcta en puntos interiores.
    REQUISITO: Usar (f[j, i+1] - f[j, i-1])/(2*hx) para puntos interiores.
    """
    print("\n" + "="*70)
    print("TEST 3: Verificación de fórmula de diferencias centrales")
    print("="*70)

    # Función simple: f(x,y) = x^2 + y^2
    X, Y, hx, hy = create_uniform_mesh(-2, 2, -2, 2, 20, 20)
    Z = X**2 + Y**2

    # Calcular derivadas numéricas
    df_dx, df_dy = partial_derivatives_central(Z, hx, hy)

    # Calcular manualmente en punto interior (centro de la malla)
    i, j = 10, 10  # Punto interior
    expected_dx = (Z[i, j+1] - Z[i, j-1]) / (2 * hx)
    expected_dy = (Z[i+1, j] - Z[i-1, j]) / (2 * hy)

    dx_ok = np.isclose(df_dx[i, j], expected_dx)
    dy_ok = np.isclose(df_dy[i, j], expected_dy)

    print(f"  ∂f/∂x en punto interior: {'✅ CORRECTO' if dx_ok else '❌ FALLO'}")
    print(f"    Calculado: {df_dx[i, j]:.6f}")
    print(f"    Esperado:  {expected_dx:.6f}")

    print(f"  ∂f/∂y en punto interior: {'✅ CORRECTO' if dy_ok else '❌ FALLO'}")
    print(f"    Calculado: {df_dy[i, j]:.6f}")
    print(f"    Esperado:  {expected_dy:.6f}")

    all_ok = dx_ok and dy_ok

    if all_ok:
        print("\n  ✅ TEST PASADO: Fórmula de diferencias centrales correcta")
    else:
        print("\n  ❌ TEST FALLIDO: Fórmula incorrecta")

    assert all_ok, "La fórmula de diferencias centrales es incorrecta"

    return all_ok


def test_analytical_comparison():
    """
    Verifica que las derivadas numéricas coincidan con las analíticas.
    REQUISITO: Comparar resultados numéricos vs analíticos.
    """
    print("\n" + "="*70)
    print("TEST 4: Comparación con derivadas analíticas")
    print("="*70)

    # Función: f(x,y) = sin(x)*cos(y)
    # ∂f/∂x = cos(x)*cos(y)
    # ∂f/∂y = -sin(x)*sin(y)

    X, Y, hx, hy = create_uniform_mesh(-2, 2, -2, 2, 100, 100)
    Z = np.sin(X) * np.cos(Y)

    # Derivadas numéricas
    df_dx_num, df_dy_num = partial_derivatives_central(Z, hx, hy)

    # Derivadas analíticas
    df_dx_exact = np.cos(X) * np.cos(Y)
    df_dy_exact = -np.sin(X) * np.sin(Y)

    # Calcular errores (solo puntos interiores)
    error_dx = np.abs(df_dx_num[1:-1, 1:-1] - df_dx_exact[1:-1, 1:-1])
    error_dy = np.abs(df_dy_num[1:-1, 1:-1] - df_dy_exact[1:-1, 1:-1])

    max_error_dx = np.max(error_dx)
    max_error_dy = np.max(error_dy)

    # Tolerancia para diferencias finitas de segundo orden: O(h^2)
    tolerance = 0.01

    dx_ok = max_error_dx < tolerance
    dy_ok = max_error_dy < tolerance

    print(f"  ∂f/∂x: Error máximo = {max_error_dx:.2e} {'✅ CORRECTO' if dx_ok else '❌ FALLO'}")
    print(f"  ∂f/∂y: Error máximo = {max_error_dy:.2e} {'✅ CORRECTO' if dy_ok else '❌ FALLO'}")
    print(f"  Tolerancia: {tolerance:.2e}")

    all_ok = dx_ok and dy_ok

    if all_ok:
        print("\n  ✅ TEST PASADO: Derivadas numéricas precisas")
    else:
        print("\n  ❌ TEST FALLIDO: Error excede tolerancia")

    assert all_ok, "Las derivadas numéricas difieren demasiado de las analíticas"

    return all_ok


def test_validation_function():
    """
    Verifica que la función de validación funcione correctamente.
    """
    print("\n" + "="*70)
    print("TEST 5: Verificación de función validate_against_analytical")
    print("="*70)

    # Crear datos de prueba
    X, Y, hx, hy = create_uniform_mesh(-2, 2, -2, 2, 50, 50)
    Z = X**2 + Y**2

    # Derivadas numéricas
    df_dx_num, df_dy_num = partial_derivatives_central(Z, hx, hy)

    # Validar contra derivadas analíticas
    try:
        validation = validate_against_analytical(
            X, Y, df_dx_num, df_dy_num,
            '2*x', '2*y'
        )

        print("  Métricas de validación para ∂f/∂x:")
        print(f"    Error máximo absoluto:  {validation['df_dx']['max_error_abs']:.2e}")
        print(f"    Error promedio absoluto: {validation['df_dx']['mean_error_abs']:.2e}")
        print(f"    RMSE: {validation['df_dx']['rmse']:.2e}")

        print("  Métricas de validación para ∂f/∂y:")
        print(f"    Error máximo absoluto:  {validation['df_dy']['max_error_abs']:.2e}")
        print(f"    Error promedio absoluto: {validation['df_dy']['mean_error_abs']:.2e}")
        print(f"    RMSE: {validation['df_dy']['rmse']:.2e}")

        print("\n  ✅ TEST PASADO: Función de validación funciona correctamente")
        return True

    except Exception as e:
        print(f"\n  ❌ TEST FALLIDO: Error en función de validación: {str(e)}")
        return False


def run_all_tests():
    """
    Ejecuta todos los tests de verificación.
    """
    print("\n" + "="*70)
    print("SUITE DE TESTS: Verificación de Derivadas Parciales")
    print("="*70)
    print("Verificando cumplimiento de requisitos de la tarea...")

    tests = [
        test_border_duplication,
        test_dimensions,
        test_central_differences_formula,
        test_analytical_comparison,
        test_validation_function
    ]

    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except AssertionError as e:
            print(f"\n  ⚠️  Assertion Error: {str(e)}")
            results.append(False)
        except Exception as e:
            print(f"\n  ⚠️  Error inesperado: {str(e)}")
            results.append(False)

    # Resumen final
    print("\n" + "="*70)
    print("RESUMEN DE TESTS")
    print("="*70)

    passed = sum(results)
    total = len(results)

    print(f"\nTests pasados: {passed}/{total}")

    if all(results):
        print("\n🎉 ¡TODOS LOS TESTS PASARON!")
        print("✅ La implementación cumple con todos los requisitos de la tarea")
    else:
        print("\n⚠️  ALGUNOS TESTS FALLARON")
        print("Por favor, revisa los errores arriba")

    print("\n" + "="*70 + "\n")

    return all(results)


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
