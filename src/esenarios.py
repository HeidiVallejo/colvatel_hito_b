import pulp
import pandas as pd

# Función para correr el modelo con parámetros modificables
def resolver_modelo(alpha, beta, q, cap_am, cap_pm, nombre):
    visitas = pd.read_csv('data/visitas_anonimizadas.csv').head(10)
    tecnicos = pd.read_csv('data/tecnicos_anonimizados.csv').head(5)
    distancias = pd.read_csv('data/distancias_zonas.csv', index_col=0)
    
    J = list(visitas['id'])
    I = list(tecnicos['id'])
    franja = dict(zip(visitas['id'], visitas['franja']))
    zona_v = dict(zip(visitas['id'], visitas['zona']))
    zona_t = dict(zip(tecnicos['id'], tecnicos['zona']))
    
    def d(j, k):
        if j == k: return 0
        return distancias.loc[zona_v[j], zona_v[k]]

    prob = pulp.LpProblem(f"Colvatel_{nombre}", pulp.LpMinimize)
    
    x = {(i, j): prob.add_variable(f"x_{i}_{j}", cat="Binary") for i in I for j in J}
    carga = {i: prob.add_variable(f"carga_{i}", lowBound=0, cat="Integer") for i in I}
    d_plus = {i: prob.add_variable(f"d_plus_{i}", lowBound=0) for i in I}
    d_minus = {i: prob.add_variable(f"d_minus_{i}", lowBound=0) for i in I}

    prob += (
        alpha * pulp.lpSum(d(j, k) * x[(i, j)] for i in I for j in J for k in J if j < k) / max(1, len(J))
        + beta * pulp.lpSum(d_plus[i] + d_minus[i] for i in I)
    )

    for j in J:
        prob += pulp.lpSum(x[(i, j)] for i in I) == 1

    for i in I:
        prob += carga[i] == pulp.lpSum(x[(i, j)] for j in J)
        prob += carga[i] - q == d_plus[i] - d_minus[i]

    # Restricciones de capacidad AM/PM
    for i in I:
        prob += pulp.lpSum(x[(i, j)] for j in J if str(franja[j]).startswith('AM')) <= cap_am
        prob += pulp.lpSum(x[(i, j)] for j in J if str(franja[j]).startswith('PM')) <= cap_pm

    # Resolver silenciosamente
    prob.solve(pulp.PULP_CBC_CMD(msg=0))
    
    if pulp.LpStatus[prob.status] == 'Optimal':
        asignaciones = sum(pulp.value(x[(i, j)]) for i in I for j in J)
        print(f"--- {nombre} ---")
        print(f"Estado: Optimal | Objetivo: {pulp.value(prob.objective)}")
        print(f"Visitas asignadas: {int(asignaciones)}")
        for i in I:
            print(f"  Técnico {i}: {int(pulp.value(carga[i]))} visitas")
        print("\n")
    else:
        print(f"--- {nombre} ---")
        print("No se encontró solución factible con estos parámetros.\n")

# 1. Escenario Base
print("=== ESCENARIOS HITO C ===\n")
resolver_modelo(alpha=10, beta=3, q=5, cap_am=3, cap_pm=3, nombre="Base (Original)")

# 2. Escenario 1: Capacidad AM/PM más restrictiva
# ¿Qué pasa si los técnicos solo pueden hacer máximo 1 visita AM y 1 PM al día?
resolver_modelo(alpha=10, beta=3, q=5, cap_am=1, cap_pm=1, nombre="Restricción de Capacidad (AM max 1, PM max 1)")

# 3. Escenario 2: Equilibrar la carga (Cambiar q a 2)
# Como son 10 visitas y 5 técnicos, el promedio real es 2. Cambiamos la meta de 5 a 2.
resolver_modelo(alpha=10, beta=3, q=2, cap_am=3, cap_pm=3, nombre="Equilibrio de carga (q=2)")

# 4. Escenario 3: Priorizar la distancia sobre la carga
# Aumentamos alpha (distancia) y bajamos beta (desviación de carga)
resolver_modelo(alpha=100, beta=1, q=5, cap_am=3, cap_pm=3, nombre="Priorizar distancia (alpha=100, beta=1)")
