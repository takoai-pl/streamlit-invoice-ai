# Copyright (c) TaKo AI Sp. z o.o.

import os
import tempfile
import subprocess
from io import BytesIO

from flask import send_file, Flask

from src.domain.entities.invoice_entity import InvoiceEntity
from src.domain.entities.product_entity import ProductEntity
from src.utils.const import assets_path, product_latex_template
from src.utils.language import i18n as _
from streamlit.elements.widgets.button import marshall_file


app = Flask(__name__)


@app.route("/download")
def download(self, invoice: InvoiceEntity) -> None:
    try:
        self.generate(invoice)
    except ValueError as e:
        raise e

    # file_data = self.latex_compile()
    # file_object = BytesIO(file_data)

    #mock file object:
    file_object = BytesIO(b"mocked file data")

    invoice_str = _("invoice")
    send_file(file_object,
              as_attachment=True,
              download_name=f"{invoice_str}_{invoice.invoiceNo}_{invoice.language}.pdf",
              )


class Generator:
    def __init__(self):
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

    def substitute_invoice_details(self, invoice: InvoiceEntity) -> None:
        try:
            invoice.are_all_fields_filled()
        except ValueError as e:
            raise e

        footer_first = _("generated_footer_first_part")
        footer_second = _("generated_footer_second_part")
        invoice_str = _("generated_invoice")
        issued_at = _("generated_issued_at")
        due_to = _("generated_due_to")
        vat = _("vat")
        vat_no = _("vat_no")
        notes = _("note")

        details = {
            "LINE10": "IBAN",
            "LINE11": invoice.business.iban,
            "INVOICE": invoice,
            "INVOICENO": invoice.invoiceNo,
            "ISSUEDATTEXT": issued_at,
            "ISSUEDDATE": (
                invoice.issuedAt.strftime("%Y-%m-%d")
                if invoice.issuedAt
                else ""
            ),
            "DUETOTEXT": due_to,
            "DUETODATE": (
                invoice.dueTo.strftime("%Y-%m-%d") if invoice.dueTo else ""
            ),
            "CLIENTLINE1": invoice.client.name,
            "CLIENTLINE2": invoice.client.street,
            "CLIENTLINE3": f"{invoice.client.postCode} {invoice.client.town}",
            "CLIENTLINE4": invoice.client.country,
            "CLIENTLINE5": f"{vat_no}: {invoice.client.vatNo}",
            "CLIENTLINE6": notes,
            "CLIENTLINE7": invoice.note,
            "LINE1": invoice.business.name,
            "LINE2": invoice.business.street,
            "LINE3": invoice.business.town,
            "LINE4": invoice.business.phone,
            "LINE5": invoice.business.email,
            "LINE6": vat,
            "LINE7": invoice.business.vatNo,
            "LINE8": vat_no,
            "LINE9": invoice.business.bic,
            "FOOTERTEXT": f"{footer_first}{invoice.business.name}{footer_second}{invoice.invoiceNo}",
        }
        for key, value in details.items():
            self.substitute(key, value)

    def generate(self, invoice: InvoiceEntity) -> str | None:
        self.substitute_invoice_details(invoice)
        self.substitute_table()
        self.append_products(invoice.products)
        self.substitute("TOTAL1", "Subtotal")
        self.substitute("TOTAL2", str(invoice.subtotal))
        self.substitute("TOTAL3", str(invoice.vat_value))
        self.substitute("TOTAL4", "Total")
        self.substitute("TOTAL5", str(invoice.total))

        return self.layout

    def latex_compile(self) -> bytes | None:
        with tempfile.TemporaryDirectory() as tempdir:
            tex_path = os.path.join(tempdir, "invoice.tex")
            pdf_path = os.path.join(tempdir, "invoice.pdf")

            with open(tex_path, "w") as f:
                f.write(self.layout)

            result = subprocess.run(
                ["xelatex", "-output-directory", tempdir, tex_path],
                capture_output=True,
                text=True
            )

            if result.returncode != 0:
                print("XeLaTeX compilation failed")
                print(result.stdout)
                print(result.stderr)
                return None

            with open(pdf_path, "rb") as f:
                return f.read()
