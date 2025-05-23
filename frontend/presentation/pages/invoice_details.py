# Copyright (c) TaKo AI Sp. z o.o.
import json
import logging
import re
import uuid
from datetime import datetime, timedelta

import requests.exceptions
import streamlit as st

from frontend.domain.entities.invoice_entity import InvoiceEntity
from frontend.presentation.handler import handler
from frontend.utils.const import currencies
from frontend.utils.language import i18n as _

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _on_change_product(key: str, attribute: str, product_index: int) -> None:
    current_value = st.session_state[key]
    try:
        if attribute in ["price", "quantity"]:
            product = st.session_state.invoice.products[product_index]
            product.vat = st.session_state.invoice.vatPercent
            logger.info(
                f"Setting product {product_index} VAT to match invoice VAT: {st.session_state.invoice.vatPercent}"
            )

        if attribute == "description" and current_value is None:
            current_value = ""

        st.session_state.invoice.edit_product(
            product_index, **{attribute: current_value}
        )
        logger.info(f"Product {product_index} {attribute} updated to: {current_value}")
    except requests.exceptions.HTTPError as e:
        logger.error(
            f"HTTP error while updating product {product_index} {attribute}: {str(e)}"
        )
        st.error(str(e))
    except Exception as e:
        logger.warning(
            f"Warning while updating product {product_index} {attribute}: {str(e)}"
        )
        st.warning(str(e))


def _on_change_details(key: str) -> None:
    current_value = st.session_state[key]
    try:
        if key == "invoiceNo":
            logger.info(f"Validating invoice number: {current_value}")
            InvoiceEntity.validate_invoice_no(current_value)
        elif key == "issuedAt":
            logger.info(f"Validating issue date: {current_value}")
            InvoiceEntity.validate_dates(current_value)

            # Automatically set due date to 2 weeks later
            due_date = current_value + timedelta(weeks=2)
            st.session_state.invoice.dueTo = due_date
            logger.info(
                f"Automatically set due date to 2 weeks after issue date: {due_date}"
            )

        elif key == "dueTo":
            logger.info(f"Validating due date: {current_value}")
            InvoiceEntity.validate_dates(current_value)
            if st.session_state.issuedAt:
                InvoiceEntity.validate_due_date(
                    current_value, {"issuedAt": st.session_state.issuedAt}
                )
        elif key == "vatPercent":
            # When VAT changes, update all products' VAT
            logger.info(f"Updating all products' VAT to: {current_value}")
            for product in st.session_state.invoice.products:
                product.vat = current_value

        st.session_state.invoice.edit_field(key, current_value)
        logger.info(f"Field {key} updated to: {current_value}")
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP error while updating field {key}: {str(e)}")
        st.error(str(e))
    except Exception as e:
        logger.warning(f"Warning while updating field {key}: {str(e)}")
        st.warning(str(e))


def _on_change_business_select(key: str, *args) -> None:
    current_value = st.session_state[key]
    if current_value == "" or current_value is None:
        return

    try:
        business_id = st.session_state.business_id_mapping.get(current_value)
        if business_id:
            business_entity = handler.get_business_details(business_id)
            if business_entity:
                st.session_state.invoice.edit_business(**business_entity.__dict__)
                logger.info(
                    f"Business selection updated. Current business: {current_value}"
                )

                try:
                    all_invoices = handler.get_all_invoices()
                    business_invoices = [
                        invoice
                        for invoice in all_invoices
                        if invoice.business.businessID == business_id
                    ]

                    if business_invoices:
                        latest_invoice = max(
                            business_invoices, key=lambda x: x.invoiceNo
                        )
                        if latest_invoice.invoiceNo:
                            numeric_parts = re.findall(
                                r"(\d+)/(\d+)", latest_invoice.invoiceNo
                            )
                            if numeric_parts:
                                year, invoice_num = numeric_parts[0]

                                current_year = datetime.now().year

                                if int(year) < current_year:
                                    new_invoice_no = f"{current_year}/0001"
                                else:
                                    next_num = str(int(invoice_num) + 1).zfill(4)
                                    new_invoice_no = f"{year}/{next_num}"

                                st.session_state.invoice.edit_field(
                                    "invoiceNo", new_invoice_no
                                )
                                logger.info(
                                    f"Auto-incremented invoice number to: {new_invoice_no}"
                                )
                            else:
                                current_year = datetime.now().year
                                new_invoice_no = f"{current_year}/0001"
                                st.session_state.invoice.edit_field(
                                    "invoiceNo", new_invoice_no
                                )
                                logger.info(
                                    f"Started new invoice numbering: {new_invoice_no}"
                                )
                    else:

                        current_year = datetime.now().year
                        new_invoice_no = f"{current_year}/0001"
                        st.session_state.invoice.edit_field("invoiceNo", new_invoice_no)
                        logger.info(f"Started new invoice numbering: {new_invoice_no}")

                except Exception as e:
                    logger.warning(f"Could not auto-increment invoice number: {str(e)}")

                    current_year = datetime.now().year
                    new_invoice_no = f"{current_year}/0001"
                    st.session_state.invoice.edit_field("invoiceNo", new_invoice_no)
                    logger.info(f"Set default invoice number: {new_invoice_no}")

    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP error while getting business details: {str(e)}")
        st.error(str(e))
    except Exception as e:
        logger.warning(f"Warning while getting business details: {str(e)}")
        st.warning(str(e))


