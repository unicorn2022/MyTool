import json
from tqdm import tqdm
from MyGeneticAlgorithm import GeneticAlgorithm
import sys

if __name__ == '__main__':
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
        solution.debug_fittness()
        individual = solution.get_best_individual()
        # individual.calc_fittness(True)
        process_bar.desc = f"繁殖代数[{epoch + 1}/{epochs}], 最优个体为: {individual.__str__()}"
        print("")
        