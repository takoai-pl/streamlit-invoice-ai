# Copyright (c) TaKo AI Sp. z o.o.
import requests.exceptions
import streamlit as st

from frontend.presentation.handler import handler
from frontend.utils.language import i18n as _


def build_history() -> None:
    st.subheader(_("history"))

    try:
        invoices = handler.get_all_invoices()
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
    ) = st.columns([0.75, 1, 1, 1, 0.25, 0.33, 0.33, 0.33])

    for i, invoice in enumerate(invoices):
        issueddate.text(invoice.issuedAt)
        invoiceno.text(invoice.invoiceNo)
        client.text(invoice.client.name)
        business.text(invoice.business.name)
        language.text(invoice.language)
        edit.button(
            ":pencil:",
            key=f"edit-{i}",
        )
        download.button(
            label=":floppy_disk:",
            on_click=handler.download_invoice,
            args=(invoice,),
            key=f"download-{i}",
        )
        delete.button(
            ":x:",
            key=f"delete-{i}",
        )
