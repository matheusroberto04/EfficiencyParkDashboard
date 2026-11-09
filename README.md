# Efficiency Park

Módulo energético do **Neighborhood Action Dashboard — CitizenTech**.
Global Solution 2026.2 | Ciência da Computação | **Soluções em Energias Renováveis e Sustentáveis (SERS)**.

## Integrantes

| Nome | RM |
| --- | --- |
| Matheus Roberto | 575653 |
| Gustavo Oliveira Baptista | 575597 |
| Ana Luísa Santos | 574806 |

## Problema comunitário e objetivo

Uma praça comunitária precisa de iluminação noturna adequada, mas tecnologias menos eficientes aumentam a demanda elétrica. O Efficiency Park compara alternativas para reduzir essa demanda e avaliar a utilização de energia solar, apoiando decisões de moradores e responsáveis pela manutenção.

O estudo usa uma **praça de referência simulada**, com 10 pontos e 12 horas de iluminação por dia. Não houve visita, medição ou orçamento de implantação. São Paulo é apenas o contexto da tarifa de referência; não afirmamos que uma praça real foi diagnosticada.

Comparamos o cenário atual (lâmpadas convencionais na rede) com duas melhorias:

- **A — LED na rede:** substituição das luminárias, aproveitando a infraestrutura existente.
- **B — LED solar isolado:** uma luminária, um conjunto com dois painéis/controlador/baterias e um inversor por ponto, sem conexão à rede.

As alternativas usam a mesma quantidade de pontos e o mesmo horário. A comparação pressupõe iluminação adequada: fluxo luminoso é uma triagem, não uma validação fotométrica. Não há redução de horas ou economia atribuída a sensores.

**Estágio atual:** simulador em Python/Streamlit, com entradas manuais, indicadores, tabela, gráfico, diagrama, checagem solar, alertas de déficit, fontes e exportação JSON. Não é monitoramento em tempo real e não controla luminárias. Este é o módulo de SERS do integrador; não afirma integrar módulos de outras disciplinas já existentes.

## Primeiro acesso: baixar, instalar e testar

O painel funciona no navegador, mas precisa ser iniciado pelo Python no seu computador. As instruções abaixo estão separadas para **Windows** e **macOS (MacBook)**.

### 1. O que você precisa

