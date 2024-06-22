# Copyright (c) TaKo AI Sp. z o.o.

import os
from src.models.invoice import Invoice
from src.models.product import Product
from src.utils.const import product_latex_template, assets_path


class Generator:
    def __init__(self, invoice: Invoice):
        self.invoice = invoice

        layout_path = os.path.join(assets_path, 'layout.tex')
        with open(layout_path, 'r') as f:
            self.layout = f.read()

    def substitute(self, key: str, value: str):
        self.layout = self.layout.replace(key, str(value))

    def append_products(self, products: list[Product]):
        product_latex = ''
        for product in products:
            product_latex += product_latex_template.format(
                description=product.description,
                quantity=product.quantity,
                unit=product.unit,
                price=product.price,
                vat=product.vat,
                sum=product.sum
            )
        self.substitute('% PRODUCTS %', product_latex)

    def substitute_invoice_details(self):
        details = {
            'INVOICE': 'Invoice',
            'INVOICENO': self.invoice.invoiceNo,
            'ISSUEDATTEXT': 'Issued at',
            'ISSUEDDATE': self.invoice.issuedAt.strftime('%Y-%m-%d') if self.invoice.issuedAt else '',
            'DUETOTEXT': 'Due to',
            'DUETODATE': self.invoice.dueTo.strftime('%Y-%m-%d') if self.invoice.dueTo else '',
            'CLIENTLINE1': self.invoice.client.name,
            'CLIENTLINE2': self.invoice.client.street,
            'CLIENTLINE3': self.invoice.client.town,
            'CLIENTLINE4': self.invoice.client.vatNo,
            'LINE1': self.invoice.business.name,
            'LINE2': self.invoice.business.street,
            'LINE3': self.invoice.business.town,
            'LINE4': self.invoice.business.phone,
            'LINE5': self.invoice.business.email,
            'LINE6': 'VAT',
            'LINE7': self.invoice.business.vatNo,
            'LINE8': 'KVK',
            'LINE9': self.invoice.business.kvk,
            'LINE10': 'IBAN',
            'LINE11': self.invoice.business.iban,
            'FOOTERTEXT': 'Thank you for your business!'
        }
        for key, value in details.items():
            self.substitute(key, value)

    def generate(self):
        self.substitute_invoice_details()
        self.append_products(self.invoice.products)
        self.substitute('TOTAL1', 'Subtotal')
        self.substitute('TOTAL2', self.invoice.subtotal)
        self.substitute('TOTAL3', self.invoice.vat_value)
        self.substitute('TOTAL4', 'Total')
        self.substitute('TOTAL5', self.invoice.total)
        return self.layout
