# Copyright (c) TaKo AI Sp. z o.o.

import streamlit as st

from frontend.utils.language import (
    Language,
)
from frontend.utils.language import (
    i18n as _,
)


def _on_change_language(key: str, language: Language) -> None:
    selected_language = st.session_state[key]
    selected_language_value = Language.language_dict[selected_language]
    language.change_language(selected_language_value)


def build_language_selector(language: Language) -> None:
    st.subheader(_("language"))

    language_options = list(Language.language_dict.keys())

    current_language_value = st.session_state.language
    current_language_name = next(
        (
            name
            for name, value in Language.language_dict.items()
            if value == current_language_value
        ),
        None,
    )

    key = "language_selector"
    st.selectbox(
        label=_("select_language"),
        options=language_options,
        index=(
            language_options.index(current_language_name)
            if current_language_name
            else None
        ),
        on_change=_on_change_language,
        key=key,
        args=(key, language),
    )
