"""Contas do simulador com funções, condições e dicionários de Python."""


def calcular(dados):
    n = dados["quantidade"]
    dias = dados["dias"]
    horas = dados["horas"]
    demanda_dia = n * dados["potencia_led"] * horas / 1000
    atual = n * (dados["potencia_atual"] + dados["perda_reator"]) * horas * dias / 1000
    led = demanda_dia * dias
    economia = atual - led
    economia_percentual = economia / atual * 100 if atual > 0 else 0.0

    # O rendimento global já contém perdas até a carga. Não multiplicar
    # novamente pelo aproveitamento da descarga da bateria.
    geracao_util_dia = n * dados["painel_wp"] * dados["hsp"] * dados["rendimento_solar"] / 1000
    bateria_nominal = n * dados["bateria_v"] * dados["bateria_ah"] / 1000
    bateria_util = bateria_nominal * dados["descarga"] * dados["rendimento_descarga"]
    capacidade_inversores = n * dados["inversor_w"] * horas / 1000
    # Dias iguais, carga noturna e um conjunto idêntico em cada ponto.
    solar_dia = min(demanda_dia, geracao_util_dia, bateria_util, capacidade_inversores)
    solar = solar_dia * dias
    deficit = max(0.0, led - solar)
    atende = deficit <= 0.0000001
    participacao = solar / led * 100 if led > 0 else 0.0
    potencia_carga = n * dados["potencia_led"] / 1000
    autonomia = bateria_util / potencia_carga if potencia_carga > 0 else 0.0

    materiais_led = n * dados["preco_led"]
    materiais_solar = n * (dados["preco_led"] + dados["preco_kit"] + dados["preco_inversor"])
    investimento_led = materiais_led * (1 + dados["instalacao_led"])
    investimento_solar = materiais_solar * (1 + dados["instalacao_solar"])
    reserva_rede = materiais_led * dados["reserva_rede"] / 12 * dias / 30
    reserva_solar = materiais_solar * dados["reserva_solar"] / 12 * dias / 30
    energia_atual = atual * dados["tarifa"]
    energia_led = led * dados["tarifa"]
    operacao_atual = energia_atual + reserva_rede
    operacao_led = energia_led + reserva_rede
    # B é isolado: déficit não é comprado da rede nem vira economia válida.
    operacao_solar = reserva_solar
    economia_operacao_solar = operacao_atual - operacao_solar if atende else None

    return {
        "consumo_atual": atual, "consumo_led": led,
        "economia_energia": economia, "economia_percentual": economia_percentual,
        "demanda_dia": demanda_dia, "geracao_util_dia": geracao_util_dia,
        "bateria_nominal": bateria_nominal, "bateria_util": bateria_util,
        "autonomia_horas": autonomia, "solar_atendida": solar,
        "deficit_solar": deficit, "participacao_solar": participacao, "atende": atende,
        "custo_energia_atual": energia_atual, "custo_energia_led": energia_led,
        "investimento_led": investimento_led, "investimento_solar": investimento_solar,
        "reserva_rede": reserva_rede, "reserva_solar": reserva_solar,
        "operacao_atual": operacao_atual, "operacao_led": operacao_led,
        "operacao_solar": operacao_solar,
        "economia_operacao_led": operacao_atual - operacao_led,
        "economia_operacao_solar": economia_operacao_solar
    }
