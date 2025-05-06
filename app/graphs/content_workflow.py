import os
import markdown
from app.llm.agents.landing_agent import land_agent
from app.llm.agents.ad_agent import ad_agent
from app.llm.agents.seo_agent import seo_agent
from app.pydantic.structured_outputs import ContentSpec, KeywordList
from app.llm.llm_services import llm_openai
from app.prompts.prompt import content_prompt
from langchain.schema import SystemMessage, HumanMessage
from app.llm.agents.state import ContentState
from pytrends.request import TrendReq
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import InMemorySaver
from app.prompts.prompt import keyword_prompt
from app.core.checkpointer import checkpointer


pytrend = TrendReq(hl='en-US', tz=360)

def content_function(state:ContentState)-> ContentState:
    input= state["user_input"]
    content= llm_openai.with_structured_output(ContentSpec)
    response = content.invoke([
    SystemMessage(content=content_prompt()),
    HumanMessage(content=input)])
    return {"persona": response.persona_profile,
            "target": response.target_channel,
            "position": response.positioning_kit,
            "function": response.function
    }

def route_by_function(state: ContentState) -> str:
    func = state.get("function", "").lower()
    if "landing" in func:
        return "landing_page"
    elif "seo" in func:
        return "seo"
    elif "ad" in func:
        return "ad_copy"
    else:
        return "unknown"
    
def generate_landing_page(state:ContentState, output_path: str = "output/landing_page.html") -> str:
    response = land_agent.invoke({
        "position": state["position"],
        "target": state["target"],
        "persona": state["persona"]
    })
            # md_content = response["output"]

            # html_body = markdown.markdown(md_content, extensions=['fenced_code', 'tables'])
            # full_html = f"""
            # <!DOCTYPE html>
            # <html lang="en">
            # <head>
            #     <meta charset="UTF-8">
            #     <title>Generated Landing Page</title>
            #     <style>
            #         body {{ font-family: Arial, sans-serif; margin: 40px; }}
            #         h1, h2, h3 {{ color: #333; }}
            #         a.button {{ display: inline-block; padding: 10px 20px; background: #007bff; color: white; text-decoration: none; border-radius: 5px; }}
            #     </style>
            # </head>
            # <body>
            #     {html_body}
            # </body>
            # </html>
            # """


            # os.makedirs(os.path.dirname(output_path), exist_ok=True)
            # with open(output_path, "w", encoding="utf-8") as f:
            #     f.write(full_html)

            # print(f" Landing page saved to {output_path}")
    return {"messages":response["output"]}


def generate_ad(state:ContentState)-> ContentState:
    response = ad_agent.invoke({
        "position": state["position"],
        "target": state["target"],
        "persona": state["persona"]
    })
    return {"messages":response["output"]}

def generate_seo(state: ContentState) -> ContentState:
    llm = llm_openai.with_structured_output(KeywordList)
    prompt = keyword_prompt(
        position=state["position"],
        target=state["target"],
        persona=state["persona"]
    )
    response = llm.invoke([HumanMessage(content=prompt)])
    keywords = response.keywords
    all_titles = []
    for keyword in keywords:
        suggestions = pytrend.suggestions(keyword)
        all_titles.extend([k["title"] for k in suggestions if "title" in k])
    keywords_str = "\n".join(f"- {title}" for title in all_titles)
    print(keywords_str)
    response = seo_agent.invoke({
        "position": state["position"],
        "target": state["target"],
        "persona": state["persona"],
        "keywords": keywords_str
    })
    return {"messages":response["output"]}


graph = StateGraph(ContentState)

graph.add_node("content", content_function)
graph.add_node("landing_page", generate_landing_page)
graph.add_node("seo", generate_seo)
graph.add_node("ad_copy", generate_ad)

graph.set_entry_point("content")

graph.add_conditional_edges(
    "content",
    route_by_function,
    {
        "landing_page": "landing_page",
        "seo": "seo",
        "ad_copy": "ad_copy",
        "unknown": END
    }
)

graph.add_edge("landing_page", END)
graph.add_edge("seo", END)
graph.add_edge("ad_copy", END)
#checkpointer = InMemorySaver()
checkpointer.setup()
workflow = graph.compile(checkpointer=checkpointer)