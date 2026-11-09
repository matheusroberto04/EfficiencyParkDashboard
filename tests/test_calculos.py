"""Conferência dos casos em que uma comparação energética pode enganar."""
import json
from pathlib import Path
import sys
import unittest

PASTA = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PASTA))
from calculos import calcular


class TestCalculos(unittest.TestCase):
    def setUp(self):
        self.dados = json.loads((PASTA / "dados.json").read_text(encoding="utf-8"))["valores"]

    def test_exemplo_de_referencia(self):
        r = calcular(self.dados)
        self.assertAlmostEqual(r["consumo_atual"], 450)
        self.assertAlmostEqual(r["consumo_led"], 180)
        self.assertAlmostEqual(r["economia_percentual"], 60)
        self.assertAlmostEqual(r["custo_energia_led"], 78.1488)
        self.assertAlmostEqual(r["investimento_led"], 4709.21)
        self.assertAlmostEqual(r["investimento_solar"], 56027.88)
        self.assertAlmostEqual(r["geracao_util_dia"], 13.23)
        self.assertAlmostEqual(r["bateria_nominal"], 22.32)
        self.assertAlmostEqual(r["bateria_util"], 9.486)
        self.assertAlmostEqual(r["autonomia_horas"], 18.972)
        self.assertTrue(r["atende"])

    def test_dia_com_pouco_sol_nao_vira_falsa_economia(self):
        self.dados["hsp"] = 1
        r = calcular(self.dados)
        self.assertAlmostEqual(r["solar_atendida"], 88.2)
        self.assertAlmostEqual(r["deficit_solar"], 91.8)
        self.assertAlmostEqual(r["participacao_solar"], 49)
        self.assertFalse(r["atende"])
        self.assertIsNone(r["economia_operacao_solar"])

    def test_banco_insuficiente_limita_carga_noturna(self):
        self.dados["bateria_ah"] = 10
        r = calcular(self.dados)
        self.assertAlmostEqual(r["solar_atendida"], 30.6)
        self.assertFalse(r["atende"])

    def test_inversor_insuficiente_limita_atendimento(self):
        self.dados["inversor_w"] = 25
        r = calcular(self.dados)
        self.assertAlmostEqual(r["participacao_solar"], 50)
        self.assertFalse(r["atende"])

    def test_sem_sol_nao_inventa_carga_inicial(self):
        self.dados["hsp"] = 0
        r = calcular(self.dados)
        self.assertEqual(r["solar_atendida"], 0)
        self.assertEqual(r["deficit_solar"], 180)

    def test_sem_demanda_nao_divide_por_zero(self):
        self.dados["horas"] = 0
        r = calcular(self.dados)
        self.assertEqual(r["consumo_atual"], 0)
        self.assertEqual(r["economia_percentual"], 0)
        self.assertEqual(r["participacao_solar"], 0)
        self.assertGreater(r["operacao_solar"], 0)

    def test_mudar_periodo_mantem_custos_na_mesma_base(self):
        r30 = calcular(self.dados)
        self.dados["dias"] = 31
        r31 = calcular(self.dados)
        self.assertAlmostEqual(r31["operacao_led"], r30["operacao_led"] * 31 / 30)
        self.assertAlmostEqual(r31["operacao_solar"], r30["operacao_solar"] * 31 / 30)
        self.assertEqual(r31["investimento_solar"], r30["investimento_solar"])

    def test_escala_dos_pontos_e_reator(self):
        self.dados["quantidade"] = 20
        self.dados["perda_reator"] = 10
        r = calcular(self.dados)
        self.assertAlmostEqual(r["consumo_atual"], 972)
        self.assertAlmostEqual(r["consumo_led"], 360)
        self.assertAlmostEqual(r["bateria_nominal"], 44.64)

    def test_led_mais_potente_e_tarifa_zero(self):
        self.dados["potencia_led"] = 200
        self.dados["tarifa"] = 0
        r = calcular(self.dados)
        self.assertLess(r["economia_energia"], 0)
        self.assertEqual(r["custo_energia_led"], 0)
        self.assertGreater(r["operacao_led"], 0)


if __name__ == "__main__":
    unittest.main()
