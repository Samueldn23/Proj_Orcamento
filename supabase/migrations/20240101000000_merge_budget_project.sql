-- 1. Adicionar coluna valor_total na tabela projetos
ALTER TABLE projetos
ADD COLUMN valor_total DECIMAL(10,2);

-- 2. Copiar dados dos orçamentos para projetos
UPDATE projetos p
SET valor_total = o.valor_total
FROM orcamentos o
WHERE p.cliente_id = o.cliente_id;

-- 3. Atualizar as referências nas tabelas relacionadas
ALTER TABLE fundacoes RENAME COLUMN orcamento_id TO projeto_id;
ALTER TABLE contrapisos RENAME COLUMN orcamento_id TO projeto_id;
ALTER TABLE lajes RENAME COLUMN orcamento_id TO projeto_id;
ALTER TABLE telhados RENAME COLUMN orcamento_id TO projeto_id;
ALTER TABLE eletricas RENAME COLUMN orcamento_id TO projeto_id;
ALTER TABLE paredes RENAME COLUMN orcamento_id TO projeto_id;

-- 4. Remover a tabela de orçamentos
DROP TABLE orcamentos;
