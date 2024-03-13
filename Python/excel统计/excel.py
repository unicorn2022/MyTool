import pandas as pd

name = input("请输入专业名: ")

# 读取2021届计算机专业的学生 21-22学年的数据, 并按照学号降序排列
data_21_22 = pd.read_excel('2021-21-22.xlsx', sheet_name=name)
data_21_22.sort_values(by='学号', inplace=True, ascending=False)
data_21_22.reset_index(drop=True, inplace=True)
length_21_22 = len(data_21_22) 

# 读取2021届计算机专业的学生 22-23学年的数据, 并按照学号降序排列
data_22_23 = pd.read_excel('2021-22-23.xlsx', sheet_name=name)
data_22_23.sort_values(by='学号', inplace=True, ascending=False)
data_22_23.reset_index(drop=True, inplace=True)
length_22_23 = len(data_21_22)

if length_21_22 != length_22_23:
    print('两个表格的长度不一致')
    exit(0)

# 创建一个新的dataframe, 用于存储计算后的数据
data_all = pd.DataFrame(columns=['学号', '总学分', '总学分绩点', '平均绩点', '排名', '行政班'])
data_all_length = length_21_22
# 计算每一个学号获得的总学分
for i in range(data_all_length):
    学号 = data_21_22.loc[i]['学号']
    总学分 = data_21_22.loc[i]['学年获得总学分'] + data_22_23.loc[i]['学年获得总学分']
    总学分绩点 = data_21_22.loc[i]['学年获得总学分'] * data_21_22.loc[i]['所有课程学年平均绩点'] + data_22_23.loc[i]['学年获得总学分'] * data_22_23.loc[i]['所有课程学年平均绩点']
    平均绩点 = 总学分绩点 / 总学分
    排名 = 0
    行政班 = data_21_22.loc[i]['行政班']
    data_all.loc[i] = [学号, 总学分, 总学分绩点, 平均绩点, 排名, 行政班]

data_all.sort_values(by='平均绩点', inplace=True, ascending=False)
data_all.reset_index(drop=True, inplace=True)

for i in range(data_all_length):
    data_all.at[i, '排名'] = i + 1

# data_all.to_excel('2021-all.xlsx', sheet_name='计算机')
percent = 0.28
count = int(data_all_length * percent)
print('2021届计算机, 均绩排名前{0}%({1}名)的同学:'.format(int(percent * 100), count))
print(data_all.head(count))