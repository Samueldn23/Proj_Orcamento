DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM information_schema.columns
        WHERE table_name = 'usuarios'
        AND column_name = 'data_nascimento'
    ) THEN
        ALTER TABLE usuarios ADD COLUMN data_nascimento DATE;
    END IF;
END $$;