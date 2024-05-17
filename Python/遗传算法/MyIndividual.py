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
if map_config["rand_weight"] == True:
    map_weight = np.random.random((map_width, map_height))
else:
    map_weight = np.ones((map_width, map_height))
safe_distance = map_config["safe_distance"]
'''无人机属性'''
choice = [0, 1, 2, 3] # 0左转, 1前进, 2右转, 3后退
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
        if self.data == 0:
            return "L"
        elif self.data == 1:
            return "U"
        elif self.data == 2:
            return "R"
        elif self.data == 3:
            return "D"
        else:
            return "ERROR"

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
        res = f"fit: {self.fittness:4.3f} "
        for UAV_index in range(UAV_num):
            res += f"[({UAV_start_position[UAV_index][0]}, {UAV_start_position[UAV_index][1]})"
            for i in range(self.gene_start_index[UAV_index], self.gene_start_index[UAV_index + 1]):
                res += self.genotype[i].__str__()
            res += "], "
        return res

    def mutation(self):
        '''基因突变'''
        if random.uniform(0, 1) > self.mutation_prob:
            return
        index = random.randint(0, self.gene_count - 1)
        self.genotype[index].mutation()
        return
      
    def calc_fittness(self, debug=False):
        '''计算个体适应性, 适应性保证非负, 且适应性越高, 个体越不容易被淘汰'''
        positions = np.array(UAV_start_position, dtype=int) # 无人机当前位置
        timer = np.array(UAV_search_cost, dtype=int)        # 无人机当前飞行倒计时
        step = np.zeros(UAV_num, dtype=int)                 # 无人机当前飞了多少步
        map_vist = np.zeros((map_width, map_height), dtype=int)  # 地图, 记录当前位置是否被搜索到

        def update_map(time):
            '''
            更新地图
            :return 当前被探索过的区域权重和
            '''
            # 判断是否有无人机相撞
            for i in range(UAV_num):
                # 位置是否合法
                if positions[i][0] < 0 or positions[i][0] >= map_width:
                    return time - UAV_search_time
                if positions[i][1] < 0 or positions[i][1] >= map_height:
                    return time - UAV_search_time
                # 是否与其他无人机相撞
                for j in range(i):
                    if math.dist(positions[i], positions[j]) < safe_distance:
                        return time - UAV_search_time
            
            # 更新地图
            for index in range(UAV_num):
                position = positions[index]
                search_radius = UAV_search_radius[index]
                for i in range(max(0, position[0] - search_radius), min(map_width, position[0] + search_radius)):
                    for j in range(max(0, position[1] - search_radius), min(map_width, position[1] + search_radius)):
                        if math.dist([i, j], position) <= search_radius:
                            map_vist[i][j] = 1
            return sum(sum(map_vist * map_weight))

        self.fittness = update_map(0)
        # 模拟搜索过程
        for time in range(UAV_search_time):
            for UAV_index in range(UAV_num):
                timer[UAV_index] -= 1
                if timer[UAV_index] == 0:
                    # 无人机飞行一步
                    option = self.genotype[self.gene_start_index[UAV_index] + step[UAV_index]]
                    if option.data == 0: # 左转
                        positions[UAV_index][0] += -1
                        positions[UAV_index][1] += 0
                    elif option.data == 1:  # 前进
                        positions[UAV_index][0] += 0
                        positions[UAV_index][1] += 1
                    elif option.data == 2:  # 右转
                        positions[UAV_index][0] += 1
                        positions[UAV_index][1] += 0
                    elif option.data == 3:  # 后退
                        positions[UAV_index][0] += 0
                        positions[UAV_index][1] += -1 
                    # 重置计时器
                    timer[UAV_index] = UAV_search_cost[UAV_index]
            self.fittness = update_map(time)
            if self.fittness < 0:
                return
    
        if debug == True:
            print(f"map: ({self.fittness:.3f})")
            for i in range(map_vist.shape[0]):
                print(map_vist[i])