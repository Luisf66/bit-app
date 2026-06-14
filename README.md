# 💰 BitApp — Sistema de Gestão Financeira Pessoal

> Plataforma web completa para controle de finanças pessoais, com análise de carteira Bitcoin via leitura de dados da plataforma BIPA, consulta de carteiras na blockchain e análise inteligente dos dados financeiros via IA.

---

## 📋 Sobre o Projeto

O **BitApp** é um sistema web de gestão financeira pessoal desenvolvido com **Django** e **Django REST Framework**. Ele permite que o usuário registre seus ganhos e despesas mensais, visualize seu desempenho financeiro através de dashboards interativos e analise sua carteira de Bitcoin com base em arquivos exportados da plataforma BIPA, consultando cotações e saldos em tempo real diretamente na blockchain.

Além disso, o BitApp conta com um módulo de **análise inteligente via IA (Groq)**, que avalia os dados financeiros do usuário e gera insights, tendências e recomendações em linguagem natural.

A aplicação é totalmente containerizada com **Docker**, possui suíte de **testes unitários** com cobertura mínima garantida e um pipeline de **Integração Contínua (CI)** que valida cada alteração antes do merge.

---

## ✨ Funcionalidades

### 🔐 Autenticação
- Registro de novos usuários
- Login / Logout
- Edição de perfil (incluindo chave de API pessoal da Groq)
- Autenticação via JWT (para consumo da API REST)
- Proteção de rotas — acesso às funcionalidades apenas para usuários autenticados
- Isolamento total de dados entre usuários (multi-tenant)

### 💵 Gestão de Ganhos
- Cadastro de receitas mensais
- Categorização de ganhos
- Histórico e edição de registros

### 💸 Gestão de Despesas
- Cadastro de despesas mensais
- Categorização de gastos
- Histórico e edição de registros

### 📊 Dashboard Financeiro
- Compras de Bitcoin realizadas na BIPA
- Ganho acumulado ao longo do tempo
- Ganho mensal
- Gasto mensal
- Gráfico de donut com a relação entre compras e compras recorrentes de BTC
- Gráfico de donut com as movimentações de entrada e saída de BTC

