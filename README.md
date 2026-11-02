# Hito B - Colvatel S.A.S.

## Descripcion
Modelo de asignacion diaria de visitas tecnicas con PuLP 4.0.

## Requisitos
pip install -r requirements.txt

## Ejecucion
python src/modelo.py
python src/verificar.py

## Estructura
- data/: datos anonimizados
- src/: codigo del modelo
- output/: resultados

## Hallazgos
- Con 10 visitas y 5 tecnicos, el modelo asigna todas las visitas.
- La carga promedio es de X visitas por tecnico.
- El objetivo optimo es Y.

## Autores
Paola Moreno, Daniel Segura, Heidi Vallejo