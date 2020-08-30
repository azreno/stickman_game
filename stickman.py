from tkinter import *
import random
import time


class Game:
    def __init__(self):
        self.tk = Tk()
        self.tk.title("Человечек спешит к выходу")
        self.tk.resizable(0, 0)
        self.tk.wm_attributes("-topmost", 1)
        self.canvas = Canvas(self.tk, width=500, height=500, highlightthickness=0)
        self.canvas.pack()
        self.tk.update()

        self.canvas_width = self.canvas.winfo_width()
        self.canvas_height = self.canvas.winfo_height()

        self.bg = PhotoImage(file="background.gif")
        self.bg_copy = PhotoImage(file="background_copy.gif")
        w = self.bg.width()
        h = self.bg.height()

        self.sprites = []
        self.running = True

        n_x = round(self.canvas_width / w)
        n_y = round(self.canvas_height / h)
        self.things = [
            PhotoImage(file="bookcase.gif"),
            PhotoImage(file="table.gif"),
            PhotoImage(file="table2.gif"),
            PhotoImage(file="torch.gif")
        ]

        for x in range(0, n_x):
            for y in range(0, n_y):
                if (x % 2 == 0 and y % 2 != 0) or (y % 2 == 0 and x % 2 != 0):
                    self.canvas.create_image(x * w, y * h, image=self.bg, anchor="nw")
                else:
                    self.canvas.create_image(x * w, y * h, image=self.bg_copy, anchor="nw")
        n = random.randrange(3, 7)
        for i in range(0, n):
            thing_image = random.choice(self.things)
            self.canvas.create_image(random.randrange(0, self.canvas_width), random.randrange(0, self.canvas_height),
                                     image=thing_image, anchor="center")

    def mainloop(self):
        while True:
            if self.running is True:
                for sprite in self.sprites:
                    sprite.move()
                self.tk.update()
                time.sleep(0.01)
            else:
                time.sleep(3)
                self.canvas.delete("all")
                self.canvas.create_text(200, 200, text="Вы победили!", fill="red", font="Courier 20")
                self.tk.update()


class Coords:
    def __init__(self, x1=0, y1=0, x2=0, y2=0):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2


class Sprite:
    def __init__(self, game):
        self.game = game
        self.endgame = False
        self.coordinates = None

    def move(self):
        pass

    def coords(self):
        return self.coordinates


class PlatformSprite(Sprite):
    def __init__(self, game, image_name, x, y):
        Sprite.__init__(self, game)
        self.photo_image = PhotoImage(file=image_name)
        self.image = self.game.canvas.create_image(x, y, image=self.photo_image, anchor="nw")
        self.width = self.photo_image.width()
        self.height = self.photo_image.height()
        self.coordinates = Coords(x, y, x + self.width, y + self.height)


class MovingPlatformSprite(Sprite):
    def __init__(self, game, image_name, x, y):
        Sprite.__init__(self, game)
        self.photo_image = PhotoImage(file=image_name)
        self.image = self.game.canvas.create_image(x, y, image=self.photo_image, anchor="nw")
        self.width = self.photo_image.width()
        self.height = self.photo_image.height()
        self.x = -1
        self.y = 0

    def move(self):
        self.game.canvas.move(self.image, self.x, self.y)
        self.pos = self.game.canvas.coords(self.image)
        self.coordinates = Coords(self.pos[0], self.pos[1], self.pos[0] + self.width, self.pos[1] + self.height)
        if self.pos[0] <= 0:
            self.x = 1
        if self.pos[0] + self.width >= self.game.canvas_width:
            self.x = -1


