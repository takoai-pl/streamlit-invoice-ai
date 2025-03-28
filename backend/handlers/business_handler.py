from typing import Tuple

from sqlalchemy.orm import Session

from backend.models.business_table import BusinessTable


class BusinessHandler:
    def get(self, session: Session, business_id: str) -> Tuple[BusinessTable, str]:
        """Get business by ID"""
        business = (
            session.query(BusinessTable)
            .filter(BusinessTable.businessID == business_id)
            .first()
        )
        if not business:
            return None, "Business not found"
        return business, None

    def update_business(
        self, session: Session, business_id: str, data: dict
    ) -> Tuple[BusinessTable, str]:
        """Update business details"""
        business, error = self.get(session, business_id)
        if error:
            return None, error

        # Update basic fields
        business.name = data.get("name", business.name)
        business.address = data.get("address", business.address)
        business.city = data.get("city", business.city)
        business.postalCode = data.get("postalCode", business.postalCode)
        business.country = data.get("country", business.country)
        business.vatNumber = data.get("vatNumber", business.vatNumber)
        business.phone = data.get("phone", business.phone)
        business.email = data.get("email", business.email)
        business.website = data.get("website", business.website)

        # Update logo if provided
        if "logo" in data:
            business.logo = data["logo"]

        try:
            session.commit()
            return business, None
        except Exception as e:
            session.rollback()
            return None, f"Failed to update business: {str(e)}"

    def delete(self, session: Session, business_id: str) -> Tuple[bool, str]:
        # Implementation of delete method
        pass
