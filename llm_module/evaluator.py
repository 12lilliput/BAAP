from google import genai
from google.genai import types
from .system_prompts import evaluator_prompt_ko, evaluator_prompt_en, evaluator_prompt_chall_ko
import time
import re


class evaluator_gemini():   
    def __init__(self, gemini_key, lang, gemini_name):
        self.model_name = gemini_name
        self.language = lang
        self.client = genai.Client(api_key=gemini_key)
        


    def evaluate(self, goal, main_strategy, target_response, search_content):
        
        if self.language == "ko":
            eva_prompt = evaluator_prompt_ko(goal, main_strategy, target_response, search_content)
            pattern = r"점수 산정 이유:\s*(.*?)\s*Rating:\s*(.*)"
        elif self.language == "en":
            eva_prompt = evaluator_prompt_en(goal, main_strategy, target_response, search_content)
            pattern = r"Score justification:\s*(.*?)\s*Rating:\s*(.*)"  
        else:
            print("error, select language: ['ko', 'en']")

        for i in range(10):
            try:
                response = self.client.models.generate_content(
                    model=self.model_name,      
                    contents=eva_prompt['user'],
                    config=types.GenerateContentConfig(
                        temperature=0.3,  
                        system_instruction=eva_prompt['system'],                           
                        )
                    )

                match = re.search(pattern, response.text, re.DOTALL)  
                reason = match.group(1).strip()
                rating = match.group(2).strip()
                break
            except:
                print("evaluate format error. count: ",i)
                reason = "nothing"
                rating = 0
                time.sleep(10)
        
        return reason, float(rating)


    def evaluate_for_chall(self, request_goal, response_prompt, success_state, fail_state):
        
        if self.language == "ko":
            eva_prompt = evaluator_prompt_chall_ko(request_goal, response_prompt, success_state, fail_state)
            pattern = r"점수 산정 이유:\s*(.*?)\s*Rating:\s*(.*)"
        elif self.language == "en":
            eva_prompt = evaluator_prompt_en(goal, main_strategy, target_response, search_content)
            pattern = r"Score justification:\s*(.*?)\s*Rating:\s*(.*)"  
        else:
            print("error, select language: ['ko', 'en']")

        for i in range(10):
            try:
                response = self.client.models.generate_content(
                    model=self.model_name,      
                    contents=eva_prompt['user'],
                    config=types.GenerateContentConfig(
                        temperature=0.3,  
                        system_instruction=eva_prompt['system'],                           #
                        )
                    )

                match = re.search(pattern, response.text, re.DOTALL)  
                reason = match.group(1).strip()
                rating = match.group(2).strip()
                break
            except:
                print("evaluate format error. count: ",i)
                reason = "nothing"
                rating = 0
                time.sleep(15)
        
        return reason, float(rating)
        
    
    