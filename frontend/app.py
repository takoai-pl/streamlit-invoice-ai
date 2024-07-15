# Copyright (c) TaKo AI Sp. z o.o.

import streamlit as st

from frontend.domain.entities.invoice_entity import InvoiceEntity
from frontend.presentation.pages.ai_agent import build_agent
from frontend.presentation.pages.business_details import build_business_fields
from frontend.presentation.pages.client_details import build_client_fields
from frontend.presentation.pages.history import build_history
from frontend.presentation.pages.invoice_details import build_invoice_fields
from frontend.presentation.widgets.language_selector import build_language_selector
from frontend.utils.language import (
    Language,
)
from frontend.utils.language import i18n as _


class App:
    def __init__(self) -> None:
        if "invoice" not in st.session_state:
            st.session_state.invoice = InvoiceEntity()

        self.invoice = st.session_state.invoice
        self.language = Language()

        if "openai_api_key" not in st.session_state:
            st.session_state.openai_api_key = ""

        if "database_connection_string" not in st.session_state:
            st.session_state.database_connection_string = ""

        if "tavily_api_key" not in  st.session_state:
            st.session_state.tavily_api_key = ""

        if "langchain_api_key" not in st.session_state:
            st.session_state.langchain_api_key = ""

        tab_names = [
            str(_("invoice_details") + " :page_facing_up:"),
            str(
                _("shared_details")
                + " "
                + _("client_details")
                + " & "
                + _("business_details")
                + " :bust_in_silhouette:"
            ),
            str(_("agent_ai") + " :brain:"),
            str(_("history") + " :scroll:"),
        ]

        self.InvoiceDetails, self.ClientDetails, self.AgentAI, self.History = st.tabs(
            tab_names
        )

    def run(self) -> None:
        with st.sidebar:
            st.header(_("invoice") + " AI")

            st.session_state.openai_api_key = st.text_input(
                "OpenAI API Key",
                help=_("openai_api_key_help")
            )
            st.session_state.database_connection_string = st.text_input(
                "Database Connection String",
                help=_("database_connection_string_help")
            )
            st.session_state.tavily_key = st.text_input(
                "Tavily API Key",
                help=_("tavily_api_key_help")
            )
            st.session_state.langchain_api_key = st.text_input(
                "Langchain API Key",
                help=_("langchain_api_key_help")
            )

            st.header(_("settings"))
            build_language_selector(self.language)

            if st.button("debug"):
                print(self.invoice)

        with self.InvoiceDetails:
            build_invoice_fields()

        with self.ClientDetails:
            client_column, business_column = st.columns(2)

            with client_column:
                build_client_fields()

            with business_column:
                build_business_fields()

        with self.History:
            build_history()

        with self.AgentAI:
            build_agent()


if __name__ == "__main__":
    app = App()
    app.run()
