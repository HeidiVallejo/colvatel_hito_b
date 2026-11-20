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
Con 10 visitas y 5 técnicos, el modelo asigna todas las visitas.
La carga promedio es de 2 visitas por técnico.
El objetivo óptimo es 135.0.

## Autores
Paola Moreno, Daniel Segura, Heidi Vallejo
