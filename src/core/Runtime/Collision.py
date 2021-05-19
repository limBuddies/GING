class CollisionDetector:
    def __init__(self):
        self.positionL = []
        # 创建一个空数列来存放过程中还没有闭合的区间的sprite
        self.projection = []
        self.L = []
        self.collide = []

    def tick(self, sprites):
        # 计算每次位置
        for k in sprites.keys():
            x1 = sprites[k].transform.x - sprites[k].collision.size.x / 2
            x2 = sprites[k].transform.x + sprites[k].collision.size.x / 2
            y1 = sprites[k].transform.y - sprites[k].collision.size.y / 2
            y2 = sprites[k].transform.y - sprites[k].collision.size.y / 2
            location = {
                'name': k,
                'x': sprites[k].transform.x,
                'y': sprites[k].transform.y,
                'x1': x1,
                'x2': x2,
                'y1': y1,
                'y2': y2
            }
            self.positionL.append(location)
            self.projection.append((x1, k))
            self.projection.append((x2, k))
        # position = sorted(self.positionL, key=lambda item: item["x"])
        # self.positionL = position
        # self.L.append(self.positionL[0].name)
        projections = sorted(self.projection, key=lambda item: item[0])
        self.projection = projections
        i = 0
        self.L.append(self.projection[i][1])
        while i < len(self.projection):
            if self.projection[i][1] != self.projection[i + 1][1]:
                if self.projection[i][1] not in self.L:
                    self.L.append(self.projection[i][1])
                    self.collide.append((self.projection[i][1], self.projection[i + 1][1]))
                    i += 1
                else:
                    self.L.remove(self.projection[i][1])
                    i += 1
            else:
                i += 2

    def enters(self):
        # 进入collision 状态

        pass

    def exits(self):
        pass

    def stays(self):
        pass
