import pulp
import pandas as pd

# 1. Cargar datos
visitas = pd.read_csv('data/visitas_anonimizadas.csv').head(10)
tecnicos = pd.read_csv('data/tecnicos_anonimizados.csv').head(5)
distancias = pd.read_csv('data/distancias_zonas.csv', index_col=0)

J = list(visitas['id'])
I = list(tecnicos['id'])

franja = dict(zip(visitas['id'], visitas['franja']))
zona_v = dict(zip(visitas['id'], visitas['zona']))
zona_t = dict(zip(tecnicos['id'], tecnicos['zona']))

comp = {(i, j): (1 if zona_t[i] == zona_v[j] else 0) for i in I for j in J}

def d(j, k):
    if j == k:
        return 0
    return distancias.loc[zona_v[j], zona_v[k]]

# 2. Crear problema
prob = pulp.LpProblem("Colvatel", pulp.LpMinimize)

# 3. Variables
x = {}
for i in I:
    for j in J:
        x[(i, j)] = prob.add_variable(f"x_{i}_{j}", cat="Binary")

carga = {}
for i in I:
    carga[i] = prob.add_variable(f"carga_{i}", lowBound=0, cat="Integer")

d_plus = {}
d_minus = {}
for i in I:
    d_plus[i] = prob.add_variable(f"d_plus_{i}", lowBound=0)
    d_minus[i] = prob.add_variable(f"d_minus_{i}", lowBound=0)

# 4. Funcion objetivo
alpha, beta, q = 10, 3, 5

prob += (
    alpha * pulp.lpSum(d(j, k) * x[(i, j)] for i in I for j in J for k in J if j < k) / max(1, len(J))
    + beta * pulp.lpSum(d_plus[i] + d_minus[i] for i in I)
)

# 5. Restricciones
for j in J:
    prob += pulp.lpSum(x[(i, j)] for i in I) == 1

for i in I:
    prob += carga[i] == pulp.lpSum(x[(i, j)] for j in J)

for i in I:
    prob += carga[i] - q == d_plus[i] - d_minus[i]

for i in I:
    for j in J:
        prob += x[(i, j)] <= comp[(i, j)]

# --- AQUI ESTAN LAS RESTRICCIONES AM/PM QUE PIDIO EL DOCENTE ---
for i in I:
    prob += pulp.lpSum(x[(i, j)] for j in J if str(franja[j]).startswith('AM')) <= 3
    prob += pulp.lpSum(x[(i, j)] for j in J if str(franja[j]).startswith('PM')) <= 3
# ---------------------------------------------------------------

# 6. Resolver
print("Resolviendo...")
stats = prob.solve(pulp.COIN_CMD(msg=0, timeLimit=30))

print(f"Estado: {stats.status_str}")
print(f"Objetivo: {stats.objective}")
print(f"Hay solucion: {stats.has_solution}")

# 7. Guardar resultados
if stats.has_solution:
    resultados = []
    for i in I:
        for j in J:
            val = pulp.value(x[(i, j)])
            if val is not None and val > 0.5:
                resultados.append({
                    'tecnico': i,
                    'visita': j,
                    'franja': franja[j],
                    'zona': zona_v[j]
                })

    df_result = pd.DataFrame(resultados)
    df_result.to_csv('output/asignacion_final.csv', index=False)

    print(f"\nVisitas asignadas: {len(df_result)}")
    print(f"Tecnicos usados: {df_result['tecnico'].nunique()}")
    print("\nCarga por tecnico:")
    print(df_result.groupby('tecnico').size().describe())
    print("\nPrimeras asignaciones:")
    print(df_result.head(10))
else:
 print("El modelo no encontro solucion en el tiempo limite")
    print("El modelo no encontro solucion en el tiempo limite")
