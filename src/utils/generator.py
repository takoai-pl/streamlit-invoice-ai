# Copyright (c) TaKo AI Sp. z o.o.

import os

from src.domain.entities.invoice_entity import InvoiceEntity
from src.domain.entities.product_entity import ProductEntity
from src.utils.const import assets_path, product_latex_template
from src.utils.language import i18n as _


class Generator:
    def __init__(self, invoice: InvoiceEntity):
        self.invoice = invoice

        layout_path = os.path.join(assets_path, "layout.tex")
        with open(layout_path, "r") as f:
            self.layout = f.read()

    def substitute(self, key: str, value: str | None) -> None:
        self.layout = self.layout.replace(key, str(value))

    def append_products(self, products: list[ProductEntity]) -> None:
        product_latex = ""
        for product in products:
            product_latex += product_latex_template.format(
                description=product.description,
                quantity=product.quantity,
                unit=product.unit,
                price=product.price,
                vat=product.vat,
                sum=product.sum,
            )
        self.substitute("% PRODUCTS %", product_latex)

    def substitute_table(self) -> None:
        description = _("generated_description")
        quantity = _("generated_quantity")
        unit = _("generated_unit")
        price = _("generated_price")
        vat = _("vat")
        total = _("generated_sum")

        self.substitute("TABLE1", description)
        self.substitute("TABLE2", quantity)
        self.substitute("TABLE3", unit)
        self.substitute("TABLE4", price)
        self.substitute("TABLE5", vat)
        self.substitute("TABLE6", total)

    def substitute_invoice_details(self) -> None:
        try:
            self.invoice.are_all_fields_filled()
        except ValueError as e:
            raise e

        footer_first = _("generated_footer_first_part")
        footer_second = _("generated_footer_second_part")
        invoice = _("generated_invoice")
        issued_at = _("generated_issued_at")
        due_to = _("generated_due_to")
        vat = _("vat")
        vat_no = _("vat_no")
        notes = _("note")

        details = {
            "LINE10": "IBAN",
            "LINE11": self.invoice.business.iban,
            "INVOICE": invoice,
            "INVOICENO": self.invoice.invoiceNo,
            "ISSUEDATTEXT": issued_at,
            "ISSUEDDATE": (
                self.invoice.issuedAt.strftime("%Y-%m-%d")
                if self.invoice.issuedAt
                else ""
            ),
            "DUETOTEXT": due_to,
            "DUETODATE": (
                self.invoice.dueTo.strftime("%Y-%m-%d") if self.invoice.dueTo else ""
            ),
            "CLIENTLINE1": self.invoice.client.name,
            "CLIENTLINE2": self.invoice.client.street,
            "CLIENTLINE3": f"{self.invoice.client.postCode} {self.invoice.client.town}",
            "CLIENTLINE4": self.invoice.client.country,
            "CLIENTLINE5": f"{vat_no}: {self.invoice.client.vatNo}",
            "CLIENTLINE6": notes,
            "CLIENTLINE7": self.invoice.note,
            "LINE1": self.invoice.business.name,
            "LINE2": self.invoice.business.street,
            "LINE3": self.invoice.business.town,
            "LINE4": self.invoice.business.phone,
            "LINE5": self.invoice.business.email,
            "LINE6": vat,
            "LINE7": self.invoice.business.vatNo,
            "LINE8": vat_no,
            "LINE9": self.invoice.business.bic,
            "FOOTERTEXT": f"{footer_first}{self.invoice.business.name}{footer_second}{self.invoice.invoiceNo}",
        }
        for key, value in details.items():
            self.substitute(key, value)

    def generate(self) -> str:
        self.substitute_invoice_details()
        self.substitute_table()
        self.append_products(self.invoice.products)
        self.substitute("TOTAL1", "Subtotal")
        self.substitute("TOTAL2", str(self.invoice.subtotal))
        self.substitute("TOTAL3", str(self.invoice.vat_value))
        self.substitute("TOTAL4", "Total")
        self.substitute("TOTAL5", str(self.invoice.total))

        return self.layout
