# Copyright (c) TaKo AI Sp. z o.o.

import streamlit as st
from src.utils.language import i18n


def build_file_uploader() -> None:
    if "uploaded_file" not in st.session_state:
        st.session_state.uploaded_file = None

        uploaded_file = st.file_uploader(
            "Choose a JSON file",
            accept_multiple_files=False,
            type="json",
            help=i18n("Upload a JSON file with invoice data"),
            on_change=st.session_state.invoice.from_json,
        )
