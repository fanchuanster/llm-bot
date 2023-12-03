# from ubuntu:22.04
from python:3.8

RUN pip install -U langchain openai chromadb langchainhub bs4
RUN pip install -U pandas
RUN pip install -U tiktoken

# RUN pip install pysqlite3-binary

WORKDIR /app/

# ENTRYPOINT [ "python /app/agent.py" ]