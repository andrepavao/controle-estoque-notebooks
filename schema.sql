-- ============================================================
--  Controle de Estoque de Notebooks e Tablets - Escola Publica
--  Schema SQL - PostgreSQL
--  Versao 1.0 | Setembro 2026
-- ============================================================
--  Como usar:
--  1. Crie o banco de dados:
--       CREATE DATABASE estoque_notebooks;
--  2. Conecte ao banco 'estoque_notebooks' no pgAdmin
--  3. Abra este arquivo no Query Tool (File > Open)
--  4. Execute com F5
--  5. Carregue a planilha com:  python importar_equipamentos.py
-- ============================================================

-- Remove a tabela se ja existir (para recriar do zero)
DROP TABLE IF EXISTS equipamentos;

-- Criacao da tabela principal
CREATE TABLE equipamentos (
    id             SERIAL PRIMARY KEY,
    tipo           VARCHAR(10)  NOT NULL CHECK (tipo IN ('NOTEBOOK','TABLET')),
    carrinho       VARCHAR(40)  NOT NULL,          -- local: aba da planilha (Carrinho 1, Carrinho 2, Acessa...)
    numero         INTEGER      NOT NULL,          -- coluna N: numero do aparelho na plataforma
    serie          VARCHAR(30),                    -- coluna SERIE (pode ficar vazia)
    equipamento    VARCHAR(60)  NOT NULL,          -- coluna EQUIPAMENTO: marca ou modelo
    status         VARCHAR(15)  NOT NULL DEFAULT 'COMPLETO'
                   CHECK (status IN ('COMPLETO','FUNCIONAL','EM_ANALISE',
                                     'REPARO','NAO_FUNCIONAL','DESAPARECIDO')),
    observacao     TEXT,                           -- teclas faltando, tela trincada, etc.
    atualizado_em  TIMESTAMP    NOT NULL DEFAULT NOW(),
    UNIQUE (tipo, carrinho, numero)
);

CREATE INDEX idx_equipamentos_serie  ON equipamentos (serie);
CREATE INDEX idx_equipamentos_status ON equipamentos (status);

-- ============================================================
--  Verificacao: deve retornar 0 (a carga vem do importador)
-- ============================================================
SELECT COUNT(*) AS total_equipamentos FROM equipamentos;
