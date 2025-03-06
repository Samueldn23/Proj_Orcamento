-- Atualizar restrições de chave estrangeira para todas as tabelas relacionadas ao projeto

-- Paredes
ALTER TABLE paredes DROP CONSTRAINT IF EXISTS paredes_projeto_id_fkey;
ALTER TABLE paredes ADD CONSTRAINT paredes_projeto_id_fkey
FOREIGN KEY (projeto_id) REFERENCES projetos(id) ON DELETE CASCADE;

-- Fundações
ALTER TABLE fundacoes DROP CONSTRAINT IF EXISTS fundacoes_projeto_id_fkey;
ALTER TABLE fundacoes ADD CONSTRAINT fundacoes_projeto_id_fkey
FOREIGN KEY (projeto_id) REFERENCES projetos(id) ON DELETE CASCADE;

-- Contrapisos
ALTER TABLE contrapisos DROP CONSTRAINT IF EXISTS contrapisos_projeto_id_fkey;
ALTER TABLE contrapisos ADD CONSTRAINT contrapisos_projeto_id_fkey
FOREIGN KEY (projeto_id) REFERENCES projetos(id) ON DELETE CASCADE;

-- Lajes
ALTER TABLE lajes DROP CONSTRAINT IF EXISTS lajes_projeto_id_fkey;
ALTER TABLE lajes ADD CONSTRAINT lajes_projeto_id_fkey
FOREIGN KEY (projeto_id) REFERENCES projetos(id) ON DELETE CASCADE;

-- Telhados
ALTER TABLE telhados DROP CONSTRAINT IF EXISTS telhados_projeto_id_fkey;
ALTER TABLE telhados ADD CONSTRAINT telhados_projeto_id_fkey
FOREIGN KEY (projeto_id) REFERENCES projetos(id) ON DELETE CASCADE;

-- Elétricas
ALTER TABLE eletricas DROP CONSTRAINT IF EXISTS eletricas_projeto_id_fkey;
ALTER TABLE eletricas ADD CONSTRAINT eletricas_projeto_id_fkey
FOREIGN KEY (projeto_id) REFERENCES projetos(id) ON DELETE CASCADE; 