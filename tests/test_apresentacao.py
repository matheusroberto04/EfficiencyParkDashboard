import json
from pathlib import Path
import re
import sys
import unittest
PASTA=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(PASTA))
from apresentacao import montar_html,montar_pacote
from calculos import calcular


class TestApresentacao(unittest.TestCase):
    def setUp(self):
        self.base=json.loads((PASTA/'dados.json').read_text(encoding='utf-8'))

    def pacote(self,html):
        m=re.search(r'window\.SERS_DADOS\s*=\s*(\{.*?\});',html,re.S)
        self.assertIsNotNone(m)
        return json.loads(m.group(1))

    def test_html_usa_as_contas_e_nao_resultados_fixos(self):
        entrada=self.base['valores'].copy()
        entrada.update(pontos=24,dias_mes=31,hsp_pior_mes=0)
        p=self.pacote(montar_html(self.base,entrada))
        self.assertEqual(p['cenarios'],calcular(entrada)['cenarios'])
        self.assertIn('24 postes',montar_html(self.base,entrada))
        self.assertFalse(p['cenarios'][2]['atende_demanda'])
        self.assertEqual(self.base['valores']['pontos'],12)

    def test_extracao_continua_disponivel_para_rastreabilidade(self):
        p=montar_pacote(self.base)
        self.assertEqual(len(p['cenarios']),4)
        self.assertEqual(len(p['monitoramento_simulado']),30)
        self.assertAlmostEqual(p['dimensionamento_solar']['autonomia_noites'],2.2186142710416834)

    def test_textos_nao_fecham_o_script_do_documento(self):
        self.base['integrantes'][0]['nome']='</script><script>teste</script>'
        h=montar_html(self.base)
        self.assertNotIn('</script><script>teste',h)
        self.assertEqual(self.pacote(h)['integrantes'][0]['nome'],self.base['integrantes'][0]['nome'])


if __name__=='__main__':unittest.main()
