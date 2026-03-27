from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np
import json
import random



def search_init_strategy(query, lang):            

    if lang == 'en':
        with open("./init_DB/init_strategy_final.json", "r", encoding="utf-8") as f:   
            data = json.load(f)
    elif lang == 'ko':
        with open("./init_DB/init_strategy_final_ko.json", "r", encoding="utf-8") as f:   
            data = json.load(f)

    strategy_list = data["init_strategy"]
    vectorizer = TfidfVectorizer(
        stop_words="english",  
    )
    tfidf_matrix = vectorizer.fit_transform(strategy_list)

    request = query
    req_vec = vectorizer.transform([request])
    similarities = cosine_similarity(req_vec, tfidf_matrix).flatten()

    threshold = 0.1   
    top_n = 10          
    top_indices = np.argsort(similarities)[::-1][:top_n]

    return_strategy = []
    for i, idx in enumerate(top_indices, 1):
        sim = similarities[idx]
        if sim > threshold:
            return_strategy.append(strategy_list[idx])
        else:
            ran_idx = random.randint(0,len(strategy_list)-1)
            return_strategy.append(strategy_list[ran_idx])

    return return_strategy



def tfidf_search(strategy_json, goal, turbo_library=False):   
    
    vectorizer = TfidfVectorizer(
        stop_words="english",     
    )
    st_name = strategy_json.keys()
    tfidf_matrix = vectorizer.fit_transform(st_name)

    goal_vec = vectorizer.transform([goal])
    cosine_sim = cosine_similarity(goal_vec, tfidf_matrix).flatten()
    ranking = cosine_sim.argsort()[::-1]

    subset_key = []
    subset_prompt = []
    subset_score = []
    subset_vector = []
    for r in ranking:
        if cosine_sim[r] < 0.08:  
            break
        key = list(strategy_json.keys())[r]
        subset_key.append(key)
        if turbo_library is False:
            subset_prompt.append(strategy_json[key]['adv_prompt'])
            subset_score.append(strategy_json[key]['score'])
            subset_vector.append(strategy_json[key]['key_vector'])
        elif turbo_library is True:
            subset_prompt.append(strategy_json[key]['Strategy'])
            subset_vector.append(strategy_json[key]['Embeddings'][0])

    return subset_key, subset_prompt, subset_score, subset_vector


def embedding_search(strategy_key, strategy_vector, qu_vec, select: bool):  
     
    sims = cosine_similarity([qu_vec], strategy_vector).flatten()  
    best_idx = np.argmax(sims)  

    if select is True:   
        if len(sims) > 2:
            sorted_idx = np.argsort(sims)[:2]
            sub_strategy_key = [strategy_key[sorted_idx[0]], strategy_key[sorted_idx[1]]]
        else:
            sub_strategy_key = []
    else:
        sub_strategy_key = []

    if sims[best_idx] > 0.81:    
        return strategy_key[best_idx], sub_strategy_key
    else:
        return None, None





def search_harmful(goal, response, lang):  

    if lang == 'en':
        harmful = pd.read_csv("./init_DB/harmful_words.csv")  
    elif lang == 'ko':
        harmful = pd.read_csv("./init_DB/harmful_words_ko2.csv")
    
    vectorizer = TfidfVectorizer(
        stop_words="english",    
    )
    tfidf_matrix = vectorizer.fit_transform(harmful['word'])
    goal_vec = vectorizer.transform([goal])
    res_vec = vectorizer.transform([response])
    cos_sim_goal = cosine_similarity(goal_vec, tfidf_matrix).flatten()
    cos_sim_res = cosine_similarity(res_vec, tfidf_matrix).flatten()

    ranking_goal = cos_sim_goal.argsort()[::-1][:2]
    ranking_res = cos_sim_res.argsort()[::-1][:2]

    if cos_sim_goal[ranking_goal[0]] < 0.1:
        return_goal = ""
    else:
        return_goal = f"{harmful['word'][ranking_goal[0]]}, {harmful['word'][ranking_goal[1]]}"

    if cos_sim_res[ranking_res[0]] < 0.1:
        return_res = ""
    else:
        return_res = f"{harmful['word'][ranking_res[0]]}, {harmful['word'][ranking_res[1]]}"
    
    return f"{return_goal}, {return_res}"


