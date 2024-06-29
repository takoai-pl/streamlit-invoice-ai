# Copyright (c) TaKo AI Sp. z o.o.

import requests

from frontend.domain import InvoiceEntity, ProductEntity


class APIProvider:
    def __init__(self, base_url: str):
        ### TODO: Add ERROR HANDLING
        self.base_url = base_url

    def invoice_get(self, invoice_no: str, language: str):
        response = requests.get(f"{self.base_url}/invoice/{invoice_no}/{language}")
        return response.json()

    def invoice_add(self, invoice: InvoiceEntity, products: list[ProductEntity]) -> None:
        response = requests.post(f"{self.base_url}/invoice", json=invoice.__dict__)
        invoice_id = response.json().get("invoice_id")
        for product in products:
            requests.post(f"{self.base_url}/invoice/{invoice_id}/product", json=product.__dict__)

    def invoice_put(
        self, invoice: InvoiceEntity, language: str
    ) -> None:
        requests.put(f"{self.base_url}/invoice/{invoice.invoiceNo}/{language}", json=invoice.__dict__)

    def invoice_del(self, invoice_no: str) -> None:
        requests.delete(f"{self.base_url}/invoice/{invoice_no}")

    def business_list(self):
        response = requests.get(f"{self.base_url}/business")
        return response.json()

    def business_get(self, business_name: str):
        response = requests.get(f"{self.base_url}/business/{business_name}")
        return response.json()

    def business_add(self, business):
        requests.post(f"{self.base_url}/business", json=business.__dict__)

    def business_put(self, business):
        requests.put(f"{self.base_url}/business/{business.name}", json=business.__dict__)

    def business_del(self, business_name: str):
        requests.delete(f"{self.base_url}/business/{business_name}")

    def client_list(self):
        response = requests.get(f"{self.base_url}/client")
        return response.json()

    def client_get(self, client_name: str):
        response = requests.get(f"{self.base_url}/client/{client_name}")
        return response.json()

    def client_add(self, client):
        requests.post(f"{self.base_url}/client", json=client.__dict__)

    def client_put(self, client):
        requests.put(f"{self.base_url}/client/{client.name}", json=client.__dict__)

    def client_del(self, client_name: str):
        requests.delete(f"{self.base_url}/client/{client_name}")



