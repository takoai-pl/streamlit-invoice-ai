# Copyright (c) TaKo AI Sp. z o.o.
import requests
import streamlit as st

from frontend.utils.language import i18n as _


def _on_change_client(key: str, attribute: str) -> None:
    current_value = st.session_state[key]
    try:
        st.session_state.invoice.edit_client(**{attribute: current_value})
    except requests.exceptions.HTTPError as e:
        st.error(str(e))


def build_client_fields() -> None:
    st.subheader(_("client_details"))

    client_fields = ["name", "street", "postCode", "town", "country", "vatNo"]

    for field in client_fields:
        class_name = st.session_state.invoice.client.__class__.__name__.lower()
        key = f"{class_name}_{field}"
        st.text_input(
            _(field),
            value=getattr(st.session_state.invoice.client, field, ""),
            key=key,
            on_change=_on_change_client,
            args=(key, field, st.session_state.invoice),
        )
