from pathlib import Path
import json

import streamlit as st

from calculos import calcular


# 1. Identificação e dados de referência
PASTA = Path(__file__).parent
base = json.loads((PASTA / "dados.json").read_text(encoding="utf-8"))
d = base["valores"].copy()


def numero(valor, casas=2):
    return f"{valor:,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".")


st.set_page_config(page_title="Efficiency Park", page_icon="💡", layout="wide")
st.title("💡 Efficiency Park")
st.write("Módulo energético do Neighborhood Action Dashboard / CitizenTech")
st.caption("Global Solution 2026.2 | Ciência da Computação | " + base["disciplina"])
st.info("Simulação acadêmica: referências de equipamentos e tarifa + premissas editáveis. Sem medições ou controle de equipamentos.")
with st.expander("Equipe e problema comunitário"):
    for pessoa in base["integrantes"]:
        st.write(f"{pessoa['nome']} · RM{pessoa['rm']}")
    st.write("Praça de referência simulada: comparar a iluminação convencional com LED na rede (A) e LED solar com bateria (B), mantendo quantidade e horário. Beneficiários: moradores, usuários da praça e responsáveis pela manutenção.")

# 2. Entradas manuais; origens e premissas também aparecem no painel.
st.sidebar.header("Dados da praça")
d["quantidade"] = st.sidebar.number_input("Quantidade de luminárias", 1, 100, d["quantidade"])
d["potencia_atual"] = st.sidebar.number_input("Potência da lâmpada atual (W)", 1.0, 1000.0, d["potencia_atual"])
d["perda_reator"] = st.sidebar.number_input("Perda adicional do reator (W/ponto)", 0.0, 200.0, d["perda_reator"])
d["potencia_led"] = st.sidebar.number_input("Potência LED (W/ponto)", 1.0, 1000.0, d["potencia_led"])
d["horas"] = st.sidebar.number_input("Horas ligadas por dia", 0.0, 24.0, d["horas"], step=0.5)
d["dias"] = st.sidebar.number_input("Dias do período", 1, 31, d["dias"])
d["tarifa"] = st.sidebar.number_input("Tarifa de referência (R$/kWh)", 0.0, 10.0, d["tarifa"], step=0.01, format="%.5f")
st.sidebar.caption("Inicial: B4a Enel SP, TUSD + TE, sem adicionais. Consulte a origem dos dados abaixo.")

with st.sidebar.expander("Sistema solar por ponto"):
    d["painel_wp"] = st.number_input("Arranjo FV (Wp/ponto)", 0.0, 2000.0, d["painel_wp"])
    d["hsp"] = st.number_input("Sol equivalente - HSP (h/dia)", 0.0, 8.0, d["hsp"], step=0.5)
    d["rendimento_solar"] = st.number_input("Rendimento global até a carga (%)", 0.0, 100.0, d["rendimento_solar"] * 100) / 100
    d["bateria_v"] = st.number_input("Banco por ponto (V)", 1.0, 96.0, d["bateria_v"])
    d["bateria_ah"] = st.number_input("Banco por ponto (Ah)", 0.0, 1000.0, d["bateria_ah"])
    d["descarga"] = st.number_input("Descarga máxima de ensaio (%)", 0.0, 100.0, d["descarga"] * 100) / 100
    d["rendimento_descarga"] = st.number_input("Aproveitamento da saída do banco (%)", 0.0, 100.0, d["rendimento_descarga"] * 100) / 100
    d["inversor_w"] = st.number_input("Inversor - potência contínua (W/ponto)", 0.0, 3000.0, d["inversor_w"])
    st.caption("Um kit, um painel extra e um inversor por ponto. Alterar capacidade exige rever preços. Coeficientes são hipóteses de ensaio.")

