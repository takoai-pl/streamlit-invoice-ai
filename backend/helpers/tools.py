from langchain_core.tools import tool

from backend.controllers import BusinessController


def get_researcher_tools() -> list:
    return [
        get_business_details_by_name
    ]


def get_accountant_tools() -> list:
    return []


@tool()
def get_business_details_by_name(business_name: str):
    """ Get business details by name """

    business_controller = BusinessController("")

    return business_controller.list()
