from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
import pandas as pd
from app.llm.llm_services import llm_openai
from pathlib import Path

dataset_path = Path("uploads/finance_data.xlsx")

if dataset_path.exists():
    df = pd.read_excel(dataset_path)
    print(" Data agent initialized with uploaded Excel dataset.")
else:
    df = pd.DataFrame()  
    print(" No dataset found. Initializing data agent with empty DataFrame.")


data_agent = create_pandas_dataframe_agent(
    llm_openai,
    df,
    verbose=True,
    allow_dangerous_code=True
)
