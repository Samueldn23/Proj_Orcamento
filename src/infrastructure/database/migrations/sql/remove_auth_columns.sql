-- Script para remover colunas de autenticação da tabela usuarios
-- Estas colunas não são mais necessárias pois o Supabase Auth gerencia a autenticação

-- Remover as colunas email e password_hash da tabela usuarios
ALTER TABLE usuarios DROP COLUMN IF EXISTS email;
ALTER TABLE usuarios DROP COLUMN IF EXISTS password_hash;

-- Nota: Este script deve ser executado após verificar que o código da aplicação
-- não depende mais destas colunas 