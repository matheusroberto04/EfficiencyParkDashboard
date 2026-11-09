"""Modelo energético do HTML original, com premissas editáveis e checagens."""
import math
from datetime import date, timedelta


def calcular(dados):
    p = dados.copy()
    for nome, valor in p.items():
        if not isinstance(valor, (int, float)) or not math.isfinite(valor) or valor < 0:
            raise ValueError("Valor inválido: " + nome)
    if p['pontos'] < 1 or p['dias_mes'] < 1 or p['intervalo_reposicao_anos'] < 1:
        raise ValueError('Pontos, período e intervalo de reposição devem ser positivos.')
    for nome in ['dim_pct', 'presenca_pct', 'descarga_pct', 'eficiencia_bateria_pct', 'rendimento_fv_pct']:
        if p[nome] > 100:
            raise ValueError('Percentual acima de 100: ' + nome)
    if p['horas_noite'] > 24 or p['horas_iot'] > 24:
        raise ValueError('Horas por dia não podem ultrapassar 24.')

    n, dias = p['pontos'], p['dias_mes']
    intenso = min(p['horas_uso_intenso'], p['horas_noite'])
    madrugada = p['horas_noite'] - intenso
    presenca = p['presenca_pct'] / 100
    espera = p['dim_pct'] / 100
    horas_equivalentes = intenso + madrugada * (presenca + (1 - presenca) * espera)
    e_atual = (p['p_lampada_w'] + p['p_reator_w']) * p['horas_noite'] / 1000
    e_led = p['p_led_w'] * horas_equivalentes / 1000
    e_iot = p['p_iot_w'] * p['horas_iot'] / 1000
    e_alt = e_led + e_iot
    rendimento = p['rendimento_fv_pct'] / 100
    banco_util = p['bateria_kwh'] * p['descarga_pct'] / 100 * p['eficiencia_bateria_pct'] / 100
    solar_dia = p['painel_wp'] / 1000 * p['hsp_pior_mes'] * rendimento
    atendida_a2 = min(e_alt, solar_dia, banco_util)
    deficit_dia = max(0.0, e_alt - atendida_a2)
    atende_a2 = deficit_dia <= 1e-9
    fv_ano = p['kwp_quiosque'] * p['hsp_media'] * rendimento * 365
    alt_ano = e_alt * n * 365
    cobertura_a3 = min(fv_ano, alt_ano)
    # Não se usa o excedente além da demanda anual no modelo de crédito.
    credito_ano = min(cobertura_a3 * p['valor_credito_rs_kwh'], alt_ano * p['tarifa_rs_kwh'])
    trocas = max(0, math.ceil(p['horizonte_anos'] / p['intervalo_reposicao_anos']) - 1)

    p.update(p_atual_w=p['p_lampada_w'] + p['p_reator_w'], horas_uso_intenso=intenso,
             hora_fim_intenso=(18 + intenso) % 24, horas_dimerizado=madrugada * (1 - presenca),
             e_a0_ponto_dia=e_atual, e_led_ponto_dia=e_led, e_iot_ponto_dia=e_iot, e_alt_ponto_dia=e_alt)
    configuracoes = [
        ('A0', 'Situação atual', 'Referência de sódio na rede, sem dimerização', e_atual, e_atual, 0, 0, n * p['manut_atual_ponto_ano'], 0),
        ('A1', 'LED + sensores na rede', 'LED e sensores na rede elétrica; automação simulada', e_alt, e_alt, 0, n * p['capex_a1_ponto'], n * p['manut_a1_ponto_ano'], 0),
        ('A2', 'Luminárias solares autônomas', 'LED e sensores com painel e bateria por poste; cenário isolado', e_alt, 0, atendida_a2 * n * 365, n * p['capex_a2_ponto'], n * p['manut_a2_ponto_ano'], n * p['reposicao_a2_ponto'] * trocas),
        ('A3', 'LED + sensores + solar na rede', 'A1 e painéis no quiosque; compensação financeira hipotética em balanço anual', e_alt, e_alt, cobertura_a3, n * p['capex_a1_ponto'] + p['kwp_quiosque'] * p['capex_fv_kwp'], n * p['manut_a1_ponto_ano'] + p['kwp_quiosque'] * p['manut_fv_kwp_ano'], 0)
    ]
    cenarios = []
    for codigo, nome, descricao, demanda_dia, rede_dia, fv_local, capex, manut, reposicoes in configuracoes:
        demanda_ano = demanda_dia * n * 365
        rede_ano = rede_dia * n * 365
        custo_ano = rede_ano * p['tarifa_rs_kwh'] - (credito_ano if codigo == 'A3' else 0)
        deficit = deficit_dia * n * dias if codigo == 'A2' else 0.0
        atendida = demanda_dia * n * dias - deficit
        c = dict(codigo=codigo, nome=nome, descricao=descricao,
                 fonte_energia='Solar isolado' if codigo == 'A2' else 'Rede + FV local (balanço)' if codigo == 'A3' else 'Rede elétrica (SIN)',
                 energia_demandada_kwh_mes=demanda_dia * n * dias, energia_demandada_kwh_ano=demanda_ano,
                 consumo_rede_kwh_mes=rede_dia * n * dias, consumo_rede_kwh_ano=rede_ano,
                 renovavel_kwh_ano=fv_local, renovavel_kwh_mes=fv_local / 365 * dias,
                 participacao_renovavel_pct=fv_local / demanda_ano * 100 if demanda_ano else 0,
                 custo_energia_ano=custo_ano, custo_energia_mes=custo_ano / 365 * dias,
                 capex=capex, om_ano=manut, reposicoes_horizonte=reposicoes,
                 operacao_ano=custo_ano + manut, operacao_periodo=(custo_ano + manut) / 365 * dias,
                 deficit_kwh_mes=deficit, energia_atendida_kwh_mes=atendida,
                 atende_demanda=atende_a2 if codigo == 'A2' else True,
                 horas_dimerizado_dia=p['horas_dimerizado'] if codigo != 'A0' else 0,
                 emissoes_rede_kgco2_ano=rede_ano * p['fator_emissao'],
                 emissoes_kgco2_ano=max(0, demanda_ano - fv_local) * p['fator_emissao'],
                 custo_energia_ano_bandeira_vermelha=custo_ano + rede_ano * p['adicional_tarifa'])
        if codigo == 'A3':
            c['geracao_fv_kwh_ano'] = fv_ano
            c['credito_estimado_ano'] = credito_ano
        cenarios.append(c)
    a0 = cenarios[0]
    for c in cenarios:
        c['economia_kwh_mes'] = a0['consumo_rede_kwh_mes'] - c['consumo_rede_kwh_mes']
        c['economia_rede_pct'] = c['economia_kwh_mes'] / a0['consumo_rede_kwh_mes'] * 100 if a0['consumo_rede_kwh_mes'] else 0
        c['reducao_demanda_pct'] = (a0['energia_demandada_kwh_ano'] - c['energia_demandada_kwh_ano']) / a0['energia_demandada_kwh_ano'] * 100 if a0['energia_demandada_kwh_ano'] else 0
        economia = a0['operacao_ano'] - c['operacao_ano']
        c['economia_rs_ano'] = economia if c['atende_demanda'] else None
        c['economia_rs_mes'] = economia / 365 * dias if c['atende_demanda'] else None
        c['payback_anos'] = c['capex'] / economia if economia > 0 and c['capex'] > 0 and c['atende_demanda'] else None
        c['custo_total_10_anos'] = c['capex'] + c['operacao_ano'] * p['horizonte_anos'] + c['reposicoes_horizonte']
        c['emissoes_evitadas_kgco2_ano'] = a0['emissoes_kgco2_ano'] - c['emissoes_kgco2_ano'] if c['atende_demanda'] else None

    denominador = p['hsp_pior_mes'] * rendimento
    rendimento_banco = p['descarga_pct'] / 100 * p['eficiencia_bateria_pct'] / 100
    dimensionamento = dict(
        painel_necessario_wp=e_alt / denominador * 1000 if denominador else None,
        painel_escolhido_wp=p['painel_wp'],
        margem_pior_mes_pct=(solar_dia / e_alt - 1) * 100 if e_alt else 0,
        bateria_necessaria_kwh=e_alt * p['autonomia_desejada'] / rendimento_banco if rendimento_banco else None,
        bateria_escolhida_kwh=p['bateria_kwh'], banco_util_kwh=banco_util,
        autonomia_noites=banco_util / e_alt if e_alt else None,
        geracao_util_poste_dia=solar_dia, deficit_a2_kwh_mes=deficit_dia * n * dias,
        geracao_fv_quiosque_kwh_ano=fv_ano, valor_credito_rs_kwh=p['valor_credito_rs_kwh'])
    perfil = []
    # Pontos do gráfico são amostras de potência das luminárias, sem a carga IoT.
    for i in range(max(2, math.ceil(p['horas_noite'] * 4))):
        t = min(i / 4, p['horas_noite'])
        fator = 1 if t < intenso else presenca + (1 - presenca) * espera
        minutos = round((18 + t) * 60) % 1440
        perfil.append(dict(hora=f'{minutos // 60:02d}:{minutos % 60:02d}', atual_w=n * p['p_atual_w'], led_w=n * p['p_led_w'] * fator))
    return dict(parametros=p, cenarios=cenarios, dimensionamento_solar=dimensionamento, perfil_noite=perfil)