with st.sidebar.expander("Custos e provisões"):
    for chave, rotulo in [("preco_led", "Luminária LED (R$/un.)"), ("preco_kit", "Conjunto solar sem inversor (R$/ponto)"), ("preco_inversor", "Inversor (R$/un.)")]:
        d[chave] = st.number_input(rotulo, min_value=0.0, value=d[chave], step=10.0)
    for chave, rotulo in [("instalacao_led", "Instalação A (% dos equipamentos)"), ("instalacao_solar", "Instalação B (% dos equipamentos)"), ("reserva_rede", "Reserva anual atual/A (% das luminárias)"), ("reserva_solar", "Reserva anual B (% dos equipamentos)")]:
        d[chave] = st.number_input(rotulo, 0.0, 100.0, d[chave] * 100) / 100
    st.caption("Instalação e reservas são hipóteses orçamentárias. Sem frete, obras civis ou postes novos.")

# 3. Cálculos separados da interface para facilitar a conferência.
r = calcular(d)
periodo = f"{d['dias']} dias"
st.subheader(f"Resultados projetados em {periodo}")
c1, c2, c3 = st.columns(3)
c1.metric("Consumo atual", numero(r["consumo_atual"], 1) + " kWh")
c2.metric("Demanda com LED", numero(r["consumo_led"], 1) + " kWh")
c3.metric("Economia energética com LED", numero(r["economia_percentual"], 1) + "%")
c4, c5, c6 = st.columns(3)
c4.metric("Energia economizada com LED", numero(r["economia_energia"], 1) + " kWh")
c5.metric("Economia na energia comprada - A", "R$ " + numero(r["custo_energia_atual"] - r["custo_energia_led"]))
c6.metric("Demanda coberta por solar - B", numero(r["participacao_solar"], 1) + "%")
st.caption("Economia financeira do indicador considera só a compra de energia. Cobertura solar é estimativa do balanço, não medição nem garantia de autonomia.")
if r["economia_energia"] <= 0 and r["consumo_atual"] > 0:
    st.warning("As potências informadas não produzem economia com LED.")
if any(d[chave] != base["valores"][chave] for chave in ("potencia_atual", "potencia_led", "painel_wp", "bateria_v", "bateria_ah", "inversor_w")):
    st.warning("Capacidades alteradas: as referências e os preços iniciais podem deixar de representar os equipamentos simulados. Atualize o orçamento e verifique a iluminação entregue.")

# 4. Comparação para o mesmo serviço e período
st.subheader("Comparação energética e financeira")
tabela = {
    "Cenário": ["Atual - rede", "A - LED na rede", "B - LED solar isolado"],
    "Demanda (kWh/período)": [r["consumo_atual"], r["consumo_led"], r["consumo_led"]],
    "Energia atendida (kWh/período)": [r["consumo_atual"], r["consumo_led"], r["solar_atendida"]],
    "Déficit (kWh/período)": [0.0, 0.0, r["deficit_solar"]],
    "Compra da rede (kWh/período)": [r["consumo_atual"], r["consumo_led"], 0.0],
    "Compra de energia (R$/período)": [r["custo_energia_atual"], r["custo_energia_led"], 0.0],
    "Provisão manutenção/reposição (R$/período)": [r["reserva_rede"], r["reserva_rede"], r["reserva_solar"]],
    "Energia + provisão (R$/período)": [r["operacao_atual"], r["operacao_led"], r["operacao_solar"]],
    "Novo investimento (R$)": [0.0, r["investimento_led"], r["investimento_solar"]]
}
st.dataframe(tabela, hide_index=True)
st.caption("Provisões são reservas estimadas. Investimento atual = zero porque a instalação existente é a referência. Toda operação usa o período selecionado.")
st.bar_chart(tabela, x="Cenário", y=["Energia atendida (kWh/período)", "Déficit (kWh/período)"])
st.write(f"Economia operacional estimada de A: R$ {numero(r['economia_operacao_led'])} em {periodo}.")
if r["atende"]:
    st.write(f"Saldo operacional atual menos B: R$ {numero(r['economia_operacao_solar'])} em {periodo}. Valor negativo indica custo maior para B.")
else:
    st.error(f"B apresenta déficit de {numero(r['deficit_solar'])} kWh. Não atende à mesma necessidade: seu menor gasto não pode ser apresentado como economia de um serviço equivalente.")

