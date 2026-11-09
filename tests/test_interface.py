from pathlib import Path
import sys
import unittest
from streamlit.testing.v1 import AppTest
PASTA=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(PASTA))


class TestInterface(unittest.TestCase):
    def entrada(self,app,rotulo):return next(x for x in app.number_input if x.label==rotulo)

    def test_valores_originais_editaveis_e_restauracao(self):
        app=AppTest.from_file(str(PASTA/'app.py'),default_timeout=30).run()
        self.assertEqual(len(app.exception),0)
        self.assertEqual(app.metric[0].value,'491,3 kWh')
        self.assertEqual(app.metric[1].value,'177,6 kWh')
        self.assertEqual(app.metric[2].value,'63,9%')
        self.entrada(app,'Quantidade de postes').set_value(24)
        app.run()
        self.assertEqual(len(app.exception),0)
        self.assertEqual(app.metric[0].value,'982,6 kWh')
        next(x for x in app.button if x.label=='Restaurar valores do HTML original').click()
        app.run()
        self.assertEqual(len(app.exception),0)
        self.assertEqual(app.metric[0].value,'491,3 kWh')

    def test_falta_de_sol_e_presenca(self):
        app=AppTest.from_file(str(PASTA/'app.py'),default_timeout=30).run()
        self.entrada(app,'HSP de ensaio conservador A2 (h/dia)').set_value(0.0)
        app.run()
        self.assertEqual(len(app.exception),0)
        self.assertTrue(any('A2 não atende' in x.value for x in app.error))
        self.entrada(app,'Presença estimada na madrugada (%)').set_value(100.0)
        app.run()
        self.assertEqual(len(app.exception),0)
        self.assertGreater(float(app.metric[1].value.split()[0].replace(',','.')),177.6)


if __name__=='__main__':unittest.main()
