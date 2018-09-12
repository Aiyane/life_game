## life_game
一个简单的生命游戏

## 要求
python3

## 安装
python setup.py install

## 测试
python test.py

## 配置
|参数|描述|默认|
|:---:|:---:|:---:|
|DEBUG|`True`时会打印每次更新结果|`False`|
|ROW_NUMS|游戏一行的格子数|`50`|
|COLUMN_NUMS|游戏一列的格子数|`50`|
|WINDOW_WIDTH|窗口宽度|`800`|
|WINDOW_HEIGHT|窗口高度|`600`|
|MARGIN_TOP|窗口距离顶部的距离|`200`|
|MARGIN_LEFT|窗口距离左部的距离|`500`|
|SLEEP_TIME|刷新时间(毫秒)|`300`|
|WINDOW_CHANGE|`True`时可以改变窗口大小|`False`|
|INIT_CELLS|是一个二维 list 初始化活的细胞 `None` 则随机|`None`|
|CELL_SIZE|细胞大小|`10`|
|CANVAS_MARGIN_TOP|画布距离窗口顶部距离|`50`|
|CANVAS_MARGIN_LEFT|画布距离窗口左部距离|`135`|
|CELL_COLOR|细胞颜色|`"black"`|
|BACKGROUND|画布背景颜色|`"white"`|

## 例子
```py
from life_game import Game

game = Game()
game.start()
```
或者新建配置文件`settings.py`
```py
SLEEP_TIME = 100
INIT_CELLS = [
    [5, 1], [5, 2], [6, 1], [6, 2], [1, 25], [2, 25], [2, 23], [3, 22], 
    [3, 21], [3, 14], [3, 13], [3, 35], [3, 36], [4, 35], [4, 36], [4, 12],
    [4, 16], [4, 21], [4, 22], [5, 11], [5, 17], [5, 21], [5, 22], [6, 11],
    [6, 15], [6, 17], [6, 18], [6, 23], [6, 25], [7, 11], [7, 17], [7, 25],
    [8, 12], [8, 16], [9, 13], [9, 14]
]
```
在同级目录下新建`test.py`
```py
from life_game import Game
import settings

game = Game()
game.config.from_object(settings)
game.start()
```
运行 `python test.py`
