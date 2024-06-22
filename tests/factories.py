# Copyright (c) TaKo AI Sp. z o.o.

import factory
from sqlalchemy.orm import Session
from factory.alchemy import SQLAlchemyModelFactory

from src.infrastructure.providers.database_schema import business_table, client_table, invoice_table, product_table
from src.infrastructure.providers.database_schema import SessionLocal


class BusinessFactory(SQLAlchemyModelFactory):
    class Meta:
        model = business_table
        sqlalchemy_session = SessionLocal

    id = factory.Sequence(lambda n: n)
    name = factory.Faker('name')
    street = factory.Faker('street_address')
    postCode = factory.Faker('zipcode')
    town = factory.Faker('city')
    country = factory.Faker('country')
    vatNo = factory.Faker('random_number')
    bic = factory.Faker('random_number')
    iban = factory.Faker('random_number')


class ClientFactory(SQLAlchemyModelFactory):
    class Meta:
        model = client_table
        sqlalchemy_session = SessionLocal

    id = factory.Sequence(lambda n: n)
    name = factory.Faker('name')
    street = factory.Faker('street_address')
    postCode = factory.Faker('zipcode')
    town = factory.Faker('city')
    country = factory.Faker('country')
    vatNo = factory.Faker('random_number')


class InvoiceFactory(SQLAlchemyModelFactory):
    class Meta:
        model = invoice_table
        sqlalchemy_session = SessionLocal

    id = factory.Sequence(lambda n: n)
    invoiceNo = factory.Faker('random_number')
    currency = factory.Faker('currency_code')
    vatPercent = factory.Faker('random_int')
    issuedAt = factory.Faker('date_time')
    dueTo = factory.Faker('date_time')
    note = factory.Faker('sentence')
    business_id = factory.SubFactory(BusinessFactory)
    client_id = factory.SubFactory(ClientFactory)


class ProductFactory(SQLAlchemyModelFactory):
    class Meta:
        model = product_table
        sqlalchemy_session = SessionLocal

    id = factory.Sequence(lambda n: n)
    description = factory.Faker('sentence')
    quantity = factory.Faker('random_int')
    unit = factory.Faker('word')
    price = factory.Faker('random_number')
    vatPercent = factory.Faker('random_int')
    invoice_id = factory.SubFactory(InvoiceFactory)
