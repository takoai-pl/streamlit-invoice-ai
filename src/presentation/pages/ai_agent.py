# Copyright (c) TaKo AI Sp. z o.o.

import streamlit as st


def build_agent():
    st.subheader("Agent Helper")
    st.text("This is a helper for the agent. He can help you manage your accounting.")

    st.text("")
    st.chat_input(placeholder="Type your message here...")
