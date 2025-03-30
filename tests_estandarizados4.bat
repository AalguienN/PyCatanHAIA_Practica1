::  --games_per_generation no funciona al ser partidas estandarizadas
:: Prueba 1: Configuración Básica
echo "Test 1: Básico"
py alg_gen.py --extra_name "muchos_estandarizado4" --num_indiv 50 --generations 100 --games_per_agent_standarized 10 --elite_size 2 --tournament_size 5 --mutation_rate 0.5 --mutation_strength 0.1
py generar_graficas.py --extra_name "muchos_estandarizado4"

echo "All tests completed!"
 