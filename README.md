# Controle de Estoque de Notebooks
Sistema de controle do estoque de notebooks e tablets de uma escola pública.
Mesma estrutura do sistema de empréstimos da biblioteca (Flask + PostgreSQL), adaptada para inventário.

## O que o sistema faz
- Lista todos os equipamentos com **Nº, Série, Equipamento, Status e Observação** (mais o carrinho/local e o tipo: notebook ou tablet).
- Cartões-resumo por status (clique no cartão para filtrar) e busca por série, nº ou observação.
- Filtros por tipo, carrinho e status.
- **Editar** um equipamento: série, marca/modelo, status e observação.
- **+ Novo equipamento**: cadastra um aparelho novo (o Nº segue a sequência do carrinho).

## Status
| Status | Significado |
|---|---|
| Completo / Funcional | À disposição para uso |
| Em análise | Fica com o responsável técnico; havendo peças e ferramentas, o reparo é feito na escola |
| Reparo | Enviado para conserto fora do ambiente escolar |
| Não funcional | Fora da garantia e sem conserto |
| Desaparecido | Equipamento furtado |

Os status ficam definidos em `status.py` (e no `CHECK` do `schema.sql`).

## Requisitos
- Python 3.11+
- PostgreSQL 16+

## Instalação

1. Instale as dependências:
   pip install -r requirements.txt

2. Crie o banco de dados no PostgreSQL:
   - Crie um banco chamado: estoque_notebooks
   - Execute o arquivo: schema.sql no pgAdmin

3. Configure a senha do banco em db.py (ou defina a variável de ambiente DB_PASSWORD):
   password="estoque"

4. Prepare e carregue a planilha de inventário:
   A planilha da escola **não faz parte deste repositório** (ela lista os números de série dos aparelhos).
   Use a sua própria planilha, no formato descrito em "Formato da planilha" abaixo, salva na pasta do projeto.
   O arquivo `modelo_planilha.xlsx` é um modelo com dados fictícios: copie-o, apague os exemplos e preencha com os seus dados.
   python importar_equipamentos.py minha_planilha.xlsx
   Sem informar o nome do arquivo, o script procura por RELACAO_INVENTARIO_EDITADO.xlsx.
   Para só conhecer o sistema, importe o próprio modelo (`python importar_equipamentos.py modelo_planilha.xlsx`)
   em um banco de teste. Não importe o modelo em um banco que já tenha dados reais.
   O script mostra um relatório de conferência (séries repetidas, aparelhos sem série, status em branco).

5. (Opcional) Troque `NOME_ESCOLA` em app.py e coloque o logo da escola em static/logo.jpeg.

6. Inicie o servidor:
   python app.py

7. Acesse no navegador:
   http://localhost:5000

## Formato da planilha
O importador lê um arquivo .xlsx com **uma aba por carrinho (ou local)**. Veja o exemplo em `modelo_planilha.xlsx`:

- **Nome da aba:** `Tipo - Carrinho`. Exemplos: "N - Carrinho 1" (notebook, carrinho "Carrinho 1") e
  "Tablet - Acessa" (tablet, carrinho "Acessa"). Se o nome da aba ou o título na célula A1 contiver "Tablet",
  os aparelhos são tablets; caso contrário, são notebooks. Sem o " - " no nome, a aba inteira vira o carrinho.
- **Cabeçalho:** uma linha (dentro das 14 primeiras da aba) com as colunas **Nº, SÉRIE, EQUIPAMENTO, STATUS e OBSERVAÇÃO**.
  Linhas de título acima do cabeçalho são ignoradas. SÉRIE e EQUIPAMENTO são obrigatórias; as demais são opcionais.
- **Nº:** número do aparelho na plataforma. Pode ser um número ou uma fórmula; se não for número,
  o script numera em sequência (1, 2, 3...) dentro da aba.
- **SÉRIE:** código de identificação do aparelho. Pode ficar vazia ou com "-".
- **EQUIPAMENTO:** marca ou modelo.
- **STATUS:** completo, funcional, em análise, reparo, não funcional ou desaparecido (maiúsculas e acentos não importam).
  Se estiver em branco, o aparelho entra como **COMPLETO** (`STATUS_PADRAO` em importar_equipamentos.py).
  Qualquer outro valor interrompe a importação e o script informa a aba e a linha para corrigir.
- **OBSERVAÇÃO:** texto livre (teclas faltando, tela trincada, qualquer dano).

## Recarregar a planilha
Se já houver dados no banco, o importador **não apaga nada** sem o parâmetro `--substituir`
(que também cria a tabela `equipamentos_backup` antes de recarregar). Cuidado: recarregar descarta as
alterações feitas pelo sistema web depois da primeira carga.
