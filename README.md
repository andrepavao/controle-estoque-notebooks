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

4. Carregue a planilha de inventário:
   python importar_equipamentos.py
   O script mostra um relatório de conferência (séries repetidas, aparelhos sem série, status em branco).

5. (Opcional) Troque `NOME_ESCOLA` em app.py e coloque o logo da escola em static/logo.jpeg.

6. Inicie o servidor:
   python app.py

7. Acesse no navegador:
   http://localhost:5000

## Importante sobre a planilha
- Cada aba vira um **carrinho**: "N - Carrinho 1" (notebook, Carrinho 1), "Tablet - Acessa" (tablet, Acessa) etc.
- Linhas com STATUS em branco entram como **COMPLETO** (`STATUS_PADRAO` em importar_equipamentos.py).
- Se já houver dados no banco, o importador **não apaga nada** sem o parâmetro `--substituir`
  (que também cria a tabela `equipamentos_backup` antes de recarregar).
