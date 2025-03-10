echo "Starting Genetic Algorithm Tests..."

:: Prueba 1: Configuración Básica
echo "Test 1: Basico"
py alg_gen.py --extra_name "basico" --num_indiv 25 --generations 100 --games_per_generation 150 --elite_size 2 --tournament_size 3 --mutation_rate 0.1 --mutation_strength 0.05
py generar_graficas.py --extra_name "basico"

:: Prueba 2: Mayor Diversidad Genética (Más individuos, más mutación)
echo "Test 2: Alta Diversidad"
py alg_gen.py --extra_name "alta_diversidad" --num_indiv 50 --generations 100 --games_per_generation 150 --elite_size 2 --tournament_size 3 --mutation_rate 0.3 --mutation_strength 0.1
py generar_graficas.py --extra_name "alta_diversidad"

:: Prueba 3: Evolución Lenta (Menos mutación y más generaciones)
echo "Test 3: Evolucion Lenta"
py alg_gen.py --extra_name "evolucion_lenta" --num_indiv 25 --generations 200 --games_per_generation 150 --elite_size 2 --tournament_size 3 --mutation_rate 0.05 --mutation_strength 0.02
py generar_graficas.py --extra_name "evolucion_lenta"

:: Prueba 4: Evolución Acelerada (Menos generaciones pero más mutación)
echo "Test 4: Evolucion Rápida"
py alg_gen.py --extra_name "evolucion_rapida" --num_indiv 25 --generations 50 --games_per_generation 150 --elite_size 2 --tournament_size 3 --mutation_rate 0.5 --mutation_strength 0.2
py generar_graficas.py --extra_name "evolucion_rapida"

:: Prueba 5: Pequeña Población (Menos individuos, más presión selectiva)
echo "Test 5: Poblacion Pequeña"
py alg_gen.py --extra_name "poblacion_pequena" --num_indiv 10 --generations 100 --games_per_generation 150 --elite_size 2 --tournament_size 3 --mutation_rate 0.1 --mutation_strength 0.05
py generar_graficas.py --extra_name "poblacion_pequena"

:: Prueba 6: Selección de Torneo Grande (Menos aleatoriedad en la selección)
echo "Test 6: Selección de Torneo Grande"
py alg_gen.py --extra_name "torneo_grande" --num_indiv 25 --generations 100 --games_per_generation 150 --elite_size 2 --tournament_size 8 --mutation_rate 0.1 --mutation_strength 0.05
py generar_graficas.py --extra_name "torneo_grande"

:: Prueba 7: Sin Elitismo (Mayor exploración, pero más riesgo de perder buenos individuos)
echo "Test 7: Sin Elitismo"
py alg_gen.py --extra_name "sin_elitismo" --num_indiv 25 --generations 100 --games_per_generation 150 --elite_size 0 --tournament_size 3 --mutation_rate 0.1 --mutation_strength 0.05
py generar_graficas.py --extra_name "sin_elitismo"

:: Fin de las pruebas
echo "All tests completed!"