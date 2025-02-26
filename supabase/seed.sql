
-- Inserir dados iniciais na tabela de clientes
INSERT INTO clientes (nome, email, telefone) VALUES
('Cliente Teste', 'teste@email.com', '11999999999');

-- Inserir dados iniciais na tabela de projetos
INSERT INTO projetos (cliente_id, nome, descricao, status, data_inicio) VALUES
(1, 'Projeto Teste', 'Projeto inicial para teste', 'em_andamento', CURRENT_TIMESTAMP);

-- Inserir configurações padrão do sistema
INSERT INTO configuracoes (chave, valor) VALUES
('versao_sistema', '1.0.0'),
('moeda_padrao', 'BRL'),
('formato_data', 'dd/MM/yyyy');
