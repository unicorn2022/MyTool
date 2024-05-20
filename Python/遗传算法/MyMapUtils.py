import numpy as np
import math
import matplotlib.pyplot as plt
import pyexr
import random
import sys

class MapUtils:
    def __init__(self, width:int, height:int, safe_distance:float, rand_weight:bool):
        '''
        :param width: 地图宽度
        :param height: 地图高度
        :param safe_distance: 安全距离
        :param rand_weight: 是否随机权重
        '''
        self.width = width
        self.height = height
        self.safe_distance = safe_distance
        # 物资权重
        self.map_weight = np.ones((width, height))
        for i in range(width):
            for j in range(height):
                if rand_weight == True:
                    self.map_weight[i][j] = random.uniform(0, 1)
                else:
                    # self.map_weight[i][j] = random.randint(0, 1)
                    if i == 3 and j in range(10, 21):
                        self.map_weight[i][j] = 1
                    elif i == 4 and j in range(2, 26):
                        self.map_weight[i][j] = 1
                    elif i == 5 and j in range(2, 41):
                        self.map_weight[i][j] = 1
                    elif i in range(6, 20) and j in range(2, 46):
                        self.map_weight[i][j] = 1
                    elif i in range(20, 26) and j in range(10, 46):
                        self.map_weight[i][j] = 1
                    elif i in range(26, 36) and j in range(5, 36):
                        self.map_weight[i][j] = 1
                    elif i in range(36, 45) and j in range(2, 46):
                        self.map_weight[i][j] = 1
                    elif i in range(45, 48) and j in range(5, 35):
                        self.map_weight[i][j] = 1
                    elif i == 48 and j in range(10, 16):
                        self.map_weight[i][j] = 1
                    else:
                        self.map_weight[i][j] = 0

        # 飞行时间
        self.map_time = np.zeros((width, height), dtype=int)
        for i in range(width):
            for j in range(height):
                # self.map_time[i][j] = np.random.randint(1, 5)
                # if np.random.rand() < 0.1:
                #     self.map_time[i][j] = -1
                if i in range(8, 13) and j in range(10, 16):
                    self.map_time[i][j] = -1
                elif i in range(30, 36) and j in range(25, 31):
                    self.map_time[i][j] = -1
                elif i in range(10, 16) and j in range(10, 26):
                    self.map_time[i][j] = 2
                else:
                    self.map_time[i][j] = 1

        return
    
    def init_individual_setup(self):
        # 生成个体时使用
        self.map_weight_for_init = self.map_weight
        return
    
    def init_individual_update_map(self, position:np.array, search_radius:float):
        '''更新未搜索的地图权重
        :param position 无人机位置
        :param search_radius 无人机半径
        '''
        for i in range(max(0, position[0] - search_radius - 1), min(self.width, position[0] + search_radius + 1)):
            for j in range(max(0, position[1] - search_radius - 1), min(self.height, position[1] + search_radius + 1)):
                if math.dist([i, j], position) <= search_radius:
                    self.map_weight_for_init[i][j] = 0
        return
    
    def init_individual_get_direction(self, UAV_position:np.array, last_direction:str) -> str:
        '''获取当前位置下的合法前进方向的随机一个
        :param UAV_position 无人机当前位置
        :param last_direction 无人机上一次的飞行方向
        return 合法的位置集合
        '''
        direction = []
        total_weight = []
        # 左
        if last_direction != "R" and self.check_position(UAV_position + np.array([-1,  0])):
            direction.append("L")
            total_weight.append(sum(sum(self.map_weight_for_init[0:UAV_position[0], 0:])))
        # 右
        if last_direction != "L" and self.check_position(UAV_position + np.array([ 1,  0])):
            direction.append("R")
            total_weight.append(sum(sum(self.map_weight_for_init[UAV_position[0]+1:, 0:])))
        # 上
        if last_direction != "D" and self.check_position(UAV_position + np.array([ 0,  1])):
            direction.append("U")
            total_weight.append(sum(sum(self.map_weight_for_init[0:, UAV_position[1]+1:])))
        # 下
        if last_direction != "U" and self.check_position(UAV_position + np.array([ 0, -1])):
            direction.append("D")
            total_weight.append(sum(sum(self.map_weight_for_init[0:, 0:UAV_position[1]])))
        
        # 有可前进方向, 根据权重随机选择
        if len(direction) != 0:
            total_weight /= sum(total_weight)
            temp = random.uniform(0.0, 1.0)
            for i in range(len(direction)):
                if temp - total_weight[i] <= 0:
                    return direction[i]
                temp -= total_weight[i]
        return "P"


    def check_position(self, UAV_position:np.array) -> bool:
        '''判断单个无人机位置是否合法:
        :param UAV_position: 无人机位置
        :return True表示合法, False表示不合法
        '''
        if UAV_position[0] < 0 or UAV_position[0] >= self.width:
            return False
        if UAV_position[1] < 0 or UAV_position[1] >= self.height:
            return False
        if self.map_time[UAV_position[0]][UAV_position[1]] == -1:
            return False
        return True
    
    def check_collision(self, UAV_positions:np.array) -> bool:
        '''判断无人机是否会相撞:
        :param UAV_positions: 多个无人机的位置
        :return True表示合法, False表示不合法
        '''
        for i in range(len(UAV_positions)):
            for j in range(i):
                if math.dist(UAV_positions[i], UAV_positions[j]) < self.safe_distance:
                    return False
        return True
    
    def clear_map(self):
        self.map_visit = np.zeros((self.width, self.height), dtype=int)
        self.map_record = np.zeros((self.width, self.height), dtype=int)
        self.total_weight = 0
        return

    def update_map(self, UAV_positions:np.array, UAV_search_radius:np.array) -> float:
        '''更新
        :param UAV_positions: 无人机当前位置
        :param UAV_search_radius: 无人机搜索半径
        :return 搜索过的所有位置的权重和, 如果不合法则返回-1
        '''
        if self.check_collision(UAV_positions) == False:
            return -1
        for index in range(len(UAV_positions)):
            position = UAV_positions[index]
            if self.check_position(position) == False:
                return -1
            self.map_record[position[0]][position[1]] = index + 1
            search_radius = UAV_search_radius[index]
            for i in range(max(0, position[0] - search_radius - 1), min(self.width, position[0] + search_radius + 1)):
                for j in range(max(0, position[1] - search_radius - 1), min(self.height, position[1] + search_radius + 1)):
                    if self.map_visit[i][j] == 1:
                        continue
                    if self.map_time[i][j] == -1:
                        continue
                    if math.dist([i, j], position) <= search_radius:
                        self.map_visit[i][j] = 1
                        self.total_weight += self.map_weight[i][j]
        return self.total_weight

    def get_map_time(self, target_position:np.array) -> int:
        '''获取到达地图某个位置所需的飞行时间
        :param target_position: 目标位置
        :return 飞行时间
        '''
        if self.check_position(target_position) == False:
            return 1e10
        return self.map_time[target_position[0]][target_position[1]]

    def debug(self, epoch:int, fittness:float):
        img = np.zeros((self.width, self.height, 3))
        for i in range(self.width):
            for j in range(self.height):
                # 地图权重: blue
                if self.map_weight[i][j] == 0:
                    img[i][j] = np.array([1, 1, 1])
                else:
                    img[i][j] = self.map_weight[i][j] * np.array([0, 0.25, 0.5])
                # 地图时间: black
                if self.map_time[i][j] == -1:
                    img[i][j] = np.array([0, 0, 0]) 
                # 飞机搜索位置: green
                if self.map_visit[i][j] != 0:
                    img[i][j] = np.array([0, 1, 0])
                # 飞机位置: red
                if self.map_record[i][j] != 0:
                    img[i][j] = np.array([1, 0, 0])
        pyexr.write(f"log/epoch_{epoch:02d}_fit_{fittness:.4f}.exr", img)
        # # 飞机位置
        # plt.imshow(self.map_record, cmap='gray')
        # plt.savefig(f"log/epoch_{epoch:02d}_飞机位置.jpg")
        # # 飞机搜索位置
        # plt.imshow(self.map_visit, cmap='gray')
        # plt.savefig(f"log/epoch_{epoch:02d}_飞机搜索位置.jpg")
        # # 地图到达时间
        # plt.imshow(self.map_time, cmap='gray')
        # plt.savefig(f"log/epoch_{epoch:02d}_地图到达时间.jpg")
        # # 地图权重 
        # plt.imshow(self.map_weight, cmap='gray')
        # plt.savefig(f"log/epoch_{epoch:02d}_地图权重.jpg")
        return
            