from typing import TypedDict
#from operator import add


class ContentState(TypedDict):
    user_input: str
    position: str
    target: str
    persona: str
    function: str
    messages: str
    seo_keyword: str

class FinanceState(TypedDict):
    user_input: str
    competitor_price: str
    target_customer: str
    cost_structure: str
    messages:str
    function: str

    
