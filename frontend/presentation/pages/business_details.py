# Copyright (c) TaKo AI Sp. z o.o.

import base64

import requests
import streamlit as st

from frontend.domain.entities.business_entity import BusinessEntity
from frontend.presentation.handler import handler
from frontend.utils.language import (
    i18n as _,
)


def _on_change_business_select(key: str, *args) -> None:
    current_value = st.session_state[key]
    if current_value == "" or current_value is None:
        return

    if current_value == _("add_new_business"):
        st.session_state.invoice.business = BusinessEntity()
        return

    try:
        business_entity = handler.get_business_details(current_value)
        if business_entity:
            st.session_state.invoice.edit_business(**business_entity.__dict__)
    except requests.exceptions.HTTPError as e:
        st.error(str(e))
    except Exception as e:
        st.warning(str(e))


def _on_change_business_field(key: str, field: str) -> None:
    current_value = st.session_state[key]
    try:
        st.session_state.invoice.edit_business(**{field: current_value})
    except requests.exceptions.HTTPError as e:
        st.error(str(e))
    except Exception as e:
        st.warning(str(e))


def _create_business() -> None:
    try:
        handler.create_business(st.session_state.invoice.business)
        st.success(_("business_created"))
    except requests.exceptions.HTTPError as e:
        st.error(str(e))
    except Exception as e:
        st.warning(str(e))


def _delete_business() -> None:
    try:
        handler.delete_business(st.session_state.invoice.business.name)
        st.session_state.invoice.business = BusinessEntity()
        st.success(_("business_deleted"))
    except requests.exceptions.HTTPError as e:
        st.error(str(e))
    except Exception as e:
        st.warning(str(e))


def _update_business() -> None:
    try:
        handler.update_business(st.session_state.invoice.business)
        st.success(_("business_updated"))
    except requests.exceptions.HTTPError as e:
        st.error(str(e))
    except Exception as e:
        st.warning(str(e))


def build_business_fields() -> None:
    st.subheader(_("business_details"))

    business_names = handler.get_all_businesses_names()
    business_names.append(_("add_new_business"))

    current_business = (
        st.session_state.invoice.business.name
        if st.session_state.invoice.business.name
        else None
    )
    current_index = (
        business_names.index(current_business)
        if current_business in business_names
        else None
    )

    selected_business = st.selectbox(
        _("business"),
        business_names,
        index=current_index,
        placeholder=_("select_business"),
        on_change=_on_change_business_select,
        key="business_select",
        args=("business_select",),
    )

    if selected_business == _("add_new_business"):
        st.session_state.invoice.business = BusinessEntity()

    # Business fields
    business_fields = [
        ("name", ""),
        ("street", ""),
        ("postCode", ""),
        ("town", ""),
        ("country", ""),
        ("vatNo", ""),
        ("bic", ""),
        ("iban", ""),
        ("phone", ""),
        ("email", ""),
    ]

    for field, help_text in business_fields:
        class_name = st.session_state.invoice.business.__class__.__name__.lower()
        key = f"{class_name}_{field}"
        st.text_input(
            _(field),
            value=getattr(st.session_state.invoice.business, field, ""),
            key=key,
            on_change=_on_change_business_field,
            args=(key, field),
            help=help_text,
        )

    # Logo upload section at the bottom
    st.subheader(_("business_logo"))
    uploaded_file = st.file_uploader(
        _("upload_logo"),
        type=["png", "jpg", "jpeg"],
        key="business_logo_uploader",
    )

    if uploaded_file is not None:
        # Convert uploaded file to base64
        file_bytes = uploaded_file.getvalue()
        base64_image = base64.b64encode(file_bytes).decode()
        st.session_state.invoice.business.logo = base64_image

        # Display the uploaded image
        st.image(uploaded_file, caption=_("current_logo"))
    elif st.session_state.invoice.business.logo:
        # Display existing logo if available
        st.image(
            base64.b64decode(st.session_state.invoice.business.logo),
            caption=_("current_logo"),
        )

    col1, col2 = st.columns(2)
    with col1:
        if selected_business == _("add_new_business") or not selected_business:
            st.button(
                _("create_business"),
                on_click=_create_business,
                type="primary",
            )
        else:
            st.button(
                _("update_business"),
                on_click=_update_business,
                type="primary",
            )
    with col2:
        if selected_business and selected_business != _("add_new_business"):
            st.button(
                _("delete_business"),
                on_click=_delete_business,
                type="secondary",
            )
