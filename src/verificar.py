# verificar.py
# Verificacion de restricciones - Hito B
# Ejecutar desde la raiz del repositorio:
#   python src/verificar.py

import pandas as pd

asignacion = pd.read_csv('output/asignacion_final.csv')
visitas = pd.read_csv('data/visitas_anonimizadas.csv').head(10)

print("=" * 60)
print("VERIFICACION DE RESTRICCIONES")
print("=" * 60)

# R1. Cobertura total
asignadas = asignacion['visita'].nunique()
total = len(visitas)
print(f"\nR1. Visitas asignadas: {asignadas}/{total}")
print("  OK" if asignadas == total else f"  FALLA: faltan {total - asignadas}")

# R2. Sin duplicados
duplicadas = asignacion[asignacion.duplicated('visita')]
print(f"\nR2. Visitas duplicadas: {len(duplicadas)}")
print("  OK" if len(duplicadas) == 0 else "  FALLA")

# R3. Carga por tecnico
carga = asignacion.groupby('tecnico').size()
print(f"\nR3. Carga por tecnico:")
print(carga.describe())

# R14. Capacidad AM/PM
print(f"\nR14. Capacidad por franja:")
fallas = 0
for tec in asignacion['tecnico'].unique():
    sub = asignacion[asignacion['tecnico'] == tec]
    am = len(sub[sub['franja'].isin(['AM4', 'AM_R', 'AM1'])])
    pm = len(sub[sub['franja'] == 'PM3'])
    if am > 3 or pm > 3:
        print(f"  FALLA en {tec}: AM={am}, PM={pm}")
        fallas += 1
if fallas == 0:
    print("  OK")

print("\n" + "=" * 60)
print("VERIFICACION COMPLETA")
print("=" * 60)