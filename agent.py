
import getpass
import os, sys
import pandas as pd 

from langchain.embeddings import OpenAIEmbeddings
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

def main(argv):
    os.environ["OPENAI_API_KEY"] = argv[0]

    # os.environ["LANGCHAIN_TRACING_V2"] = "true"
    # still beta not generally available.
    # os.environ["LANGCHAIN_API_KEY"] = LANGCHAIN_API_KEY

    df = pd.read_csv("resources/content.csv")
    df['page_content'] = "Title: " + df["title"] + "\n" + \
                        "Content: " + df["content"] + "\n" + \
                        "Source: " + df["source"]

    docs = DataFrameLoader(df, page_content_column='page_content').load()
    db = Chroma.from_documents(docs, OpenAIEmbeddings())
    retriever = db.as_retriever(search_type="similarity_score_threshold", search_kwargs={"k": 2, "score_threshold":.18})

    prompt = PromptTemplate.from_template("""Given the following extracted parts of a RnD internal knowledge database and a question, create a final answer with the knowledge document link as source ("SOURCE").
        If you don't know the answer, just say that you don't know. Don't try to make up an answer. ALWAYS return a "SOURCE" part in your answer.
        Use numbered list whenever possible
        Question: {question} 
        Context: {context}
        Answer:""")

    rag_chain = (
        RunnablePassthrough.assign(context=condense_question | retriever | format_docs)
        | prompt
        | get_llm()
        | StrOutputParser())

    chat_history = []
    question = ''
    while 'exit()' not in question:
        if question:
            answer = rag_chain.invoke({"question": question, "chat_history": chat_history})
            print("answer:", answer)
            # chat_history.extend([HumanMessage(content=question), answer])
        question = input("Input your question ('exit()' to exit):")

if __name__ == '__main__':
    main(sys.argv[1:])