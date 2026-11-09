from pathlib import Path

import streamlit as st


# 1. Configuração da página
st.set_page_config(page_title="Eficiency Park - Dashboard", page_icon="💡", layout="wide")
st.title("💡 Eficiency Park - Dashboard")
st.write("Simulador de alternativas para a iluminação de uma praça comunitária.")
st.info("Projeto acadêmico: os valores iniciais são hipotéticos, não são medições ou orçamentos.")

# 2. Dados informados pelo usuário
st.sidebar.header("Dados da praça")
quantidade = st.sidebar.number_input("Quantidade de luminárias", 1, 100, 10)
potencia_atual = st.sidebar.number_input("Potência atual por luminária (W)", 1, 1000, 150)
potencia_led = st.sidebar.number_input("Potência LED por luminária (W)", 1, 1000, 50)
horas = st.sidebar.number_input("Horas ligadas por dia", 0.0, 24.0, 12.0, step=0.5)
dias = st.sidebar.number_input("Dias do período", 1, 31, 30)
tarifa = st.sidebar.number_input("Tarifa estimada (R$/kWh)", 0.0, 10.0, 1.0, step=0.05)

with st.sidebar.expander("Custos por luminária — exemplos fictícios"):
    custo_led = st.number_input("LED instalado (R$ por unidade)", 0.0, value=350.0, step=50.0)
    custo_solar = st.number_input("Kit solar instalado (R$ por unidade)", 0.0, value=1650.0, step=50.0)
    manutencao_led = st.number_input("Reserva mensal LED (R$ por unidade)", 0.0, value=2.0)
    manutencao_solar = st.number_input("Reserva mensal solar (R$ por unidade)", 0.0, value=5.0)

# 3. Cálculos básicos: potência em watts deve ser dividida por 1000
consumo_atual = quantidade * potencia_atual * horas * dias / 1000
consumo_led = quantidade * potencia_led * horas * dias / 1000
economia_energia = consumo_atual - consumo_led
economia_percentual = 0.0
if consumo_atual > 0:
    economia_percentual = economia_energia / consumo_atual * 100

# A luminária solar também consome energia. Neste cenário idealizado,
# supomos que um kit com painel e bateria atenda toda a demanda do LED.
consumo_solar = consumo_led
energia_rede_solar = 0.0
energia_solar_util = consumo_solar
participacao_solar = 0.0
if consumo_solar > 0:
    participacao_solar = energia_solar_util / consumo_solar * 100

custo_energia_atual = consumo_atual * tarifa
custo_energia_led = consumo_led * tarifa
custo_energia_solar = energia_rede_solar * tarifa
implantacao_led = quantidade * custo_led
implantacao_solar = quantidade * custo_solar
operacao_led = custo_energia_led / dias * 30 + quantidade * manutencao_led
operacao_solar = custo_energia_solar / dias * 30 + quantidade * manutencao_solar

# 4. Indicadores do dashboard
st.subheader("Resultados do período")
coluna1, coluna2, coluna3 = st.columns(3)
coluna1.metric("Consumo atual", f"{consumo_atual:.1f} kWh")
coluna2.metric("Consumo com LED", f"{consumo_led:.1f} kWh")
coluna3.metric("Economia energética com LED", f"{economia_percentual:.1f}%")
coluna4, coluna5, coluna6 = st.columns(3)
coluna4.metric("Energia economizada com LED", f"{economia_energia:.1f} kWh")
coluna5.metric("Economia na energia comprada — LED", f"R$ {custo_energia_atual - custo_energia_led:.2f}")
coluna6.metric("Participação solar no cenário B", f"{participacao_solar:.0f}%")
st.caption(f"Período: {dias} dias. Economia financeira acima considera apenas a energia comprada.")

if potencia_led >= potencia_atual:
    st.warning("Com as potências informadas, o LED não reduz o consumo. Reveja a comparação.")

# Listas e dicionários organizam os dados da tabela e do gráfico.
comparacao = {
    "Cenário": ["Atual", "A — LED na rede", "B — LED solar com bateria"],
    "Consumo das luminárias (kWh/período)": [consumo_atual, consumo_led, consumo_solar],
    "Energia da rede (kWh/período)": [consumo_atual, consumo_led, energia_rede_solar],
    "Custo da energia (R$/período)": [custo_energia_atual, custo_energia_led, custo_energia_solar],
    "Investimento novo (R$)": [0.0, implantacao_led, implantacao_solar],
}
st.subheader("Comparação das alternativas")
st.dataframe(comparacao, hide_index=True)
st.caption("O investimento atual é zero porque não há uma nova instalação nesse cenário.")
st.bar_chart(comparacao, x="Cenário", y="Energia da rede (kWh/período)", color="#2e7d32")
st.write(f"A: implantação de R$ {implantacao_led:.2f}. B: implantação de R$ {implantacao_solar:.2f}.")
st.write(f"Operação estimada em 30 dias: A = R$ {operacao_led:.2f}; B = R$ {operacao_solar:.2f}.")
st.caption("Operação inclui energia e reserva para manutenção; o investimento inicial é separado.")

st.subheader("Como interpretar")
st.write("A alternativa A usa a rede existente e exige conferir a compatibilidade da instalação.")
st.write("A alternativa B usa energia solar e precisa de local sem sombra, painel e bateria adequados.")
st.warning(
    "Os 100% de atendimento solar são uma hipótese, não uma geração calculada. "
    "Este protótipo não dimensiona painel ou bateria e não comprova autonomia em dias nublados."
)
st.write(
    "O LED reduz a demanda no exemplo. A fonte solar substitui a energia da rede, "
    "mas não elimina o consumo das luminárias. A comparação pressupõe iluminação equivalente."
)
st.write(
    "Benefícios esperados: menor desperdício e apoio à decisão da comunidade. "
    "Na implantação, é preciso verificar a iluminação adequada e o descarte de lâmpadas, painéis e baterias."
)

# 5. Diagrama conceitual e transparência dos cálculos
with st.expander("Ver o funcionamento da solução"):
    st.image(str(Path(__file__).with_name("diagrama.svg")))
    st.caption("As informações são digitadas manualmente. O painel não recebe dados de sensores reais.")

with st.expander("Ver as contas"):
    st.write("Consumo (kWh) = quantidade × potência (W) × horas/dia × dias ÷ 1000")
    st.write("Custo de energia (R$) = energia comprada da rede (kWh) × tarifa (R$/kWh)")
    st.write("Economia (%) = (consumo atual − consumo LED) ÷ consumo atual × 100")
    st.write("Implantação (R$) = quantidade × custo instalado por luminária")
    st.write("Operação em 30 dias (R$) = custo diário da energia × 30 + reserva mensal de manutenção")
    st.caption("Os dados, as limitações e as referências estão explicados no README do projeto.")
