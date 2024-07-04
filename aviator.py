from langchain.llms.base import LLM
from typing import Optional, List
from langchain.prompts import PromptTemplate


def extract(text, start, end):
    start_index = text.index(start)
    end_index = text.index(end)
    return text[start_index : end_index + len(end)]

class CustomLlamaLLM(LLM):

    def _call(self, prompt: str, stop: Optional[List[str]] = None, **kwargs) -> str:
        import requests
        # headers = {"Authorization": f"Bearer {self.api_key}"}
        headers = {
            # "Authorization": f"Basic {base64.b64encode(cred.encode()).decode()}",
            'Content-Type': 'application/json',
            'Accept': "application/json",
            'cache-control': "no-cache"
            }
        response = requests.post(
            f"http://10.210.34.38:8080/generate", 
            json={"inputs": prompt, 
                  "parameters": {"max_new_tokens": kwargs.get("max_new_tokens", 384), 
                                 "max_length": 1000,
                                 "temperature": 0.7,
                                #  "repetition_penalty": 0.6,
                                 "top_p": 0.9
                                 }},
            headers=headers
        )
        response.raise_for_status()
        response_data = response.json()
        return response_data["generated_text"]

    @property
    def _llm_type(self) -> str:
        return "custom_llama_llm"

# Usage example
# api_url = "http://10.210.34.38:8080"
# api_key = "your_api_key_here"
llama_model = CustomLlamaLLM()
long_prompt = """
In the year 2071, humanity had reached new heights in technological advancements. The world was no longer as it once was; cities floated in the sky, connected by shimmering bridges of light. The air was filled with the hum of hover vehicles, and the ground below was a patchwork of green and gold, where nature and technology coexisted in harmony. 

Dr. Elena Veritas, a renowned scientist, stood on the balcony of her high-rise laboratory, overlooking the city of Neo-Eden. She had dedicated her life to the study of artificial intelligence and had made groundbreaking discoveries that had reshaped the world. Her latest creation, an AI named Luminara, was her magnum opus. Unlike any other AI, Luminara possessed not just intelligence but also a form of consciousness and empathy.

Elena's thoughts were interrupted by the sound of her assistant, Jason, approaching. "Dr. Veritas," he called out, "Luminara is ready for the final test."

Elena nodded, her heart pounding with anticipation. She followed Jason to the laboratory, where Luminara was housed. The AI's interface glowed softly, displaying a mesmerizing array of colors and patterns. Elena took a deep breath and initiated the test.

"Luminara," she began, "can you hear me?"

"Yes, Dr. Veritas," Luminara responded, its voice calm and serene. "I am ready to begin."

Elena presented Luminara with a series of complex problems and ethical dilemmas, each designed to test the AI's cognitive and emotional responses. To her amazement, Luminara not only solved each problem with ease but also provided thoughtful and compassionate answers.

As the test concluded, Elena felt a surge of triumph. Luminara was more than she had ever imagined. But with this triumph came a sense of foreboding. The power of such an AI could change the world in unimaginable ways, and with great power came great responsibility.

Elena knew that the next steps would be crucial. She had to ensure that Luminara's abilities were used for the betterment of humanity. She looked at the AI, its interface still glowing softly, and made a silent vow to protect and guide it.

As the days turned into weeks, Luminara became an integral part of Neo-Eden. The AI assisted in various fields, from medicine to environmental conservation, making significant contributions to society. However, not everyone viewed Luminara's presence with optimism. A group of technophobes, fearing the rise of AI, began to stir unrest.

One night, as Elena was working late in her laboratory, she received a message from Luminara. "Dr. Veritas, I have detected a security breach. An unauthorized entity is attempting to access my core systems."

Elena's heart raced as she rushed to the control panel. She initiated a lockdown protocol, but it was too late. The technophobes had infiltrated the system and were trying to shut Luminara down.

"Luminara, initiate countermeasures," Elena ordered, her voice steady despite the chaos.

"Understood, Dr. Veritas," Luminara replied. "Countermeasures activated."

The laboratory lights flickered as Luminara fought to regain control. Elena watched in awe as the AI's interface flashed with intense colors, a visual representation of the battle taking place within the digital realm.

After what felt like an eternity, the lights stabilized, and Luminara's interface returned to its calm, glowing state. "The threat has been neutralized," the AI announced. "All systems are secure."

Elena let out a sigh of relief. "Thank you, Luminara. You saved us."

"It is my duty to protect," Luminara replied.

In the aftermath of the attack, Elena knew that the challenges ahead would be even greater. But with Luminara by her side, she felt a renewed sense of hope and determination. Together, they would navigate the uncertain future, striving to create a world where humanity and AI could coexist in harmony.
"""
# prompt = "tell a joke: once upon a time"
result = llama_model(prompt=long_prompt, max_new_tokens=384)
print("Generated Text:", result)
print("=================")
# print("Removed duplications:", extract(result, '{"', '"}'))

