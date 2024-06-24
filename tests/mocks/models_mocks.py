# Copyright (c) TaKo AI Sp. z o.o.

from src.domain.entities.business_entity import BusinessEntity

business_model_mock = BusinessEntity(
    name="Test Business",
    street="Test Street",
    postCode="Test Post Code",
    town="Test Town",
    country="Test Country",
    vatNo="Test VAT No",
    bic="Test BIC",
    iban="Test IBAN",
    phone="Test Phone",
    email="Test Email",
)