def _on_change_client_select(key: str, *args) -> None:
    current_value = st.session_state[key]
    if current_value == "" or current_value is None:
        return
    try:
        client_id = st.session_state.client_id_mapping.get(current_value)
        if client_id:
            client_entity = handler.get_client_details(client_id)
            if client_entity:
                st.session_state.invoice.edit_client(**client_entity.__dict__)
                logger.info(
                    f"Client selection updated. Current client: {current_value}"
                )
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP error while getting client details: {str(e)}")
        st.error(str(e))
    except Exception as e:
        logger.warning(f"Warning while getting client details: {str(e)}")
        st.warning(str(e))


def build_invoice_fields() -> None:
    if "issuedAt" not in st.session_state:
        st.session_state.issuedAt = st.session_state.invoice.issuedAt

    if st.session_state.get("is_editing", False):
        st.warning(_("editing_mode"))

    if st.session_state.invoice.vatPercent is None:
        st.session_state.invoice.vatPercent = 0
        logger.info(
            f"Setting default invoice VAT to: {st.session_state.invoice.vatPercent}"
        )
        for product in st.session_state.invoice.products:
            product.vat = st.session_state.invoice.vatPercent
            logger.info(
                f"Setting product VAT to match invoice VAT: {st.session_state.invoice.vatPercent}"
            )

    client, business = st.columns(2)

    key_client = "client"

    with client:
        st.subheader(_("client_details"))
        try:
            clients = handler.get_all_clients()
            client_names = [client.name for client in clients]
            st.session_state.client_id_mapping = {
                client.name: client.clientID for client in clients
            }
            current_client = (
                st.session_state.invoice.client.name
                if st.session_state.invoice.client.name
                else None
            )
            current_index = (
                client_names.index(current_client)
                if current_client in client_names
                else None
            )

            st.selectbox(
                _("client"),
                client_names,
                index=current_index,
                placeholder=_("select_client"),
                on_change=_on_change_client_select,
                key=key_client,
                args=(key_client,),
            )
            logger.info(f"Client selection updated. Current client: {current_client}")
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error while getting client names: {str(e)}")
            st.error(str(e))
            return

    key_business = "business"

    with business:
        st.subheader(_("business_details"))
        try:
            businesses = handler.get_all_businesses()

            if st.session_state.user:
                user_data = (
                    json.loads(st.session_state.user)
                    if isinstance(st.session_state.user, str)
                    else st.session_state.user
                )
                if user_data.get("business_ids"):
                    businesses = [
                        business
                        for business in businesses
                        if business.businessID in user_data["business_ids"]
                    ]

            business_names = [business.name for business in businesses]
            st.session_state.business_id_mapping = {
                business.name: business.businessID for business in businesses
            }

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

            st.selectbox(
                _("business"),
                business_names,
                index=current_index,
                placeholder=_("select_business"),
                on_change=_on_change_business_select,
                key=key_business,
                args=(key_business,),
            )
        except requests.exceptions.HTTPError as e:
            st.error(str(e))
            return

    st.subheader(_("invoice_details"))

    column1, column2, column3 = st.columns([1, 1, 2])

    with column1:
        key_invoice_no = "invoiceNo"
        st.text_input(
            _("invoice_no"),
            value=st.session_state.invoice.invoiceNo,
            key=key_invoice_no,
            on_change=_on_change_details,
            args=(key_invoice_no,),
        )
    with column2:
        key_currency = "currency"
        currency = currencies.index(st.session_state.invoice.currency)
        st.selectbox(
            _("currency"),
            currencies,
            key=key_currency,
            index=currency if currency != "" else None,
            placeholder=_("select_currency"),
            on_change=_on_change_details,
            args=(key_currency,),
        )

    with column3:
        key_vat_percent = "vatPercent"

        vat_percent_options = [0, 4, 5, 7, 8, 9, 21, 23]

        current_vat = st.session_state.invoice.vatPercent

        try:
            _vat_index = vat_percent_options.index(current_vat)
        except ValueError:
            current_vat = 0
            st.session_state.invoice.vatPercent = current_vat
            logger.info(f"Setting VAT rate to default: {current_vat}")

        st.select_slider(
            _("vat_percent"),
            vat_percent_options,
            value=current_vat,
            key=key_vat_percent,
            on_change=_on_change_details,
            args=(key_vat_percent,),
        )

    key_issued_at = "issuedAt"
    key_due_to = "dueTo"
    c1, c2 = st.columns([1, 1])

    with c1:
        st.date_input(
            _("issued_date"),
            value=st.session_state.issuedAt,
            key=key_issued_at,
            format="DD/MM/YYYY",
            on_change=_on_change_details,
            args=(key_issued_at,),
        )

        st.date_input(
            _("due_date"),
            value=st.session_state.invoice.dueTo,
            key=key_due_to,
            format="DD/MM/YYYY",
            on_change=_on_change_details,
            args=(key_due_to,),
            min_value=st.session_state.issuedAt,
        )

    with c2:
        key_note = "note"
        st.text_area(
            _("note"),
            value=st.session_state.invoice.note,
            key=key_note,
            height=122,
            on_change=_on_change_details,
            args=(key_note,),
        )

    st.subheader(_("products"))

    product_display_values = [_("description"), _("quantity"), _("unit"), _("price")]

    unit_options = [_("piece"), _("hour"), _("day"), "kg", "m2", "m3", "m", "km", ""]

    for i, product in enumerate(st.session_state.invoice.products):
        c1, c2, c3, c4, c5 = st.columns([4, 2, 2, 2, 1])
        with c1:
            key_description = f"product_{i}_description"
            label = product_display_values[0] if i <= 1 else "hidden_label"
            st.text_input(
                label,
                label_visibility="collapsed" if i > 0 else "visible",
                value=product.description,
                key=key_description,
                on_change=_on_change_product,
                args=(key_description, "description", i),
            )
        with c2:
            key_quantity = f"product_{i}_quantity"
            label = "_" if i > 1 else product_display_values[1]
            st.number_input(
                label,
                label_visibility="collapsed" if i > 0 else "visible",
                value=product.quantity,
                key=key_quantity,
                on_change=_on_change_product,
                args=(key_quantity, "quantity", i),
            )
        with c3:
            key_unit = f"product_{i}_unit"
            label = "_" if i > 1 else product_display_values[2]
            unit = unit_options.index(product.unit)
            st.selectbox(
                label,
                unit_options,
                label_visibility="collapsed" if i > 0 else "visible",
                key=key_unit,
                index=unit if unit != "" else None,
                on_change=_on_change_product,
                args=(key_unit, "unit", i),
            )
        with c4:
            key_price = f"product_{i}_price"
            label = "_" if i > 1 else product_display_values[3]
            st.number_input(
                label,
                label_visibility="collapsed" if i > 0 else "visible",
                value=product.price,
                key=key_price,
                on_change=_on_change_product,
                args=(key_price, "price", i),
            )
        with c5:
            if i == 0:
                st.container(height=13, border=False)

            st.button(
                _("x"),
                key=f"delete_{i}",
                use_container_width=True,
                type="primary",
                on_click=st.session_state.invoice.delete_product,
                args=(i,),
            )

    c1, c2, c3, c4 = st.columns([6.3, 2.1, 2, 1])

    with c1:
        st.button(
            _("add_product"),
            on_click=st.session_state.invoice.add_product,
            args=("", 0, "", 0.0),
        )

    if len(st.session_state.invoice.products) > 0:
        with c2:
            st.text(f'{_("subtotal")}:')
            st.text(f'{_("vat_value")}:')
            st.text(f'{_("total")}:')

        with c3:
            st.text(f"{st.session_state.invoice.subtotal}")
            st.text(f"{st.session_state.invoice.vat_value}")
            st.text(
                f"{st.session_state.invoice.subtotal + st.session_state.invoice.vat_value}"
            )

    st.divider()

    col1, col2 = st.columns([1, 1])

    with col1:
        if st.session_state.get("is_editing", False):
            if st.button(_("save_changes"), type="primary"):
                try:
                    logger.info("Attempting to save invoice changes")
                    # Get the original invoice ID from the session state
                    original_invoice_id = st.session_state.get("original_invoice_id")
                    if original_invoice_id:
                        st.session_state.invoice.invoiceID = original_invoice_id
                        logger.info(
                            f"Preserving original invoice ID: {original_invoice_id}"
                        )
                    st.session_state.invoice.validate_invoice()

                    handler.update_invoice(st.session_state.invoice)
                    logger.info("Invoice updated successfully")
                    st.success(_("invoice_updated"))
                    st.session_state.is_editing = False
                    st.rerun()
                except ValueError as e:
                    logger.error(f"Validation error while updating invoice: {str(e)}")
                    st.error(f"Validation error: {str(e)}")
                except Exception as e:
                    logger.error(f"Error while updating invoice: {str(e)}")
                    st.error(str(e))
        else:
            if st.button(_("add_invoice"), type="primary"):
                try:
                    logger.info("Attempting to add invoice")
                    st.session_state.invoice.invoiceID = str(uuid.uuid4())

                    st.session_state.invoice.validate_invoice()
                    handler.add_invoice(st.session_state.invoice)
                    logger.info("Invoice added successfully")
                    st.success(_("invoice_added"))
                except ValueError as e:
                    logger.error(f"Validation error while adding invoice: {str(e)}")
                    st.error(f"Validation error: {str(e)}")
                except Exception as e:
                    logger.error(f"Error while adding invoice: {str(e)}")
                    st.error(str(e))

    with col2:
        if st.session_state.get("is_editing", False):
            if st.button(_("switch_to_generate")):
                st.session_state.is_editing = False
                st.rerun()
