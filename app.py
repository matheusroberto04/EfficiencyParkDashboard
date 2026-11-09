from pathlib import Path
import json

import streamlit as st

from calculos import calcular, simular_dias
from apresentacao import montar_html

PASTA = Path(__file__).parent
base = json.loads((PASTA / 'dados.json').read_text(encoding='utf-8'))
original = json.loads((PASTA / 'referencias/html_original_dados.json').read_text(encoding='utf-8'))
PADRAO = base['valores']


def numero(n, casas=2):
    if n is None:
        return '—'
    return f'{n:,.{casas}f}'.replace(',', 'X').replace('.', ',').replace('X', '.')


def entrada(chave, titulo, maximo=None, passo=None, formato=None):
    valor = PADRAO[chave]
    inteiro = isinstance(valor, int)
    if chave not in st.session_state:
        st.session_state[chave] = valor
    opcoes = dict(min_value=(1 if chave in ['pontos','dias_mes','intervalo_reposicao_anos','horizonte_anos'] else 0) if inteiro else 0.0, key=chave)
    if maximo is not None:
        opcoes['max_value'] = int(maximo) if inteiro else float(maximo)
    if passo is not None:
        opcoes['step'] = int(passo) if inteiro else float(passo)
    if formato:
        opcoes['format'] = formato
    return st.number_input(titulo, **opcoes)


st.set_page_config(page_title='Efficiency Park', page_icon='💡', layout='wide')
st.title('💡 Efficiency Park')
st.write('Iluminação comunitária com LED, sensores e energia solar — módulo SERS / CitizenTech')
st.info('Simulador acadêmico baseado no HTML original. Altere os dados na barra lateral: os resultados, gráficos e a apresentação são recalculados. Sem equipamentos reais conectados.')

st.sidebar.header('Experimente outros valores')
if st.sidebar.button('Restaurar valores do HTML original'):
    for chave, valor in PADRAO.items():
        st.session_state[chave] = valor

with st.sidebar.expander('Carregar uma simulação salva'):
    arquivo = st.file_uploader('JSON exportado por esta versão do dashboard', type=['json'])
    if arquivo and st.button('Aplicar arquivo'):
        try:
            salvo = json.loads(arquivo.getvalue())
            novos = salvo['entradas']
            if salvo.get('versao_modelo') != 2 or set(novos) != set(PADRAO):
                raise ValueError('Use um JSON exportado pelo modelo atual, baseado no HTML original.')
            calcular(novos)
            for chave, valor in novos.items():
                if isinstance(PADRAO[chave], int) and int(valor) != valor:
                    raise ValueError('Valor inteiro necessário: ' + chave)
            for chave, valor in novos.items():
                st.session_state[chave] = int(valor) if isinstance(PADRAO[chave], int) else float(valor)
            st.success('Simulação carregada.')
        except (ValueError, KeyError, TypeError) as erro:
            st.error(str(erro))

with st.sidebar:
    with st.expander('Praça e consumo', expanded=True):
        entrada('pontos', 'Quantidade de postes', 100, 1)
        entrada('p_lampada_w', 'Potência da lâmpada atual (W)', 1000, 5)
        entrada('p_reator_w', 'Potência do reator (W/ponto)', 200, 1)
        entrada('p_led_w', 'Potência LED (W/ponto)', 1000, 5)
        entrada('horas_noite', 'Horas ligadas por noite', 24, 0.25, '%.4f')
        entrada('dias_mes', 'Dias do período', 31, 1)
        entrada('tarifa_rs_kwh', 'Tarifa (R$/kWh)', 10, 0.01, '%.5f')
    with st.expander('Sensores e dimerização'):
        entrada('horas_uso_intenso', 'Horas de luz total por noite', 24, 0.5)
        entrada('dim_pct', 'Potência no modo de espera (%)', 100, 5)
        entrada('presenca_pct', 'Presença estimada na madrugada (%)', 100, 5)
        entrada('p_iot_w', 'Potência do módulo IoT (W/ponto)', 100, 0.1)
        entrada('horas_iot', 'Horas de operação do IoT por dia', 24, 1)
        st.caption('Potência proporcional à dimerização é uma hipótese; validar driver e iluminação mínima.')
    with st.expander('Solar e bateria'):
        entrada('painel_wp', 'Painel por poste A2 (Wp)', 5000, 50)
        entrada('bateria_kwh', 'Bateria nominal por poste A2 (kWh)', 100, 0.1)
        entrada('descarga_pct', 'Descarga máxima de ensaio (%)', 100, 5)
        entrada('eficiencia_bateria_pct', 'Aproveitamento da saída do banco (%)', 100, 1)
        entrada('autonomia_desejada', 'Noites de autonomia desejadas', 30, 0.5)
        entrada('kwp_quiosque', 'Potência FV no quiosque A3 (kWp)', 1000, 0.1)
        entrada('hsp_pior_mes', 'HSP de ensaio conservador A2 (h/dia)', 8, 0.1)
        entrada('hsp_media', 'HSP média de ensaio A3 (h/dia)', 8, 0.1)
        entrada('rendimento_fv_pct', 'Rendimento FV global até a carga (%)', 100, 1)
        entrada('valor_credito_rs_kwh', 'Crédito hipotético A3 (R$/kWh)', 10, 0.01, '%.6f')
    with st.expander('Investimento, manutenção e reposições'):
        entrada('capex_a1_ponto', 'A1 instalado (R$/ponto)', passo=25)
        entrada('capex_a2_ponto', 'A2 instalado (R$/ponto)', passo=100)
        entrada('capex_fv_kwp', 'FV A3 instalado (R$/kWp)', passo=100)
        entrada('manut_atual_ponto_ano', 'Manutenção atual (R$/ponto/ano)', passo=5)
        entrada('manut_a1_ponto_ano', 'Manutenção A1 (R$/ponto/ano)', passo=5)
        entrada('manut_a2_ponto_ano', 'Manutenção A2 (R$/ponto/ano)', passo=5)
        entrada('manut_fv_kwp_ano', 'Manutenção FV A3 (R$/kWp/ano)', passo=5)
        entrada('reposicao_a2_ponto', 'Reposição A2 por evento (R$/ponto)', passo=100)
        entrada('intervalo_reposicao_anos', 'Intervalo de reposição de ensaio (anos)', 50, 1)
        entrada('horizonte_anos', 'Horizonte de comparação (anos)', 50, 1)
    with st.expander('Referências ambientais e de iluminação'):
        entrada('fator_emissao', 'Fator de emissão adotado (kg CO₂/kWh)', 10, 0.001, '%.4f')
        entrada('fluxo_sodio_lm', 'Fluxo nominal da referência (lm)', passo=100)
        entrada('fluxo_led_lm', 'Fluxo nominal LED (lm)', passo=100)
        entrada('mercurio_mg', 'Mercúrio informado na referência (mg)', passo=1)
        entrada('adicional_tarifa', 'Adicional tarifário de ensaio (R$/kWh)', 10, 0.01, '%.5f')

