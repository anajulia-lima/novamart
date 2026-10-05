# Módulo 3 — Minhas Anotações de EDA
**Mindus Data School · NovaMart · PostgreSQL**

> **Como usar este arquivo:**
> 1. Rode cada bloco do `Modulo3_EDA_Script.sql` no DBeaver
> 2. Preencha as células `→` com o que você observou
> 3. Marque cada pergunta com: **[PERGUNTAR]** (pro stakeholder) | **[BUG]** (problema técnico) | **[OK]** (esperado)
> 4. No final, leve as questões marcadas como [PERGUNTAR] pra reunião com a Marina
>
> **Não deixe nenhuma célula em branco.** Se não sabe, escreva "não sei — perguntar".

---

## NÍVEL 1 — Volumetria

### 1.1 Contagem de registros **[OK]**
| Tabela | Registros observados | Esperado? |
|---|---|---|
| customers |100|S|
| sellers |15|S|
| products |150|S|
| orders |800|S|
| order_items |1823|S|
| payments |800|S|
| reviews |488|S| 

→ **Observação geral:** A quantidade de registros em cada tabela parece coerente. Temos a mesma quantidade de dados de pagamento do que de pedidos, menor quantidade de reviews do que de pedidos (nesse caso deveria ser menor ou igual). 

→ **Alguma tabela surpreendeu? Por quê?** A princípio, a volumetria de dados de nenhuma tabela se destaca.

---

### 1.2 Período dos dados **[OK]**
→ **Primeiro pedido:** 01/07/2024
→ **Último pedido:** 30/12/2025
→ **Período total coberto:** 18 meses
→ **O volume é consistente ao longo dos meses?** Sim, podemos ver isso através da média de pedidos no período (44,4), medida de localização que condiz com os resultados demonstrados ao longo dos meses.

---

### 1.3 Volume mensal **[OK]**
→ **Mês com mais pedidos:** Outubro de 2024, com 55 pedidos
→ **Mês com menos pedidos:** Maio de 2025, com 34 pedidos
→ **Observei alguma sazonalidade?** Os dados não apresentam uma sazonalidade notória.

---

### 1.4 Status e métodos de pagamento disponíveis **[OK]**
→ **Status existentes no banco (lista completa):** Não entendi se eram status da tabela de pagamentos ou orders_statuses, então listo os dois: Tabela Payments: approved, cancelled, pending, refunded. Tabela orders_statuses: Pendente, Pagamento Confirmado, Em Processamento, Enviado, Entregue, Cancelado, Reembolsado, Devolvido.

→ **Qual ID = "entregue"?** 5
→ **Qual ID = "cancelado"?** 6
→ **Métodos de pagamento ativos:** Cartão de Crédito, Cartão de Débito, PIX, Boleto Bancário, Carteira Digital

---

## NÍVEL 2 — Auditoria de NULLs 

### 2.1 NULLs em customers **[PERGUNTAR]**

| Campo | Total NULL | % | Esperado ou Bug? |
|---|---|---|---|
| cpf |5|5%|Não sei - perguntar|
| email |1|1%|Não sei - perguntar|
| telefone |0|0|Sim|
| data_nascimento |0|0|Sim|
| cep |0|0|Sim|

→ **Campos que me preocuparam:** 5% de CPFs não preenchidos. O que ocasionou isso? Bug? 

→ **Pergunta(s) pro stakeholder:** Como proceder com os CPFs e e-mails faltando. 

---

### 2.2 NULLs em products **[PERGUNTAR]**

→ **% de produtos com preco_custo NULL:** 10%
→ **O que acho que significa um preco_custo NULL:** [PERGUNTAR]

→ **Pergunta:** O que diferem estes produtos para terem preço nulo? É um erro no cadastro? Como tratar? No que utilizamos o preco_custo (imagino que em cálculos de lucro, por exemplo), e que possa ser impactado pelos dados faltantes?

---

### 2.3 NULLs em orders (datas) [PERGUNTAR] / [BUG]

→ **Pedidos sem delivered_at:** 292
→ **Pedidos sem tracking_code:** 97
→ **Faz sentido um pedido ter status "entregue" sem entregue_em?** [PERGUNTAR] / [BUG]

→ **Pergunta:** Há alguma falha entre sistemas para que hajam essas divergências em resultados na tabela orders? O que ocorre para que não haja o registro de data de entrega? Como se confirma se a entrega ocorreu?

