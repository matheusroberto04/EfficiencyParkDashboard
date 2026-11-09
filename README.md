# Praça Eficiente
Projeto desenvolvido para solução da Global Solution da faculdade FIAP! 
## O problema

Uma praça comunitária precisa de iluminação noturna. Uma instalação com potência elevada pode consumir mais energia do que uma alternativa eficiente, aumentando o gasto de operação.

Este trabalho considera uma **praça de referência simulada**, sem afirmar que foi realizada uma visita ou medição. O público beneficiado seriam os moradores que utilizam o espaço e os responsáveis por sua manutenção. O problema concreto analisado é a demanda de energia da iluminação durante a noite.

**Pergunta:** como reduzir essa demanda e comparar o fornecimento pela rede elétrica com uma alternativa solar?

## Nossa solução

Um painel em Python calcula o consumo e compara três cenários para a mesma quantidade de luminárias, tempo de funcionamento e necessidade de iluminação:

1. **Atual:** luminárias de referência alimentadas pela rede.
2. **Alternativa A:** substituição por LED alimentado pela rede.
3. **Alternativa B:** LED alimentado por um kit com painel solar e bateria.

O cenário atual é a referência. A e B são as duas alternativas de melhoria. Não há redução de horas nem sensor de presença nesta versão: a economia energética vem da potência informada para o LED. Um controle de horário é apenas uma condição operacional proposta, comum às alternativas, e não é executado pelo software.

**Estágio atual:** simulador funcional, com entrada manual, cálculos, tabela, gráfico e indicadores. Não é uma instalação física nem um sistema de monitoramento em tempo real.

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
3. Localize a pasta que contém `app.py`, `requirements.txt` e `diagrama.svg`. Dependendo de como o repositório foi organizado, esses arquivos podem estar dentro de uma subpasta chamada `praca_eficiente`.
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

### 6. Como testar o projeto

1. Observe os indicadores, a tabela e o gráfico com os valores iniciais.
2. Na barra lateral, altere a quantidade de luminárias e observe o recálculo automático.
3. Altere o número de horas ligadas por dia para verificar a mudança de consumo.
4. Expanda **Custos por luminária** para simular outros investimentos e reservas de manutenção.
5. Abra **Ver o funcionamento da solução** e **Ver as contas** para consultar o diagrama e as fórmulas.

Com os valores iniciais de **10 luminárias, 150 W atuais, 50 W LED, 12 horas/dia, 30 dias e tarifa de R$ 1,00/kWh**, confira:

| Resultado esperado | Valor |
| --- | --- |
| Consumo atual | 540 kWh no período |
| Consumo com LED | 180 kWh no período |
| Economia energética | 360 kWh, aproximadamente 66,7% |
| Economia somente na energia comprada — alternativa A | R$ 360 no período |

Se você mudar apenas a quantidade de 10 para 20, os consumos devem dobrar para 1.080 kWh e 360 kWh. Ao informar zero horas de funcionamento, o consumo deve ficar zero.

**Os dados iniciais são fictícios.** A alternativa solar supõe um kit capaz de atender toda a demanda; o programa não dimensiona painel ou bateria nem comprova essa capacidade. Consulte as premissas e limitações abaixo.

### 7. Como abrir novamente em outro dia

Abra o terminal na mesma pasta do projeto e execute somente o comando correspondente ao seu sistema:

