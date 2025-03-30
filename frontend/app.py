# Copyright (c) TaKo AI Sp. z o.o.

import importlib
import time

import streamlit as st
from streamlit_cookies_controller import CookieController

from frontend.domain.entities.invoice_entity import InvoiceEntity
from frontend.presentation.pages.business_details import build_business_fields
from frontend.presentation.pages.client_details import build_client_fields
from frontend.presentation.pages.history import build_history
from frontend.presentation.pages.invoice_details import build_invoice_fields
from frontend.presentation.pages.login import build_login_page, clear_session_cookies
from frontend.presentation.widgets.language_selector import build_language_selector
from frontend.utils.language import (
    Language,
)
from frontend.utils.language import i18n as _


class App:
    def __init__(self) -> None:
        self.controller = CookieController()

        if "authenticated" not in st.session_state:
            st.session_state.authenticated = self.controller.get("authenticated")

        if "user" not in st.session_state:
            st.session_state.user = self.controller.get("user")

        if "invoice" not in st.session_state:
            st.session_state.invoice = InvoiceEntity()

        self.invoice = st.session_state.invoice
        self.language = Language()

        if "openai_api_key" not in st.session_state:
            st.session_state.openai_api_key = ""

        if "database_connection_string" not in st.session_state:
            st.session_state.database_connection_string = ""

        if "tavily_api_key" not in st.session_state:
            st.session_state.tavily_api_key = ""

        if "langchain_api_key" not in st.session_state:
            st.session_state.langchain_api_key = ""

    def run(self) -> None:
        st.session_state.authenticated = self.controller.get("authenticated")
        st.session_state.user = self.controller.get("user")
        time.sleep(1)
        if not st.session_state.authenticated:
            build_login_page()
            return

        tab_names = [
            str(_("invoice_details") + " :material/description:"),
            str(_("history") + " :material/history:"),
            str(
                _("client_details")
                + " & "
                + _("business_details")
                + " :material/apartment:"
            ),
        ]

        self.InvoiceDetails, self.History, self.ClientDetails = st.tabs(tab_names)

        with st.sidebar:
            st.header(_("settings"))
            build_language_selector(self.language)
            if st.button(_("logout")):
                clear_session_cookies(self.controller)
                st.rerun()
            st.markdown(f"**Version:** {importlib.metadata.version('invoice-ai')}")

        with self.InvoiceDetails:
            build_invoice_fields()

        with self.History:
            build_history()

        with self.ClientDetails:
            with st.expander(_("client_details"), expanded=True):
                build_client_fields()

            with st.expander(_("business_details"), expanded=True):
                build_business_fields()


if __name__ == "__main__":
    st.set_page_config(initial_sidebar_state="collapsed")
    app = App()
    app.run()
