-- Criação da tabela de lajes
CREATE TABLE IF NOT EXISTS lajes (
    id BIGSERIAL PRIMARY KEY,
    projeto_id BIGINT REFERENCES projetos(id) ON DELETE CASCADE,
    comprimento NUMERIC(10, 2) NOT NULL,
    largura NUMERIC(10, 2) NOT NULL,
    espessura NUMERIC(10, 2) NOT NULL,
    valor_m3 NUMERIC(10, 2) NOT NULL,
    custo_total NUMERIC(10, 2) NOT NULL,
    tipo_laje VARCHAR(50),
    volume NUMERIC(10, 2),
    criado_em TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Adicionar coluna tipo_laje se não existir
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM information_schema.columns
        WHERE table_name = 'lajes'
        AND column_name = 'tipo_laje'
    ) THEN
        ALTER TABLE lajes ADD COLUMN tipo_laje VARCHAR(50);
    END IF;
END $$;

-- Adicionar coluna volume se não existir
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM information_schema.columns
        WHERE table_name = 'lajes'
        AND column_name = 'volume'
    ) THEN
        ALTER TABLE lajes ADD COLUMN volume NUMERIC(10, 2);
    END IF;
END $$; 