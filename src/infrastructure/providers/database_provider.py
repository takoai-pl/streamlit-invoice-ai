# Copyright (c) TaKo AI Sp. z o.o.

from .database_schema import product_table, business_table, invoice_table
from sqlalchemy import select
from sqlalchemy.orm import Session


def get_business(session: Session, business_id: int):
    stmt = select(business_table).where(business_table.c.id == business_id)
    result = session.execute(stmt)
    return result.fetchone()


def get_all_products(session: Session):
    stmt = select(product_table)
    result = session.execute(stmt)
    return result.fetchall()


def get_invoice_by_client(session: Session, client_id: int):
    stmt = select(invoice_table).where(invoice_table.c.client_id == client_id)
    result = session.execute(stmt)
    return result.fetchall()


def get_product_by_invoice(session: Session, invoice_id: int):
    stmt = select(product_table).where(product_table.c.invoice_id == invoice_id)
    result = session.execute(stmt)
    return result.fetchall()