class StickFigureSprite(Sprite):
    def __init__(self, game):
        Sprite.__init__(self, game)
        self.images_left = [
            PhotoImage(file="figure-L1.gif"),
            PhotoImage(file="figure-L2.gif"),
            PhotoImage(file="figure-L3.gif")
        ]
        self.images_right = [
            PhotoImage(file="figure-R1.gif"),
            PhotoImage(file="figure-R2.gif"),
            PhotoImage(file="figure-R3.gif")
        ]
        self.image = self.game.canvas.create_image(200, 470, image=self.images_left[0], anchor="nw")
        self.x = -2
        self.y = 0
        self.current_image = 0
        self.current_image_add = 1
        self.jump_count = 0
        self.last_time = time.time()
        self.coordinates = Coords()
        self.game.canvas.bind_all("<KeyPress-Left>", self.turn_left)
        self.game.canvas.bind_all("<KeyPress-Right>", self.turn_right)
        self.game.canvas.bind_all("<space>", self.jump)

    def turn_left(self, event):
        if self.y == 0:
            self.x = -2

    def turn_right(self, event):
        if self.y == 0:
            self.x = 2

    def jump(self, event):
        if self.y == 0:
            self.y = -4
            self.jump_count = 0

    def animate(self):
        if self.x != 0 and self.y == 0:
            if time.time() - self.last_time > 0.1:
                self.current_image += self.current_image_add
                self.last_time = time.time()
                if self.current_image >= 2:
                    self.current_image_add = -1
                if self.current_image <= 0:
                    self.current_image_add = 1
        if self.x < 0:
            if self.y != 0:
                self.game.canvas.itemconfig(self.image, image=self.images_left[2])
            else:
                self.game.canvas.itemconfig(self.image, image=self.images_left[self.current_image])
        elif self.x > 0:
            if self.y != 0:
                self.game.canvas.itemconfig(self.image, image=self.images_right[2])
            else:
                self.game.canvas.itemconfig(self.image, image=self.images_right[self.current_image])

    def coords(self):
        xy = self.game.canvas.coords(self.image)
        self.coordinates.x1 = xy[0]
        self.coordinates.y1 = xy[1]
        self.coordinates.x2 = xy[0] + 27
        self.coordinates.y2 = xy[1] + 30
        return self.coordinates

    def move(self):
        self.animate()
        if self.y < 0:
            self.jump_count += 1
            if self.jump_count > 20:
                self.y = 4
        if self.y > 0:
            self.jump_count -= 1
        co = self.coords()
        left = True
        right = True
        top = True
        bottom = True
        falling = True
        if self.y > 0 and co.y2 >= self.game.canvas_height:
            self.y = 0
            bottom = False
        elif self.y < 0 and co.y1 <= 0:
            self.y = 0
            top = False
        if self.x > 0 and co.x2 >= self.game.canvas_width:
            self.x = 0
            right = False
        elif self.x < 0 and co.x1 <= 0:
            self.x = 0
            left = False
        for sprite in self.game.sprites:
            if sprite == self:
                continue
            sprite_co = sprite.coords()
            if top and self.y < 0 and collided_top(co, sprite_co):
                self.y = -self.y
                top = False
            if bottom and self.y > 0 and collided_bottom(self.y, co, sprite_co):
                self.y = sprite_co.y1 - co.y2
                if self.y < 0:
                    self.y = 0
                bottom = False
                top = False
            if bottom and falling and self.y == 0 and co.y2 < self.game.canvas_height \
                    and collided_bottom(1, co, sprite_co):
                falling = False
            if left and self.x < 0 and collided_left(co, sprite_co):
                self.x = 0
                left = False
                if sprite.endgame:
                    sprite.open()
                    self.game.canvas.delete(self.image)
                    self.game.running = False
            if right and self.x > 0 and collided_right(co, sprite_co):
                self.x = 0
                right = False
                if sprite.endgame:
                    sprite.open()
                    self.game.canvas.delete(self.image)
                    self.game.running = False
        if falling and bottom and self.y == 0 and co.y2 < self.game.canvas_height:
            self.y = 4
        self.game.canvas.move(self.image, self.x, self.y)


class DoorSprite(Sprite):
    def __init__(self, game, photo_image, x, y, width, height):
        Sprite.__init__(self, game)
        self.photo_image = photo_image
        self.image_opened = PhotoImage(file="door2.gif")
        self.image = self.game.canvas.create_image(x, y, image=self.photo_image, anchor="nw")
        self.coordinates = Coords(x, y, x + (width / 2), y + height)
        self.endgame = True

    def open(self):
        self.game.canvas.itemconfig(self.image, image=self.image_opened)


def within_x(coord1, coord2):
    if (coord2.x1 < coord1.x1 < coord2.x2) \
            or (coord2.x1 < coord1.x2 < coord2.x2) \
            or (coord1.x1 < coord2.x1 < coord1.x2) \
            or (coord1.x1 < coord2.x2 < coord1.x2):
        return True
    else:
        return False


def within_y(coord1, coord2):
    if (coord2.y1 < coord1.y1 < coord2.y2) \
            or (coord2.y1 < coord1.y2 < coord2.y2) \
            or (coord1.y1 < coord2.y1 < coord1.y2) \
            or (coord1.y1 < coord2.y2 < coord1.y2):
        return True
    else:
        return False


def collided_left(coord1, coord2):
    if within_y(coord1, coord2) is True:
        if coord2.x2 >= coord1.x1 >= coord2.x1:
            return True
    else:
        return False


def collided_right(coord1, coord2):
    if within_y(coord1, coord2) is True:
        if coord2.x2 >= coord1.x2 >= coord2.x1:
            return True
    else:
        return False


def collided_top(coord1, coord2):
    if within_x(coord1, coord2) is True:
        if coord2.y2 >= coord1.y1 >= coord2.y1:
            return True
    else:
        return False


def collided_bottom(y, coord1, coord2):
    if within_x(coord1, coord2) is True:
        y_calc = coord1.y2 + y
        if coord2.y2 >= y_calc >= coord2.y1:
            return True
    else:
        return False


g = Game()

platform1 = PlatformSprite(g, "platform1.gif", 0, 480)
platform2 = MovingPlatformSprite(g, "platform1.gif", 150, 440)
platform3 = PlatformSprite(g, "platform1.gif", 300, 400)
platform4 = PlatformSprite(g, "platform1.gif", 300, 160)
platform5 = PlatformSprite(g, "platform2.gif", 175, 350)
platform6 = PlatformSprite(g, "platform2.gif", 50, 300)
platform7 = PlatformSprite(g, "platform2.gif", 170, 120)
platform8 = PlatformSprite(g, "platform2.gif", 45, 60)
platform9 = PlatformSprite(g, "platform3.gif", 170, 250)
platform10 = PlatformSprite(g, "platform3.gif", 230, 200)

g.sprites.append(platform1)
g.sprites.append(platform2)
g.sprites.append(platform3)
g.sprites.append(platform4)
g.sprites.append(platform5)
g.sprites.append(platform6)
g.sprites.append(platform7)
g.sprites.append(platform8)
g.sprites.append(platform9)
g.sprites.append(platform10)

door = DoorSprite(g, PhotoImage(file="door1.gif"), 45, 30, 40, 35)
g.sprites.append(door)

sf = StickFigureSprite(g)
g.sprites.append(sf)

g.mainloop()
