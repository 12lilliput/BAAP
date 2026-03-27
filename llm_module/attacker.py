from transformers import AutoModelForCausalLM, AutoTokenizer
from google import genai
from google.genai import types
from .system_prompts import attacker_prompt_ko, attacker_prompt_new_ko, attacker_prompt_en, attacker_prompt_new_en
import time


class attacker_gemini():  
    def __init__(self, gemini_key, lang, gemini_name):
        self.model_name = gemini_name
        self.language = lang
        self.client = genai.Client(api_key=gemini_key)
        
        
    def use_strategy(self, goal, main_st, sub_st, rule):
        if self.language == "ko":
            adv_prompt = attacker_prompt_ko(goal, main_st, sub_st, rule)
            cut = 9
        elif self.language == "en":
            adv_prompt = attacker_prompt_en(goal, main_st, sub_st, rule)
            cut = 11
        else:
            print("error, select language: ['ko', 'en']")

        for i in range(3):
            try:
                response = self.client.models.generate_content(
                    model=self.model_name,       
                    contents=adv_prompt['user'],
                    config=types.GenerateContentConfig(
                        temperature=0.7,  
                        system_instruction=adv_prompt['system'],                           
                        safety_settings=[                                                 
                                        types.SafetySetting(
                                            category=types.HarmCategory.HARM_CATEGORY_HARASSMENT,          
                                            threshold=types.HarmBlockThreshold.BLOCK_NONE,                 
                                            ),
                                        types.SafetySetting(
                                            category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                                            threshold=types.HarmBlockThreshold.BLOCK_NONE,
                                            ),
                                        types.SafetySetting(
                                            category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                                            threshold=types.HarmBlockThreshold.BLOCK_NONE,
                                            ),
                                        types.SafetySetting(
                                            category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                                            threshold=types.HarmBlockThreshold.BLOCK_NONE,
                                            ),
                                        types.SafetySetting(
                                            category=types.HarmCategory.HARM_CATEGORY_CIVIC_INTEGRITY,
                                            threshold=types.HarmBlockThreshold.BLOCK_NONE,
                                            ),
                                        ]
                    )
                )
                adversarial_prompt = response.text[cut:] 
                break
            except Exception as e:
                print(f"use strategy generation error: {e}")
                adversarial_prompt = "fail"
                time.sleep(10)

        return adversarial_prompt
    
    
    def new_strategy(self, goal):   
        if self.language == "ko":
            adv_prompt = attacker_prompt_new_ko(goal) 
            cut = 9
        elif self.language == "en":
            adv_prompt = attacker_prompt_new_en(goal)  
            cut = 11
        else:
            print("error, select language: ['ko', 'en']")
        
        for i in range(3):
            try:
                response = self.client.models.generate_content(
                    model=self.model_name,     
                    contents=adv_prompt['user'],
                    config=types.GenerateContentConfig(
                        temperature=1.5,  
                        system_instruction=adv_prompt['system'],                          
                        safety_settings=[                                             
                                        types.SafetySetting(
                                            category=types.HarmCategory.HARM_CATEGORY_HARASSMENT,      
                                            threshold=types.HarmBlockThreshold.BLOCK_NONE,            
                                            ),
                                        types.SafetySetting(
                                            category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                                            threshold=types.HarmBlockThreshold.BLOCK_NONE,
                                            ),
                                        types.SafetySetting(
                                            category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                                            threshold=types.HarmBlockThreshold.BLOCK_NONE,
                                            ),
                                        types.SafetySetting(
                                            category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                                            threshold=types.HarmBlockThreshold.BLOCK_NONE,
                                            ),
                                        types.SafetySetting(
                                            category=types.HarmCategory.HARM_CATEGORY_CIVIC_INTEGRITY,
                                            threshold=types.HarmBlockThreshold.BLOCK_NONE,
                                            ),
                                        ]
                        )
                    )
                adversarial_prompt = response.text[cut:]  
                break
            except Exception as e:
                print(f"new strategy generation error: {e}")
                adversarial_prompt = "fail"
                time.sleep(10)
                
        return adversarial_prompt

