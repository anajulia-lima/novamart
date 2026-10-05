# NovaMart

Projeto de marketplace fictício para explorar um fluxo de dados de ponta a ponta: aplicação web em Flask, banco PostgreSQL com dados sintéticos e modelos analíticos dbt.

## Funcionalidades

- Cadastro, consulta e edição de clientes, vendedores, produtos e pedidos.
- Página inicial com indicadores do marketplace e pedidos recentes.
- Relatórios mensais exportados em PDF.
- Página preparada para incorporar um dashboard do Metabase.
- Geração de dados sintéticos com casos intencionais de qualidade de dados para análise.
- Transformações dbt em camadas de staging, intermediate e marts, incluindo uma fato de itens de pedido e análise de Pareto de produtos.
- Pipeline opcional para ingestão, execução dos modelos e testes dbt, geração da documentação e alertas no Discord.

## Tecnologias

- Python, Flask, Jinja2 e ReportLab
- PostgreSQL e psycopg2
- dbt Core com adaptador PostgreSQL (`dbt-postgres`)
- Metabase (incorporação do dashboard configurada à parte)

## Pré-requisitos

- Python e `pip`
- PostgreSQL
- Para executar as transformações: dbt Core e o adaptador `dbt-postgres`
- Para usar alertas do pipeline: URL de webhook do Discord (opcional)

## Configuração local

1. Clone o repositório e entre na pasta do projeto:

   ```bash
   git clone https://github.com/anajulia-lima/novamart.git
   cd novamart
   ```

2. Crie e ative um ambiente virtual e instale as dependências da aplicação:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

   No Windows, ative o ambiente com `venv\Scripts\activate`.

3. Crie um banco PostgreSQL vazio chamado `nova_market` (ou escolha outro nome) e configure a conexão em um arquivo `.env` na raiz:

   ```dotenv
   DATABASE_URL=postgresql://postgres:SUA_SENHA@localhost:5432/nova_market
   ```

   Como alternativa, configure `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER` e `DB_PASS`. O arquivo `.env` não deve ser enviado ao Git.

4. Crie as tabelas e gere a carga inicial de dados sintéticos:

   ```bash
   python scripts/create_tables.py
   python scripts/generate_seed_data.py
   ```

   A carga cria um conjunto fictício de clientes, vendedores, produtos, pedidos, pagamentos e avaliações, incluindo inconsistências planejadas para os exercícios de qualidade de dados.

5. Inicie a aplicação:

   ```bash
   python app/app.py
   ```

   Acesse [http://localhost:5000](http://localhost:5000). A aplicação espera encontrar as tabelas no schema `app`. A página de dashboard também depende de uma URL de incorporação válida do Metabase.

## Dados e análises

O projeto inclui materiais de exploração e regras de negócio:

- `Modulo3_EDA_Script.sql` e `Modulo3_DUVIDAS_EDA.md`: consultas e anotações de exploração dos dados.
- `Business Rules.md` e `scripts/BUSINESS_RULES.md`: decisões de negócio e tratamento de casos de qualidade.
- `scripts/inject_bad_data.py`: ferramenta para injetar casos de dados inválidos durante os exercícios.
- `scripts/continuous_ingestion.py`: simulador de ingestão de novos pedidos.

Para executar a ingestão uma vez, com cinco pedidos (padrão):

```bash
python scripts/continuous_ingestion.py
```

É possível definir o volume ou repetir a ingestão em intervalos:

```bash
python scripts/continuous_ingestion.py --orders 10
python scripts/continuous_ingestion.py --loop 60
```

## dbt e pipeline

Instale as dependências adicionais usadas pelo fluxo analítico:

```bash
pip install dbt-postgres requests
```

Configure o perfil dbt `novamart_analytics` em `~/.dbt/profiles.yml` para apontar ao mesmo banco PostgreSQL. O projeto dbt está em `novamart_analytics/`, lê as tabelas do schema `app` e organiza os modelos em `stg`, `int` e `marts`.

Com o perfil configurado, execute os modelos e testes:

```bash
cd novamart_analytics
dbt build
dbt docs generate
```

O orquestrador `scripts/run_pipeline.py` coordena a ingestão, constrói as camadas dbt em sequência e gera a documentação ao final. Para alertas, acrescente `DISCORD_WEBHOOK_URL` ao `.env`. A execução desse orquestrador usa caminhos absolutos definidos no próprio script; ajuste-os para o ambiente antes de usá-lo:

```bash
python scripts/run_pipeline.py
python scripts/run_pipeline.py --full-refresh
```

## Estrutura do projeto

```text
app/                    Aplicação Flask, acesso ao banco e templates
novamart_analytics/      Projeto dbt, fontes, modelos e seed de categorias
scripts/                Criação do schema, dados sintéticos e pipeline
Modulo3_EDA_Script.sql   Consultas de exploração dos dados
requirements.txt        Dependências Python da aplicação e dos scripts
```

## Observações

- Os dados são sintéticos e destinados a demonstração, estudo e exploração analítica.
- `requirements.txt` lista as dependências Python da aplicação e dos scripts; dbt e `requests` são instalados à parte para o pipeline.
- A chave secreta Flask e o endereço de incorporação do Metabase precisam ser configurados adequadamente antes de qualquer uso público ou em produção.
