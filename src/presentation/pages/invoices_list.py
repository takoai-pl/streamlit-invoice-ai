import streamlit as st

from src.presentation.handler import handler
from src.utils.language import i18n as _


def build_invoices_list():
    st.subheader(_("invoices_list"))

    c1, c2, c3, c4,  = st.columns([])
    st.table(handler.get_all_invoices())