st.subheader("Checagem simplificada da opção solar")
st.write(f"Demanda LED: {numero(r['demanda_dia'], 3)} kWh/dia. Potencial útil solar: {numero(r['geracao_util_dia'], 3)} kWh/dia.")
st.write(f"Banco total: {numero(r['bateria_nominal'], 3)} kWh nominais e {numero(r['bateria_util'], 3)} kWh úteis de ensaio.")
if d["horas"] > 0:
    st.write(f"Autonomia teórica com banco inicialmente cheio: {numero(r['autonomia_horas'], 1)} horas na potência LED, condicionada ao inversor e às hipóteses.")
else:
    st.write("Sem demanda de iluminação: cobertura solar = 0% por convenção; não há economia de energia.")
st.warning("Balanço de dias iguais e carga noturna. Não acompanha estado de carga, sequência de dias nublados, envelhecimento ou consumo em vazio real. Atendimento no modelo não comprova confiabilidade de uma instalação.")

# 5. Diagrama, explicação, fontes e exportação
with st.expander("Benefícios, viabilidade e limites"):
    st.write("Arranjo de referência: dois módulos 210 Wp em série, total de 420 Wp por ponto. O segundo módulo está incluído no preço do conjunto solar; um único módulo de Vmp 20,05 V não sustenta a carga do banco de 24 V. Limites elétricos finais dependem da validação do controlador.")
    st.write("A aproveita a rede existente e tem menor investimento no exemplo. B usa fonte renovável direta e armazenamento, com maior investimento e necessidade de abrigo, área sem sombra e manutenção das baterias.")
    st.write("Referência luminosa: cerca de 6.250 lm na lâmpada convencional e 7.500 lm na oferta LED. Fluxo luminoso sugere uma alternativa plausível, mas não comprova iluminância, uniformidade ou atendimento a normas. Verificar altura, espaçamento, óptica e condições da praça.")
    st.write("Benefícios esperados: reduzir a demanda elétrica mantendo iluminação adequada e apoiar a decisão do gestor. Não medimos segurança ou satisfação dos moradores. Lâmpadas com mercúrio, baterias, painéis e eletrônica exigem destinação adequada.")
    st.write("Não calculamos CO₂ evitado nem afirmamos que a rede não usa renováveis. A cobertura solar refere-se somente à demanda de B. Sem análise de ciclo de vida, projeto executivo ou retorno do investimento.")
with st.expander("Diagrama de funcionamento"):
    st.image(str(PASTA / "diagrama.svg"))
    st.caption("Fluxo energético proposto e dados manuais. O software não lê sensores nem aciona equipamentos.")
with st.expander("Cálculos e premissas"):
    st.write("Consumo = quantidade × potência (W) × horas/dia × dias ÷ 1.000.")
    st.write("Economia (%) = (consumo atual − demanda LED) ÷ consumo atual × 100; sem consumo atual, usamos 0%.")
    st.write("Potencial solar útil/dia = quantidade × Wp/ponto × HSP × rendimento global ÷ 1.000.")
    st.write("Banco útil = quantidade × V × Ah × descarga × aproveitamento de saída ÷ 1.000.")
    st.write("Solar atendida/dia = menor valor entre demanda, potencial solar útil, banco útil e limite diário dos inversores. Déficit = demanda − atendida.")
    st.write("Cobertura solar = energia solar atendida ÷ demanda LED × 100; sem demanda, usamos 0%.")
    st.write("Implantação = equipamentos × (1 + provisão de instalação). Operação = energia comprada × tarifa + reserva anual de equipamentos ÷ 12 × dias ÷ 30.")
    for premissa in base["premissas"]:
        st.markdown(f"**{premissa['parametro']}**: {premissa['origem']}")
with st.expander("Dados e fontes consultadas"):
    st.caption("Consulta: " + base["consulta"] + ". Ofertas não são orçamentos de implantação; preços e tarifas podem mudar.")
    for fonte in base["fontes"]:
        st.markdown(f"**{fonte['id']} · [{fonte['titulo']}]({fonte['url']})** — {fonte['uso']}")
st.download_button("Baixar entradas e resultados da simulação (JSON)", json.dumps({"entradas": d, "resultados": r, "referencias": base["fontes"], "premissas": base["premissas"]}, ensure_ascii=False, indent=2), file_name="efficiency_park_simulacao.json", mime="application/json")