---

### 2.4 NULLs em payments (por status) [PERGUNTAR] / [BUG] 

| Status | Total | Sem paid_at | % sem data |
|---|---|---|---|
| approved |669|25|3,7%|
| pending |23|23|100%|
| outros |108|108|100%|

→ **Pagamento 'approved' sem paid_at é:** [PERGUNTAR] / [BUG] 
→ **Pergunta:** O que significa um pedido com pagamento aprovado, mas sem data de pago_em? Como tratar esses casos?

---

### 2.5 NULLs em sellers **[OK]**

→ **Sellers sem taxa_comissao:** 0
→ **O que usar quando taxa é NULL?** Não vou perguntar porque não é o caso hoje. Se formos mapear todas as possíveis combinações de dados faltantes, o projeto não terminaria.
→ **Pergunta:** -

---

## NÍVEL 3 — Distribuições

### 3.1 Pedidos por status **[OK]**

→ **Distribuição que observei (top 3 status):** Entregue (536 pedidos), Enviado (77 pedidos), Cancelado (66 pedidos)

→ **Parece saudável? Algum status com % inesperado?** 10% dos pedidos foram cancelados ou reembolsados. Importante entender o que houve com estes clientes, para compreender o que pode estar movimentando estes resultados. 

---

### 3.2 Receita por estado (top 5) **[OK]**

| Estado | Receita | Ticket Médio |
|---|---|---|
| 1.SP|367.522,13|2.295,86|
| 2.RJ|251.755,20|2.288,68|
| 3.PR|216.284,99|3.327,46|
| 4.MG|210.464,74|2.964,29|
| 5.PE|192.139,08|3.049,82|

→ **O estado líder faz sentido para o perfil do marketplace?** O estado de São Paulo é líder para o marketplace, possuindo o maior número de pedidos e o maior valor em receita dentre todos os estados, sendo quase 50% maior do que o segundo colocado, no caso, RJ. Apesar disso, seu ticket médio é o 11º colocado na lista. Estados com tickets médios maiores, como PA ou RN, concentram poucos pedidos. 
---

### 3.3 Distribuição de preços
→ **Faixa com mais produtos:** Dentro dos ranges que determinei, a maior presença de produtos se dá em valores até R$100. 
→ **Produto mais caro encontrado (aprox):** iPhone 9 Pro, no valor de R$8.169,13
→ **Há outliers de preço que parecem erro de cadastro?** Nenhum produto nas faixas superiores e inferiores de preço foram identificados como outliers

---

### 3.4 Top 3 produtos mais vendidos

| Produto | SKU | Unidades vendidas |
|---|---|---|
| 1. Barraca Camping|ESP-CAM-00001|32|
| 2. Notebook Consul i5 8GB |INF-NOT-00001|30|
| 3. Quadro Decorativo Clássico|DEC-QUA-00007|30|

→ **Esses produtos têm boa margem ou são volume sem lucro?** No caso da barraca, o preco_custo é nulo, portanto não podemos estimar. Os outros produtos parecem ter sim uma margem legal.

---

### 3.5 Sellers por volume
→ **Há sellers com avaliação alta (≥ 4.5) e volume baixo de pedidos?** Sim
→ **Lista de sellers nessa situação (se houver):** O seller da Mata - SE possui nota 5 com 57 pedidos.

→ **Possível causa:** [PERGUNTAR] / [Seller novo] / [Produto de nicho]

---

### 3.6 Distribuição de avaliações
→ **Nota mais frequente:** 5
→ **% de notas 5:** 45%
→ **% de notas 1:** 3%
→ **Distribuição parece real ou fabricada?** Difícil afirmar. A distribuição cresce junto com as notas. 

---

## NÍVEL 4 — Consistência de FKs

| Verificação | Resultado | Problema? |
|---|---|---|
| Pedidos sem cliente |0|N/A|
| Itens sem produto |0|N/A|
| Pedidos sem pagamento |0|N/A|
| Pedidos com 2+ pagamentos |0|N/A|
| Reviews sem pedido |0|N/A|
| Produtos sem categoria |0|N/A|

→ **Alguma inconsistência de FK encontrada?** A partir das investigações feitas, não
→ **O que fazer com registros órfãos?** [PERGUNTAR] / [Descartar] / [Manter com flag]

---

## NÍVEL 5 — Anomalias Investigadas

