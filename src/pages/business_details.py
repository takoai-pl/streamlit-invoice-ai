# Copyright (c) TaKo AI Sp. z o.o.

import streamlit as st
from utils.language import Language
from models import Invoice


def _on_change_business(key, attribute):
    current_value = st.session_state[key]
    st.session_state.invoice.edit_business(**{attribute: current_value})


def build_business_fields():
    st.subheader(_("business_details"))
    business_fields = [_('name'), _('street'), _('city'), _('country'), 'kvk', 'vatNo', 'iban', 'phone', 'email']

    for field in business_fields:
        class_name = st.session_state.invoice.business.__class__.__name__.lower()
        key = f"{class_name}_{field}"
        st.text_input(_(field),
                      value=getattr(st.session_state.invoice.business, field, ""),
                      key=key,
                      on_change=_on_change_business,
                      args=(key, field, st.session_state.invoice)
                      )
