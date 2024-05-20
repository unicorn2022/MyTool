import random
import json
import numpy as np
from MyMapUtils import MapUtils

file = open("config.json", "r")
config = json.load(file)
file.close()
'''读取地图设置'''
map_config = config["Map_Config"]
map_width = map_config["width"]
map_height = map_config["height"]
safe_distance = map_config["safe_distance"]
rand_weight = map_config["rand_weight"]
'''读取无人机属性'''
direction = {
    "L" : np.array([-1,  0]),
    "R" : np.array([ 1,  0]),
    "U" : np.array([ 0,  1]),
    "D" : np.array([ 0, -1]),
    "P" : np.array([ 0,  0])
}
UAV_config = config["UAV_Config"]
UAV_num = UAV_config["num"]
UAV_search_time = UAV_config["search_time"]
UAV_search_radius = UAV_config["search_radius"]
UAV_start_position = UAV_config["start_position"]

class Gene:
    def __init__(self, data:str=None, position:np.array=None, map_utils:MapUtils=None, last_direction:str=None):
        '''基因
        :param data: 基因携带的信息
        :param position: 无人机当前位置
        :param map_utils: 辅助工具
        '''
        if data != None:
            self.data = data
        else:
            self.data = map_utils.get_random_direction(position, last_direction)
        return
    
    def __str__(self) -> str:
        return self.data

    def mutation(self):
        '''基因突变'''
        self.data = random.choice(["L", "R", "U", "D"])
        return

    def get_direction(self):
        return direction[self.data]

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
        if father == None and mother == None:
            self.create_random(mutation_prob)
        else:
            self.create_by_parent(father, mother)
        return

    def create_by_parent(self, father, mother):
        '''个体
        :param father: 父代
        :param mother: 母代
        '''
        self.map_utils = MapUtils(map_width, map_height, safe_distance, rand_weight)
        self.mutation_prob = father.mutation_prob
        self.gene_count = father.gene_count
        self.gene_start_index = father.gene_start_index
        self.genotype = []
        # 基因重组
        index = random.randint(0, self.gene_count - 1)
        for i in range(0, index):
            self.genotype.append(Gene(data=father.genotype[i].data))
        for i in range(index, self.gene_count):
            self.genotype.append(Gene(data=mother.genotype[i].data))
        # 基因突变
        self.mutation()
        # 计算个体适应性
        self.calc_fittness()
        return

    def create_random(self, mutation_prob:float):
        '''个体
        :param gene_count: 一个个体包含的基因个数
        :param mutation_prob: 基因突变的概率
        '''
        self.map_utils = MapUtils(map_width, map_height, safe_distance, rand_weight)
        # 随机初始化
        self.mutation_prob = mutation_prob
        # 初始化基因型
        self.genotype = []
        self.gene_count = 0
        self.gene_start_index = []
        # 创建飞机的飞行轨迹
        for index in range(UAV_num):
            self.gene_start_index.append(self.gene_count)
            self.gene_count += UAV_search_time
            position = UAV_start_position[index]
            last_direction = None
            for time in range(UAV_search_time):
                gene = Gene(position=position, map_utils=self.map_utils, last_direction=last_direction)
                self.genotype.append(gene)
                last_direction = gene.data
                position += gene.get_direction()
        self.gene_start_index.append(self.gene_count)            
        # 计算个体适应性
        self.calc_fittness()
        return
    
    def __str__(self, detail=False) -> str:
        res = f"fit: {self.fittness:4.3f} "
        if detail == True:
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
      
    def calc_fittness(self):
        '''计算个体适应性, 适应性保证非负, 且适应性越高, 个体越不容易被淘汰'''
        UAV_positions = np.array(UAV_start_position) # 无人机当前位置
        UAV_fly_timer = np.zeros(UAV_num)            # 无人机当前飞行倒计时
        UAV_fly_distance = np.zeros((UAV_num, 2))    # 无人机当前飞行长度
        UAV_fly_step = np.zeros(UAV_num, dtype=int)  # 无人机当前飞了多少步

        # 清空 map_utils
        self.map_utils.clear_map()

        # 模拟搜索过程
        self.fittness = self.map_utils.update_map(UAV_positions, UAV_search_radius)
        for time in range(UAV_search_time):
            # 无人机飞行
            for UAV_index in range(UAV_num):
                # 计时器为0, 根据策略选择飞行目标, 设置飞行倒计时
                if UAV_fly_timer[UAV_index] == 0:
                    # 飞行策略 => 飞行距离
                    gene = self.genotype[self.gene_start_index[UAV_index] + UAV_fly_step[UAV_index]]
                    UAV_fly_distance[UAV_index] = gene.get_direction()
                    UAV_fly_step[UAV_index] += 1
                    # 计算目标位置
                    UAV_positions[UAV_index] = np.ceil(UAV_positions[UAV_index])
                    target_position = (UAV_positions[UAV_index] + UAV_fly_distance[UAV_index]).astype(int)
                    # 从地图中读取飞行时间
                    UAV_fly_timer[UAV_index] = self.map_utils.get_map_time(target_position)
                # 前进一个单位时间
                UAV_positions[UAV_index][0] += 1.0 / UAV_fly_timer[UAV_index] * UAV_fly_distance[UAV_index][0]
                UAV_positions[UAV_index][1] += 1.0 / UAV_fly_timer[UAV_index] * UAV_fly_distance[UAV_index][1]
                UAV_fly_timer[UAV_index] -= 1
            # 更新地图
            self.fittness = self.map_utils.update_map(UAV_positions, UAV_search_radius)
            if self.fittness < 0:
                self.fittness = time - UAV_search_time
                return
                   
    def debug_fittness(self, epoch:int):
        self.map_utils.debug(epoch, self.fittness)