Reporte – Algoritmia y Optimización
Alumno: [tu nombre]  Repositorio: [URL pública de GitHub/GitLab]  Video (≤ 8 min): [enlace]
Todo se reproduce con pip install -r requirements.txt && python run_all.py. Las figuras quedan en results/.
Ejercicio 1 – Aceleración paralela (estimate_pi)
Monte Carlo con 40 M de puntos repartidos en 1, 2, 4 y 8 procesos (multiprocessing.Pool), mediana de 3 corridas. Figura: results/ex1_speedup.png.
⚠️ Reemplaza esta tabla con tus mediciones. Yo ejecuté el código en un entorno con 1 solo núcleo, así que el speedup ahí es ≈ 1 (0.50 s → 0.54 s con 8 procesos): no puede haber paralelismo real sin núcleos físicos. En tu equipo (os.cpu_count() ≥ 8) corre python experiments/ex1_speedup.py y pega aquí tus tiempos.
Procesos	Tiempo (s)	Speedup
1	tuyo	1.00
2	tuyo	tuyo
4	tuyo	tuyo
8	tuyo	tuyo


Análisis. El speedup no es lineal porque: (1) Ley de Amdahl: S(p) = 1 / ((1−f) + f/p); la parte serial (crear el pool, repartir trabajos, sumar los conteos parciales) no se acelera y limita el máximo a 1/(1−f). (2) Sobrecosto de comunicación/creación de procesos: lanzar procesos, serializar argumentos (pickle) y recolectar resultados cuesta tiempo fijo que pesa más cuando hay más procesos. (3) Sincronización: map espera al proceso más lento (barrera final). (4) Recursos compartidos: al pasar de núcleos físicos a hilos lógicos (hyper-threading) o saturar ancho de banda de memoria/caché, cada proceso rinde menos. (5) Si p supera el número de núcleos, solo se añade cambio de contexto.
Ejercicio 2 – Mochila voraz: menor peso vs. valor/peso
Se implementaron ambos criterios en src/knapsack.py. Figura/tabla: results/ex2_knapsack.png.
Instancia A (10 objetos aleatorios, capacidad 40): ambos métodos eligen los mismos 6 objetos (o9, o5, o10, o6, o8, o3), peso usado 39, valor 249. Coinciden, lo cual muestra que el criterio de menor peso a veces "funciona" por casualidad.
Instancia B – contraejemplo diseñado (capacidad 10):
Objeto	Peso	Valor	Valor/peso
A	3	1	0.33
B	4	1	0.25
C	5	50	10.0


Método	Objetos	Capacidad usada	Valor total
Valor/peso	"C, A"	8	51
Menor peso	"A, B"	7	2


El criterio de menor peso llena la mochila con objetos ligeros pero casi sin valor y ya no cabe C, que aporta casi todo el valor. Ignora por completo el valor, de ahí que pueda ser arbitrariamente malo.
Ejercicio 3 – 2-opt (búsqueda local) para TSP
2-opt con primera mejora, 50 instancias aleatorias de 50 ciudades; dos inicios: tour aleatorio vs. Vecino Más Cercano (nodo inicial aleatorio). Figura: results/ex3_2opt.png.
Inicio	Mejoras (media ± d.e.)	Costo inicial medio	Costo del óptimo local (media)
Aleatorio	118.8 ± 10.8	26.28	6.038
Vecino más cercano	17.8 ± 6.0	6.94	5.988


