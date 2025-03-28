# Copyright (c) TaKo AI Sp. z o.o.
import streamlit as st

from frontend.domain.entities import InvoiceEntity
from frontend.utils.generator import Generator
from frontend.utils.language import i18n as _


@st.dialog("generation_options", width="large")
def show_generation_options(invoice: InvoiceEntity) -> None:
    st.markdown(_("generation_options_title"))
    st.markdown(
        f"**{invoice.invoiceNo}** {invoice.client.name} {invoice.business.name}"
    )

    selected_language = st.selectbox(
        _("select_language"),
        options=["en", "pl", "de", "fr"],
        format_func=lambda x: _(f"language_{x}"),
    )

    col1, col2 = st.columns(2)
    with col1:
        selected_currency = st.selectbox(
            _("select_currency"),
            options=["EUR", "USD", "PLN", "GBP"],
            index=["EUR", "USD", "PLN", "GBP"].index(invoice.currency),
        )
    with col2:
        currency_multiplier = st.number_input(
            _("currency_multiplier"),
            min_value=0.0,
            max_value=1000.0,
            value=1.0,
            step=0.01,
        )

    st.info(_("original_currency_info").format(currency=invoice.currency))

    col1, col2 = st.columns(2)
    with col1:
        if st.button(_("cancel"), use_container_width=True):
            st.rerun()
    with col2:
        if st.button(_("generate"), type="primary", use_container_width=True):
            try:
                generator = Generator()
                # Create a copy of the invoice with modified values
                modified_invoice = InvoiceEntity(**invoice.__dict__)
                modified_invoice.currency = selected_currency
                # Apply multiplier to all prices
                for product in modified_invoice.products:
                    product.price *= currency_multiplier

                pdf_data = generator.generate(
                    modified_invoice, language=selected_language
                )
                if pdf_data:
                    st.download_button(
                        label=_("download_invoice"),
                        data=pdf_data,
                        file_name=f"invoice_{invoice.invoiceNo}.pdf",
                        mime="application/pdf",
                        key="download_pdf",
                    )
                else:
                    st.error(_("invoice_generation_failed"))
            except Exception as e:
                st.error(str(e))
