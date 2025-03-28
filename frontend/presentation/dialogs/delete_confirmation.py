# Copyright (c) TaKo AI Sp. z o.o.
import requests.exceptions
import streamlit as st

from frontend.domain.entities import InvoiceEntity
from frontend.presentation.handler import handler
from frontend.utils.language import i18n as _


@st.dialog("confirm_delete")
def show_delete_confirmation(invoice: InvoiceEntity) -> None:
    st.markdown(_("delete_invoice_confirmation"))
    st.markdown(
        f"**{invoice.invoiceNo}** {invoice.client.name} {invoice.business.name}"
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button(_("cancel"), use_container_width=True):
            st.rerun()
    with col2:
        if st.button(_("delete"), type="primary", use_container_width=True):
            try:
                handler.delete_invoice(invoice.invoiceID)
                st.success(_("invoice_deleted"))
                st.rerun()
            except requests.exceptions.HTTPError as e:
                st.error(str(e))
            except Exception as e:
                st.warning(str(e))
