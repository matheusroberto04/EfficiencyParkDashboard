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



def montar_html(base, entradas=None):
    pacote = montar_pacote(base, entradas)
    def seguro(objeto):
        return json.dumps(objeto, ensure_ascii=False).replace('<', '\\u003c')
    modelo = (PASTA / 'apresentacao_template.html').read_text(encoding='utf-8')
    html = modelo.replace('__SERS_DADOS__', seguro(pacote))
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
