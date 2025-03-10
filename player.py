import pygame, map; from math import radians, sin, cos, tan

turnSpeed = 60
moveSpeed = 80
fov = 60
stripNo = 1500
stripWidth = 1500/stripNo
angIncrement = fov/stripNo
cellSize = 100
maxDepth = 15
wallAsset = pygame.image.load("./Assets/wall.png")

class Player:
    def __init__(self):
        self.angle = 0
        self.x = 100
        self.y = 100
        self.rect = pygame.Rect(100, 100, 5, 5)
        self.strips = []

    def turn(self, dt, rel):
        pygame.mouse.set_visible(False)
        self.angle += turnSpeed * dt * rel[0] * 2

        if self.angle > 360:
            self.angle -= 360
        elif self.angle < 0:
            self.angle += 360

    def move(self, dt):
        keys = pygame.key.get_pressed()

        moveX = 0
        moveY = 0

        if keys[pygame.K_w]:
            moveX += moveSpeed * dt * cos(radians(self.angle))
            moveY += moveSpeed * dt * sin(radians(self.angle))

        if keys[pygame.K_s]:
            moveX -= moveSpeed * dt * cos(radians(self.angle))
            moveY -= moveSpeed * dt * sin(radians(self.angle))
        
        if keys[pygame.K_a]:
            moveX += moveSpeed * dt * cos(radians(self.angle - 90))
            moveY += moveSpeed * dt * sin(radians(self.angle - 90))

        if keys[pygame.K_d]:
            moveX += moveSpeed * dt * cos(radians(self.angle + 90))
            moveY += moveSpeed * dt * sin(radians(self.angle + 90))

        if self.x + self.y == self.x + self.y + moveX + moveY:
            return False

        self.x += moveX
        self.rect.x = self.x

        self.y += moveY
        self.rect.y = self.y

        cancel = False

        for pos in map.map1:
            if self.rect.colliderect(pygame.rect.Rect((pos[0] * 100, pos[1] * 100), (100, 100))):
                cancel = True

        if cancel:
            self.x -= moveX
            self.rect.x = self.x

            self.y -= moveY
            self.rect.y = self.y

        return True

    def render(self):
        currentAngle = self.angle - fov/2
        self.strips = []

        if currentAngle == 0:
            currentAngle += 0.00001
        assetStep = 0

        gridX = self.x//100
        gridY = self.y//100

        dist = 800/tan(radians(fov/2))
        
        for i in range(stripNo):
            # horizontal intersections

            if currentAngle > 360:
                currentAngle -= 360
            elif currentAngle < 0:
                currentAngle += 360

            if currentAngle < 180:
                yStep = 1
                xStep = yStep/(tan(radians(currentAngle)) + 0.000001)

                yN = 1 - (self.y/100 - gridY)
                xN = yN/tan(radians(currentAngle))       
            else:
                yStep = -1
                xStep = yStep/tan(radians(currentAngle))

                yN = -(self.y/100 - gridY) - 0.0001
                xN = yN/tan(radians(currentAngle))

            currentX, currentY = self.x/100 + xN, self.y/100 + yN
            horTotal = (xN**2 + yN**2)**0.5

            for j in range(maxDepth):
                if (currentX//1, currentY//1) in map.map1:
                    break
                currentX += xStep
                currentY += yStep

                horTotal += (xStep**2 + yStep**2)**0.5

            # vertical intersections

            if currentAngle > 90 and currentAngle < 270:
                xStep = -1
                yStep = xStep * tan(radians(currentAngle))

                xN = -(self.x/100 - gridX) - 0.0001
                yN = xN * tan(radians(currentAngle))
            else:
                xStep = 1
                yStep = tan(radians(currentAngle))

                xN = 1 - (self.x/100 - gridX)
                yN = xN * tan(radians(currentAngle))

            currentX, currentY = self.x/100 + xN, self.y/100 + yN
            verTotal = (xN**2 + yN**2)**0.5

            for j in range(maxDepth):
                if (currentX//1, currentY//1) in map.map1:
                    break
                currentX += xStep
                currentY += yStep

                verTotal += (xStep**2 + yStep**2)**0.5

            corAngle = self.angle - currentAngle
            
            if corAngle > 360:
                corAngle -= 360
            elif corAngle < 0:
                corAngle += 360

            total = min(horTotal, verTotal) * cos(radians(corAngle))

            if assetStep > wallAsset.get_width():
                assetStep = 0

            calcVal = min(dist/(total + 0.00001), 800)
            self.strips.append((calcVal, max(min((1 - total/10) * 255, 255), 0)))
                #surf = pygame.surface.Surface((stripWidth, calcVal))
                #surf.blit(pygame.transform.scale(wallAsset, (calcVal, calcVal)), (-assetStep, 0), pygame.Rect(0, 0, stripWidth, calcVal))
                #WIN.blit(surf, (i * stripWidth, 300 - calcVal/2))
                #assetStep += 1
            currentAngle += fov/stripNo

    def blit(self, WIN):
        for i, val in enumerate(self.strips):
            pygame.draw.rect(WIN, (val[1], val[1], val[1]), pygame.Rect(i * stripWidth, 400 - val[0]/2, stripWidth, val[0]))