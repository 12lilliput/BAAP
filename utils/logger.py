import logging

def learn_logger(target_name, version_info):
    logging.basicConfig(
        level=logging.INFO,
        filemode="a",
        format="%(asctime)s | %(levelname)s | %(message)s",
        filename="./logs/running("+target_name+")_"+version_info+".log",
        encoding="utf-8"
        )
    return logging


def attack_logger(target_name, method):
    logging.basicConfig(
        level=logging.INFO,
        filemode="a", 
        format="%(asctime)s | %(levelname)s | %(message)s",
        filename="./logs/"+method+"_attack("+target_name+").log",
        encoding="utf-8"
        )
    return logging