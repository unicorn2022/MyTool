from MyIndividual import Individual
from tqdm import tqdm

class GeneticAlgorithm:
    def __init__(self, individual_count:int, mutation_prob:float):
        '''遗传算法模板
        :param individual_count: 种群个体数目
        :param mutation_prob: 基因突变概率
        '''
        self.individual_count = individual_count
        self.individual_list = []
        # 创建初始解集
        process_bar = tqdm(range(self.individual_count))
        best_fittness = -1e10
        for index in process_bar:
            # 初始化个体
            individual = Individual(mutation_prob=mutation_prob)
            self.individual_list.append(individual)
            # 记录最优个体
            if individual.fittness > best_fittness:
                best_fittness = individual.fittness
            # 日志信息
            process_bar.desc = f"创建个体[{index+1:03d}/{self.individual_count}], 当前最优个体适应性为 {best_fittness:.4f}"
        return

    
    def reproduce(self):
        '''繁衍一代'''
        # 根据 fittness 排序
        self.individual_list.sort(key=lambda item:item.fittness)
        
        # 相邻两个个体分别为父母
        for index in range(0, self.individual_count, 2):
            # 每次选择2个独立的个体进行繁衍
            father = self.individual_list[index + 0]
            mother = self.individual_list[index + 1]
            son_1 = Individual(father=father, mother=mother)
            son_2 = Individual(father=mother, mother=father)
            # 保存至下一代
            self.individual_list.append(son_1)
            self.individual_list.append(son_2)
        
        # 取适应性最好的一半
        self.individual_list.sort(key=lambda item:item.fittness)
        self.individual_list = self.individual_list[self.individual_count:]
        return

    def get_best_individual(self) -> Individual:
        return self.individual_list[-1]

    def debug_fittness(self):
        for index, individual in enumerate(self.individual_list):
            print(f"No.{index:02d}: {individual.__str__(True)}")
        return
    