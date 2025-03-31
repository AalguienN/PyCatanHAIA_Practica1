::  --games_per_generation no funciona al ser partidas estandarizadas
:: Prueba 1: Configuración Básica
echo "Test 1: Básico"
py alg_gen.py --extra_name "small_estandarizado" --num_indiv 10 --generations 5 --games_per_agent_standarized 5 --elite_size 2 --tournament_size 1 --mutation_rate 0.5 --mutation_strength 0.1
py generar_graficas.py --extra_name "small_estandarizado"

echo "All tests completed!"
 