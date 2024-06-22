# Copyright (c) TaKo AI Sp. z o.o.

import streamlit as st


def build_address_fields(on_change):
    st.text_input(_('street'), )
    c1, c2 = st.columns([1, 3])
    with c1:
        st.text_input(_('postCode'), )
    with c2:
        st.text_input(_('town'), )
    st.text_input(_('country'), )
