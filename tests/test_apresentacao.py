"""Evita divergências entre o HTML, as entradas da sessão e o cálculo Python."""
import json
from pathlib import Path
import re
import sys
import unittest

PASTA = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PASTA))
from apresentacao import montar_html
from calculos import calcular


class TestApresentacao(unittest.TestCase):
    def setUp(self):
        self.base = json.loads((PASTA / "dados.json").read_text(encoding="utf-8"))

    def pacote(self, html):
        trecho = re.search(r'<script id="projectData" type="application/json">(.*?)</script>', html, re.S)
        self.assertIsNotNone(trecho)
        return json.loads(trecho.group(1))

    def test_referencia_e_deficit_compartilham_modelo(self):
        p = self.pacote(montar_html(self.base))
        self.assertEqual(p["referencia"]["resultados"], calcular(self.base["valores"]))
        self.assertAlmostEqual(p["teste_solar"]["resultados"]["participacao_solar"], 49)
        self.assertAlmostEqual(p["teste_solar"]["resultados"]["deficit_solar"], 91.8)

    def test_download_usa_entradas_da_sessao(self):
        entradas = self.base["valores"].copy()
        entradas.update(quantidade=20, dias=31, hsp=0.0)
        p = self.pacote(montar_html(self.base, entradas))
        self.assertEqual(p["referencia"]["entradas"], entradas)
        self.assertEqual(p["referencia"]["resultados"], calcular(entradas))
        self.assertFalse(p["referencia"]["resultados"]["atende"])
        self.assertEqual(self.base["valores"]["quantidade"], 10)

    def test_texto_importado_nao_fecha_script(self):
        self.base["integrantes"][0]["nome"] = '</script><script>exemplo</script>'
        html = montar_html(self.base)
        self.assertNotIn('</script><script>exemplo', html)
        self.assertEqual(self.pacote(html)["base"]["integrantes"][0]["nome"], self.base["integrantes"][0]["nome"])


if __name__ == "__main__":
    unittest.main()
