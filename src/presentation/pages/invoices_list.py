# Copyright (c) TaKo AI Sp. z o.o.

import streamlit as st

from src.presentation.handler import handler
from src.utils.language import i18n as _


def build_invoices_list() -> None:
    st.subheader(_("invoices_list"))
    st.table(handler.get_all_invoices())