### 5.1 Pedidos "entregues" sem data de entrega
→ **Quantidade:** 28
→ **% do total de pedidos entregues:** 5,2%
→ **Classifico como:** [BUG] / [Regra de negócio — PERGUNTAR]
→ **Pergunta exata pro stakeholder:** Dado que não há data de entrega, como certificar que o pedido foi entregue? O que faz com que um pedido seja dado como entregue?

---

### 5.2 Pagamentos aprovados sem data
→ **Quantidade:** 25
→ **% dos pagamentos aprovados:** 3,7%
→ **Classifico como:** [BUG de pipeline] / [Regra — PERGUNTAR]
→ **Pergunta exata pro stakeholder:** O que fez o pedido seguir como aprovado sem a data de pagamento? Certificar que o pedido está pago, como fazer isso?

---

### 5.3 Produtos com margem negativa
→ **Quantidade:** 4
→ **Categoria mais afetada:** Beleza, com 2 produtos listados.
→ **São promoções intencionais ou erro de cadastro?** [PERGUNTAR] / [BUG]
→ **Pergunta exata pro stakeholder:** Há produtos com margem negativa. Eles devem existir? Devem ser mantidos no catálogo? 

---

### 5.4 CPF em múltiplos formatos

| Formato | Quantidade | % |
|---|---|---|
| Com máscara (XXX.XXX.XXX-XX) |65|65%|
| Só números (11 dígitos) |21|21%|
| Formato inválido |9|9%|
| NULL |5|5%| - Já identificados antes

→ **De onde vieram os formatos diferentes?** [PERGUNTAR]
→ **Devemos normalizar no dbt?** [PERGUNTAR] / sim / não
→ **Pergunta exata pro stakeholder:** Como tratar os CPS em diferentes formatos? Existe um preferido? O que fazer com os nulos? 

---

### 5.5 Emails inválidos
→ **Sem arroba:** 2
→ **Sem domínio:** 4
→ **Total inválidos:** 1 nulo, já identificado préviamente
→ **O que fazer com esses emails no modelo?** [PERGUNTAR] / [Flag is_email_valid] / [NULL]
→ **Pergunta exata pro stakeholder:** Como tratar e-mails fora do formato default?

---

## CONSOLIDADO — Perguntas para o Stakeholder

> Copie aqui todas as perguntas marcadas como [PERGUNTAR] nos níveis anteriores.
> Esta lista é o que você vai levar pra reunião com a Marina.

1. Como proceder com os CPFs e e-mails faltando?
2. O que diferem estes produtos para terem preço nulo? É um erro no cadastro? Como tratar? No que utilizamos o preco_custo (imagino que em cálculos de lucro, por exemplo), e que possa ser impactado pelos dados faltantes?
3. Há alguma falha entre sistemas para que hajam essas divergências em resultados na tabela orders? O que ocorre para que não haja o registro de data de entrega? Como se confirma se a entrega ocorreu?
4. O que significa um pedido com pagamento aprovado, mas sem data de pago_em? Como tratar e proceder com esses casos?
5. Dado que não há data de entrega, como certificar que o pedido foi entregue? O que faz com que um pedido seja dado como entregue?
6. O que fez o pedido seguir como aprovado sem a data de pagamento? Certificar que o pedido está pago, como fazer isso?
7. Há produtos com margem negativa. Eles devem existir? Devem ser mantidos no catálogo? 
8. Como tratar os CPS em diferentes formatos? Existe um preferido? O que fazer com os nulos? 
9. Como tratar e-mails fora do formato default? E faltantes?
10. Sellers com poucos pedidos e avaliações altas: produtos de nicho? Público específico? Quanto isso se torna uma redflag?

---

## CONSOLIDADO — Bugs para Reportar à Engenharia

> Itens marcados como [BUG] que não precisam de decisão de negócio — apenas correção técnica.

1. CPFs, e-mails nulos
2. Falta de dados como datas de entrega ou de pagamento, e pedidos entregues ou aprovados
3. Produtos com preco_custo nulo: como surgem? O que podemos fazer para corrigir?

---

## CONSOLIDADO — Decisões já claras (não precisa perguntar)

> Coisas que você entendeu pelo contexto e não precisam de validação com stakeholder.

1. A integração das tabelas
2. O que é esperado ver em cada uma delas

---

*Próximo passo: leve as perguntas do consolidado pra sessão com a Marina (STAKEHOLDER_SKILL.md).*
