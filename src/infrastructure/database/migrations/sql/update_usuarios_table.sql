-- Adiciona as colunas de email e senha para autenticação
ALTER TABLE usuarios ADD COLUMN IF NOT EXISTS email VARCHAR(255) UNIQUE;
ALTER TABLE usuarios ADD COLUMN IF NOT EXISTS password_hash VARCHAR(255);

-- Atualiza as colunas para NOT NULL após certificar-se que foram adicionadas
ALTER TABLE usuarios ALTER COLUMN email SET NOT NULL;
ALTER TABLE usuarios ALTER COLUMN password_hash SET NOT NULL;

-- Adiciona trigger para atualizar o timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Recria trigger se não existir
DROP TRIGGER IF EXISTS update_usuarios_updated_at ON usuarios;
CREATE TRIGGER update_usuarios_updated_at
BEFORE UPDATE ON usuarios
FOR EACH ROW
EXECUTE PROCEDURE update_updated_at_column(); 