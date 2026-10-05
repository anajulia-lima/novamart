"""
NovaMart - Bad Data Injector (ferramenta didática)
=====================================================
Insere, de propósito, linhas inválidas nas tabelas "app.*" (dados brutos
da aplicação) para que o pipeline agendado (ingestão + dbt build) capture
o problema via teste do dbt, dispare o alerta de falha no Discord, e você
possa demonstrar em aula o ciclo completo: erro -> alerta -> debug -> fix.

Casos disponíveis:
  1 - Genérico (accepted_values): status de pagamento fora da lista válida
  2 - Genérico (relationships): cliente com indicado_por_id_cliente órfão
      (essa coluna NÃO tem FK real no Postgres — auto-referência solta em
      app.customers — por isso o insert passa no banco e só é pego pelo
      teste do dbt)
  3 - Customizado (teste singular): preco_total não bate com quantidade * preco_unitario

Uso:
    python inject_bad_data.py --case 1
    python inject_bad_data.py --case 2
    python inject_bad_data.py --case 3
"""

import argparse
import random
from datetime import datetime

import psycopg2
from faker import Faker
from generate_seed_data import DB_CONFIG, generate_address_raw, generate_cpf, generate_phone

fake = Faker("pt_BR")


def get_conn():
    return psycopg2.connect(**DB_CONFIG)


def case_1_invalid_payment_status(conn):
    """Dispara o teste genérico accepted_values em stg_payments.status."""
    cur = conn.cursor()
    cur.execute("SELECT id, valor_total FROM app.orders ORDER BY RANDOM() LIMIT 1")
    row = cur.fetchone()
    if not row:
        print("[WARN] Nenhum pedido encontrado para anexar o pagamento inválido.")
        return
    id_pedido, total = row
    cur.execute(
        """
        INSERT INTO app.payments (id_pedido, id_metodo_pagamento, status, valor, parcelas, criado_em)
        VALUES (%s, 3, 'chargeback_iniciado', %s, 1, %s)
        """,
        (id_pedido, total, datetime.now()),
    )
    conn.commit()
    cur.close()
    print(f"[INJECT] Pagamento com status inválido 'chargeback_iniciado' inserido no pedido {id_pedido}.")
    print("         -> Teste esperado: accepted_values em stg_payments.status")


def case_2_orphan_referral(conn):
    """Dispara o teste genérico relationships em stg_customers.indicado_por_id_cliente
    (auto-relacionamento cliente -> cliente que indicou). Diferente de
    id_produto/id_vendedor/etc, essa coluna NÃO tem REFERENCES na DDL de
    app.customers, então o Postgres aceita o insert numa boa — só o teste
    do dbt (comparando contra stg_customers.id) é que vai pegar o problema."""
    cur = conn.cursor()
    now = datetime.now()
    fake_referrer_id = 999999999

    cpf_fmt = True
    cur.execute(
        """
        INSERT INTO app.customers
        (nome_completo, email, telefone, cpf, data_nascimento, endereco_raw, cidade, estado,
         cep, status, indicado_por_id_cliente, criado_em, atualizado_em)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,'active',%s,%s,%s)
        RETURNING id
        """,
        (
            fake.name(), fake.email(), generate_phone(), generate_cpf(formatted=cpf_fmt),
            fake.date_of_birth(minimum_age=18, maximum_age=65), generate_address_raw(),
            fake.city(), "SP", f"{random.randint(10000,99999)}-{random.randint(100,999)}",
            fake_referrer_id, now, now,
        ),
    )
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    print(f"[INJECT] Cliente {new_id} inserido com indicado_por_id_cliente apontando para cliente inexistente ({fake_referrer_id}).")
    print("         -> Teste esperado: relationships em stg_customers.indicado_por_id_cliente -> stg_customers.id")


def case_3_price_mismatch(conn):
    """Dispara um teste customizado (singular): preco_total != quantidade * preco_unitario."""
    cur = conn.cursor()
    cur.execute("SELECT id, id_vendedor, preco FROM app.products ORDER BY RANDOM() LIMIT 1")
    row = cur.fetchone()
    if not row:
        print("[WARN] Nenhum produto encontrado.")
        return
    id_produto, id_vendedor, preco = row
    cur.execute("SELECT id FROM app.orders ORDER BY RANDOM() LIMIT 1")
    id_pedido = cur.fetchone()[0]
    quantidade = 3
    preco_unitario = float(preco)
    preco_total_errado = 0.01  # deveria ser quantidade * preco_unitario
    cur.execute(
        """
        INSERT INTO app.order_items
        (id_pedido, id_produto, id_vendedor, quantidade, preco_unitario, preco_total, valor_desconto)
        VALUES (%s, %s, %s, %s, %s, %s, 0)
        """,
        (id_pedido, id_produto, id_vendedor, quantidade, preco_unitario, preco_total_errado),
    )
    conn.commit()
    cur.close()
    print(f"[INJECT] Item de pedido com preco_total inconsistente ({preco_total_errado}) no pedido {id_pedido}.")
    print("         -> Teste esperado: teste singular assert_order_item_price_matches_quantity")


CASES = {
    1: case_1_invalid_payment_status,
    2: case_2_orphan_referral,
    3: case_3_price_mismatch,
}


def main():
    parser = argparse.ArgumentParser(description="NovaMart Bad Data Injector")
    parser.add_argument("--case", type=int, choices=sorted(CASES.keys()), required=True)
    args = parser.parse_args()

    conn = get_conn()
    try:
        CASES[args.case](conn)
    except Exception as e:
        conn.rollback()
        print(f"[ERROR] Falha ao injetar dado problemático: {e}")
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()
