from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
from accelerate import init_empty_weights, load_checkpoint_and_dispatch
import torch
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

model_name="meta-llama/Meta-Llama-3-8B-Instruct"

logger.info(f"from_pretrained {model_name} ...")
tokenizer=AutoTokenizer.from_pretrained(model_name)

with init_empty_weights():
    # model = AutoModelForCausalLM.from_config(model_name)
    pass

model = load_checkpoint_and_dispatch(
    model,
    checkpoint=model_name,
    device_map="auto",
    offload_folder="offload"  # Folder where parts of the model will be offloaded to
)

terminators = [
    tokenizer.eos_token_id,
    tokenizer.convert_tokens_to_ids("<|eot_id|>")
]

logger.info("construct pipeline")
pipeline=pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    torch_dtype=torch.float16,
    # trust_remote_code=True,
    device_map="auto",
    # do_sample=True,
    # top_p=0.95, 
    # top_k=40, 
    max_new_tokens=256,
    eos_token_id=terminators,  # I already set the eos_token_id here, still no end for its self-coververstaion
    pad_token_id=tokenizer.eos_token_id,
    offload_folder="offload"
    )

logger.info("construct HuggingFacePipeline")
llm = HuggingFacePipeline(pipeline=pipeline, model_kwargs={"temperature": 0})


from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain.schema import AIMessage, HumanMessage
 
template = "Act as an experienced but grumpy high school teacher that teaches {subject}. Always give responses in one sentence with anger."
human_template = "{text}"
 
chat_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(template),
        HumanMessage(content="Hello teacher!"),
        AIMessage(content="Welcome everyone!"),
        HumanMessagePromptTemplate.from_template(human_template),
    ]
)
 
messages = chat_prompt.format_messages(
    subject="Artificial Intelligence", text="What is the most powerful AI model?"
)
print(messages)

result = llm.predict_messages(messages)
print(result.content)