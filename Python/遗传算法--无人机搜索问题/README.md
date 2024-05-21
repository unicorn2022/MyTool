根据`environment.yml`创建**anaconda**环境

```bash
conda env create -f environment.yml
```

激活环境，运行`main,py`脚本

```python
python main.py
```

- 在控制台中，可以监控到遗传算法的计算进度
- 在`best.txt`中，可以看到每一代的最优个体，及其对应搜索策略
- 在`config.json`中，可以修改无人机的属性
- 在`MyMapUtils.py`中的`MapUtils.__init__()`中，修改地图属性