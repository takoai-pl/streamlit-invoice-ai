# Copyright (c) TaKo AI Sp. z o.o.
import uuid

import requests
import streamlit as st

from frontend.domain.entities.client_entity import ClientEntity
from frontend.presentation.handler import handler
from frontend.utils.language import i18n as _


def _on_change_client_select(key: str, *args) -> None:
    current_value = st.session_state[key]
    if current_value == "" or current_value is None:
        return

    if current_value == _("add_new_client"):
        st.session_state.invoice.client = ClientEntity()
        st.session_state.invoice.client.clientID = str(uuid.uuid4())
        return

    try:
        client_id = st.session_state.client_id_mapping.get(current_value)
        if client_id:
            client_entity = handler.get_client_details(client_id)
            if client_entity:
                st.session_state.invoice.edit_client(**client_entity.__dict__)
    except requests.exceptions.HTTPError as e:
        st.error(str(e))
    except Exception as e:
        st.warning(str(e))


def _on_change_client_field(key: str, field: str) -> None:
    current_value = st.session_state[key]
    try:
        st.session_state.invoice.edit_client(**{field: current_value})
    except requests.exceptions.HTTPError as e:
        st.error(str(e))
    except Exception as e:
        st.warning(str(e))


def _create_client() -> None:
    try:
        if not st.session_state.invoice.client.clientID:
            st.session_state.invoice.client.clientID = str(uuid.uuid4())
        handler.create_client(st.session_state.invoice.client)
        st.success(_("client_created"))
    except requests.exceptions.HTTPError as e:
        st.error(str(e))
    except Exception as e:
        st.warning(str(e))


def _delete_client() -> None:
    try:
        handler.delete_client(st.session_state.invoice.client.clientID)
        st.session_state.invoice.client = ClientEntity()
        st.success(_("client_deleted"))
    except requests.exceptions.HTTPError as e:
        st.error(str(e))
    except Exception as e:
        st.warning(str(e))


def _update_client() -> None:
    try:
        handler.update_client(st.session_state.invoice.client)
        st.success(_("client_updated"))
    except requests.exceptions.HTTPError as e:
        st.error(str(e))
    except Exception as e:
        st.warning(str(e))


def build_client_fields() -> None:
    st.subheader(_("client_details"))

    clients = handler.get_all_clients()
    client_names = [client.name for client in clients]
    st.session_state.client_id_mapping = {
        client.name: client.clientID for client in clients
    }
    client_names.append(_("add_new_client"))

    current_client = (
        st.session_state.invoice.client.name
        if st.session_state.invoice.client.name
        else None
    )
    current_index = (
        client_names.index(current_client) if current_client in client_names else None
    )

    selected_client = st.selectbox(
        _("client"),
        client_names,
        index=current_index,
        placeholder=_("select_client"),
        on_change=_on_change_client_select,
        key="client_select",
        args=("client_select",),
    )

    if selected_client == "":
        st.session_state.invoice.client = ClientEntity()
        st.session_state.invoice.client.clientID = str(uuid.uuid4())

    # Create two columns for the main content
    main_col, extra_col = st.columns([3, 1])

    with main_col:
        client_fields = [
            ("name", ""),
            ("street", ""),
            ("postCode", ""),
            ("town", ""),
            ("country", ""),
            ("vatNo", ""),
        ]

        for field, help_text in client_fields:
            class_name = st.session_state.invoice.client.__class__.__name__.lower()
            key = f"{class_name}_{field}"
            st.text_input(
                _(field),
                value=getattr(st.session_state.invoice.client, field, ""),
                key=key,
                on_change=_on_change_client_field,
                args=(key, field),
                help=help_text,
            )

    with extra_col:
        # This column is reserved for any future additional client information
        # that might be added later
        pass

    # Action buttons at the bottom
    if selected_client == _("add_new_client") or not selected_client:
        st.button(
            _("create_client"),
            on_click=_create_client,
            type="primary",
        )
    else:
        col1, col2 = st.columns(2)
        with col1:
            st.button(
                _("update_client"),
                on_click=_update_client,
                type="primary",
            )
        with col2:
            st.button(
                _("delete_client"),
                on_click=_delete_client,
                type="secondary",
            )