- **Python:** use uma versão compatível com o Streamlit do projeto. A documentação consultada informa suporte a Python 3.11 a 3.15. O instalador está no [site oficial do Python](https://www.python.org/downloads/).
- **Internet durante a instalação:** para baixar as bibliotecas.
- **Um navegador:** para abrir o painel local.
- **VS Code, opcional:** facilita abrir a pasta e usar o terminal. Também é possível usar o PowerShell no Windows ou o Terminal no macOS.

Não é necessário instalar banco de dados, criar conta no Streamlit ou ter equipamentos físicos. O Git também é opcional: é possível baixar o projeto como ZIP.

### 2. Baixe e abra o projeto

1. Na página do repositório no GitHub, clique no botão **Code** e selecione **Download ZIP**.
2. Extraia o arquivo ZIP para uma pasta do computador. No Windows, use **Extrair Tudo**; no macOS, abra o ZIP para descompactar.
3. Localize a pasta que contém `app.py`, `calculos.py`, `dados.json`, `requirements.txt` e `diagrama.svg`. Mantenha esses arquivos juntos e abra a pasta principal do projeto.
4. No VS Code, selecione **Arquivo/File → Abrir Pasta/Open Folder** e escolha essa pasta.
5. Abra **Terminal → Novo Terminal/New Terminal**.

**Execute os comandos na pasta que contém `app.py` e `requirements.txt`, com o ZIP já extraído.** Digite uma linha por vez e aguarde sua conclusão antes de executar a próxima.

### 3. Instalação e execução no Windows

Use o terminal **PowerShell** do VS Code ou o PowerShell do Windows aberto na pasta do projeto.

**Confira se o Python está instalado:**

```powershell
py --version
```

O comando deve mostrar a versão do Python. Se `py` não for reconhecido, tente `python --version`. Se nenhum dos dois funcionar, instale o Python pelo site oficial, feche e abra novamente o terminal.

**Crie o ambiente virtual do projeto:**

```powershell
py -m venv .venv
```

Se o seu computador reconhece apenas `python`, use `python -m venv .venv` nesse passo.

**Instale as bibliotecas:**

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

**Inicie o painel:**

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Os comandos utilizam diretamente o Python da pasta `.venv`. Por isso, não é necessário executar um comando separado de ativação.

### 4. Instalação e execução no macOS / MacBook

Use o terminal do VS Code ou o aplicativo **Terminal**, aberto na pasta do projeto.

**Confira se o Python está instalado:**

```bash
python3 --version
```

Se o comando não for reconhecido ou a versão não for compatível, instale uma versão compatível pelo site oficial do Python e abra novamente o terminal.

**Crie o ambiente virtual do projeto:**

```bash
python3 -m venv .venv
```

**Instale as bibliotecas:**

```bash
.venv/bin/python -m pip install -r requirements.txt
```

**Inicie o painel:**

```bash
.venv/bin/python -m streamlit run app.py
```

Assim como no Windows, os comandos utilizam diretamente o Python do ambiente virtual.

### 5. Abra o painel no navegador

Após iniciar o sistema, o terminal mostrará um endereço chamado **Local URL**, normalmente:

**http://localhost:8501**

Abra esse endereço no navegador do mesmo computador. Se o terminal indicar outra porta, use o endereço exibido nele.

Mantenha o terminal aberto enquanto utiliza o painel. Para encerrar o sistema, pressione **Ctrl + C** no terminal; no Mac, também é a tecla Control.

## Dados, fontes e premissas

O arquivo [`dados.json`](dados.json) é a base de referência: contém integrantes, valores iniciais, fontes específicas e premissas. O painel apresenta essas informações e permite exportar entradas/resultados em JSON. As alterações feitas na interface não sobrescrevem a base; uma nova sessão usa os valores iniciais.

Referências consultadas em **09/11/2026**. Ofertas são registros de preço do vendedor na consulta, sem frete ou descontos especiais; não são médias de mercado, recomendações de compra ou orçamentos completos. A disponibilidade pode mudar.

| Entrada de referência | Valor | Origem e interpretação |
| --- | --- | --- |
| Quantidade e operação | 10 pontos, 12 h/dia, 30 dias | Cenário didático delimitado pela equipe. Não representa medição. |
| Lâmpada atual | 125 W; cerca de 6.250 lm | F1: potência nominal × eficiência luminosa de 50 lm/W. A estimativa não inclui perdas externas do reator. |
| Perdas adicionais do reator | 0 W no ensaio inicial | Limite inferior por falta de medição, não afirmação de perda física zero. O usuário pode informar perdas para uma comparação mais completa. |
| LED | 50 W, 7.500 lm; R$ 428,11/un. | F2: oferta de luminária pública Ourolux SI05126A. Fluxo é referência de triagem, não prova de iluminância equivalente. |
| Tarifa | R$ 0,43416/kWh | F3: B4a Enel São Paulo, tabela vigente desde 04/07/2026. `(259,83 + 174,33) / 1.000`. Sem tributos/adicionais separados, bandeiras ou custos fixos. Confirmar enquadramento antes de implantar. |
| Conjunto solar por ponto | R$ 2.801,88 | Kit F4 de R$ 2.402,88 + painel adicional F8 de R$ 399,00. Total: dois módulos de 210 Wp, controlador, duas baterias 12 V / 93 Ah e acessórios. Sem inversor. |
| Banco por ponto | 24 V e 93 Ah | Duas baterias de 12 V em série: a tensão soma, os Ah permanecem 93. Energia nominal = 2,232 kWh/ponto. |
| Inversor por ponto | 300 W contínuos; R$ 1.439,00 | F5: Volt, senoidal, 24 V / 127 V. Faz a conversão para a luminária CA. Deve ficar protegido do tempo e ter compatibilidade verificada. |
| Sol equivalente (HSP) | 4,5 h/dia | Condição de ensaio escolhida, não uma média meteorológica local. Testamos também 1 e 2 h/dia. Na implantação consultar recurso local e pior mês. |
| Rendimento solar global | 70% | Hipótese de perdas totais até a carga, incluindo armazenamento, conversão e auxiliares; não é eficiência medida. |
| Descarga / aproveitamento da saída | 50% / 85% | Hipóteses para estimar energia útil do banco inicialmente cheio. Não são limites certificados para a bateria. Não são multiplicadas novamente na geração, que já usa rendimento global. |
| Instalação A / B | 10% / 20% dos equipamentos | Provisão de escopo: B exige montagem, abrigo e proteção adicionais. Não é cotação de serviço. Sem postes novos, obras civis ou frete. |
| Reserva anual atual e A | 2% do custo de reposição das luminárias LED | Hipótese comum aos cenários na rede para não atribuir vantagem artificial de manutenção ao LED. Não é custo histórico da instalação atual. |
| Reserva anual B | 5% dos equipamentos solares e luminárias | Hipótese maior pela presença de baterias e eletrônica. Não é garantia de cobertura das reposições. Rateio mensal por 12. |

Valores de referência e hipóteses são diferentes: F1–F5, F8 e F9 sustentam características/ofertas/tarifa; **não validam** HSP, rendimentos, percentuais de instalação ou reservas. F6 fundamenta os conceitos do modelo, não seus coeficientes. As hipóteses estão explicitadas e são editáveis para análise de sensibilidade.

## Mesma necessidade de iluminação

A e B usam o mesmo LED e horário. A referência convencional tem fluxo nominal aproximado de 6.250 lm e a oferta LED declara 7.500 lm. Isso indica uma possibilidade a estudar, mas lúmens não são lux na praça: óptica, altura, espaçamento, perdas da luminária, envelhecimento e uniformidade mudam o resultado. O simulador não certifica equivalência luminosa nem atendimento às normas. Uma implantação depende dessa verificação. O consumo atual nominal é conservador por excluir o reator não medido.

## Cálculos de consumo e custos

Todos os resultados de consumo e operação usam **o mesmo período selecionado**. A reserva mensal é proporcional a `dias / 30`, adotando um mês contábil de 30 dias; não é extrapolação meteorológica anual.

```text
E_atual = quantidade × (potência atual + perda do reator) × horas/dia × dias / 1.000
E_LED = quantidade × potência LED × horas/dia × dias / 1.000
Economia = E_atual - E_LED
Economia (%) = Economia / E_atual × 100
Custo de compra = energia da rede × tarifa
Materiais A = quantidade × preço LED
Materiais B = quantidade × (preço LED + preço conjunto solar + preço inversor)
Implantação = materiais × (1 + percentual de instalação)
Reserva atual/A = materiais A × percentual anual rede / 12 × dias / 30
Reserva B = materiais B × percentual anual solar / 12 × dias / 30
Operação = compra de energia + reserva de manutenção/reposição
```

Sem consumo atual, a economia percentual é 0% por convenção. A economia financeira destacada nos indicadores considera somente energia comprada; a tabela inclui também provisões. O investimento inicial é separado. Sem análise de retorno, taxa de desconto, inflação ou garantia de reposições futuras.

## Checagem solar simplificada

O modelo considera **carga noturna, conjuntos idênticos por ponto e repetição de um dia de referência**, sem crédito por carga inicial de bateria. B não recebe energia da rede. O uso de inversor é necessário porque a luminária de referência é CA e o banco é CC.

O conjunto proposto adapta a referência comercial: **dois módulos de 210 Wp em série por ponto**, somando 420 Wp e Vmp nominal de 40,10 V. Um só módulo tem Vmp de 20,05 V e não sustenta a carga de um banco de 24 V. O módulo adicional de R$ 399,00 está incluído no custo. Os 420 Wp ficam abaixo dos 520 W declarados para o controlador em 24 V. A faixa MPPT, o Voc em baixa temperatura e os demais limites elétricos ainda precisam de validação no manual; não se trata de esquema de instalação.

```text
Demanda_LED_dia = quantidade × potência LED × horas/dia / 1.000
Potencial_solar_útil_dia = quantidade × painel_Wp × HSP × rendimento_global / 1.000
Banco_nominal = quantidade × tensão_banco × Ah / 1.000
Banco_útil = Banco_nominal × descarga × aproveitamento_saída
Limite_inversores_dia = quantidade × potência_contínua_inversor × horas/dia / 1.000
Solar_atendida_dia = mínimo(demanda, potencial útil, banco útil, limite inversores)
Déficit_período = (demanda_dia - solar_atendida_dia) × dias
Cobertura_solar (%) = solar_atendida / demanda_LED × 100
Autonomia_teórica (h) = banco_útil / potência_total_LED_em_kW
```

O limite de inversor é apenas um teto de energia; uma potência insuficiente também impede o atendimento integral instantâneo. A energia parcialmente atendida representa limite agregado do estudo, não prova de que o driver opera normalmente com alimentação insuficiente. A autonomia pressupõe banco cheio, inversor compatível e os coeficientes de ensaio.

**Não há soma de energia da bateria à geração:** a bateria armazena energia, não a cria. O rendimento global já inclui as perdas do caminho solar; o aproveitamento de saída é usado somente na checagem independente de capacidade do banco. Não se descontam as mesmas perdas duas vezes.

No padrão: demanda de 6 kWh/dia; potencial útil de 13,230 kWh/dia; banco nominal de 22,32 kWh e útil de 9,486 kWh. Autonomia teórica de 18,972 horas na potência de 500 W, aproximadamente 1,58 noites de 12 h, partindo de banco cheio. Isso **não comprova autonomia meteorológica**, confiabilidade ou operação durante várias noites sem recarga.

A referência comercial “até 750 Wh/dia” do kit não é usada como garantia. Calculamos com a potência dos componentes e as premissas. Em 1 HSP/dia, o potencial útil cai a 2,94 kWh/dia: somente 49% da demanda diária. Em 2 HSP/dia, a cobertura é 98% e ainda existe déficit. O painel mostra o déficit e bloqueia a indicação de economia operacional de B em serviço equivalente.

Não há simulação temporal do estado de carga, eventos climáticos, temperatura, envelhecimento, corrente de partida, limite real de descarga ou consumo em vazio. O estudo precisa ser validado com fichas completas, série solar e profissional habilitado antes de uma implantação. O título de atendimento no modelo é sempre condicional.

## Resultados no cenário de referência (30 dias)

| Item | Atual | A — LED na rede | B — LED solar isolado |
| --- | ---: | ---: | ---: |
| Demanda das luminárias (kWh) | 450,00 | 180,00 | 180,00 |
| Energia atendida (kWh) | 450,00 | 180,00 | 180,00 |
| Déficit no modelo (kWh) | 0,00 | 0,00 | 0,00 |
| Compra de energia da rede (kWh) | 450,00 | 180,00 | 0,00 |
| Compra de energia (R$) | 195,37 | 78,15 | 0,00 |
| Reserva para manutenção/reposição (R$) | 7,14 | 7,14 | 194,54 |
| Compra + reserva (R$) | 202,51 | 85,28 | 194,54 |
| Novo investimento estimado (R$) | 0,00 | 4.709,21 | 56.027,88 |

As diferenças são calculadas antes do arredondamento. A economia energética com LED é **270 kWh, ou 60%**. A economia na energia comprada de A é **R$ 117,22**. B cobre 100% da demanda no ensaio inicial, mas custa mais para implantar e provisiona mais manutenção. Compra zero de energia não significa consumo ou operação zero.

O investimento atual é zero por ser a instalação existente, não por ser gratuita. Não foi feita avaliação patrimonial do sistema atual. A provisão atual de manutenção é uma convenção de comparação, não um levantamento de despesas.

## Comparação técnica, ambiental e comunitária

| Aspecto | A — LED na rede | B — LED solar isolado |
| --- | --- | --- |
| Implantação | Menor investimento no exemplo; reaproveitar suportes e rede compatíveis. | Maior investimento; montagem dos painéis, abrigo, proteção e verificação estrutural. |
| Atendimento | Depende da rede e da iluminação adequada entregue. | Depende de recurso solar, carga, armazenamento, conversão e manutenção. Déficit invalida comparação financeira com serviço integral. |
| Eficiência | Reduz demanda de 450 para 180 kWh no exemplo. | Mesma demanda LED; a origem solar muda o fornecimento, não elimina o consumo. |
| Impactos | Menor demanda elétrica; destinação das lâmpadas convencionais, que podem conter mercúrio. | Fonte renovável direta; fabricação e destinação de baterias, painéis e eletrônica também causam impactos. |
| Benefícios esperados | Menor gasto e apoio à manutenção de iluminação adequada. | Uso local de renovável e estudo de opção para locais sem rede. |
| Limitações | Continuidade depende da rede; investimento e desempenho precisam de verificação local. | Maior complexidade e custo; autonomia não comprovada por este balanço. |

**Decisão no exemplo:** A é a opção inicial mais simples e de menor investimento para a praça com rede existente. B é uma alternativa renovável relevante quando autonomia em relação à rede é prioridade, sujeita à validação técnica e ao orçamento. Não existe vencedora universal. A comparação não demonstra aumento medido de segurança ou satisfação dos moradores.

Não calculamos CO₂ evitado por não ter sido adotado fator de emissão. Não atribuímos 0% de renováveis à rede e não chamamos B de “impacto zero”. Uma análise de ciclo de vida não foi realizada.

## Indicadores integrados ao dashboard

| Indicador | Unidade | Como é obtido |
| --- | --- | --- |
| Consumo atual e demanda LED | kWh/período | Quantidade × potência × tempo. |
| Economia de energia | kWh/período e % | Diferença entre atual e LED. |
| Economia na energia comprada de A | R$/período | Diferença dos consumos × tarifa. |
| Cobertura solar direta de B | % da demanda LED | Energia atendida pelo sistema solar / demanda. É indicador de uso de fonte renovável, não de emissões. |
| Déficit solar | kWh/período | Demanda LED - energia atendida. |
| Investimento e operação | R$ e R$/período | Equipamentos, provisões e compra da rede. |

Consumo e economia são indicadores energéticos; cobertura renovável e redução de demanda são os indicadores de sustentabilidade adotados. Gráfico e tabela mostram energia atendida e déficit, evitando apresentar falta de iluminação como eficiência. Indicadores correspondem às contas do módulo; o dashboard não é genérico.

## Diagrama conceitual

![Fontes, conversão, luminárias e dados manuais do Efficiency Park](diagrama.svg)

Setas contínuas: energia proposta. Setas tracejadas: dados digitados e processados. Sensores, temporizadores e automação física não estão implementados. O horário é um dado de operação assumido, comum às alternativas.

## Como conferir e demonstrar

1. Execute o painel e confira os resultados de referência acima.
2. Dobre os pontos para 20: os consumos, custos e capacidades totais devem dobrar.
3. Em “Sistema solar por ponto”, mude HSP para 1: cobertura de 49%, déficit de 91,8 kWh em 30 dias e alerta de serviço incompleto.
4. Informe zero horas: consumo e cobertura percentual ficam zero; reservas fixas permanecem.
5. Se alterar equipamentos, revise os preços e a iluminação entregue. O painel avisa dessa necessidade.
6. Baixe o JSON para registrar exatamente as entradas, saídas, fontes e premissas usadas.
7. Clique em **Baixar apresentação HTML desta simulação**: o arquivo usa as entradas atuais e os mesmos cálculos. No HTML, você também pode importar um JSON exportado pelo dashboard.

Testes dos cálculos, sem biblioteca adicional:

```bash
python -m unittest discover -s tests -v
```

No Mac, use `python3` ou `.venv/bin/python`. Os testes cobrem consumo, custos, déficit por falta de sol/bateria/inversor, ausência de demanda, perdas do reator, escala e coerência do período. A interface também possui teste de execução e mudanças de entradas em `tests/test_interface.py`, que usa o Streamlit instalado.

## Arquivos e contribuição de SERS

| Arquivo | Função |
| --- | --- |
| `app.py` | Interface Streamlit, entradas, resultados e exportação. |
| `calculos.py` | Cálculos de energia, checagem solar e custos. |
| `apresentacao.py` | Monta o HTML com resultados produzidos por `calculos.py`. |
| `apresentacao_template.html` | Modelo visual autossuficiente da apresentação, com fontes embutidas. |
| `apresentacao.html` | Apresentação offline gerada com as entradas de referência. |
| `dados.json` | Valores de referência, integrantes, fontes e premissas. |
| `diagrama.svg` | Funcionamento conceitual da solução. |
| `requirements.txt` | Dependência para execução. |
| `tests/` | Testes de cálculo e execução da interface. |
| `roteiro_video.md` | Sugestão de demonstração técnica de até 3 minutos. |
| `entrega_modelo.txt` | Integrantes, GitHub e campo a preencher com vídeo real. |

## Apresentação HTML integrada

Abra `apresentacao.html` no navegador. Há uma página de indicadores, modo apresentação em oito cenas e roteiro com cronômetro. As setas passam as cenas; F alterna tela cheia, R mostra as notas e H oculta os controles. O HTML é autossuficiente e não precisa de internet para exibir conteúdo. O botão **Abrir dashboard local** depende do Streamlit iniciado em `http://localhost:8501`.

O HTML não refaz os cálculos em JavaScript: incorpora entradas e resultados de `calculos.py`. O gerador inclui a referência e um ensaio com HSP = 1; o déficit do ensaio é calculado para a mesma quantidade e o mesmo período. O modo **Importar JSON do dashboard** usa a simulação exportada e atualiza indicadores e falas. Para voltar aos dados embutidos, use **Restaurar referência**. Importar um arquivo não altera o Python ou `dados.json`.

Se alterar dados ou o modelo visual do repositório, regenere a versão de referência:

```bash
python apresentacao.py
```

No Mac, use `python3` ou `.venv/bin/python`. A opção de download dentro do Streamlit já gera o HTML com as entradas da sessão. Fontes Barlow Condensed, Public Sans e IBM Plex Mono foram preservadas do HTML fornecido, originalmente embutidas sob a licença SIL Open Font License. A ilustração é conceitual e não representa projeto de iluminação validado.

## Entrega e próximos passos

- [x] Identificação do grupo, problema, duas alternativas e fonte renovável.
- [x] Cálculos, origem dos dados, hipóteses, limitações, diagrama e indicadores.
- [x] Código para o módulo energético e testes de cenários críticos.
- [ ] Gravar e publicar vídeo **não listado no YouTube, com no máximo 3 minutos**.
- [ ] Preencher o link real do vídeo no `entrega_modelo.txt`, verificar ambos os links e enviar **apenas o .txt** no Portal, no prazo informado pelo professor.

O vídeo deve mostrar problema, análise energética, alternativas, diagrama, dashboard, benefícios e limites. O roteiro é apoio: não substitui a gravação.

Em uma etapa de implantação: selecionar a praça real, ouvir a comunidade, medir cargas e perdas, conferir tarifa, validar iluminação e estrutura, obter orçamentos completos, analisar o pior mês solar e definir manutenção e descarte. Esses itens são próximos passos de campo, não realizações deste protótipo.

## Referências

Os links completos e a aplicação de cada fonte estão em [`dados.json`](dados.json), também visíveis no painel:

- **F1:** Philips/Signify, ficha HPL-N 125 W — potência e eficiência luminosa nominal.
- **F2:** Santa Iluminação, oferta Ourolux SI05126A — referência de LED e preço de venda.
- **F3:** Enel São Paulo, tabela de tarifas — referência B4a e conversão de R$/MWh para R$/kWh.
- **F4:** Energy Shop, kit solar 24 V — componentes e preço da oferta.
- **F5:** JC Network, inversor Volt 300 W — conversão senoidal e preço da oferta.
- **F6:** Ministério de Minas e Energia, *Sistemas Híbridos: Soluções Energéticas para a Amazônia*, 2008 — conceitos de geração, armazenamento e perdas.
- **F7:** Streamlit, documentação oficial — instalação e execução.
- **F8:** Energy Shop, módulo Resun 210 Wp — preço do painel adicional e tensões de referência.
- **F9:** Energy Shop, MPPT120D — limite nominal de potência em 24 V; já incluído no kit.

As fontes comerciais são referências de características declaradas e ofertas, sem endosso de fornecedor. A checagem de compatibilidade e o orçamento de engenharia continuam necessários para uso real.
