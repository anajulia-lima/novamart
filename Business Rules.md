# RESUMO DAS DECISÕES — Reunião com Marina Souza

## 1. **CPF em múltiplos formatos**
- **Decisão:** Normalizar para 11 dígitos, apenas números (remover máscara)
- **Validação:** Usar módulo 11 do CPF
- **Registros inválidos:** Marcar com flag `cpf_invalido = true`
- **NULLs:** Manter como NULL com flag `cpf_missing = true`

---

## 2. **Produtos com `preco_custo NULL` (10%)**
- **Decisão:** NÃO descarta o produto do catálogo
- **Causa:** Produto novo (custo ainda não cadastrado) ou importado (custo varia por câmbio)
- **Para análise de margem:** EXCLUIR da análise — não usar zero (daria 100% margem falso)
- **Flag:** `tem_preco_custo = false`

---

## 3. **Pedidos entregues SEM `entregue_em` (28 registros, 5,2%)**
- **Decisão:** Status "Entregue" = pedido foi realmente entregue (transportadora confirmou)
- **Causa:** Bug de integração com transportadora (falha ao registrar data)
- **Tratamento:** Marcar com flag `delivered_at_missing = true`
- **Receita:** CONTAR como receita (entrega confirmada pela transportadora)
- **Data estimada:** Usar `enviado_em` ou `criado_em` do status como proxy

---

## 4. **Pagamentos aprovados SEM `pago_em` (25 registros, 3,7%)**
- **Decisão:** Status 'approved' = pagamento foi autorizado (dinheiro recebido)
- **Causa:** Bug de pipeline na migração de gateway (2024) — falha ao registrar data
- **Tratamento:** Usar `criado_em` como proxy de `pago_em`
- **Flag:** `pago_em_proxy = true` para documentar a decisão
- **Receita:** CONTAR como receita (pagamento aprovado)

---

## 5. **Produtos com margem negativa (4 produtos)**
- **Decisão:** Criar flag `has_negative_margin = true`
- **Ação:** Não descartar — revisar caso a caso
- **Probabilidade:** 90% erro de cadastro, 10% promoção temporária legítima
- **Próximo passo:** Mandar relatório detalhado para validação manual

---

## 6. **E-mails inválidos e faltantes**
- **Decisão:** Manter registros do cliente, não descartar
- **Flag:** `email_valido = false` para emails sem @, sem domínio ou NULL
- **Uso:** 
  - Análise de clientes: incluir com flag
  - Comunicação (email marketing): filtrar só `email_valido = true`

---

## 7. **Sellers com poucos pedidos e avaliações altas**
- **Decisão:** NÃO é red flag automático
- **Análise necessária:**
  - Verificar ticket médio
  - Confirmar categoria (nicho vs produto barato)
  - Data de entrada (seller novo é normal)
- **Contexto:** Pode ser legítimo (nicho, produto caro) ou seller novo

---

## 📋 **REGRAS CONSOLIDADAS PARA DBT:**

| Situação | Ação |
|---|---|
| CPF com máscara | Remover, validar módulo 11 |
| `preco_custo NULL` | Excluir de análise de margem + flag |
| `delivered_at NULL` com status "Entregue" | Contar receita + flag `delivered_at_missing = true` |
| `pago_em NULL` com status "approved" | Usar `criado_em` como proxy + flag `pago_em_proxy = true` |
| Email inválido | Manter + flag `email_valido = false` |
| Margem negativa | Flag `has_negative_margin = true` + revisão manual |

---

**Status Final:** ✅ Todas as perguntas respondidas. Pronto para implementar no modelo de dados.