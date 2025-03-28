# Copyright (c) TaKo AI Sp. z o.o.

from typing import List
from urllib.parse import quote

import requests
from dotenv import load_dotenv

from frontend.data.models import BusinessModel, ClientModel, InvoiceModel

load_dotenv()


class APIProvider:
    def __init__(self, base_url: str | None, api_key: str | None):
        if not base_url:
            raise Exception("BASE_URL environment variable not set")
        if not api_key:
            raise Exception("API_KEY environment variable not set")
        self.base_url = base_url
        self.api_key = api_key
        self.headers = {"Authorization": f"Bearer {self.api_key}"}

    def invoice_list(self) -> List[InvoiceModel]:
        response = requests.get(f"{self.base_url}/invoice/", headers=self.headers)
        response.raise_for_status()
        return [InvoiceModel.from_json(invoice) for invoice in response.json()]

    def invoice_get(self, invoice_no: str, language: str) -> InvoiceModel:
        encoded_invoice_no = quote(invoice_no, safe="")
        response = requests.get(
            f"{self.base_url}/invoice/{encoded_invoice_no}/{language}/",
            headers=self.headers,
        )
        response.raise_for_status()
        return InvoiceModel.from_json(response.json())

    def invoice_add(self, invoice: InvoiceModel) -> None:
        response = requests.post(
            f"{self.base_url}/invoice/", json=invoice.to_json(), headers=self.headers
        )
        response.raise_for_status()

    def invoice_put(self, invoice: InvoiceModel) -> None:
        response = requests.put(
            f"{self.base_url}/invoice/", json=invoice.to_json(), headers=self.headers
        )
        response.raise_for_status()

    def invoice_del(self, invoice_id: str) -> None:
        response = requests.delete(
            f"{self.base_url}/invoice/{invoice_id}/", headers=self.headers
        )
        response.raise_for_status()

    def business_list(self) -> List[BusinessModel]:
        response = requests.get(f"{self.base_url}/business/", headers=self.headers)
        response.raise_for_status()
        return [BusinessModel.from_json(business) for business in response.json()]

    def business_get(self, business_name: str) -> BusinessModel:
        response = requests.get(
            f"{self.base_url}/business/{business_name}/", headers=self.headers
        )
        response.raise_for_status()
        return BusinessModel.from_json(response.json())

    def business_add(self, business: BusinessModel) -> None:
        response = requests.post(
            f"{self.base_url}/business/", json=business.to_json(), headers=self.headers
        )
        response.raise_for_status()

    def business_put(self, business: BusinessModel) -> None:
        response = requests.put(
            f"{self.base_url}/business/{business.name}/",
            json=business.to_json(),
            headers=self.headers,
        )
        response.raise_for_status()

    def business_del(self, business_name: str) -> None:
        response = requests.delete(
            f"{self.base_url}/business/{business_name}/", headers=self.headers
        )
        response.raise_for_status()

    def client_list(self) -> List[ClientModel]:
        response = requests.get(f"{self.base_url}/client/", headers=self.headers)
        response.raise_for_status()
        return [ClientModel.from_json(client) for client in response.json()]

    def client_get(self, client_name: str) -> ClientModel:
        response = requests.get(
            f"{self.base_url}/client/{client_name}/", headers=self.headers
        )
        response.raise_for_status()
        return ClientModel.from_json(response.json())

    def client_add(self, client: ClientModel) -> None:
        response = requests.post(
            f"{self.base_url}/client/", json=client.to_json(), headers=self.headers
        )
        response.raise_for_status()

    def client_put(self, client: ClientModel) -> None:
        response = requests.put(
            f"{self.base_url}/client/{client.name}/",
            json=client.to_json(),
            headers=self.headers,
        )
        response.raise_for_status()

    def client_del(self, client_name: str) -> None:
        response = requests.delete(
            f"{self.base_url}/client/{client_name}/", headers=self.headers
        )
        response.raise_for_status()
