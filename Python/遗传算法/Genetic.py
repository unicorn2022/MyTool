'''
题目:
    在长度为 50 的数组 nums 中选择10个元素,
    使得10个元素的和与原数组的所有元素之和的 1/10 最接近
'''

import random
import math

class Genetic:
    def __init__(self, nums:list, individual_count:int,  mutation_prob:float):
        '''
        :param nums: 数组
        :param individual_count: 种群个体数目
        :param mutation_prob: 基因突变概率
        '''
        # 创建初始解集
        self.nums = nums
        self.individual_count = individual_count
        self.total_value = sum(nums)
        self.mutation_prob = mutation_prob
        self.result_list = []
        for _ in range(self.individual_count):
            self.result_list.append(random.sample(nums, 10))

        # print("nums: ", self.nums)
        # print("total_value: ", self.total_value)
        return

    def target_function(self, result:list) -> float:
        '''计算目标函数的取值, 需要尽可能让目标函数的取值变大
        :param result: 可能的一个解
        '''
        value = abs(sum(result) - self.total_value/10)
        return -value
    
    def select_one_individual_by_posibility(self, posibility_list:list) -> int:
        '''根据概率表, 选择一个个体
        :param posibility_list: 每个个体被选中的概率, 通过(目标函数值=>归一化)得到
        :return 被选中的个体下标
        '''
        value = random.uniform(0, 1)
        for index in range(len(posibility_list)):
            if value - posibility_list[index] <= 0:
                return index
            value -= posibility_list[index]
        return 0

    def reproduce_one_generation(self):
        '''繁衍一代
        '''
        new_generation = []
        # 根据 target function, 设置选择概率
        self.func_list = [self.target_function(result) for result in self.result_list]
        self.posibility_list = [item/sum(self.func_list) for item in self.func_list]
        
        # 基因重组
        for _ in range(self.individual_count // 2):
            # 每次选择2个独立的个体进行繁衍
            father = self.result_list[self.select_one_individual_by_posibility(self.posibility_list)]
            monther = self.result_list[self.select_one_individual_by_posibility(self.posibility_list)]
            # 互换基因
            index = random.randint(0, len(father))
            son_1 = father[:index] + monther[index:]
            son_2 = monther[:index] + father[index:]
            # 保存至新解集
            new_generation.append(son_1)
            new_generation.append(son_2)
        self.result_list = new_generation

        # 基因突变
        for result in self.result_list:
            if random.uniform(0, 1) > self.mutation_prob:
                continue
            # 第 index 个基因会产生变异
            index = random.randint(0, len(result))
            result = result[:index] + random.sample(nums, 1) + result[index+1:]
        return
    
    def get_best_individual(self):
        '''获取当前种群中的最优个体'''
        max_index = 0
        max_value = self.func_list[0]
        for index in range(1, len(self.func_list)):
            if self.func_list[index] > max_value:
                max_index = index
                max_value = self.func_list[index]
        return max_index, self.result_list[max_index], max_value

if __name__ == '__main__':
    nums = random.sample(range(0, 1000), 50)
    solution = Genetic(nums, 10, 0.01)
    for i in range(100):
        print(f"epoch: {i}")
        solution.reproduce_one_generation()
        index, individual, value = solution.get_best_individual()
        print(f"best: {index}", individual, f"({value:.4f})")


    