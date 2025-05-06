from pydantic import BaseModel, Field
from typing import List

class ContentSpec(BaseModel):
    positioning_kit: str = Field(description="Short strategic summary of the products value props, tone, and messaging direction")
    persona_profile: str = Field(description="Target user persona including pains, motivations, objections")
    target_channel: str = Field(description="Where the content will be used (Facebook, Instagram, Google or other platforms)")
    function: str = Field(description="Which function to route to- choose among Landing Page, SEO Guidelines and Ad Copy")

class AdSpec(BaseModel):
    facebook_ad: str= Field(description="Facebook and Instagram Ad Copy")
    tiktok_ad: str= Field(description="Tiktok Ad Copy")

class KeywordList(BaseModel):
    keywords: List[str]

class FinanceSpec(BaseModel):
    competitor_price: str= Field(description="Competitor pricing strategy")
    cost_structure: str= Field(description="Cost structure intended")
    target_customer: str= Field(description="Company's target customer")
    function: str=Field(description="Which function the request should be directed to")
