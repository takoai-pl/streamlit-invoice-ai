# Copyright (c) TaKo AI Sp. z o.o.
import requests.exceptions
import streamlit as st

from frontend.domain.entities import InvoiceEntity
from frontend.presentation.handler import handler
from frontend.utils.generator import Generator
from frontend.utils.language import i18n as _


def build_history() -> None:
    st.subheader(_("history"))

    try:
        invoices = handler.get_all_invoices()
        if not invoices:
            st.info(_("no_invoices_yet"))
            return
    except requests.exceptions.HTTPError as e:
        st.error(str(e))
        return

    (
        issueddate,
        invoiceno,
        client,
        business,
        language,
        edit,
        download,
        delete,
    ) = st.columns([2, 2, 2, 2, 1, 1, 1, 1])

    for i, invoice in enumerate(invoices):
        issueddate.button(
            str(invoice.issuedAt), disabled=True, key=f"issueddate-{i}", type="tertiary"
        )
        invoiceno.button(
            invoice.invoiceNo, disabled=True, key=f"invoiceno-{i}", type="tertiary"
        )
        client.button(
            invoice.client.name, disabled=True, key=f"client-{i}", type="tertiary"
        )
        business.button(
            str(invoice.business.name),
            disabled=True,
            key=f"business-{i}",
            type="tertiary",
        )
        language.button(
            invoice.language, disabled=True, key=f"language-{i}", type="tertiary"
        )
        if edit.button(
            label="",
            icon=":material/edit:",
            key=f"edit-{i}",
        ):
            # Create a deep copy of the invoice data
            invoice_data = {
                "invoiceID": invoice.invoiceID,
                "invoiceNo": invoice.invoiceNo,
                "currency": invoice.currency,
                "vatPercent": invoice.vatPercent,
                "issuedAt": (
                    invoice.issuedAt.strftime("%Y-%m-%d") if invoice.issuedAt else None
                ),
                "dueTo": invoice.dueTo.strftime("%Y-%m-%d") if invoice.dueTo else None,
                "note": invoice.note,
                "language": invoice.language,
                "client": {
                    "name": invoice.client.name,
                    "street": invoice.client.street,
                    "postCode": invoice.client.postCode,
                    "town": invoice.client.town,
                    "country": invoice.client.country,
                    "vatNo": invoice.client.vatNo,
                },
                "business": {
                    "name": invoice.business.name,
                    "street": invoice.business.street,
                    "postCode": invoice.business.postCode,
                    "town": invoice.business.town,
                    "country": invoice.business.country,
                    "vatNo": invoice.business.vatNo,
                    "bic": invoice.business.bic,
                    "iban": invoice.business.iban,
                    "phone": invoice.business.phone,
                    "email": invoice.business.email,
                },
                "products": [
                    {
                        "description": product.description,
                        "quantity": product.quantity,
                        "unit": product.unit,
                        "price": product.price,
                        "vat": product.vat,
                    }
                    for product in invoice.products
                ],
            }
            st.session_state.invoice = InvoiceEntity(**invoice_data)
            st.session_state.is_editing = True
            st.session_state.original_invoice_id = invoice.invoiceID
            st.rerun()

        if download.button(
            label="",
            icon=":material/download:",
            key=f"download-{i}",
        ):
            try:
                generator = Generator()
                pdf_data = generator.generate(invoice)
                if pdf_data:
                    st.download_button(
                        label=_("download_invoice"),
                        data=pdf_data,
                        file_name=f"invoice_{invoice.invoiceNo}.pdf",
                        mime="application/pdf",
                        key=f"download_pdf_{i}",
                    )
                else:
                    st.error(_("invoice_generation_failed"))
            except Exception as e:
                st.error(str(e))

        if delete.button(
            label="",
            icon=":material/delete:",
            key=f"delete-{i}",
        ):
            try:
                handler.delete_invoice(invoice.invoiceID)
                st.rerun()
            except requests.exceptions.HTTPError as e:
                st.error(str(e))
