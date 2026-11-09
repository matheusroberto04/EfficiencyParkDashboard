import json
from pathlib import Path
import sys
import unittest

PASTA = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PASTA))
from calculos import calcular, simular_dias


class TestCalculos(unittest.TestCase):
    def setUp(self):
        self.dados = json.loads((PASTA/'dados.json').read_text(encoding='utf-8'))['valores']
        self.original = json.loads((PASTA/'referencias/html_original_dados.json').read_text(encoding='utf-8'))

    def test_reproduz_os_resultados_principais_do_html_original(self):
        r = calcular(self.dados)
        campos = ['energia_demandada_kwh_mes','consumo_rede_kwh_mes','custo_energia_ano','custo_energia_mes',
                  'capex','om_ano','reposicoes_horizonte','participacao_renovavel_pct','reducao_demanda_pct',
                  'economia_rs_mes','payback_anos','custo_total_10_anos','emissoes_evitadas_kgco2_ano']
        for novo, antigo in zip(r['cenarios'],self.original['cenarios']):
            for campo in campos:
                with self.subTest(cenario=novo['codigo'],campo=campo):
                    if antigo[campo] is None:
                        self.assertIsNone(novo[campo])
                    else:
                        self.assertAlmostEqual(novo[campo],antigo[campo],places=7)

    def test_postes_escalam_cargas_mas_nao_o_quiosque(self):
        base = calcular(self.dados)
        self.dados['pontos'] = 24
        r = calcular(self.dados)
        self.assertAlmostEqual(r['cenarios'][0]['energia_demandada_kwh_mes'],base['cenarios'][0]['energia_demandada_kwh_mes']*2)
        self.assertAlmostEqual(r['cenarios'][3]['capex'],31000)
        self.assertEqual(r['cenarios'][3]['geracao_fv_kwh_ano'],base['cenarios'][3]['geracao_fv_kwh_ano'])

    def test_presenca_alta_reduz_economia(self):
        base = calcular(self.dados)
        self.dados['presenca_pct'] = 100
        r = calcular(self.dados)
        self.assertGreater(r['cenarios'][1]['energia_demandada_kwh_mes'],base['cenarios'][1]['energia_demandada_kwh_mes'])
        self.assertEqual(r['parametros']['horas_dimerizado'],0)

    def test_espera_total_equivale_a_ausencia_de_dimerizacao(self):
        self.dados['dim_pct'] = 100
        a = calcular(self.dados)
        self.dados['presenca_pct'] = 100
        b = calcular(self.dados)
        self.assertAlmostEqual(a['cenarios'][1]['energia_demandada_kwh_mes'],b['cenarios'][1]['energia_demandada_kwh_mes'])

    def test_sem_sol_nao_chama_falta_de_luz_de_economia(self):
        self.dados['hsp_pior_mes'] = 0
        a2 = calcular(self.dados)['cenarios'][2]
        self.assertFalse(a2['atende_demanda'])
        self.assertGreater(a2['deficit_kwh_mes'],0)
        self.assertEqual(a2['consumo_rede_kwh_mes'],0)
        self.assertIsNone(a2['economia_rs_mes'])
        self.assertIsNone(a2['payback_anos'])
        self.assertIsNone(a2['emissoes_evitadas_kgco2_ano'])

    def test_bateria_zero_tambem_impede_carga_noturna(self):
        self.dados['bateria_kwh'] = 0
        self.assertFalse(calcular(self.dados)['cenarios'][2]['atende_demanda'])

    def test_a3_nao_diminui_importacao_fisica_com_credito(self):
        r = calcular(self.dados)
        a1,a3 = r['cenarios'][1],r['cenarios'][3]
        self.assertEqual(a1['consumo_rede_kwh_mes'],a3['consumo_rede_kwh_mes'])
        self.assertGreater(a1['custo_energia_mes'],a3['custo_energia_mes'])
        self.dados['valor_credito_rs_kwh'] = 100
        self.assertEqual(calcular(self.dados)['cenarios'][3]['custo_energia_mes'],0)

    def test_periodo_muda_energia_sem_mudar_custos_anuais(self):
        a=calcular(self.dados)
        self.dados['dias_mes']=31
        b=calcular(self.dados)
        self.assertAlmostEqual(b['cenarios'][1]['operacao_periodo'],a['cenarios'][1]['operacao_periodo']*31/30)
        self.assertEqual(b['cenarios'][1]['payback_anos'],a['cenarios'][1]['payback_anos'])

    def test_sem_noite_ainda_contabiliza_iot(self):
        self.dados['horas_noite']=0
        r=calcular(self.dados)
        self.assertEqual(r['cenarios'][0]['energia_demandada_kwh_mes'],0)
        self.assertAlmostEqual(r['cenarios'][1]['energia_demandada_kwh_mes'],4.32)
        self.assertEqual(r['cenarios'][1]['reducao_demanda_pct'],0)
        self.assertEqual(r['parametros']['horas_uso_intenso'],0)

    def test_reposicoes_nao_incluem_fim_do_horizonte(self):
        self.assertEqual(calcular(self.dados)['cenarios'][2]['reposicoes_horizonte'],24000)
        self.dados['horizonte_anos']=4
        self.assertEqual(calcular(self.dados)['cenarios'][2]['reposicoes_horizonte'],0)
        self.dados['horizonte_anos']=5
        self.assertEqual(calcular(self.dados)['cenarios'][2]['reposicoes_horizonte'],12000)

    def test_serie_recalcula_presenca_e_datas(self):
        self.dados['dias_mes']=31
        serie=simular_dias(self.dados,self.original['monitoramento_simulado'])
        self.assertAlmostEqual(serie[0]['fracao_presenca_madrugada'],0.323)
        self.assertEqual(serie[-1]['data'],'2026-12-01')
        self.assertTrue(all(0<=x['soc_bateria_poste_pct']<=100 for x in serie))

    def test_rejeita_percentuais_invalidos(self):
        self.dados['dim_pct']=101
        with self.assertRaises(ValueError):calcular(self.dados)


if __name__=='__main__':
    unittest.main()
