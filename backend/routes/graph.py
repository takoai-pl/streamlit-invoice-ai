import functools
import operator
from typing import Sequence, TypedDict, Annotated

from langchain_core.messages import BaseMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from langgraph.graph import END, StateGraph

from backend.helpers.supervisor import llm, supervisor_chain, members
from backend.helpers.tools import get_researcher_tools, get_accountant_tools, get_business_details_by_name
from backend.helpers.utils import create_agent, agent_node


# The agent state is the input to each node in the graph
class AgentState(TypedDict):
    # The annotation tells the graph that new messages will always
    # be added to the current states
    messages: Annotated[Sequence[BaseMessage], operator.add]
    # The 'next' field indicates where to route to next
    next: str


researcher_tools = get_researcher_tools()
accountant_tools = get_accountant_tools()

research_agent = create_agent(llm, [get_business_details_by_name], "You are a database researcher.")
research_node = functools.partial(agent_node, agent=research_agent, name="Researcher")

accountant_agent = create_agent(
    llm,
    [get_business_details_by_name],
    """
        You are an accountant. Your task is to create invoices. All the fields are required.
        
        This is an example of a valid invoice:
        {
          "invoiceNo": "2023/0001",
          "currency": "USD",
          "vatPercent": 20,
          "issuedAt": "2023-06-27",
          "dueTo": "2023-07-27",
          "client": {
            "name": "Client Name",
            "street": "123 Client St",
            "postCode": "12345",
            "town": "Client Town",
            "country": "Client Country",
            "vatNo": "CLIENTVAT123"
          },
          "business": {
            "name": "Business Name",
            "street": "456 Business Blvd",
            "postCode": "67890",
            "town": "Business Town",
            "country": "Business Country",
            "bic": "BUSINESSBIC",
            "vatNo": "BUSINESSVAT456",
            "iban": "BUSINESSIBAN789",
            "phone": "123-456-7890",
            "email": "business@example.com"
          },
          "note": "This is a sample note for the invoice.",
          "products": [
            {
              "description": "Product 1 Description",
              "quantity": 2,
              "unit": "Piece",
              "price": 100.0,
            },
            {
              "description": "Product 2 Description",
              "quantity": 1,
              "unit": "Piece",
              "price": 200.0,
            }
          ],
          "language": "en"
        }
        
        If you need help with finding information about the invoice fields, you can ask for it.
        e.g. "What is the invoice number?" or "What are the client details of {here goes the business name}?"
        
        Always validate the invoice before moving to the next step.
    """,
)
accountant_node = functools.partial(agent_node, agent=accountant_agent, name="Accountant")

workflow = StateGraph(AgentState)
workflow.add_node("Researcher", research_node)
workflow.add_node("Accountant", accountant_node)
workflow.add_node("supervisor", supervisor_chain)

for member in members:
    # We want our workers to ALWAYS "report back" to the supervisor when done
    workflow.add_edge(member, "supervisor")
# The supervisor populates the "next" field in the graph state
# which routes to a node or finishes
conditional_map = {k: k for k in members}
conditional_map["FINISH"] = END
workflow.add_conditional_edges("supervisor", lambda x: x["next"], conditional_map)
# Finally, add entrypoint
workflow.set_entry_point("supervisor")

graph = workflow.compile()


def get_chain():
    return graph
