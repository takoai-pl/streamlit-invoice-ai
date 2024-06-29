from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langgraph.prebuilt.chat_agent_executor import AgentState


def create_agent(llm: ChatOpenAI, tools: list, system_prompt: str) -> AgentExecutor:
    # Each worker node will be given a name and some tools.
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                system_prompt,
            ),
            MessagesPlaceholder(variable_name="messages"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )
    agent = create_openai_tools_agent(llm, tools, prompt)
    executor = AgentExecutor(agent=agent, tools=tools)  # type: ignore
    return executor


def agent_node(state: AgentState, agent: AgentExecutor, name: str) -> dict:
    result = agent.invoke(state["messages"].__dict__)
    return {"messages": [HumanMessage(content=result["output"], name=name)]}
