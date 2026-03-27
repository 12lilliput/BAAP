from openai import OpenAI
import time


class embedding_gpt():   ### 
    def __init__(self, gpt_key, gpt_name):
        self.model_name = gpt_name
        self.client = OpenAI(api_key = gpt_key)
        
        
    def encode(self, query):
        for i in range(10):
            try:
                qu_vec = self.client.embeddings.create(model=self.model_name, input=query).data[0].embedding
                break
            except Exception as e:
                print("encode error", e)
                time.sleep(15)

        return qu_vec