::  --games_per_generation no funciona al ser partidas estandarizadas
:: Prueba 1: Configuración Básica
echo "Test 1: Básico"
py alg_gen.py --extra_name "basico_estandarizado" --num_indiv 25 --generations 100 --games_per_agent_standarized 5 --elite_size 2 --tournament_size 3 --mutation_rate 0.1 --mutation_strength 0.05
py generar_graficas.py --extra_name "basico_estandarizado"

:: Prueba 2: Mayor Diversidad Genética
echo "Test 2: Alta Diversidad"
py alg_gen.py --extra_name "alta_diversidad_estandarizado" --num_indiv 50 --generations 100 --games_per_agent_standarized 5 --elite_size 2 --tournament_size 3 --mutation_rate 0.3 --mutation_strength 0.1
py generar_graficas.py --extra_name "alta_diversidad_estandarizado"

:: Prueba 3: Evolución Lenta (baja mutación, más generaciones)
echo "Test 3: Evolucion Lenta"
py alg_gen.py --extra_name "evolucion_lenta_estandarizado" --num_indiv 25 --generations 200 --games_per_agent_standarized 5 --elite_size 2 --tournament_size 3 --mutation_rate 0.05 --mutation_strength 0.02
py generar_graficas.py --extra_name "evolucion_lenta_estandarizado"

echo "All tests completed!"
