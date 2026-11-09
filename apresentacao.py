"""Gera a apresentação HTML usando os mesmos dados e cálculos do dashboard."""
import json
from pathlib import Path

from calculos import calcular

PASTA = Path(__file__).parent


def montar_html(base, entradas=None):
    dados = base["valores"].copy() if entradas is None else entradas.copy()
    pouco_sol = dados.copy()
    pouco_sol["hsp"] = 1.0
    pacote = {
        "base": base,
        "referencia": {"entradas": dados, "resultados": calcular(dados)},
        "teste_solar": {"entradas": pouco_sol, "resultados": calcular(pouco_sol)},
    }
    # Impede que conteúdo textual feche a tag script do documento.
    conteudo = json.dumps(pacote, ensure_ascii=False).replace("<", "\\u003c")
    modelo = (PASTA / "apresentacao_template.html").read_text(encoding="utf-8")
    return modelo.replace("__EFFICIENCY_DADOS__", conteudo)


if __name__ == "__main__":
    base = json.loads((PASTA / "dados.json").read_text(encoding="utf-8"))
    destino = PASTA / "apresentacao.html"
    destino.write_text(montar_html(base), encoding="utf-8")
    print("Apresentação atualizada: " + str(destino))
