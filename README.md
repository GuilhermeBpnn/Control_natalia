# StoreControl V1

Sistema web simples para controle de produtos, estoque, vendas e financeiro.

## O que esta versão faz

- Cadastro, edição e exclusão de produtos
- Controle de estoque com histórico de movimentações
- Registro de vendas com baixa automática do estoque
- Registro de entradas e saídas financeiras
- Dashboard com visão rápida da operação

## Como rodar

### 1. Crie e ative um ambiente virtual

#### Windows PowerShell
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

#### Windows CMD
```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

### 2. Instale as dependências
```bash
pip install -r requirements.txt
```

### 3. Rode o projeto
```bash
python run.py
```

Depois abra no navegador:

`http://127.0.0.1:8000`

## Observações

- O banco SQLite é criado automaticamente em `data/store.db`.
- Quando uma venda é registrada, o sistema também cria uma entrada financeira automática.
- Quando uma entrada de estoque é marcada com gasto, o sistema também registra uma saída financeira.
