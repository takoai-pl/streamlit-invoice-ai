# Copyright (c) TaKo AI Sp. z o.o.

import streamlit as st

from frontend.presentation.handler import handler
from frontend.utils.language import i18n as _


def build_history() -> None:
    st.subheader(_("history"))

    invoices = handler.get_all_invoices()

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

    for invoice in invoices:
        issueddate.text(invoice.issuedAt)
        invoiceno.text(invoice.invoiceNo)
        client.text(invoice.client.name)
        business.text(invoice.business.name)
        language.text(invoice.language)
        edit.button(":pencil:")
        download.button(
            label=":floppy_disk:",
            on_click=handler.download_invoice,
            args=(invoice,),
        )
        delete.button(":x:")