# Todas as entradas partem dos mesmos padrões do HTML e são efetivamente editáveis.
d = {chave: st.session_state[chave] for chave in PADRAO}
try:
    r = calcular(d)
except (ValueError, KeyError) as erro:
    st.error(str(erro))
    st.stop()
c = {item['codigo']: item for item in r['cenarios']}
periodo = f"{d['dias_mes']} dias"
if d['horas_uso_intenso'] > d['horas_noite']:
    st.warning('As horas de luz total foram limitadas à duração da noite para evitar tempo negativo na madrugada.')

codigo = st.radio('Alternativa para explorar', ['A1', 'A2', 'A3'], index=2,
                  format_func=lambda k: k + ' — ' + c[k]['nome'], horizontal=True)
sel = c[codigo]
st.caption(f"Cenário atual: {d['pontos']} postes, {numero(r['parametros']['p_atual_w'],0)} W/ponto e {numero(d['horas_noite'],4)} h/noite. Período: {periodo}.")
col = st.columns(4)
col[0].metric('Consumo atual da rede', numero(c['A0']['consumo_rede_kwh_mes'], 1) + ' kWh')
col[1].metric('Demanda LED + sensores', numero(c['A1']['energia_demandada_kwh_mes'], 1) + ' kWh')
col[2].metric('Redução da demanda', numero(c['A1']['reducao_demanda_pct'], 1) + '%')
col[3].metric('Operação atual', 'R$ ' + numero(c['A0']['operacao_periodo']))
st.subheader(sel['nome'])
col = st.columns(4)
col[0].metric('Compra física da rede', numero(sel['consumo_rede_kwh_mes'], 1) + ' kWh')
col[1].metric('Economia operacional estimada', 'R$ ' + numero(sel['economia_rs_mes']))
col[2].metric('FV local no balanço energético', numero(sel['participacao_renovavel_pct'], 1) + '%')
col[3].metric('Retorno simples', numero(sel['payback_anos'], 1) + ' anos')
col = st.columns(3)
col[0].metric('Potencial de CO₂ evitado no balanço', numero(sel['emissoes_evitadas_kgco2_ano'], 1) + ' kg/ano')
col[1].metric('Tempo estimado em espera', numero(sel['horas_dimerizado_dia'], 2) + ' h/dia')
col[2].metric('Investimento estimado', 'R$ ' + numero(sel['capex']))
st.caption('Economia operacional inclui energia e manutenção no período. Payback é simples, sem reposições ou desconto; o custo no horizonte inclui reposições. Percentual FV não descreve a composição renovável da rede.')

if not c['A2']['atende_demanda']:
    st.error('A2 não atende a mesma demanda: déficit de ' + numero(c['A2']['deficit_kwh_mes']) + ' kWh em ' + periodo + '. Economia operacional, retorno e benefício de CO₂ equivalente ficam indisponíveis para A2.')
if c['A1']['reducao_demanda_pct'] < 0:
    st.warning('As entradas aumentam a demanda das alternativas em relação ao cenário atual.')
if codigo == 'A3':
    st.info('A3 compra energia da rede à noite e gera FV de dia. Os créditos são uma hipótese financeira editável: o balanço anual não é fornecimento solar direto noturno nem fatura garantida.')

