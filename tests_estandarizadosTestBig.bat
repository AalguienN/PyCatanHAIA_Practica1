::  --games_per_generation no funciona al ser partidas estandarizadas
:: Prueba 1: Configuración Básica
@REM echo "Test 1: Rápido"
@REM py alg_gen.py --extra_name "small_estandarizado" --num_indiv 25 --generations 50 --games_per_agent_standarized 10 --elite_size 2 --tournament_size 1 --mutation_rate 0.5 --mutation_strength 0.1
@REM py generar_graficas.py --extra_name "small_estandarizado"

@REM echo "Test 2: Medio"
@REM py alg_gen.py --extra_name "muchos_estandarizado4" --num_indiv 50 --generations 150 --games_per_agent_standarized 20 --elite_size 2 --tournament_size 5 --mutation_rate 0.5 --mutation_strength 0.1
@REM py generar_graficas.py --extra_name "muchos_estandarizado4"

echo "Test 3: Robusto"
py alg_gen.py --extra_name "muchos_estandarizado4" --num_indiv 100 --generations 200 --games_per_agent_standarized 20 --elite_size 2 --tournament_size 5 --mutation_rate 0.25 --mutation_strength 0.05
py generar_graficas.py --extra_name "muchos_estandarizado4"

echo "All tests completed!"
 