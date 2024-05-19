from MyIndividual import Individual

class GeneticAlgorithm:
    def __init__(self, individual_count:int, mutation_prob:float):
        '''遗传算法模板
        :param individual_count: 种群个体数目
        :param mutation_prob: 基因突变概率
        '''
        # 创建初始解集
        self.individual_count = individual_count
        self.individual_list = [Individual(mutation_prob=mutation_prob) for _ in range(self.individual_count)]
        self.mutation_prob = mutation_prob
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

    def get_best_individual(self):
        return self.individual_list[-1]

    def debug_fittness(self):
        for index, individual in enumerate(self.individual_list):
            print(f"No.{index:02d}: {individual.__str__(True)}")
        return
    