**Windows:**

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```

**macOS:**

```bash
.venv/bin/python -m streamlit run app.py
```

Não é necessário recriar o ambiente ou reinstalar as bibliotecas a cada uso. Se você baixar uma nova cópia do projeto em outra pasta, repita a instalação nessa nova pasta. Se o `requirements.txt` for atualizado, execute novamente o comando de instalação das bibliotecas.

As alterações feitas no painel não são salvas em arquivo: uma nova sessão começa com os valores de exemplo.

### 8. Problemas comuns

| Mensagem ou situação | Como resolver |
| --- | --- |
| `Could not open requirements file` | Confirme que o terminal está na pasta do arquivo e que o comando usa exatamente `requirements.txt`, sem `~` no final. No PowerShell, use `dir`; no macOS, `ls` para conferir os arquivos. |
| `No module named streamlit` | Repita a instalação das bibliotecas e execute o painel com o Python da `.venv`, usando os comandos do seu sistema acima. |
| `py`, `python` ou `python3` não reconhecido | Confira a instalação do Python, reabra o terminal e use o comando correspondente ao seu sistema. |
| O caminho `.venv` não foi encontrado | Confirme a pasta atual e execute o passo de criação do ambiente virtual. |
| O navegador não abriu automaticamente | Copie a **Local URL** exibida no terminal e abra no navegador. |
| O painel parou de responder depois de fechar o terminal | Abra novamente o terminal na pasta do projeto e execute o comando de inicialização. |
| Erro ao carregar `diagrama.svg` | Confira se o arquivo está na mesma pasta de `app.py`; extraia todos os arquivos do projeto. |
| Erro de compilação de dependência no Mac | Confira a versão do Python e se as ferramentas de linha de comando do Xcode estão instaladas, conforme a documentação do Streamlit. O comando `xcode-select --install` inicia a instalação dessas ferramentas quando necessário. |
| Erro com versão de Python ou `No matching distribution found` | Confira os requisitos da versão indicada no arquivo e a versão mostrada pelo Python; atualize para uma versão compatível e crie novamente o ambiente virtual. |

Se o erro continuar, registre o comando executado e a mensagem completa para facilitar a identificação do problema.

## Arquivos

| Arquivo | Finalidade |
| --- | --- |
| `app.py` | Código principal, separado em cinco blocos comentados. |
| `requirements.txt` | Biblioteca necessária para executar o painel. |
| `diagrama.svg` | Diagrama conceitual mostrado no painel. |
| `README.md` | Problema, dados, contas, comparação, referências e limitações. |
| `entrega_modelo.txt` | Modelo do único arquivo a enviar no Portal, após preencher os links e os integrantes. |

## Dados utilizados e premissas

**Todos os valores iniciais são hipóteses didáticas**, escolhidas para permitir cálculos fáceis de conferir. Não são preços pesquisados, valores médios de mercado, tarifas oficiais ou características de produtos específicos. Os links de referência ao final não são a fonte desses números.

| Entrada inicial | Valor | Justificativa e origem |
| --- | --- | --- |
| Luminárias | 10 | Praça hipotética pequena, delimitada para o exercício. |
| Potência atual por luminária | 150 W | Hipótese para representar uma instalação de maior demanda. |
| Potência LED por luminária | 50 W | Hipótese de melhoria; equivalência luminosa ainda precisa de verificação técnica. |
| Funcionamento | 12 h/dia | Hipótese simplificada de funcionamento noturno constante. |
| Período | 30 dias | Mês de referência; o painel permite mudar entre 1 e 31 dias. |
| Tarifa | R$ 1,00/kWh | Valor redondo para demonstrar a multiplicação, sem pretensão de representar uma distribuidora. |
| LED instalado | R$ 350 por ponto | Hipótese: R$ 300 para equipamento e R$ 50 para instalação. |
| Kit solar instalado | R$ 1.650 por ponto | Hipótese: R$ 1.500 para conjunto LED/painel/bateria/controlador e R$ 150 para instalação. |
| Reserva para manutenção LED | R$ 2 por ponto/mês | Provisão didática para comparar operação, sem histórico de falhas. |
| Reserva para manutenção solar | R$ 5 por ponto/mês | Provisão didática maior, incluindo necessidade futura de manutenção do conjunto e bateria. Não é uma vida útil calculada. |
| Cobertura solar | 100% da demanda útil do LED | Hipótese condicional de um kit adequado; não é resultado de dimensionamento ou simulação meteorológica. |

Os custos são por ponto e multiplicados pela quantidade. Supõe-se aproveitamento da infraestrutura de suporte existente. Obras civis, troca de postes e adaptação da rede não foram orçadas. Os cenários usam a mesma praça e o mesmo período.

Para fortalecer a fundamentação antes de entregar, substituam as hipóteses de potência e custo por fichas técnicas e uma pesquisa simples de equipamentos/instalação, ou expliquem com o professor a aceitação do cenário inteiramente simulado. Registrem link, data, itens incluídos e contexto de cada valor. Para a tarifa, usem uma fonte aplicável à iluminação pública local: uma conta residencial pode não representar esse serviço.

## Cálculos

Fórmula do consumo, seguindo o enunciado:

`Energia (kWh) = quantidade × potência (W) × horas por dia × dias ÷ 1000`

Com os valores iniciais:

- Atual: `10 × 150 × 12 × 30 ÷ 1000 = 540 kWh` em 30 dias.
- LED: `10 × 50 × 12 × 30 ÷ 1000 = 180 kWh` em 30 dias.
- Economia de energia: `540 − 180 = 360 kWh` em 30 dias.
- Economia percentual: `360 ÷ 540 × 100 = 66,67%`.
- Custo atual da energia: `540 × 1,00 = R$ 540`.
- Custo da energia no LED da rede: `180 × 1,00 = R$ 180`.
- Economia somente na energia comprada, alternativa A: `540 − 180 = R$ 360`.

Na alternativa solar, **as luminárias continuam consumindo 180 kWh**. A hipótese do modelo é que toda essa energia útil seja fornecida pelo kit solar, sem compra da rede. A geração bruta necessária será maior devido às perdas; ela não é calculada nesta versão. Não se deve apresentar a tabela como prova de que um painel ou bateria específicos atendem à demanda.

`Implantação = quantidade × custo instalado por ponto`

`Operação em 30 dias = custo da energia no período ÷ dias × 30 + quantidade × reserva mensal de manutenção`

A normalização mantém a operação em 30 dias, mesmo se o usuário selecionar outro período para o consumo.

## Comparação no exemplo de 30 dias

| Critério | Atual | A — LED na rede | B — LED solar com bateria |
| --- | --- | --- | --- |
| Consumo útil das luminárias | 540 kWh | 180 kWh | 180 kWh |
| Energia comprada da rede | 540 kWh | 180 kWh | 0 kWh, sob a hipótese solar |
| Custo variável da energia | R$ 540 | R$ 180 | R$ 0, sob a hipótese solar |
| Novo investimento | R$ 0 | R$ 3.500 | R$ 16.500 |
| Reserva de manutenção em 30 dias | Não estimada | R$ 20 | R$ 50 |
| Operação em 30 dias | Não comparada por falta de manutenção atual | R$ 200 | R$ 50 |

O custo de energia é uma aproximação variável, não uma fatura completa. Não inclui encargos fixos, tributos separados ou um regime tarifário específico. Custo zero de compra da rede no cenário solar não significa custo zero de operação. Não calculamos retorno do investimento, pois seria necessário detalhar custos, manutenção e reposições.

### Viabilidade e impactos

| Aspecto | A — LED na rede | B — LED solar com bateria |
| --- | --- | --- |
| Condição técnica | Rede e instalação compatíveis; verificar a iluminação entregue. | Área sem sombreamento relevante, suporte adequado, painel/controlador/bateria dimensionados para as horas e a iluminação necessárias. |
| Benefício no modelo | Menor demanda elétrica e menor investimento inicial do que B no exemplo. | Menor demanda elétrica e substituição da compra de energia da rede por fonte renovável no cenário idealizado. |
| Limitação | Continua dependente da rede. | O modelo não comprova autonomia; clima e bateria afetam o atendimento. |
| Questão ambiental | Menor demanda, condicionada à equivalência de iluminação; destinação das lâmpadas retiradas. | Uso de fonte renovável; fabricação e destinação de painéis, eletrônicos e baterias precisam ser consideradas. |

Não estimamos emissões evitadas porque não foi selecionado um fator de emissão. Não atribuímos 0% de renováveis à rede: sua composição não foi analisada. Os 100% exibidos referem-se somente ao fornecimento solar direto hipotético da alternativa B.

Não há uma vencedora universal. A escolha depende de orçamento, infraestrutura e validação técnica. O simulador organiza essa decisão e não substitui um projeto de engenharia.

## Diagrama conceitual

![Fontes, luminárias, entrada manual, cálculos e indicadores](diagrama.svg)

As setas contínuas superiores representam energia. As setas tracejadas representam informações. O usuário digita os dados da iluminação; o programa calcula os resultados e alimenta o dashboard. O software não comanda as luminárias nem lê sensores reais.

## Indicadores e ligação com o dashboard

| Indicador | Unidade | Origem |
| --- | --- | --- |
| Consumo atual e com LED | kWh por período | Quantidade, potência e tempo. |
| Economia energética | kWh por período e % | Diferença entre atual e LED. |
| Economia na compra de energia com LED | R$ por período | Diferença dos consumos multiplicada pela tarifa. |
| Participação solar no cenário B | % | Energia útil solar assumida dividida pela demanda do cenário B. Com demanda zero, exibimos 0% por convenção. |

O gráfico compara energia da rede. A tabela também mostra o consumo das luminárias para não confundir origem da energia com eficiência. Este painel representa o módulo energético do Neighborhood Action Dashboard; não presume que outros módulos ou integrações já existam.

## Referências e origem

Consultadas em 09/11/2026:

1. **[Streamlit — documentação oficial](https://docs.streamlit.io/).** Referência da ferramenta. [Instalação por linha de comando](https://docs.streamlit.io/get-started/installation/command-line) e [gráfico de barras](https://docs.streamlit.io/develop/api-reference/charts/st.bar_chart).
2. **[ANEEL — Tarifas](https://www.gov.br/aneel/pt-br/assuntos/tarifas).** Referência institucional para entender e pesquisar tarifas. Não valida o valor fictício de R$ 1,00/kWh.
3. **[Inmetro — Tabelas de eficiência energética](https://www.gov.br/inmetro/pt-br/assuntos/regulamentacao/avaliacao-da-conformidade/programa-brasileiro-de-etiquetagem/tabelas-de-eficiencia-energetica).** Ponto de partida para pesquisar características de equipamentos quando aplicável. Não comprova equivalência luminosa entre as potências do exemplo.
