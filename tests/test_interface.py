"""Executa o Streamlit e verifica mudanças visíveis nas entradas críticas."""
from pathlib import Path
import sys
import unittest

from streamlit.testing.v1 import AppTest

PASTA = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PASTA))


class TestInterface(unittest.TestCase):
    def entrada(self, app, rotulo):
        return next(item for item in app.number_input if item.label == rotulo)

    def test_referencia_e_alerta_solar(self):
        app = AppTest.from_file(str(PASTA / "app.py"), default_timeout=30).run()
        self.assertEqual(len(app.exception), 0)
        self.assertEqual(app.title[0].value, "💡 Efficiency Park")
        self.assertEqual(app.metric[0].value, "450,0 kWh")
        self.assertEqual(app.metric[5].value, "100,0%")
        self.assertEqual(len(app.error), 0)
        self.entrada(app, "Sol equivalente - HSP (h/dia)").set_value(1.0)
        app.run()
        self.assertEqual(len(app.exception), 0)
        self.assertEqual(app.metric[5].value, "49,0%")
        self.assertEqual(len(app.error), 1)
        self.assertIn("91,80 kWh", app.error[0].value)

    def test_sem_demanda_e_periodo(self):
        app = AppTest.from_file(str(PASTA / "app.py"), default_timeout=30).run()
        self.entrada(app, "Horas ligadas por dia").set_value(0.0)
        self.entrada(app, "Dias do período").set_value(31)
        app.run()
        self.assertEqual(len(app.exception), 0)
        self.assertEqual(app.metric[0].value, "0,0 kWh")
        self.assertEqual(app.metric[5].value, "0,0%")
        self.assertEqual(len(app.error), 0)


if __name__ == "__main__":
    unittest.main()
