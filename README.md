# Sistema de Gerenciamento de Produtos e Vendas (Mini E-commerce)

Projeto Django para gerenciar produtos, clientes e pedidos — com Bootstrap, Cloudinary e pronto para deploy no Render.

## Credenciais iniciais
- Admin: **admin**
- Senha: **admin123**

## Como usar (resumo)
1. Crie e ative um virtualenv.
2. `pip install -r requirements.txt`
3. Crie `.env` a partir de `.env.example`.
4. `python manage.py migrate`
5. `python seed_db.py`
6. `python manage.py runserver`

Acesse `http://127.0.0.1:8000/` e use `/accounts/login/` para entrar com o admin.

## Deploy no Render (resumo)
- Faça push do repo para o GitHub.
- No Render, crie um Web Service apontando para o repo.
- Configure ENV vars: `SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS`, `CLOUDINARY_URL` (opcional).
- Rode migrações e `seed_db.py` no ambiente do Render.
