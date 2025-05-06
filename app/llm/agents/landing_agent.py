from langchain.agents import create_tool_calling_agent, AgentExecutor
from app.llm.llm_services import llm_openai
from app.prompts.prompt import landing_page_prompt
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
import os
from langchain_unstructured import UnstructuredLoader
from pathlib import Path
from langchain.tools.retriever import create_retriever_tool

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
os.environ["OPENAI_API_KEY"]= os.getenv("OPENAI_API_KEY")



file_path = Path("uploads/context.pdf")
tools = []

if file_path.exists():
    print(f" File found: {file_path}. Enabling RAG.")

    loader = UnstructuredLoader(str(file_path))
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings()
    vector_store = FAISS.from_documents(texts, embeddings)
    vector_store.save_local("faiss_index")

    loaded_store = FAISS.load_local(
        "faiss_index",
        embeddings,
        allow_dangerous_deserialization=True 
    )

    retriever = loaded_store.as_retriever()
    rag_tool = create_retriever_tool(
        retriever,
        "document_retriever",
        "Searches uploaded documents for relevant information"
    )

    tools.append(rag_tool)
else:
    print(" No PDF found. RAG tool will not be included.")




custom_prompt = landing_page_prompt()

agent_init = create_tool_calling_agent(llm_openai, tools, custom_prompt)

land_agent= AgentExecutor(
    agent=agent_init,
    tools= tools,
    handle_parsing_errors=True,
    return_intermediate_steps=False,
    max_iterations=7,
    verbose= True

)