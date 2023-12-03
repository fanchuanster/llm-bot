
import getpass
import os, sys
import pandas as pd 

from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma

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


os.environ["OPENAI_API_KEY"] = sys.argv[1]

# os.environ["LANGCHAIN_TRACING_V2"] = "true"
# still beta not generally available.
# os.environ["LANGCHAIN_API_KEY"] = LANGCHAIN_API_KEY

df = pd.read_csv("resources/content.csv")
df['page_content'] = "Title: " + df["title"] + "\n" + \
                     "Content: " + df["content"] + "\n" + \
                     "Source: " + df["source"]

docs = DataFrameLoader(df, page_content_column='page_content').load()

db = Chroma.from_documents(docs, OpenAIEmbeddings())

retriever = db.as_retriever(search_type="similarity_score_threshold", search_kwargs={"k": 2, "score_threshold":.19})

question = "how to modify the timezone of an ALM server?"

# retrieved_docs = retriever.get_relevant_documents(
#     question
# )
# print("retrieved_docs:", len(retrieved_docs), retrieved_docs[0].page_content)

prompt = hub.pull("rlm/rag-prompt")
print(
    prompt.invoke(
        {"context": "filler context", "question": "filler question"}
    ).to_string()
)

llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs) + "." + \
            "\n" + "Add the Source link in the end of the answer, and use numbered list if possible"

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

print(rag_chain.invoke(question))