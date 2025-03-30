# Copyright (c) TaKo AI Sp. z o.o.

import json
import os
import time

import streamlit as st
from streamlit_cookies_controller import CookieController

from frontend.data.providers.api_provider import APIProvider
from frontend.utils.language import i18n as _


def save_session_to_cookies(controller: CookieController, user_data: dict) -> None:
    # save user data to session state
    st.session_state.user = user_data
    st.session_state.authenticated = True

    # Save to cookies with 8 hour expiration
    controller.set("user", json.dumps(user_data))
    controller.set("authenticated", "true")
    time.sleep(1)


def load_session_from_cookies(controller: CookieController) -> bool:
    try:
        user_data = controller.get("user")
        authenticated = controller.get("authenticated")
        time.sleep(1)

        if user_data and authenticated == "true":
            # Parse the JSON string back into a dictionary
            st.session_state.user = (
                json.loads(user_data) if isinstance(user_data, str) else user_data
            )
            st.session_state.authenticated = True
            return True
    except Exception as e:
        print(f"Error loading cookies: {e}")
        pass
    return False


def clear_session_cookies(controller: CookieController) -> None:
    controller.remove("user")
    controller.remove("authenticated")
    time.sleep(1)
    st.session_state.user = None
    st.session_state.authenticated = False


def build_login_page() -> None:
    st.title(_("login"))

    controller = CookieController()

    if load_session_from_cookies(controller):
        st.rerun()

    with st.form("login_form"):
        username = st.text_input(_("username"))
        password = st.text_input(_("password"), type="password")
        submit_button = st.form_submit_button(_("login"))

        if submit_button:
            api_provider = APIProvider(
                base_url=os.getenv("BASE_URL"),
                api_key=os.getenv("API_KEY"),
            )
            try:
                response = api_provider.login(username, password)
                save_session_to_cookies(controller, response)
                st.rerun()
            except Exception as e:
                print(e)
                st.error(_("invalid_credentials"))
