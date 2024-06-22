# Copyright (c) TaKo AI Sp. z o.o.

from sqlalchemy import Column, Float, Integer, MetaData, String, Table, create_engine, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import insert

DATABASE_URL = "sqlite:///test.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

metadata = MetaData()

business_table = Table(
    "business",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
    Column("street", String),
    Column("postCode", String),
    Column("town", String),
    Column("country", String),
    Column("vatNo", String),
    Column("bic", String),
    Column("iban", String),
)

client_table = Table(
    "client",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
    Column("street", String),
    Column("postCode", String),
    Column("town", String),
    Column("country", String),
    Column("vatNo", String),
)

invoice_table = Table(
    "invoice",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("invoiceNo", String),
    Column("currency", String),
    Column("vatPercent", Integer),
    Column("issuedAt", String),
    Column("dueTo", String),
    Column("note", String),
    Column("business_id", Integer, ForeignKey("business.id")),
    Column("client_id", Integer, ForeignKey("client.id")),
)

product_table = Table(
    "product",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("description", String),
    Column("quantity", Float),
    Column("unit", String),
    Column("price", Float),
    Column("vatPercent", Float),
    Column("invoice_id", Integer, ForeignKey("invoice.id")),
)
