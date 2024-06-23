# Copyright (c) TaKo AI Sp. z o.o.

import streamlit as st

from src.utils.language import i18n as _


def build_address_fields() -> None:
    st.text_input(
        _("street"),
    )
    c1, c2 = st.columns([1, 3])
    with c1:
        st.text_input(
            _("postCode"),
        )
    with c2:
        st.text_input(
            _("town"),
        )
    st.text_input(
        _("country"),
    )
