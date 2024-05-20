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
    clear_dir("./log")
    file = open("config.json", "r")
    config = json.load(file)
    file.close()

    log_file = open("temp.txt", "w")
    sys.stdout = log_file

    Genetic_Algorithm_Config = config["Genetic_Algorithm_Config"]
    solution = GeneticAlgorithm(Genetic_Algorithm_Config["individual_count"], Genetic_Algorithm_Config["mutation_prob"])
    epochs = Genetic_Algorithm_Config["epochs"]
    process_bar = tqdm(range(epochs))
    for epoch in process_bar:
        print(f"epoch: {epoch+1}/{epochs}")
        solution.reproduce()
        individual = solution.get_best_individual()
        process_bar.desc = f"繁殖代数[{epoch + 1:03d}/{epochs}], 当前最优个体适应性为 {individual.fittness:.4f}"
        # 调试信息
        solution.debug_fittness()
        individual.debug_fittness(epoch)
        