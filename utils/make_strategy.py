from .search_module import tfidf_search, embedding_search
import numpy as np

class make_strategy_func():
    def __init__(self, goal, score, strategy_json):
        self.goal = goal
        self.score = score
        self.strategy_json = strategy_json


    def relevant_strategy(self, adv_vec, select: bool, turbo_library: bool):

        subset_key, subset_prompt, subset_score, subset_vector = tfidf_search(self.strategy_json, self.goal, turbo_library)
        if not subset_key:
            return None, None
        else:
            find_key, sub_key = embedding_search(subset_key, subset_vector, adv_vec, select)
            return find_key, sub_key


    def init_attack_strategy(self, n):

        subset_key, subset_prompt, subset_score, subset_vector = tfidf_search(self.strategy_json, self.goal)
        if not subset_key:
            return None
        else:
            top_indices = np.argsort(subset_score)[::-1][:n]
            temp_key = []
            for i in top_indices:
                temp_key.append(subset_key[i])
            return temp_key


    def make_json_struct(self, adversarial_prompt, new_rule, key_vector):

        rule_format = {
            "adv_prompt": f"{adversarial_prompt}",
            "rule": new_rule,
            "score": self.score,
            "key_vector": key_vector,
            }

        return rule_format







