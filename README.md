# 🛒 PC-Store: Sistema E-commerce com Django

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)

Um sistema completo de e-commerce construído com Python e Django, focado em uma loja de componentes de computador. O projeto inclui funcionalidades essenciais como catálogo de produtos, carrinho de compras, finalização de pedido e um painel administrativo robusto para gerenciamento.

---

## ✨ Principais Funcionalidades

* **Autenticação de Usuários:** Sistema completo de registro e login para clientes.
* **Gerenciamento de Contas:** Página "Minha Conta" onde os clientes podem visualizar e atualizar seus dados.
* **Catálogo de Produtos:**
    * Listagem de produtos com filtros por nome e categoria.
    * Página de detalhes para cada produto.
* **Carrinho de Compras:**
    * Adicione e remova itens do carrinho.
    * O carrinho é salvo na sessão para usuários não logados e vinculado à conta após o login.
* **Fluxo de Pedido:**
    * Página de checkout para finalizar a compra.
    * Simulação de pagamento via boleto bancário.
    * Envio de e-mail de confirmação do pedido.
    * Histórico de pedidos para o cliente.
* **Painel de Administração:**
    * Área administrativa completa para gerenciar produtos, categorias, clientes e pedidos.
    * Visão geral de todos os pedidos do site para o administrador.
    * Capacidade de cancelar pedidos diretamente pelo painel de pedidos do site.

---

## 💻 Tecnologias Utilizadas

* **Backend:** Python 3, Django 5
* **Banco de Dados:** SQLite 3 (para desenvolvimento)
* **Frontend:** Bootstrap 5, HTML, CSS
* **Armazenamento de Mídia:** Cloudinary (para salvar as imagens dos produtos na nuvem)
* **Servidor de Produção (Exemplo):** Gunicorn

---

## 🚀 Como Executar o Projeto Localmente

Siga os passos abaixo para configurar e rodar o projeto no seu ambiente de desenvolvimento.

### **Pré-requisitos**

* Python 3.8 ou superior
* Pip (gerenciador de pacotes do Python)

### **1. Clone e Prepare o Ambiente**

```bash
# Repositório 
git clone [https://github.com/KaweAugusto/loja-pcstoryyy.git](https://loja-pcstoryyy.onrender.com/t)
cd projeto-ecommerc

# Crie e ative um ambiente virtual
python -m venv venv
# Ativar
venv\Scripts\activate

```

### **2. Instale as Dependências**

```bash
pip install -r requirements.txt
```

### **3. Configure as Variáveis de Ambiente**

```dotenv
# .env
SECRET_KEY=chave-secreta
DEBUG=True
ALLOWED_HOSTS=127.0.0.1 localhost

### **4. Prepare o Banco de Dados**

Este projeto foi configurado para recomeçar do zero de forma limpa.

```bash
# Crie os arquivos de migração para todos os apps
python manage.py makemigrations clientes produto pedidos carrinho

# Aplique as migrações para criar as tabelas no banco de dados
python manage.py migrate
```

### **5. Popule o Banco com Dados Iniciais**

Use o comando customizado para criar o superusuário e adicionar produtos e categorias de exemplo.

```bash
python manage.py seed_db
```

### **6. Inicie o Servidor**

```bash
python manage.py runserver
```

Acesse [http://127.0.0.1:8000/](http://127.0.0.1:8000/) no seu navegador!

---

## 🔑 Credenciais do Superusuário

Após rodar o comando `seed_db`, você pode acessar o painel de administração em `/admin` com as seguintes credenciais:

* **Usuário:** `admin`
* **Senha:** `admin123`

---

## ☁️ Deploy

Este projeto está pronto para deploy. Publicar no [Render](https://loja-pcstoryyy.onrender.com/):
