# 💰 BitApp — Sistema de Gestão Financeira Pessoal

> Plataforma web completa para controle de finanças pessoais com suporte à análise de carteira Bitcoin via leitura de dados da plataforma BIPA.

---

## 📋 Sobre o Projeto

O **BitApp** é um sistema web de gestão financeira pessoal desenvolvido com Django. Ele permite que o usuário registre seus ganhos e despesas mensais, visualize seu desempenho financeiro através de dashboards interativos e analise sua carteira de Bitcoin com base em arquivos exportados da plataforma BIPA, consultando cotações em tempo real.

---

## ✨ Funcionalidades

### 🔐 Autenticação
- Registro de novos usuários
- Login / Logout
- Autenticação via JWT (para consumo da API REST)
- Proteção de rotas — acesso às funcionalidades apenas para usuários autenticados e permitidos

### 💵 Gestão de Ganhos
- Cadastro de receitas mensais
- Categorização de ganhos
- Histórico e edição de registros

### 💸 Gestão de Despesas
- Cadastro de despesas mensais
- Categorização de gastos
- Histórico e edição de registros

### 📊 Dashboard Financeiro
- Gráficos de receitas vs. despesas por período
- Saldo mensal e acumulado
- Distribuição de gastos por categoria
- Evolução patrimonial ao longo do tempo

### ₿ Análise de Carteira Bitcoin (BIPA)
- Upload e leitura de arquivo `.csv` exportado pela plataforma [BIPA](https://bipa.app)
- Cálculo do total investido em Bitcoin (BRL)
- Cálculo do valor atual da carteira com base na cotação do dia
- Apuração de lucro ou prejuízo realizado e não realizado
- Exibição da cotação do Bitcoin em **USD** e **BRL** em tempo real via API externa

---

## 🛠️ Stack Tecnológica

### Backend
| Tecnologia | Descrição |
|---|---|
| **Python 3.12+** | Linguagem principal |
| **Django 6.x** | Framework web principal |
| **Django REST Framework** | Construção da API REST |
| **djangorestframework-simplejwt** | Autenticação JWT para a API |
| **Pandas** | Processamento e análise do CSV da BIPA |
| **Requests / httpx** | Consumo de APIs externas de cotação |

### Frontend
| Tecnologia | Descrição |
|---|---|
| **Django Templates** | Renderização server-side das páginas |
| **Plotly** | Gráficos interativos no dashboard |
| **Bootstrap 5** | Estilização e responsividade |

### Banco de Dados
| Tecnologia | Descrição |
|---|---|
| **SQLite** | Desenvolvimento local |
| **PostgreSQL** | Ambiente de produção |

### APIs Externas
| API | Finalidade |
|---|---|
| **A Definir** | Cotação diária do Bitcoin em USD e BRL |

---

## 🏗️ Arquitetura do Projeto

```
BitApp/
│
├── app/                      # Configurações do projeto Django (settings, urls, wsgi)
│
├── authentication/           # Registro, login, perfil e JWT
├── inflows/                  # Módulo de ganhos mensais
├── outflows/                 # Módulo de despesas mensais
├── dashboard/                # Dashboard com gráficos consolidados
├── bitcoin/                  # Análise da carteira BIPA + cotação BTC
│
├── templates/                # Django Templates (HTML)
├── static/                   # Arquivos estáticos (CSS, JS, imagens)
├── media/                    # Uploads de usuários (CSVs da BIPA)
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── requirements_dev.txt
├── db.sqlite3
└── manage.py
```

---

## 🚀 Como Rodar o Projeto Localmente

### Pré-requisitos
- Python 3.12+
- Django
- pip
- virtualenv ou venv

### Passo a passo

```bash
# 1. Clone o repositório
git clone https://github.com/Luisf66/bit-app.git
cd BIT-APP

# 2. Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure as variáveis de ambiente
cp .env.example .env
# Edite o arquivo .env com suas configurações

# 5. Execute as migrations
python manage.py migrate

# 6. Crie um superusuário (opcional)
python manage.py createsuperuser

# 7. Inicie o servidor de desenvolvimento
python manage.py runserver
```

Acesse em: `http://127.0.0.1:8000`

---

## 🔑 Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com base no `.env.example`:

```env
SECRET_KEY=sua-secret-key-django
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

# Banco de dados (produção)
DATABASE_URL=postgres://user:password@localhost:5432/bit-app

# API de cotação Bitcoin
A Definir
```

---

## 📡 API REST

A aplicação expõe uma API REST com autenticação via JWT.

### Autenticação

```http
POST /api/v1/auth/token/
Content-Type: application/json

{
  "username": "usuario",
  "password": "senha"
}
```

Resposta:
```json
{
  "access": "<jwt_access_token>",
  "refresh": "<jwt_refresh_token>"
}
```

### Principais Endpoints

| Método | Endpoint | Descrição |
|---|---|---|
| `POST` | `/api/v1/auth/register/` | Registro de novo usuário |
| `POST` | `/api/v1/auth/token/` | Obter token JWT |
| `POST` | `/api/v1/auth/token/refresh/` | Renovar token JWT |
| `GET/POST` | `/api/v1/income/` | Listar / criar ganhos |
| `GET/PUT/DELETE` | `/api/v1/income/{id}/` | Detalhar / editar / excluir ganho |
| `GET/POST` | `/api/v1/expenses/` | Listar / criar despesas |
| `GET/PUT/DELETE` | `/api/v1/expenses/{id}/` | Detalhar / editar / excluir despesa |
| `POST` | `/api/v1/bitcoin/upload/` | Upload do CSV da BIPA |
| `GET` | `/api/v1/bitcoin/summary/` | Resumo da carteira Bitcoin |
| `GET` | `/api/v1/bitcoin/price/` | Cotação atual do Bitcoin |

> Todos os endpoints (exceto autenticação) requerem o header:
> `Authorization: Bearer <access_token>`

---

## 📈 Módulo Bitcoin — Como Usar

1. Acesse seu app [BIPA](https://bipa.app) e exporte para seu e-mail o histórico de transações em formato `.csv`
2. No BitApp, acesse o menu **Bitcoin → Importar Transações**
3. Faça o upload do arquivo `.csv`
4. O sistema irá processar o arquivo e exibir:
   - Total investido (BRL)
   - Quantidade de BTC acumulada
   - Valor atual da carteira (BRL e USD)
   - Lucro / Prejuízo em valor absoluto e percentual

---

## 🗺️ Roadmap

- [x] Planejamento e arquitetura inicial
- [ ] Módulo de ganhos mensais
- [ ] Módulo de despesas mensais
- [ ] Dashboard com Plotly
- [ ] Módulo de análise Bitcoin (BIPA CSV)
- [ ] Integração com API de cotação Bitcoin
- [ ] Módulo de autenticação (registro, login, JWT)
- [ ] Documentação da API com Swagger/OpenAPI
- [ ] Deploy em produção (Railway / Render / VPS)

---