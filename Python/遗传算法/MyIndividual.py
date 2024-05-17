'''
题目:
    在长度为 50 的数组 nums 中选择10个元素,
    使得10个元素的和与原数组的所有元素之和的 1/10 最接近
'''

import random

nums = random.sample(range(0, 1000), 50)

class Gene:
    def __init__(self, data:int=None):
        '''基因
        :param data: 基因携带的信息
        '''
        if data == None:
            self.data = random.sample(nums, 1)[0]
        else:
            self.data = data
        return
    
    def __str__(self) -> str:
        return f"{self.data:4d}, "

    def mutation(self):
        '''基因突变'''
        self.data = random.sample(nums, 1)[0]

class Individual:
    def __init__(self, father=None, mother=None, gene_count:int=0, mutation_prob:float=0.01):
        '''个体
        :param father: 父代
        :param mother: 母代
        :param gene_count: 一个个体包含的基因个数
        :param mutation_prob: 基因突变的概率
        '''
        # 父母为空, 随机初始化
        if father == None or mother == None:
            self.mutation_prob = mutation_prob
            self.gene_count = gene_count
            self.genotype = [Gene() for _ in range(gene_count)]
        # 父母不为空, 基因重组
        else:
            self.mutation_prob = father.mutation_prob
            self.gene_count = father.gene_count
            self.genotype = []
            # 基因重组
            index = random.randint(0, self.gene_count - 1)
            for i in range(0, index):
                self.genotype.append(Gene(father.genotype[i].data))
            for i in range(index, self.gene_count):
                self.genotype.append(Gene(mother.genotype[i].data))
            # 基因突变
            self.mutation()
        # 计算个体适应性
        self.calc_fittness()
        return

    def __str__(self) -> str:
        res = "["
        for gene in self.genotype:
            res += gene.__str__()
        res += f"], ({self.delta:4.2f}, {self.fittness:4.3f})"
        return res

    def mutation(self):
        '''基因突变'''
        if random.uniform(0, 1) > self.mutation_prob:
            return
        index = random.randint(0, self.gene_count - 1)
        self.genotype[index].mutation()
        return
    
    def calc_fittness(self):
        '''计算个体适应性, 适应性保证非负, 且适应性越高, 个体越不容易被淘汰'''
        self.sum = 0
        for gene in self.genotype:
            self.sum += gene.data
        self.delta = abs(self.sum - sum(nums)/10)
        if self.delta > 0:
            self.fittness = 1 / self.delta
        else:
            self.fittness =  1e10
