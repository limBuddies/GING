class CollisionDetector:
    def __init__(self):
        self.positionL = []
        # 创建一个空数列来存放过程中还没有闭合的区间的sprite
        self.projectionX = []
        self.projectionY = []
        self.L = []
        self.collideX = set()
        self.collideY = set()
        self.lastCollide = set()
        self.collide = set()

    # noinspection DuplicatedCode
    def tick(self, sprites):
        # 计算每次位置
        self.lastCollide = self.collide.copy()
        self.collideX.clear()
        self.collideY.clear()
        self.collide.clear()
        self.projectionX.clear()
        self.projectionY.clear()
        for k in sprites.keys():
            if not sprites[k].collision.enable:
                continue
            x1 = sprites[k].transform.position.x - sprites[k].collision.size.x / 2
            x2 = sprites[k].transform.position.x + sprites[k].collision.size.x / 2
            y1 = sprites[k].transform.position.y - sprites[k].collision.size.y / 2
            y2 = sprites[k].transform.position.y + sprites[k].collision.size.y / 2
            location = {
                'name': k,
                'x': sprites[k].transform.position.x,
                'y': sprites[k].transform.position.y,
                'x1': x1,
                'x2': x2,
                'y1': y1,
                'y2': y2
            }
            self.positionL.append(location)
            self.projectionX.append((x1, k))
            self.projectionX.append((x2, k))
            self.projectionY.append((y1, k))
            self.projectionY.append((y2, k))
        # position = sorted(self.positionL, key=lambda item: item["x"])
        # self.positionL = position
        # self.L.append(self.positionL[0].name)
        self.projectionX = sorted(self.projectionX, key=lambda item: item[0])
        # # 该方法不能检测两个以上物体同时发生碰撞时结果
        # while i < len(self.projectionX):
        #     if self.projectionX[i][1] != self.projectionX[i + 1][1]:
        #         if self.projectionX[i][1] not in self.L:
        #             self.L.append(self.projectionX[i][1])
        #             self.collideX.append((self.projectionX[i][1], self.projectionX[i + 1][1]))
        #             i += 1
        #         else:
        #             self.L.remove(self.projectionX[i][1])
        #             i += 1
        #     else:
        #         i += 2
        for i in self.projectionX:
            if i[1] not in self.L:
                for m in self.L:
                    self.collideX.add((m, i[1]) if m < i[1] else (i[1], m))
                self.L.append(i[1])
            else:
                self.L.remove(i[1])

        self.projectionY = sorted(self.projectionY, key=lambda item: item[0])
        for i in self.projectionY:
            if i[1] not in self.L:
                for m in self.L:
                    self.collideY.add((m, i[1]) if m < i[1] else (i[1], m))
                self.L.append(i[1])
            else:
                self.L.remove(i[1])
        self.collide = self.collideX.intersection(self.collideY)

    def enters(self):
        return list(self.collide.difference(self.lastCollide))

    def exits(self):
        return list(self.lastCollide.difference(self.collide))

    def stays(self):
        return list(self.collide.intersection(self.lastCollide))
