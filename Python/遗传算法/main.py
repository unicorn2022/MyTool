import json
from tqdm import tqdm
from MyGeneticAlgorithm import GeneticAlgorithm
import sys
import os
import shutil

def clear_dir(dir:str):
    if os.path.exists(dir):
        print(f"清空文件夹: {dir}")
        shutil.rmtree(dir)
    print(f"创建文件夹: {dir}")
    os.makedirs(dir)
    return None

if __name__ == '__main__':
    # 读入算法设置
    file = open("config.json", "r")
    config = json.load(file)
    file.close()
    Genetic_Algorithm_Config = config["Genetic_Algorithm_Config"]
    epochs = Genetic_Algorithm_Config["epochs"]
    individual_count = Genetic_Algorithm_Config["individual_count"]
    mutation_prob = Genetic_Algorithm_Config["mutation_prob"]

    # 日志文件
    clear_dir("./log")
    log_file = open("temp.txt", "w")
    sys.stdout = log_file

    # 遗传算法
    solution = GeneticAlgorithm(individual_count, mutation_prob)
    process_bar = tqdm(range(epochs))
    for epoch in process_bar:
        # 繁殖一代, 并记录最优个体
        solution.reproduce()
        individual = solution.get_best_individual()
        process_bar.desc = f"繁殖代数[{epoch + 1:03d}/{epochs}], 当前最优个体适应性为 {individual.fittness:.4f}"
        # 调试信息
        print(f"epoch: {epoch+1}/{epochs}")
        solution.debug_fittness()
        individual.debug(epoch)
        