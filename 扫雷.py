'''
Author: Mike Liang
Date: 2022-03-24 08:29:11
LastEditors: Mike Liang
LastEditTime: 2022-03-26 21:18:25
Description: file content
Name:非常不讲武德的扫雷
'''
import os
import sys
import time

import pygame

try:
    os.mkdir(r"./log")
except:
    pass


class Game():
    datas: dict = {}
    savetime: int = 0

    def FuncMakeMap(self) -> list:
        '''
        制作地图
        类似于
        map = [
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0]
            1 = 有
            0 = 无
        ]
        '''
        map: list = []  # 地图
        import random  # 随机数
        for i in range(9):  # 列
            tmp = []  # 每一列
            for n in range(9):  # 每一列的每一行
                t = random.randint(1, 10)  # 随机数
                ray = 0  # 雷的数量
                if t % 2 == 0 and ray <= 3:  # 如果是偶数，并且雷的数量小于等于3
                    tmp.append(1)  # 添加雷
                    ray = ray+1  # 雷的数量加1
                else:  # 如果是奇数
                    tmp.append(0)  # 添加无
            map.append(tmp)  # 添加到地图
        with open(r"./log/map{}.txt".format(self.savetime), "a+") as f:
            for i in map:
                f.write(str(i)+"\n")
        return map

    def FuncGetNums(self, x, y, map, t) -> int or str:
        '''
        获取周围雷的数量
        '''
        self.datas['INFO_X_IN_{}'.format(t)] = '{}'.format(x)
        self.datas['INFO_Y_IN_{}'.format(t)] = '{}'.format(y)
        self.datas['INFO_POS_{}'.format(t)] = '{}'.format(map[x][y])
        if map[y][x] == 1:  # 如果是雷
            return "X"  # 返回-1
        else:
            over: int = 0
            try:
                if map[y+1][x] != 0:  # 下
                    over = over+1
            except:
                pass
            try:
                if map[y-1][x] != 0:  # 上
                    over = over+1
            except:
                pass
            try:
                if map[y][x+1] != 0:  # 右
                    over = over+1
            except:
                pass
            try:
                if map[y][x-1] != 0:  # 左
                    over = over+1
            except:
                pass
            try:
                if map[y+1][x+1] != 0:  # 右下
                    over = over+1
            except:
                pass
            try:
                if map[y-1][x+1] != 0:  # 右上
                    over = over+1
            except:
                pass
            try:
                if map[y+1][x-1] != 0:  # 左下
                    over = over+1
            except:
                pass
            try:
                if map[y-1][x-1] != 0:  # 左上
                    over = over+1
            except:
                pass
            if x != 8 == True or y != 8 == True:
                return over+1
            else:
                return over

    def FuncGetNum(self, map) -> int:
        z: int = 0
        for i in map:
            z = z+i.count(1)
        return z

    def FuncGetNum2(self, map) -> int:
        z: int = 0
        for i in map:
            z = z+i.count(0)
        return z

    def run(self) -> None:
        score: int = 0
        exit: bool = False
        win: bool = False
        pygame.init()  # 初始化
        size: tuple = (380, 480)  # 设置窗口大小
        screen: pygame.Surface = pygame.display.set_mode(size)  # 设置窗口
        pygame.display.set_caption("扫雷")
        chooser: pygame.Surface = pygame.image.load('chooser.svg')  # 加载图片
        chooserrect: pygame.Surface = chooser.get_rect()  # 获取图片的矩形
        chooserrect: pygame.Surface = chooserrect.move(100, 100)  # 移动图片
        nums: list = []
        over: bool = False
        map: list = self.FuncMakeMap()  # 制作地图
        ft: float = time.time()  # 计时
        pos: list = []
        cxy: list = []
        t: int = 5
        j1: bool = False
        X: list = []
        while True:  # 循环
            font1: pygame.Surface = pygame.font.SysFont(
                '', 40, True)  # 设置字体
            sc: object = font1.render(str(self.FuncGetNum(map)),
                                      True, (0, 0, 0))  # 设置文字
            font1: pygame.Surface = pygame.font.SysFont(
                '', 40, True)  # 设置字体
            t0: pygame.Surface = font1.render("{}".format(int(time.time()-ft)),
                                              True, (0, 0, 0))  # 设置文字
            font1: object = pygame.font.SysFont(
                '', 40, True)  # 设置字体
            t1: pygame.Surface = font1.render("{}%".format(
                int((int(self.FuncGetNum(map))/81)*100)), True, (0, 0, 0))  # 设置文字
            t2: pygame.Surface = font1.render(u'{}%'.format(
                int((score/int(self.FuncGetNum2(map)))*100)), True, (0, 0, 0))
            t3: pygame.Surface = font1.render(
                u'{}'.format(int(score)), True, (0, 0, 0))
            t4: pygame.Surface = font1.render(
                u'{}'.format(int(t)), True, (0, 0, 0))
            for event in pygame.event.get():  # 事件
                if event.type == pygame.QUIT:  # 退出
                    import json
                    with open(r"./log/Gameinfo{}.json".format(self.savetime), 'a+') as f:
                        f.write(json.dumps(self.datas, sort_keys=True,
                                indent=4, separators=(',', ':')))
                    self.savetime = 0
                    sys.exit()  # 退出
                if event.type == pygame.KEYDOWN:  # 按键
                    if event.key == pygame.K_LEFT and chooserrect.x > 100:  # 左
                        chooserrect = chooserrect.move(-21, 0)  # 移动图片
                    if event.key == pygame.K_RIGHT and chooserrect.x < 268:  # 右
                        chooserrect = chooserrect.move(21, 0)  # 移动图片
                    if event.key == pygame.K_UP and chooserrect.y > 100:  # 上
                        chooserrect = chooserrect.move(0, -21)  # 移动图片
                    if event.key == pygame.K_DOWN and chooserrect.y < 268:  # 下
                        chooserrect = chooserrect.move(0, 21)  # 移动图片
                    if event.key == pygame.K_SPACE:  # 空格
                        if over == True:
                            exit = True
                            break
                        num: int = self.FuncGetNums(int((chooserrect.x-100)/21),
                                                    int((chooserrect.y-100)/21), map, time.time() - ft)  # 获取周围雷的数量
                        if num == "X" and (chooserrect.x, chooserrect.y) not in X:  # 如果是雷
                            t = t-1
                            X.append((chooserrect.x, chooserrect.y))
                            j1 = True
                            nums.append("X")  # 添加到数组
                        else:
                            nums.append(num)  # 添加到数组
                        if t <= -1:
                            over = True
                        else:
                            if (chooserrect.x, chooserrect.y) not in pos and j1 == False and (chooserrect.x, chooserrect.y) not in X:
                                score = score+1  # 得分加1
                                pos.append((chooserrect.x, chooserrect.y))
                        if score == self.FuncGetNum2(map):
                            win = True
                        cxy.append((chooserrect.x, chooserrect.y))  # 添加到数组
                        j1 = False
            if exit == True:
                break
            pygame.display.flip()  # 刷新
            screen.fill((0, 255, 0))  # 填充颜色
            if over != True:  # 如果游戏没有结束
                for i in range(0, 9):  # 循环
                    for n in range(0, 9):  # 循环
                        if (100+(n*21), 100+(i*21)) in cxy:  # 如果在数组中
                            pygame.draw.rect(screen, (0, 225, 0),
                                             (100+n*21, 100+i*21, 20, 20), 0)  # 绘制矩形
                        else:  # 如果不在数组中
                            pygame.draw.rect(screen, (225, 225, 255),
                                             (100+n*21, 100+i*21, 20, 20), 0)  # 绘制矩形
                for i in range(len(nums)):  # 循环
                    font1: pygame.Surface = pygame.font.SysFont(
                        '', 40, True)  # 设置字体
                    s: pygame.Surface = font1.render(
                        str(nums[i]), True, (0, 0, 0))  # 设置文字
                    screen.blit(s, [cxy[i][0], cxy[i][1]])  # 绘制文字
                screen.blit(chooser, chooserrect)  # 绘制图片
                screen.blit(sc, [0, 0])  # 绘制文字
                screen.blit(t0, [0, 40])  # 绘制文字
                screen.blit(t1, [0, 80])  # 绘制文字
                screen.blit(t2, [0, 120])  # 绘制文字
                screen.blit(t3, [0, 160])  # 绘制文字
                screen.blit(t4, [0, 200])  # 绘制文字
            else:  # 如果游戏结束
                font1: pygame.Surface = pygame.font.SysFont(
                    '', 40, True)  # 设置字体
                s: pygame.Surface = font1.render(
                    u'Game Over!', True, (0, 0, 0))  # 设置文字
                s2: pygame.Surface = font1.render(u'Score:Get {}%'.format(
                    int((score/int(self.FuncGetNum2(map)))*100)), True, (0, 0, 0))  # 设置文字
                screen.blit(s, [100, 240])  # 绘制文字
                screen.blit(s2, [100, 280])  # 绘制文字
            if win == True:
                font1: pygame.Surface = pygame.font.SysFont(
                    '', 40, True)  # 设置字体
                s: pygame.Surface = font1.render(
                    u'You win!', True, (0, 0, 0))  # 设置文字
                screen.blit(s, [100, 240])  # 绘制文字
        import json
        with open(r"./log/Gameinfo{}.json".format(self.savetime), 'a+') as f:
            f.write(json.dumps(self.datas, sort_keys=True,
                    indent=4, separators=(',', ':')))
        self.datas = {}
        self.savetime = 0
        pygame.quit()  # 退出


if __name__ == "__main__":
    while True:
        game = Game()  # 实例化
        game.savetime = time.time()
        game.run()
