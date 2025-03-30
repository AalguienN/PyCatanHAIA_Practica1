::  --games_per_generation no funciona al ser partidas estandarizadas
:: Prueba 1: Configuración Básica
echo "Test 1: Básico"
py alg_gen.py --extra_name "muchos_estandarizado2" --num_indiv 80 --generations 50 --games_per_agent_standarized 8 --elite_size 3 --tournament_size 10 --mutation_rate 0.5 --mutation_strength 0.1
py generar_graficas.py --extra_name "muchos_estandarizado2"

echo "All tests completed!"
 