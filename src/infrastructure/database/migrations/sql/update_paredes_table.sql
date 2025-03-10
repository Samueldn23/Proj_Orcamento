DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM information_schema.columns
        WHERE table_name = 'paredes'
        AND column_name = 'custo_tijolos'
    ) THEN
        ALTER TABLE paredes ADD COLUMN custo_tijolos NUMERIC(10,2);
    END IF;

    IF NOT EXISTS (
        SELECT 1
        FROM information_schema.columns
        WHERE table_name = 'paredes'
        AND column_name = 'custo_mao_obra'
    ) THEN
        ALTER TABLE paredes ADD COLUMN custo_mao_obra NUMERIC(10,2);
    END IF;
END $$;