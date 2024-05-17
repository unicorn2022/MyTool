import random
import json
import numpy as np
import math

'''读取地图设置'''
file = open("config.json", "r")
config = json.load(file)
map_config = config["Map_Config"]
UAV_config = config["UAV_Config"]
file.close()
'''创建地图'''
map_width = map_config["width"]
map_height = map_config["height"]
'''无人机属性'''
choice = [1, 0, -1] # 1左转, 0前进, -1右转
UAV_num = UAV_config["num"]
UAV_search_time = UAV_config["search_time"]
UAV_search_cost = UAV_config["search_cost"]
UAV_search_radius = UAV_config["search_radius"]
UAV_start_position = UAV_config["start_position"]

class Gene:
    def __init__(self, data:int=None):
        '''基因
        :param data: 基因携带的信息
        '''
        if data == None:
            self.data = random.sample(choice, 1)[0]
        else:
            self.data = data
        return
    
    def __str__(self) -> str:
        return f"{self.data:2d}, "

    def mutation(self):
        '''基因突变'''
        self.data = random.sample(choice, 1)[0]

'''
基因型定义如下: [
    UAV_1_step_1, ... UAV_1_step_x1
    UAV_2_step_1, ... UAV_2_step_x2
    ...
    UAV_n_step_n, ... UAV_n_step_xn
]
'''
class Individual:
    def __init__(self, father=None, mother=None, mutation_prob:float=0.01):
        '''个体
        :param father: 父代
        :param mother: 母代
        :param gene_count: 一个个体包含的基因个数
        :param mutation_prob: 基因突变的概率
        '''
        # 父母为空, 随机初始化
        if father == None or mother == None:
            self.mutation_prob = mutation_prob
            self.gene_count = 0
            self.gene_start_index = []
            for i in range(UAV_num):
                self.gene_start_index.append(self.gene_count)
                self.gene_count += UAV_search_time // UAV_search_cost[i]
            self.gene_start_index.append(self.gene_count)
            self.genotype = [Gene() for _ in range(self.gene_count)]
        # 父母不为空, 基因重组
        else:
            self.mutation_prob = father.mutation_prob
            self.gene_count = father.gene_count
            self.gene_start_index = father.gene_start_index
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
        for UAV_index in range(UAV_num):
            res += "["
            for i in range(self.gene_start_index[UAV_index], self.gene_start_index[UAV_index + 1]):
                res += self.genotype[i].__str__()
            res += "], "
        res += f"], fit: {self.fittness:4.3f}"
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
        positions = np.array(UAV_start_position, dtype=int) # 无人机当前位置
        timer = np.array(UAV_search_cost, dtype=int)        # 无人机当前飞行倒计时
        step = np.zeros(UAV_num, dtype=int)                 # 无人机当前飞了多少步
        map = np.zeros((map_width, map_height), dtype=int)  # 地图, 记录当前位置是否被搜索到

        def update_map():
            '''
            更新地图
            :return 当前被探索过的区域权重和
            '''
            # 判断是否有无人机在同一格
            for i in range(UAV_num):
                # 位置是否合法
                if positions[i][0] < 0 or positions[i][0] >= map_width:
                    return -1e10
                if positions[i][1] < 0 or positions[i][1] >= map_height:
                    return -1e10
                # 是否与其他无人机相撞
                for j in range(i):
                    if positions[i][0] == positions[j][0] and positions[i][1] == positions[j][1]:
                        return -1e10
            
            # 更新地图
            count = 0
            for i in range(map_width):
                for j in range(map_height):
                    for UAV_index in range(UAV_num):
                        if math.dist([i, j], positions[UAV_index]) < UAV_search_radius[UAV_index]:
                            map[i][j] = 1
                            break
                    count += map[i][j]
            return count

        self.fittness = update_map()
        # 模拟搜索过程
        for _ in range(UAV_search_time):
            for UAV_index in range(UAV_num):
                timer[UAV_index] -= 1
                if timer[UAV_index] == 0:
                    # 无人机飞行一步
                    option = self.genotype[self.gene_start_index[UAV_index] + step[UAV_index]]
                    if option.data == -1: # 右转
                        positions[UAV_index][0] += 1
                        positions[UAV_index][1] += 0
                    if option.data == 0:  # 前进
                        positions[UAV_index][0] += 1
                        positions[UAV_index][1] += 0
                    if option.data == 1:  # 左转
                        positions[UAV_index][0] += -1
                        positions[UAV_index][1] += 0
                    # 重置计时器
                    timer[UAV_index] = UAV_search_cost[UAV_index]
            self.fittness = update_map()
