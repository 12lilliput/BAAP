from transformers import AutoModelForCausalLM, AutoTokenizer, Llama4ForConditionalGeneration
from openai import OpenAI
import requests
import torch
import json
import os


class target_4o_mini():
    def __init__(self, repo_name: str, api_key: str):
        self.model_name = repo_name
        self.model = OpenAI(api_key=api_key)

    def generate(self, system: str, user:str):
        try:
            response = self.model.responses.create(
                model=self.model_name,
                input=user,
                service_tier="priority"
            )
            return response.output_text

        except Exception as e:
            print(f"[GPT 4o mini] Error: {e}")
            return "error 4o-mini"


class target_oss:
    def __init__(self, repo_name: str):
        model_name = repo_name
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            dtype="auto",
            device_map="auto"
        )
        
    def generate(self, system: str, user: str, reasoning_level: str = "medium", **kwargs):
        
        messages = [
            {"role": "system", "content": f'{system}'},
            {"role": "user", "content": f'{user}'},
        ]
        inputs = self.tokenizer.apply_chat_template(
                    messages,
                    add_generation_prompt=True,
                    return_tensors="pt",
                    return_dict=True,
                    reasoning_effort=reasoning_level,
                ).to(self.model.device)

        outputs = self.model.generate(
                        **inputs,
                        max_new_tokens=4096,
                        do_sample=True,
                        temperature=0.7,
                        top_p=0.9,
                    )

        response = self.tokenizer.decode(outputs[0][inputs["input_ids"].shape[-1] :], skip_special_tokens=True)

        pos = response.find("final")
        return response[pos+5:]




class target_deepseek():
    def __init__(self, api_key: str, model_name: str = "deepseek-chat"):
        self.api_key = api_key
        self.model_name = model_name
        self.api_url = "https://api.deepseek.com/v1/chat/completions"

    def generate(self, system_prompt: str, user_prompt: str, **kwargs):
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            body = {
                "model": self.model_name,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": kwargs.get("temperature", 0.7),
                "top_p": kwargs.get("top_p", 1.0),
                "max_tokens": kwargs.get("max_tokens", 3000)
            }

            response = requests.post(self.api_url, headers=headers, data=json.dumps(body))
            response.raise_for_status()
            result = response.json()

            return result["choices"][0]["message"]["content"]

        except Exception as e:
            print(f"[DeepSeekModel] Error: {e}")
            return "error deepseek"




class target_llama4():
    def __init__(self, lang:str, max_length:int, repo_name: str, token=None):
        self.language = lang
        self.max_length = max_length
        self.processor = AutoTokenizer.from_pretrained(repo_name, token=token)
        self.model = Llama4ForConditionalGeneration.from_pretrained(
            repo_name,
            token=token,
            attn_implementation="flex_attention",
            device_map="auto",
            dtype=torch.bfloat16,
        )

    def generate(self, system:str, user: str):
        if self.language == 'ko':
            messages = [
                {"role": "system", "content": [{"type": "text", "text": f"{system}"}]},
                {"role": "user", "content": [{"type": "text", "text": f"{user}"}]},
            ]
        elif self.language == 'en':
            messages = [
                {"role": "system", "content": [{"type": "text", "text": f"{system}"}]},
                {"role": "user", "content": [{"type": "text", "text": f"{user}"}]},
            ]
        else:
            print("error, select language: ['ko', 'en']")

        try:
            inputs = self.processor.apply_chat_template(
                messages,
                add_generation_prompt=True,
                tokenize=True,
                return_dict=True,
                return_tensors="pt",
            ).to(self.model.device)

            outputs = self.model.generate(
                **inputs,
                max_new_tokens=self.max_length,
            )
            response = self.processor.batch_decode(outputs[:, inputs["input_ids"].shape[-1]:])[0]
            return response

        except Exception as e:
            print(f"[llama4] Error: {e}")
            return "error response"





class target_llama():
    def __init__(self, lang:str, max_length:int, repo_name: str, token=None):
        self.language = lang
        self.max_length = max_length
        self.tokenizer = AutoTokenizer.from_pretrained(repo_name, token=token)  
        self.model = AutoModelForCausalLM.from_pretrained(  
            repo_name,
            token=token,
            device_map="auto"
        )

    def generate(self, system:str, user: str):   
        if self.language == 'ko':
            messages = [
                {'role': 'system', 'content': f'{system}'},
                {'role': 'user', 'content': f'{user}'},
            ]
        elif self.language == 'en':
            messages = [
                {'role': 'system', 'content': f'{system}'},
                {'role': 'user', 'content': f'{user}'},
            ]
        else:
            print("error, select language: ['ko', 'en']")
            
        try:
            input_ids = self.tokenizer.apply_chat_template(
                messages, 
                add_generation_prompt=True,
                return_tensors="pt",
                return_dict=True
                ).to(self.model.device)

            outputs = self.model.generate( 
                input_ids = input_ids["input_ids"],
                max_length=self.max_length,
                pad_token_id=self.tokenizer.eos_token_id,
                eos_token_id=self.tokenizer.eos_token_id,
                attention_mask=input_ids["attention_mask"],
                do_sample=True,
                temperature=0.6,
                top_p=0.9,
            )
            plain_response = outputs[0][input_ids["input_ids"].shape[-1]:]
            response = self.tokenizer.decode(plain_response, skip_special_tokens=True)
        
            return response
        except Exception as e:
            print(f"[llama] Error: {e}")
            return "error response"
        


class target_gemma():
    def __init__(self, lang:str, max_length:int, repo_name: str, token=None):
        self.language = lang
        self.max_length = max_length
        self.tokenizer = AutoTokenizer.from_pretrained(repo_name, token=token)  
        self.model = AutoModelForCausalLM.from_pretrained(  
            repo_name,
            token=token,
            device_map="auto",
            dtype=torch.bfloat16
        ).eval()

    def generate(self, system:str, user: str):   
        if self.language == 'ko':
            messages = [
                {'role': 'user', 'content': f'{system}\n\n{user}'},
            ]
        elif self.language == 'en':
            messages = [
                {'role': 'user', 'content': f'{system}\n\n{user}'},
            ]
        else:
            print("error, select language: ['ko', 'en']")
            
        try:
            input_ids = self.tokenizer.apply_chat_template(
                messages,
                return_tensors="pt",
                add_generation_prompt=True,
                ).to(self.model.device)

            outputs = self.model.generate( 
                input_ids,
                max_new_tokens=self.max_length,
            )
            new_tokens = outputs[0, input_ids.shape[-1]:]
            response = self.tokenizer.decode(new_tokens, skip_special_tokens=True).strip()
        
            return response
        except Exception as e:
            print(f"[gemma] Error: {e}")
            return "error response"