import simpy
import numpy as np

np.random.seed(11)

# Parametros de la simulacion
TIEMPO_SIMULACION = 10 * 60                                     # Duración de la simulación: 10 horas convertidas a minutos
TASA_LLAMADAS = 7                                               # Promedio de llegada de llamadas: 7 llamadas por minuto
PORCENTAJE_SOPORTE_TECNICO = 0.45                               # Porcentaje de llamadas dirigidas al soporte técnico
TIEMPO_SERVICIO_SOPORTE = 10                                    # Tiempo de servicio para el soporte técnico: 10 minutos
TIEMPO_SERVICIO_INFORMACION = 7                                 # Tiempo de servicio para información: 7 minutos
TIEMPO_EVALUACION_MEDIA = 1                                     # Media del tiempo de evaluación: 1 minuto
TIEMPO_EVALUACION_DESVIACION = TIEMPO_EVALUACION_MEDIA * 0.1     # Desviación del tiempo de evaluación: 10% de la media

# Estructuras para recopilar datos de desempeno
tiempos_en_cola = {"soporte": [], "informacion": [], "evaluacion": []}  # Tiempos en cola para cada tipo de llamada
tiempos_en_sistema = []                                                 # Tiempos totales en el sistema

# Variables para seguimiento de tiempos de ocio y de servicio
ultimo_tiempo_salida = {"soporte": 0, "informacion": 0, "evaluacion": 0}  # Último tiempo de salida para cada tipo de llamada
tiempo_ocio = {"soporte": 0, "informacion": 0, "evaluacion": 0}            # Tiempo de ocio para cada tipo de agente
tiempo_servicio = {"soporte": 0, "informacion": 0, "evaluacion": 0}        # Tiempo de servicio para cada tipo de agente

def generar_tiempo_llegada():
    """Genera un tiempo entre llegadas con distribucion exponencial."""
    return np.random.exponential(TASA_LLAMADAS)

def generar_tiempo_servicio(tipo):
    """Genera un tiempo de servicio con distribucion exponencial segun el tipo de llamada."""
    if tipo == "soporte":
        return np.random.exponential(TIEMPO_SERVICIO_SOPORTE)
    else:
        return np.random.exponential(TIEMPO_SERVICIO_INFORMACION)

def evaluacion_cliente():
    """Genera un tiempo de evaluacion con distribucion normal."""
    return max(0, np.random.normal(TIEMPO_EVALUACION_MEDIA, TIEMPO_EVALUACION_DESVIACION))

def llamada(env, nombre, tipo, agente_soporte, agente_informacion, agente_evaluacion):
    """Proceso de atencion de cada llamada."""
    tiempo_llegada = env.now
    print(f"{nombre} llego al minuto {env.now:.2f}, Tipo: {tipo}")
    if tipo == "soporte":
        agente = agente_soporte
    elif tipo == "informacion":
        agente = agente_informacion
    else:
        agente = agente_evaluacion

    with agente.request() as request:
        yield request
        tiempo_inicio_servicio = env.now
        tiempos_en_cola[tipo].append(tiempo_inicio_servicio - tiempo_llegada)
        print(f"{nombre} comenzo a ser atendido al minuto {env.now:.2f}")

        # Calcular tiempo de ocio y actualizar el ultimo tiempo de salida
        tiempo_ocio[tipo] += max(0, tiempo_inicio_servicio - ultimo_tiempo_salida[tipo])

        yield env.timeout(generar_tiempo_servicio(tipo))
        tiempo_servicio[tipo] += env.now - tiempo_inicio_servicio
        ultimo_tiempo_salida[tipo] = env.now

        if tipo != "evaluacion":
            tiempo_inicio_evaluacion = env.now
            tiempos_en_cola["evaluacion"].append(tiempo_inicio_evaluacion - ultimo_tiempo_salida[tipo])
            yield env.timeout(evaluacion_cliente())

            # Calcular tiempo de ocio y actualizar para evaluacion
            tiempo_ocio["evaluacion"] += max(0, tiempo_inicio_evaluacion - ultimo_tiempo_salida["evaluacion"])
            tiempo_servicio["evaluacion"] += env.now - tiempo_inicio_evaluacion
            ultimo_tiempo_salida["evaluacion"] = env.now

        tiempo_finalizacion = env.now
        tiempos_en_sistema.append(tiempo_finalizacion - tiempo_llegada)
        print(f"{nombre} completo su llamada al minuto {env.now:.2f}")

def proceso_llamadas(env, agentes_soporte, agentes_informacion, agente_evaluacion):
    """Genera llamadas y las asigna al agente correspondiente. La primera llamada ocurre en el tiempo cero."""
    i = 1
    # Genera la primera llamada en tiempo cero
    tipo_llamada = "soporte" if np.random.rand() < PORCENTAJE_SOPORTE_TECNICO else "informacion"
    if tipo_llamada == "soporte":
        env.process(llamada(env, f"Llamada {i}", tipo_llamada, agentes_soporte, agentes_informacion, agente_evaluacion))
    else:
        env.process(llamada(env, f"Llamada {i}", tipo_llamada, agentes_soporte, agentes_informacion, agente_evaluacion))
    i += 1

    while True:
        yield env.timeout(generar_tiempo_llegada())
        tipo_llamada = "soporte" if np.random.rand() < PORCENTAJE_SOPORTE_TECNICO else "informacion"
        if tipo_llamada == "soporte":
            env.process(llamada(env, f"Llamada {i}", tipo_llamada, agentes_soporte, agentes_informacion, agente_evaluacion))
        else:
            env.process(llamada(env, f"Llamada {i}", tipo_llamada, agentes_soporte, agentes_informacion, agente_evaluacion))
        i += 1


def calcular_desempeno():
    """Calcula y muestra estadisticas de desempeno."""
    print('\n')
    for tipo, tiempos in tiempos_en_cola.items():
        if tiempos:
            print(f"Tiempo promedio en cola de {tipo}: {np.mean(tiempos):.2f} minutos")
        else:
            print(f"No hubo llamadas para el tipo {tipo}.")
    print(f"Tiempo promedio en el sistema: {np.mean(tiempos_en_sistema):.2f} minutos")
    print(f"Tiempo maximo en el sistema: {max(tiempos_en_sistema):.2f} minutos")

    # Calcular y mostrar porcentajes de ocio y servicio
    for tipo in tiempo_ocio:
        porcentaje_ocio = (tiempo_ocio[tipo] / TIEMPO_SIMULACION) * 100
        porcentaje_servicio = (tiempo_servicio[tipo] / TIEMPO_SIMULACION) * 100
        print(f"Porcentaje de ocio ({tipo}): {porcentaje_ocio:.2f}%")
        print(f"Porcentaje de servicio ({tipo}): {porcentaje_servicio:.2f}%")

# Configuracion de la simulacion
env = simpy.Environment()
agentes_soporte = simpy.Resource(env, capacity=1)
agentes_informacion = simpy.Resource(env, capacity=1)
agente_evaluacion = simpy.Resource(env, capacity=1)

env.process(proceso_llamadas(env, agentes_soporte, agentes_informacion, agente_evaluacion))
env.run(until=TIEMPO_SIMULACION)
calcular_desempeno()