Análisis. Sí: el inicio con Vecino Más Cercano necesita ~6.7 veces menos mejoras (17.8 vs. 118.8) y requirió menos mejoras en 50 de 50 instancias (los boxplots ni se traslapan). Es lógico: NN ya parte de un tour de costo ~6.9, cercano al óptimo local, mientras que el aleatorio parte de ~26.3 y debe "deshacer" muchos cruces. En calidad final, ambos óptimos locales son muy parecidos (5.99 vs. 6.04; diferencia ≈ 0.8 %), con ligera ventaja para NN en este experimento. Es decir, NN ahorra trabajo sin sacrificar calidad.
Ejercicio 4 – Recocido simulado con 2-opt
SA con movimiento 2-opt aleatorio, inicio aleatorio, 50 ciudades, T₀ = 0.5, T_f = 0.005, esquemas lineal, exponencial (T₀·αᵏ) y logarítmico (T₀/(1+c·ln(1+k))), con presupuestos de 20 k, 60 k y 150 k iteraciones y 8 semillas. Figuras: results/ex4_convergence.png, results/ex4_time_quality.png.
Esquema	Costo medio 20k	60k	150k	Tiempo 20k / 60k / 150k (s)
Lineal	6.075	5.496	5.499	0.16 / 0.47 / 1.17
Exponencial	5.477	5.337	5.464	0.16 / 0.46 / 1.15
Logarítmico	5.633	5.576	5.500	0.15 / 0.46 / 1.15


Análisis.
Tiempo de cómputo: prácticamente idéntico entre esquemas (depende del número de iteraciones, no de la forma de T(k)); crece linealmente con las iteraciones. La diferencia está en la calidad por iteración.
Exponencial: mejor y más estable con presupuesto medio/bajo (5.34 ± 0.08 con 60 k): baja rápido de la fase exploratoria a la de refinamiento y dedica muchas iteraciones a temperaturas bajas.
Lineal: gasta una gran parte de las iteraciones a temperaturas altas (curva azul con costos ~20 durante mucho tiempo) y necesita más presupuesto: con 20 k queda en 6.08 (el peor).
Logarítmico (con este c): cae casi de inmediato a un costo bajo (~5.6) y se queda ahí; la temperatura baja tan rápido que se comporta casi como búsqueda local y pierde capacidad de escapar de óptimos locales, de modo que mejora poco al añadir iteraciones.
Matiz estadístico: con 8 semillas la desviación (0.1–0.3) es comparable a varias diferencias; la mejora no monótona de exponencial a 150 k (5.46) es ruido. Conviene más semillas para conclusiones finas.
Ejercicio 5 – Aproximación por MST (TSP métrico)
100 instancias euclidianas aleatorias de 9 ciudades; óptimo exacto con Held-Karp. MST (Prim) + recorrido preorden = 2-aproximación. Figuras: results/ex5_ratio.png, results/ex5_methods.png.
Método	Costo medio	Razón media	Razón máx.	Óptimo en (de 100)
Óptimo (Held-Karp)	2.760	1.000	1.000	100
MST puro	3.196	1.158	1.450	3
MST + 2-opt	2.778	1.007	1.086	74
2-opt (inicio aleatorio)	2.771	1.004	1.063	80
2-opt (inicio NN)	2.776	1.006	1.063	76
"Recocido simulado (exp., 5 000 it.)"	2.760	1.000	1.000	100


Análisis.
Cercanía al límite 2: muy lejos. La razón media de MST es 1.158 y la peor de 100 instancias 1.45, es decir, ~72 % del límite teórico en el peor caso. La cota 2 es de peor caso: exige instancias construidas adversarialmente y en puntos aleatorios casi nunca ocurre.
Impacto de 2-opt como post-proceso: enorme. Baja la razón media de 1.158 a 1.007 y la máxima de 1.45 a 1.09, y lleva a 74 de 100 instancias al óptimo. Queda al nivel de 2-opt desde inicios aleatorios o NN (1.004–1.006): en 9 ciudades todos los óptimos locales están muy cerca del óptimo, por lo que el punto de partida importa poco para la calidad final. El recocido simulado fue el mejor (óptimo en 100/100), a costa de más cómputo. El valor de MST + 2-opt es que parte de una solución con garantía teórica (≤ 2·OPT) y la mejora en pocos pasos.
Salvedad: con n = 9 es difícil diferenciar los métodos locales; para ver diferencias reales hay que usar n mayores (como en los ejercicios 3 y 4).
Conclusiones
Un buen punto de partida (NN) reduce el trabajo de la búsqueda local sin empeorar el resultado; el esquema de enfriamiento determina cuántas iteraciones "útiles" tiene SA; y las garantías de peor caso (factor 2) son muy conservadoras frente al desempeño promedio.