### ₿ Análise de Carteira Bitcoin (BIPA)
- Upload e leitura de arquivo `.csv` exportado pela plataforma [BIPA](https://bipa.app)
- Cálculo do total investido em Bitcoin (BRL)
- Cálculo do valor atual da carteira com base na cotação do dia
- Apuração de lucro ou prejuízo (valor absoluto)
- Exibição da cotação do Bitcoin em **BRL** em tempo real via API externa

### 🔗 Integração com Blockchain
- Consulta de carteiras BTC diretamente na blockchain (saldo e total de transações)
- Cálculo automático do valor da carteira em reais com base na cotação atual

### 🤖 Análise de Dados com IA
- Geração de análise financeira sob demanda, a partir dos dados de entradas, saídas e transações de Bitcoin do usuário
- Cache da análise por período configurável, evitando consumo excessivo de tokens
- Uso da chave de API pessoal da Groq cadastrada no perfil do usuário

---

## 🛠️ Stack Tecnológica

### Backend
| Tecnologia | Descrição |
|---|---|
| **Python 3.12+** | Linguagem principal |
| **Django 6.x** | Framework web principal |
| **Django REST Framework** | Construção da API REST |
| **djangorestframework-simplejwt** | Autenticação JWT para a API |
| **drf-spectacular** | Documentação automática da API (Swagger/OpenAPI) |
| **Pandas** | Processamento e análise do CSV da BIPA |
| **Requests** | Consumo de APIs externas (blockchain e IA) |

### Frontend
| Tecnologia | Descrição |
|---|---|
| **Django Templates** | Renderização server-side das páginas |
| **Plotly** | Gráficos interativos no dashboard |
| **Tailwind CSS** | Estilização e responsividade |

### Banco de Dados
| Tecnologia | Descrição |
|---|---|
| **SQLite** | Desenvolvimento local (opcional) |
| **PostgreSQL** | Desenvolvimento via Docker e ambiente de produção |

### APIs Externas
| API | Finalidade |
|---|---|
| [**blockchain.info**](https://blockchain.info) | Cotação do Bitcoin (BRL) e consulta de saldo/transações de carteiras |
| [**Groq API**](https://api.groq.com/openai/v1/chat/completions) | Geração da análise financeira via IA |

---

## 🏗️ Arquitetura do Projeto

```
bit-app/
│
├── app/                      # Configurações do projeto (settings, urls, wsgi)
│
├── usuarios/                 # Autenticação, perfil e modelo de usuário customizado
├── entradas/                 # Gestão de ganhos (entradas financeiras)
├── saidas/                    # Gestão de despesas (saídas financeiras)
├── bitcoin/                    # Dashboard, upload BIPA, integração com blockchain.info
├── ai/                          # Integração com a API da Groq para análise financeira
│
├── staticfiles/               # Arquivos estáticos coletados (collectstatic)
├── pytest.ini                  # Configuração dos testes
├── coverage.xml                # Relatório de cobertura de testes
│
├── Dockerfile                   # Imagem de produção
├── Dockerfile.dev                # Imagem de desenvolvimento (hot reload)
├── docker-compose.yml
├── entrypoint.sh
│
├── requirements.txt
├── manage.py
└── README.md
```

Cada app de domínio (`entradas`, `saidas`, `bitcoin`, `usuarios`) segue o mesmo padrão interno, separando claramente as views e rotas tradicionais (Django) das views e rotas da API (DRF). Exemplo com o app `entradas`:

```
entradas/
├── migrations/
├── forms/
├── serializer/              # Serializers do DRF
├── templates/
├── test/                     # Testes unitários (pytest)
├── urls/
│   ├── __init__.py           # Reexporta as rotas das páginas (web)
│   ├── web_url.py             # Rotas das páginas (Django views)
│   └── api_url.py              # Rotas da API (DRF router)
├── views/
│   ├── views.py                # Views tradicionais (Django)
│   └── api_views.py             # ViewSets do DRF
├── models.py
├── admin.py
└── apps.py
```

---

## 🚀 Como Rodar o Projeto Localmente

### Opção recomendada — Docker

#### Pré-requisitos
- Docker
- Docker Compose

#### Passo a passo

```bash
# 1. Clone o repositório
git clone https://github.com/Luisf66/bit-app.git
cd bit-app

# 2. Configure as variáveis de ambiente
cp .env.example .env
# Edite o arquivo .env com suas configurações

# 3. Suba os containers
docker compose up --build
```

O `entrypoint.sh` aplica as migrations automaticamente na inicialização. Acesse em: `http://localhost:8000`

Para criar um superusuário:
```bash
docker compose exec bit-app python manage.py createsuperuser
```

---

### Opção alternativa — Ambiente virtual (venv)

#### Pré-requisitos
- Python 3.12+
- pip
- virtualenv ou venv
- PostgreSQL (ou SQLite, configurando `DATABASE_LOCAL=True`)

#### Passo a passo

```bash
# 1. Clone o repositório
git clone https://github.com/Luisf66/bit-app.git
cd bit-app

# 2. Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure as variáveis de ambiente
cp .env.example .env

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
# Django
SECRET_KEY=sua-secret-key-django
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

# Banco de dados local
# True  -> usa SQLite
# False -> usa PostgreSQL (variáveis abaixo)
DATABASE_LOCAL=False

POSTGRES_DB=bit-app
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=bit-app_db
POSTGRES_PORT=5432

# IA — Groq
AI_BASE_URL=https://api.groq.com/openai/v1/chat/completions
AI_MODEL=nome-do-modelo
```

> Em produção, a variável `DATABASE_URL` (fornecida automaticamente pelo provedor de hospedagem) tem prioridade sobre as variáveis `POSTGRES_*` e `DATABASE_LOCAL`.

> A chave de API da Groq (`AI_API_KEY`) não é definida no `.env` — cada usuário cadastra a sua própria chave em **Perfil**, gerada em [console.groq.com/keys](https://console.groq.com/keys).

---

## 🧪 Testes

O projeto possui suíte de testes unitários com **pytest**, **pytest-django** e **factory-boy**, cobrindo models, services e views (incluindo isolamento de dados entre usuários).

```bash
# rodar todos os testes
docker compose exec bit-app pytest

# rodar com relatório de cobertura
docker compose exec bit-app pytest --cov=. --cov-report=xml --cov-fail-under=80
```

A cobertura mínima exigida é de **80%**.

---

## ⚙️ CI/CD

O projeto utiliza **GitHub Actions** para validar automaticamente cada `push` e `pull request`:

- Sobe um serviço de PostgreSQL para os testes
- Instala as dependências
- Executa as migrations
- Roda a suíte de testes com verificação de cobertura mínima

O deploy em produção é feito de forma contínua a partir da branch principal.

---

## 📡 API REST

A aplicação expõe uma API REST com autenticação via JWT e documentação interativa via Swagger/Redoc.

### Autenticação

```http
POST /api/v1/token/
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

> Todos os demais endpoints requerem o header:
> `Authorization: Bearer <access_token>`

### Principais Endpoints

| Método | Endpoint | Descrição |
|---|---|---|
| `POST` | `/api/v1/token/` | Obter par de tokens JWT (access/refresh) |
| `POST` | `/api/v1/token/refresh/` | Renovar o token de acesso |
| `POST` | `/api/v1/token/verify/` | Verificar a validade de um token |
| `GET/POST` | `/api/v1/entradas/` | Listar / criar entradas financeiras |
| `GET/PUT/PATCH/DELETE` | `/api/v1/entradas/{id}/` | Detalhar / editar / excluir entrada |
| `GET/POST` | `/api/v1/categorias-entradas/` | Listar / criar categorias de entrada |
| `GET/PUT/PATCH/DELETE` | `/api/v1/categorias-entradas/{id}/` | Detalhar / editar / excluir categoria |
| `GET/POST` | `/api/v1/saidas/` | Listar / criar saídas financeiras |
| `GET/PUT/PATCH/DELETE` | `/api/v1/saidas/{id}/` | Detalhar / editar / excluir saída |
| `GET/POST` | `/api/v1/categorias-saidas/` | Listar / criar categorias de saída |
| `GET/PUT/PATCH/DELETE` | `/api/v1/categorias-saidas/{id}/` | Detalhar / editar / excluir categoria |
| `GET` | `/api/v1/transacoes/` | Listar transações de Bitcoin (somente leitura) |
| `GET` | `/api/v1/transacoes/{id}/` | Detalhar transação de Bitcoin |
| `GET` | `/api/v1/schema/` | Schema OpenAPI |
| `GET` | `/api/v1/schema/swagger-ui/` | Documentação interativa (Swagger UI) |
| `GET` | `/api/v1/schema/redoc/` | Documentação interativa (Redoc) |

> Cada app de domínio segue o mesmo padrão de roteamento via `DefaultRouter`, gerando automaticamente as operações de listar, criar, detalhar, atualizar e excluir.

---

## 🖥️ Páginas (Web)

As páginas da aplicação seguem o mesmo padrão de rotas em todos os apps de domínio. Exemplo com o app `entradas`:

```python
urlpatterns = [
    path('category/create/', views.Categorias_EntradasCreateView.as_view(), name='categorias-entradas-create'),
    path('category/list/', views.Categorias_EntradasListView.as_view(), name='categorias-entradas-list'),
    path('category/<int:pk>/update/', views.Categorias_EntradasUpdateView.as_view(), name='categorias-entradas-update'),
    path('category/<int:pk>/delete/', views.Categorias_EntradasDeleteView.as_view(), name='categorias-entradas-delete'),

    path('create/', views.EntradasCreateView.as_view(), name='entradas-create'),
    path('list/', views.EntradasListView.as_view(), name='entradas-list'),
    path('<int:pk>/update/', views.EntradasUpdateView.as_view(), name='entradas-update'),
    path('<int:pk>/delete/', views.EntradasDeleteView.as_view(), name='entradas-delete'),
]
```

O mesmo padrão é replicado em `saidas` (entradas → saídas), além das rotas específicas de `bitcoin` (upload, listagem de transações, dashboard e geração de análise via IA) e `usuarios` (registro, login, logout e perfil).

---

## 📈 Módulo Bitcoin — Como Usar

1. Acesse seu app [BIPA](https://bipa.app) e exporte para seu e-mail o histórico de transações em formato `.csv`
2. No BitApp, acesse o menu **Bitcoin → Upload de Dados**
3. Faça o upload do arquivo `.csv`
4. O sistema irá processar o arquivo e exibir no dashboard:
   - Total investido (BRL)
   - Quantidade de BTC acumulada
   - Compras e compras recorrentes
   - Movimentações de entrada e saída de BTC
   - Valor atual da carteira (BRL)
   - Lucro / Prejuízo (valor absoluto)
5. Opcionalmente, busque uma carteira BTC pelo endereço para consultar saldo e total de transações diretamente na blockchain
6. Gere uma análise dos seus dados financeiros via IA a qualquer momento

---

## 🗺️ Roadmap

- [x] Planejamento e arquitetura inicial
- [x] Módulo de ganhos mensais
- [x] Módulo de despesas mensais
- [x] Dashboard com Plotly
- [x] Módulo de análise Bitcoin (BIPA CSV)
- [x] Integração com blockchain.info (cotação e consulta de carteiras)
- [x] Módulo de autenticação (registro, login, perfil, JWT)
- [x] Isolamento de dados por usuário (multi-tenant)
- [x] Análise de dados financeiros via IA (Groq)
- [x] Migração do frontend para Tailwind CSS
- [x] API REST com Django REST Framework
- [x] Documentação da API com Swagger/OpenAPI (drf-spectacular)
- [x] Testes unitários com cobertura mínima (pytest + factory-boy)
- [x] Containerização com Docker
- [x] Integração Contínua (CI) com GitHub Actions
- [x] Deploy em produção (Render)

### 🔭 Melhorias Futuras
- [ ] Responsividade completa para dispositivos móveis
- [ ] Refatoração de templates repetidos via `{% include %}`
- [ ] Alteração no prompt da IA para melhores resultados
