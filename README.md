# Gerenciador Geral de Ativos

Este projeto é um gerenciador geral de ativos desenvolvido em Python, com o objetivo de centralizar todas as informações dos seus ativos em um único aplicativo. Nele, você pode visualizar a distribuição dos seus ativos por categoria, custódia, tags e, individualmente, por ativo.

## Tecnologias Utilizadas

- **Python:** Linguagem de programação utilizada para o desenvolvimento da lógica do aplicativo.
- **JSON:** Formato utilizado para a persistência dos dados dos ativos.
- **PyQt:** Framework para a criação da interface gráfica interativa.
- **Matplotlib:** Biblioteca utilizada para gerar gráficos no canvas, permitindo a visualização visual dos dados.
- **yfinance API:** Utilizada para obter o valor atual dos ativos. **Atenção:** Ao cadastrar um ativo, o código deve ser informado conforme o utilizado na yfinance (exemplo: o código da NVIDIA deve ser "NVDA").

## Funcionalidades

### Overview dos Ativos
- **Visão Geral:** Exibe um resumo do capital acumulado.
- **Distribuição dos Ativos:** Permite visualizar os ativos agrupados por custódia, categoria e individualmente.

### Adição de Ativos e Tags
- **Adicionar Ativos:** Possibilita a inclusão de novos ativos ao sistema.  
  **Observação:** O código do ativo deve seguir o padrão da yfinance.  
- **Adicionar Tags:** Para associar uma tag a um ativo, basta arrastar a tag e soltá-la sobre o item correspondente.

### Criação de Estratégias
- **Personalização da Visualização:** Permite a criação de estratégias customizadas para analisar a distribuição dos ativos.  
  **Exemplo:** Se você deseja visualizar como está distribuída sua alocação de capital em renda variável, basta:
  1. Criar a tag "renda variável".
  2. Atribuir essa tag aos respectivos ativos.
  3. Selecionar as tags que compõem a visualização para agrupar os ativos de acordo com essa estratégia.

## Como Utilizar

1. **Clonar o repositório:**
   ```bash
   git clone https://github.com/Gustavo-Arcary-Passos/Investment-Centralizer.git
   ```

2. **Instalar as dependências:**
   Certifique-se de ter o Python instalado e, em seguida, instale as dependências necessárias:
   ```bash
   pip install -r requirements.txt
   ```
   > *Observação: O arquivo `requirements.txt` deve listar as bibliotecas `PyQt5`, `matplotlib`, `yfinance` e outras utilizadas.*

3. **Executar o aplicativo:**
   ```bash
   python main.py
   ```

## Considerações Finais

- **Desempenho:** O projeto não utiliza threads, o que pode ocasionar um desempenho abaixo do esperado em determinadas operações.
- **Objetivo do Projeto:** Este projeto foi desenvolvido com a intenção de adquirir conhecimento em PyQt e no uso de APIs.
- **Atualizações:** Não há planos, pelo menos no curto prazo, de continuar gerando novas versões ou melhorias neste projeto.
- **Localização:** O aplicativo foi concebido para o público brasileiro, portanto, as informações de capital estão em reais (BRL). Caso o ativo não seja dolarizado ou brasileiro, a conversão pode não estar correta.

