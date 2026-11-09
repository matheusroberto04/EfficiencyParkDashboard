"""Materializa o visual do HTML original com o cálculo e as entradas da sessão."""
import json
from pathlib import Path

from calculos import calcular, simular_dias

PASTA = Path(__file__).parent


def montar_pacote(base, entradas=None):
    dados = base['valores'].copy() if entradas is None else entradas.copy()
    resultado = calcular(dados)
    origem = json.loads((PASTA / 'referencias/html_original_dados.json').read_text(encoding='utf-8'))
    resultado.update(gerado_em=base['consulta'], versao_modelo=2,
                     premissas_principais={k: dados[k] for k in ['pontos','horas_noite','tarifa_rs_kwh','fator_emissao','dias_mes','horizonte_anos']},
                     monitoramento_simulado=simular_dias(dados, origem['monitoramento_simulado']),
                     fontes=base['fontes'], premissas=base['premissas'], integrantes=base['integrantes'])
    return resultado


def montar_roteiro(pacote):
    p = pacote['parametros']
    c = {x['codigo']: x for x in pacote['cenarios']}
    def n(valor, casas=1):
        return 'indisponível' if valor is None else f'{valor:.{casas}f}'.replace('.', ',')
    falas = [
        ('capa','Abertura',12,'Somos Matheus Roberto, Gustavo Oliveira Baptista e Ana Luísa Santos. O Efficiency Park compara eficiência energética e energia solar para uma praça simulada.'),
        ('problema','Problema comunitário',20,f"O cenário tem {p['pontos']} pontos de iluminação. A referência usa lâmpadas de {n(p['p_lampada_w'],0)} watts e reator de {n(p['p_reator_w'],0)} watts. Buscamos reduzir a demanda e apoiar decisões dos moradores e responsáveis pela manutenção. Não houve medição da praça."),
        ('consumo','Análise energética',22,f"O consumo é potência vezes tempo, dividido por mil, considerando todos os pontos. Na referência, são {n(c['A0']['energia_demandada_kwh_mes'])} quilowatts-hora em {p['dias_mes']} dias. Todos os cenários usam o mesmo período; a análise anual considera 365 dias."),
        ('sensor','LED e sensores simulados',20,f"Após {n(p['horas_uso_intenso'])} horas de luz total, o modelo considera espera a {n(p['dim_pct'],0)} por cento e presença em {n(p['presenca_pct'],0)} por cento da madrugada. A redução de demanda estimada é {n(c['A1']['reducao_demanda_pct'])} por cento, incluindo o consumo do módulo IoT. A animação é conceitual."),
        ('alternativas','Três alternativas',25,'A1 usa LED e sensores na rede. A2 acrescenta painel e bateria por poste. A3 usa a rede à noite e geração no quiosque de dia, com crédito financeiro hipotético. Comparamos investimento, manutenção, reposições e custo no horizonte. A3 é uma proposta a validar, não uma vencedora universal.'),
        ('diagrama','Arquitetura proposta',18,'O diagrama relaciona fontes, luminárias, sensores, lógica de controle e processamento. O MVP calcula indicadores a partir de entradas manuais. Sensores reais, comunicação e acionamento representam a arquitetura planejada, não uma instalação já realizada.'),
        ('dashboard','Demonstração do dashboard',25,'No Python, o professor pode alterar os parâmetros e observar o recálculo. Em A2, falta de sol ou bateria gera alerta de déficit. Em A3, geração, importação física e crédito financeiro são separados. O HTML baixado usa exatamente os resultados dessa simulação.'),
        ('beneficios','Benefícios e limitações',20,'Esperamos reduzir a demanda e apoiar a decisão da comunidade. É necessário validar iluminação, condições solares e orçamento. Os coeficientes são editáveis e as séries são simuladas. O fator ambiental representa uma estimativa de operação ou balanço, sem análise de ciclo de vida.'),
        ('fim','Encerramento',10,'Os resultados são projeções condicionadas às premissas. O código, os dados e as instruções de teste estão no GitHub. Obrigado.')
    ]
    roteiro = dict(gerado_em=pacote['gerado_em'], limite_s=180, total_s=sum(x[2] for x in falas), cenas=[])
    inicio = 0
    for i,(identificador,titulo,tempo,fala) in enumerate(falas):
        roteiro['cenas'].append(dict(n=i+1,id=identificador,titulo=titulo,acao='Mostrar esta cena e explicar as premissas; no dashboard, demonstrar o recálculo.',fala=fala,segundos=tempo,inicio_s=inicio))
        inicio += tempo
    return roteiro


def montar_html(base, entradas=None):
    pacote = montar_pacote(base, entradas)
    roteiro = montar_roteiro(pacote)
    def seguro(objeto):
        return json.dumps(objeto, ensure_ascii=False).replace('<', '\\u003c')
    modelo = (PASTA / 'apresentacao_template.html').read_text(encoding='utf-8')
    html = modelo.replace('__SERS_DADOS__', seguro(pacote)).replace('__SERS_ROTEIRO__', seguro(roteiro))
    html = html.replace('12 postes', str(pacote['parametros']['pontos']) + ' postes')
    html = html.replace('30 noites', str(pacote['parametros']['dias_mes'])+' noites')
    html = html.replace('depois das 23h', 'depois do uso intenso')
    html = html.replace('10 anos', str(pacote['parametros']['horizonte_anos']) + ' anos')
    grupo = [x['nome']+' · RM'+x['rm'] for x in base['integrantes']]
    html = html.replace('__SERS_GRUPO__', seguro(grupo))
    return html


if __name__ == '__main__':
    base = json.loads((PASTA / 'dados.json').read_text(encoding='utf-8'))
    (PASTA / 'apresentacao.html').write_text(montar_html(base), encoding='utf-8')
    print('Apresentação atualizada com o modelo do HTML original.')
