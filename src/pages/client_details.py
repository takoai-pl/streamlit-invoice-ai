# Copyright (c) TaKo AI Sp. z o.o.

import streamlit as st
from models import Invoice


def _on_change_client(key: str, attribute: str):
    current_value = st.session_state[key]
    st.session_state.invoice.edit_client(**{attribute: current_value})


def build_client_fields():
    st.subheader(_("client_details"))

    client_fields = ['name', 'street', 'postCode', 'town', 'country', 'vatNo']

    for field in client_fields:
        class_name = st.session_state.invoice.client.__class__.__name__.lower()
        key = f"{class_name}_{field}"
        st.text_input(_(field),
                      value=getattr(st.session_state.invoice.client, field, ""),
                      key=key,
                      on_change=_on_change_client,
                      args=(key, field, st.session_state.invoice)
                      )