def simular_dias(dados, serie_original):
    """Recalcula a série ilustrativa sem confundi-la com o dia médio do projeto."""
    resultados = []
    banco = dados['bateria_kwh'] * dados['descarga_pct'] / 100 * dados['eficiencia_bateria_pct'] / 100
    carga = banco  # hipótese inicial da série: banco cheio
    for i in range(int(dados['dias_mes'])):
        origem = serie_original[i % len(serie_original)]
        dia = dados.copy()
        dia['presenca_pct'] = min(100, origem['fracao_presenca_madrugada'] / 0.20 * dados['presenca_pct'])
        hsp = origem['hsp_simulada'] / 4.9 * dados['hsp_media']
        r = calcular(dia)
        consumo = r['parametros']['e_alt_ponto_dia']
        geracao = dados['painel_wp'] / 1000 * hsp * dados['rendimento_fv_pct'] / 100
        disponivel = min(banco, carga + geracao)
        atendida = min(consumo, disponivel)
        carga = max(0, disponivel - atendida)
        # Estado de carga nominal mantém a reserva não descarregável.
        soc = 100 - dados['descarga_pct'] + carga / banco * dados['descarga_pct'] if banco else 0
        resultados.append(dict(data=(date(2026,11,1)+timedelta(days=i)).isoformat(), fracao_presenca_madrugada=dia['presenca_pct']/100,
                               consumo_atual_kwh=r['cenarios'][0]['energia_demandada_kwh_ano']/365,
                               consumo_led_sensor_kwh=consumo * dados['pontos'], hsp_simulada=hsp,
                               geracao_poste_solar_kwh=geracao, soc_bateria_poste_pct=soc,
                               deficit_a2_kwh= max(0, consumo-atendida) * dados['pontos'],
                               geracao_fv_quiosque_kwh=dados['kwp_quiosque'] * hsp * dados['rendimento_fv_pct']/100))
    return resultados
