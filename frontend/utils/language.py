# Copyright (c) TaKo AI Sp. z o.o.

import gettext

import streamlit as st


class Language:
    language_dict = {"English": "en", "Polish": "pl"}

    def __init__(self) -> None:
        self.translations = {
            "en": gettext.translation("base", "locales", languages=["en"]),
            "pl": gettext.translation("base", "locales", languages=["pl"]),
        }

        if "language" not in st.session_state:
            st.session_state.language = "pl"

        self.change_language(st.session_state.language)

    def change_language(self, language: str) -> None:
        st.session_state.language = language
        self.translations[st.session_state.language].install(names=["_"])


def i18n(message: str) -> str:
    return _(message)  # type: ignore
