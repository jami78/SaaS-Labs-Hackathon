from app.prompts.prompt import data_prompt
from app.llm.agents.pricing_agent import pricing_agent
from app.pydantic.structured_outputs import FinanceSpec
from app.llm.llm_services import llm_openai
from app.prompts.prompt import finance_prompt
from langchain.schema import SystemMessage, HumanMessage
from app.llm.agents.state import FinanceState
from app.llm.agents.data_analyst import data_agent
from langgraph.graph import StateGraph, END
from app.core.checkpointer import checkpointer

def content_function(state:FinanceState)-> str:
    input= state["user_input"]
    content= llm_openai.with_structured_output(FinanceSpec)
    response = content.invoke([
    SystemMessage(content=finance_prompt()),
    HumanMessage(content=input)])
    return {"competitor_price": response.competitor_price,
            "cost_structure":response.cost_structure,
            "target_customer": response.target_customer,
            "function": response.function
    }

def route_by_function(state: FinanceState) -> str:
    func = state.get("function", "").lower()
    if "pricing" in func:
        return "price_function"
    elif "finance" in func:
        return "analysis_function"
    elif "data" in func:
        return "analysis_function"
    else:
        return "unknown"

def price_function(state: FinanceState)-> FinanceState:
    response = pricing_agent.invoke({
        "cost_structure":state["cost_structure"],
        "competitor_price": state["competitor_price"],
        "target_customer": state['target_customer']
    })
    return {"messages":response["output"]}

def analysis_function(state:FinanceState)-> FinanceState:
    query = data_prompt()
    response= data_agent.invoke(query, handle_parsing_error=True)
    return {"messages":response["output"]}

graph = StateGraph(FinanceState)

graph.add_node("content_function", content_function)
graph.add_node("price_function", price_function)
graph.add_node("analysis_function", analysis_function)

graph.set_entry_point("content_function")

graph.add_conditional_edges(
    "content_function",
    route_by_function,
    {
        "price_function": "price_function",
        "analysis_function": "analysis_function",
        "unknown": END
    }
)

graph.add_edge("price_function", END)
graph.add_edge("analysis_function", END)
checkpointer.setup()
workflow= graph.compile(checkpointer=checkpointer)