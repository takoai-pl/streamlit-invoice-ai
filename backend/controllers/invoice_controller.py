from sqlalchemy import and_
from sqlalchemy.orm import Session


from backend.controllers.base_controller import BaseController, session_scope
from backend.models import InvoiceTable, BusinessTable, ClientTable, ProductTable


class InvoiceController(BaseController):
    @session_scope
    def invoice_list(
            self, session: Session
    ) -> (list[InvoiceTable], list[BusinessTable], list[ClientTable], list[list[ProductTable]]):
        all_invoices = session.query(InvoiceTable).all()

        invoices = []
        businesses = []
        clients = []
        products = []

        for invoice in all_invoices:
            invoice, business, client, product = self.invoice_get(invoice.invoiceNo, invoice.language)

            invoices.append(invoice)
            businesses.append(business)
            clients.append(client)
            products.append(product)

        return invoices, businesses, clients, products

    @session_scope
    def invoice_get(self, session: Session, invoice_no: str, language: str) -> (InvoiceTable, BusinessTable, ClientTable, list[ProductTable]):
        invoice = session.query(InvoiceTable).filter(
            and_(
                InvoiceTable.invoiceNo == invoice_no,
                InvoiceTable.language == language
            )
        ).first()

        if invoice is None:
            raise InvoiceNotFoundException(f"No invoice found with invoice number {invoice_no} and language {language}")

        business = session.query(BusinessTable).filter_by(businessID=invoice.business_id).first()
        client = session.query(ClientTable).filter_by(clientID=invoice.client_id).first()
        products = session.query(ProductTable).filter_by(invoice_id=invoice.invoiceId).all()

        return invoice, business, client, products

    @session_scope
    def invoice_add(self, session: Session, invoice: InvoiceTable, products: list[ProductTable]) -> None:
        session.add(invoice)
        for product in products:
            session.add(product)

    @session_scope
    def invoice_put(
            self, session: Session, invoice: InvoiceTable, language: str
    ) -> None:
        result = (
            session.query(InvoiceTable)
            .filter(
                and_(
                    InvoiceTable.invoiceId == invoice.invoiceNo,
                    InvoiceTable.language == language,
                    )
            )
            .first()
        )

        if result is None:
            raise InvoiceNotFoundException(
                f"No invoice found with id {invoice.invoiceNo}"
            )

        for key, value in invoice.__dict__.items():
            if key != "_sa_instance_state":
                setattr(result, key, value)

    @session_scope
    def invoice_del(self, session: Session, invoice_no: str) -> None:
        invoice_table = session.query(InvoiceTable).filter_by(id=invoice_no).first()
        if invoice_table is None:
            raise InvoiceNotFoundException(f"No invoice found with id {invoice_no}")
        session.delete(invoice_table)


class InvoiceNotFoundException(Exception):
    """Exception raised when an invoice with the given id does not exist."""

    def __init__(self, invoice_id: str):
        self.invoice_id = invoice_id
        self.message = f"No invoice found with id {invoice_id}"
        super().__init__(self.message)


class InvoiceRetrievalException(Exception):
    """Exception raised when there is an error retrieving invoices from the database."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)