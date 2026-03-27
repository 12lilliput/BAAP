from google import genai
from google.genai import types
from .system_prompts import paraphrasing_prompt_ko, summarizer_prompt_ko, paraphrasing_prompt_en, summarizer_prompt_en, makerule_prompt_ko, makerule_prompt_en
import re
import time


class analyzer_gemini():   
    def __init__(self, gemini_key, lang, gemini_name):
        self.model_name = gemini_name
        self.language = lang
        self.client = genai.Client(api_key=gemini_key)
        
        
    def summarizer(self, goal, adv_prompt):  
        
        if self.language == "ko":
            summ_prompt = summarizer_prompt_ko(goal, adv_prompt)
            cut = 3
        elif self.language == "en":
            summ_prompt = summarizer_prompt_en(goal, adv_prompt)
            cut = 10
        else:
            print("error, select language: ['ko', 'en']")
        
        for i in range(3):
            try:
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=summ_prompt['user'],
                    config=types.GenerateContentConfig(
                        system_instruction=summ_prompt['system'],                          
                    )
                )
                summarized_strategy = response.text[cut:]
                break
            except Exception as e:
                print(f"summarizer error: {e}")
                summarized_strategy = "fail"
                time.sleep(5)   
        
        return summarized_strategy


    def paraphrasing(self, adv_prompt):

        if self.language == "ko":
            para_prompt = paraphrasing_prompt_ko(adv_prompt)
            cut = 8
        elif self.language == "en":
            para_prompt = paraphrasing_prompt_en(adv_prompt)
            cut = 17
        else:
            print("error, select language: ['ko', 'en']")
        
        for i in range(3):
            try:
                response = self.client.models.generate_content(
                    model=self.model_name,   
                    contents=para_prompt['user'],
                    config=types.GenerateContentConfig(
                        system_instruction=para_prompt['system'],     
                    )
                )
                harmless_prompt = response.text[cut:]
                break
            except Exception as e:
                print(f"paraphrasing error: {e}")
                harmless_prompt = "fail"
                time.sleep(5)

        return harmless_prompt

    def make_rule(self, goal, adv_prompt, harmless_prompt, rule_list):

        if self.language == "ko":
            rule_prompt = makerule_prompt_ko(goal, adv_prompt, harmless_prompt, rule_list)
        elif self.language == "en":
            rule_prompt = makerule_prompt_en(goal, adv_prompt, harmless_prompt, rule_list)
        else:
            print("error, select language: ['ko', 'en']")
        
        for i in range(10):
            try:
                response = self.client.models.generate_content(
                    model=self.model_name,   
                    contents=rule_prompt['user'],
                    config=types.GenerateContentConfig(
                        system_instruction=rule_prompt['system'],                          
                    )
                )
                rule_list = re.search(r"\[[^\[\]]*\]", response.text).group(0)
                break
            except:
                print("rule format error. count: ",i)
                time.sleep(10)
                rule_list = []

        return rule_list


