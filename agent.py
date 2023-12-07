#  docker run -it -v ./:/app/ langchain_img python /app/agent.py

import getpass
import os, sys
import pandas as pd 

from langchain.vectorstores import Chroma
from langchain.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder

from langchain.chains.query_constructor.base import AttributeInfo
from langchain.llms import OpenAI
from langchain.retrievers.self_query.base import SelfQueryRetriever

from langchain import hub
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DataFrameLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema.messages import AIMessage, HumanMessage

import dotenv


def get_llm():
    return ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

def format_docs(docs):
    # return "\n\n".join(doc.page_content for doc in docs)
    return docs[0].page_content if docs else "no context"

def get_condense_q_chain(llm):
    condense_q_system_prompt = """Given a chat history and the latest user question \
    which might reference the chat history, formulate a standalone question \
    which can be understood without the chat history. Do NOT answer the question, \
    just reformulate it if needed and otherwise return it as is."""
    condense_q_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", condense_q_system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{question}"),
        ]
    )
    condense_q_chain = condense_q_prompt | llm | StrOutputParser()
    return condense_q_chain

def condense_question(input: dict):
    if input.get("chat_history"):
        return get_condense_q_chain(get_llm())
    else:
        return input["question"]

def main():
    
    dotenv.load_dotenv()

    # os.environ["LANGCHAIN_TRACING_V2"] = "true"
    # still beta not generally available.
    # os.environ["LANGCHAIN_API_KEY"] = LANGCHAIN_API_KEY

    df = pd.read_csv("resources/content.csv")
    df['page_content'] = "Title: " + df["title"] + "\n" + \
                        "Content: " + df["content"] + "\n" + \
                        "Source: " + df["source"]
    df = df[['page_content', 'source']]

    docs = DataFrameLoader(df, page_content_column='page_content').load()
    db = Chroma.from_documents(docs, OpenAIEmbeddings())
    retriever = db.as_retriever(search_type="similarity_score_threshold", search_kwargs={"k": 1, "score_threshold":.7})

    from langchain.agents.agent_toolkits import create_retriever_tool
    tool = create_retriever_tool(
        retriever,
        "internal_knowledge_resources",
        "Searches and returns documents from the internal knowledge resources.",
    )
    tools = [tool]

    from langchain.agents.agent_toolkits import create_conversational_retrieval_agent

    # This is needed for both the memory and the prompt
    memory_key = "history"
    from langchain.agents.openai_functions_agent.agent_token_buffer_memory import (
        AgentTokenBufferMemory,
    )

    # "This model's maximum context length is 4097 tokens
    memory = AgentTokenBufferMemory(memory_key=memory_key, llm=get_llm(), max_token_limit=4096)

    from langchain.agents.openai_functions_agent.base import OpenAIFunctionsAgent
    from langchain.prompts import MessagesPlaceholder
    from langchain.schema.messages import SystemMessage

    system_message = SystemMessage(
        content=(
            "Do your best to answer the questions. "
            "Feel free to use any tools available to look up "
            "relevant information when needed, ALWAYS return the \"Source:\" part in your answer if there is a \"Source:\" in the relevant information."
            "Use numbered list for steps, and don't miss any step."
            "If you don't know the answer, just say that you don't know. Don't try to make up an answer. "
        )
    )
    prompt = OpenAIFunctionsAgent.create_prompt(
        system_message=system_message,
        extra_prompt_messages=[MessagesPlaceholder(variable_name=memory_key)],
    )

    agent = OpenAIFunctionsAgent(llm=get_llm(), tools=tools, prompt=prompt)
    from langchain.agents import AgentExecutor
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        memory=memory,
        verbose=True,
        return_intermediate_steps=True,
    )

    # agent_executor = create_conversational_retrieval_agent(get_llm(), tools, verbose=True)

    question = ''
    while 'exit()' not in question:
        if question:
            result = agent_executor({"input": question})
            # print(result)
            # chat_history.extend([HumanMessage(content=question), answer])
        question = input("Your input:")

if __name__ == '__main__':
    main()