st.subheader('Comparação dos quatro cenários')
linhas = []
for item in r['cenarios']:
    linhas.append({'Cenário': item['codigo'], 'Demanda (kWh/período)': item['energia_demandada_kwh_mes'],
                   'Rede física (kWh/período)': item['consumo_rede_kwh_mes'], 'Déficit (kWh/período)': item['deficit_kwh_mes'],
                   'Custo energia (R$/período)': item['custo_energia_mes'], 'Energia + manutenção (R$/período)': item['operacao_periodo'],
                   'FV local no balanço (%)': item['participacao_renovavel_pct'], 'Investimento (R$)': item['capex'],
                   'Retorno simples (anos)': item['payback_anos'], 'Custo no horizonte (R$)': item['custo_total_10_anos']})
st.dataframe(linhas, hide_index=True)
st.caption('A0 é a referência. A1 usa rede; A2 é isolado; A3 usa rede e FV no quiosque. Um custo menor em A2 com déficit não representa serviço equivalente.')
a, b = st.columns(2)
a.bar_chart(linhas, x='Cenário', y='Demanda (kWh/período)')
b.bar_chart(linhas, x='Cenário', y='Energia + manutenção (R$/período)')

with st.expander('Checagem do solar autônomo A2', expanded=codigo == 'A2'):
    sol = r['dimensionamento_solar']
    st.write('Demanda por ponto: ' + numero(r['parametros']['e_alt_ponto_dia'], 4) + ' kWh/dia. Geração útil no ensaio: ' + numero(sol['geracao_util_poste_dia'], 4) + ' kWh/dia.')
    st.write('Painel mínimo no ensaio: ' + numero(sol['painel_necessario_wp'], 1) + ' Wp. Banco nominal necessário para a autonomia desejada: ' + numero(sol['bateria_necessaria_kwh'], 3) + ' kWh/ponto.')
    st.write('Banco útil: ' + numero(sol['banco_util_kwh'], 3) + ' kWh/ponto. Autonomia teórica partindo de banco cheio: ' + numero(sol['autonomia_noites'], 2) + ' noites.')
    st.caption('Balanço conceitual: não garante sequência de noites nubladas. Verificar driver, controlador, tensão, corrente, iluminação mínima, bateria e condições locais na implantação.')

with st.expander('Perfil noturno e série diária simulada'):
    st.write('Perfil de potência das luminárias (IoT contabilizado separadamente na demanda):')
    st.line_chart(r['perfil_noite'], x='hora', y=['atual_w', 'led_w'])
    serie = simular_dias(d, original['monitoramento_simulado'])
    st.write('Série ilustrativa recalculada com as entradas atuais. Não é medição nem a base do dia médio dos indicadores:')
    st.line_chart(serie, x='data', y=['consumo_atual_kwh', 'consumo_led_sensor_kwh'])
    st.line_chart(serie, x='data', y='soc_bateria_poste_pct')
    st.dataframe(serie, hide_index=True)

with st.expander('Diagrama, equipe, cálculos e fontes'):
    st.image(str(PASTA / 'diagrama.svg'))
    for p in base['integrantes']:
        st.write(p['nome'] + ' · RM' + p['rm'])
    st.code('E_atual/dia = postes × (W_lâmpada + W_reator) × h_noite / 1000\n'
            'h_equivalentes_LED = h_intenso + h_madrugada × [presença + (1−presença) × espera]\n'
            'E_LED+IoT/dia = postes × [W_LED × h_equivalentes + W_IoT × h_IoT] / 1000\n'
            'E_período = E_dia × dias; E_ano = E_dia × 365\n'
            'FV_ano = kWp × HSP × rendimento × 365\n'
            'Operação_período = (energia_ano + manutenção_ano) × dias/365\n'
            'Payback simples = implantação / economia anual recorrente\n'
            'Custo_horizonte = implantação + operação_ano × anos + reposições', language=None)
    for p in base['premissas']:
        st.markdown('**' + p['parametro'] + ':** ' + p['origem'])
    for f in base['fontes']:
        url = f['url'] if f['url'].startswith('https://') else 'https://github.com/matheusroberto04/EfficiencyParkDashboard/blob/main/' + f['url']
        st.markdown('**[' + f['titulo'] + '](' + url + ')** — ' + f['uso'])

st.subheader('Salvar e apresentar esta simulação')
exportacao = {'versao_modelo': 2, 'entradas': d, 'resultados': r, 'fontes': base['fontes'], 'premissas': base['premissas']}
st.download_button('Baixar simulação em JSON', json.dumps(exportacao, ensure_ascii=False, indent=2), 'efficiency_park_simulacao.json', 'application/json')
st.download_button('Baixar apresentação HTML desta simulação', montar_html(base, d), 'Efficiency_Park_Apresentacao.html', 'text/html; charset=utf-8')
st.caption('As alterações são locais à sessão. Salve o JSON para carregar depois. O botão de restauração recupera os valores do HTML original; o HTML baixado contém os resultados recalculados.')
