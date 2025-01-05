import pyxel

class Object(object):
    def __init__(self, x, y, img, imgx, imgy, w, h):
        """Inicializa um objeto com posição, imagem e dimensões."""
        self.x = x
        self.y = y
        self.img = img
        self.imgx = imgx
        self.imgy = imgy
        self.w = w
        self.h = h
        self.scores = 0

    def move(self, cond1, cond2, cond3=None, cond4=None):
        """Move o objeto com base nas condições fornecidas."""
        if (cond1 and self.y > 7):
            self.y -= 2
            
        if (cond2 and self.y + self.h <= pyxel.height - 9):
            self.y += 2
            
        if cond3:
            self.x -= 1
            
        if cond4:
            self.x += 1

    def check_collision(self, obj):
        """Verifica se este objeto colide com outro objeto."""
        if (self.y + self.h >= obj.y and
            self.y <= obj.y + obj.h):
            
            if (self.x + self.w >= obj.x and
                self.x <= obj.x + obj.w):
                return True

    def draw(self):
        """Desenha o objeto usando a função blt do pyxel."""
        pyxel.blt(self.x, self.y, self.img, self.imgx, self.imgy, self.w, self.h)

class Game:
    def __init__(self):
        """Inicializa o jogo, configura os objetos e inicia o pyxel."""
        pyxel.init(100, 100, "Pong")

        self.play = False
        self.pause = False
        self.modePlayer1 = True
        self.modePlayer2 = False
        
        self.CENTER_SCREEN_X = pyxel.width / 2
        self.CENTER_SCREEN_Y = pyxel.height / 2
        self.btnPlayer1 = Object(self.CENTER_SCREEN_X - 14, self.CENTER_SCREEN_Y + 20, 0, 32, 35, 32, 6)
        self.btnPlayer2 = Object(self.CENTER_SCREEN_X - 14, self.CENTER_SCREEN_Y + 30, 0, 0, 45, 32, 6)
        self.listButtons = [self.btnPlayer1, self.btnPlayer2]

        # Objetos
        self.player1 = Object(3, self.CENTER_SCREEN_Y - (15 / 2), 0, 64, 8, 5, 15)
        self.player2 = Object(pyxel.width - 8, self.CENTER_SCREEN_Y - (15 / 2), 0, 64, 8, 5, 15)
        self.ball = Object(self.CENTER_SCREEN_X - 3, self.CENTER_SCREEN_Y - 3, 0, 70, 8, 6, 6)
        self.ball.eixX1 = False
        self.ball.eixX2 = True
        self.ball.eixY1 = False
        self.ball.eixY2 = True

        self.list_objs = [self.player1, self.player2, self.ball]

        pyxel.load("assets/pong.pyxres")
        pyxel.run(self.update, self.draw)

    def reset(self):
        """Reinicia o jogo para o estado inicial."""
        self.ball.x, self.ball.y = self.CENTER_SCREEN_X - 3, self.CENTER_SCREEN_Y - 3
        self.player1.y = self.CENTER_SCREEN_Y - (15 / 2)
        self.player2.y = self.CENTER_SCREEN_Y - (15 / 2)
        self.player1.scores = 0
        self.player2.scores = 0
        self.pause = False
        self.play = False

    def flip_ball(self, obj):
        """Inverte a direção da bola com base na colisão com um objeto."""
        if self.ball.y < obj.y + obj.h / 2 - 3:
            self.ball.eixY1 = True
            self.ball.eixY2 = False
            
        elif self.ball.y + self.ball.h / 2 > obj.y + obj.h / 2 + 3:
            self.ball.eixY1 = False
            self.ball.eixY2 = True
            
        else:
            self.ball.eixY1 = False
            self.ball.eixY2 = False

    def move_objects(self):
        self.player1.move(cond1= (pyxel.btn(pyxel.KEY_W) or
                                  pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP)),
                          cond2= (pyxel.btn(pyxel.KEY_S) or
                                  pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN)))

        if self.modePlayer1:
            self.player2.move(cond1= self.player2.y + 7 > self.ball.y,
                              cond2= self.player2.y + 7 < self.ball.y)
            
        elif self.modePlayer2:
            self.player2.move(cond1= (pyxel.btn(pyxel.KEY_UP) or
                                      pyxel.btn(pyxel.GAMEPAD2_BUTTON_DPAD_UP)),
                              cond2= (pyxel.btn(pyxel.KEY_DOWN) or
                                      pyxel.btn(pyxel.GAMEPAD2_BUTTON_DPAD_DOWN)))

        self.ball.move(cond1= self.ball.eixY1,
                       cond2= self.ball.eixY2,
                       cond3= self.ball.eixX1,
                       cond4= self.ball.eixX2)

    def check_object_collisions(self):
        if self.ball.check_collision(self.player1):
            self.ball.eixX1 = False
            self.ball.eixX2 = True
            self.flip_ball(self.player1)
            pyxel.play(0, 0)

        if self.ball.check_collision(self.player2):
            self.ball.eixX1 = True
            self.ball.eixX2 = False
            self.flip_ball(self.player2)
            pyxel.play(0, 0)

        if self.ball.y >= pyxel.height - self.ball.h - 7:
            self.ball.eixY1 = True
            self.ball.eixY2 = False
            pyxel.play(0, 0)

        if self.ball.y <= 7:
            self.ball.eixY1 = False
            self.ball.eixY2 = True
            pyxel.play(0, 0)

    def check_score(self):
        if self.ball.x < -3:
            self.ball.x = self.CENTER_SCREEN_X - 3
            self.ball.y = self.CENTER_SCREEN_Y - 3
            self.player2.scores += 1
            pyxel.play(1, 1)

        if self.ball.x > pyxel.width:
            self.ball.x = self.CENTER_SCREEN_X - 3
            self.ball.y = self.CENTER_SCREEN_Y - 3
            self.player1.scores += 1
            pyxel.play(1, 1)

    def update(self):
        """Atualiza o estado do jogo e trata a entrada do jogador."""
        if self.play:
            if not self.pause:
                self.move_objects()
                self.check_object_collisions()
                self.check_score()

                for obj in self.list_objs:
                    if obj.scores == 5:
                        self.pause = True

            if self.pause:
                if (pyxel.btnr(pyxel.KEY_RETURN) or
                    pyxel.btnr(pyxel.KEY_KP_ENTER) or
                    pyxel.btnr(pyxel.GAMEPAD1_BUTTON_A)):
                    self.reset()

            if (pyxel.btn(pyxel.KEY_R) or
               pyxel.btnr(pyxel.GAMEPAD1_BUTTON_A)):
                self.reset()

        else:
            if (pyxel.btnp(pyxel.KEY_UP) or
                pyxel.btnp(pyxel.KEY_W) or
                pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP)):
                
                self.btnPlayer1.imgx = 32
                self.btnPlayer2.imgx = 0
                self.modePlayer2 = False
                self.modePlayer1 = True
                pyxel.play(0, 0)

            if (pyxel.btnp(pyxel.KEY_DOWN) or
                pyxel.btnp(pyxel.KEY_S) or
                pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN)):
                
                self.btnPlayer2.imgx = 32
                self.btnPlayer1.imgx = 0
                self.modePlayer1 = False
                self.modePlayer2 = True
                pyxel.play(0, 0)

            if (pyxel.btnr(pyxel.KEY_RETURN) or
                pyxel.btnr(pyxel.KEY_KP_ENTER) or
                pyxel.btnr(pyxel.GAMEPAD1_BUTTON_A)):
                self.play = True

    def draw(self):
        """Desenha o estado atual do jogo na tela."""
        pyxel.cls(1)
        pyxel.blt(0, 0, 0, 0, 0, 110, 7)
        pyxel.blt(0, pyxel.height - 7, 0, 0, 0, 110, 7)
        for obj in self.list_objs:
            obj.draw()

            if obj.scores == 5:
                if obj.x < self.CENTER_SCREEN_X:
                    TXT = "Player 1 winner!"
                    CENTER_TXT = len(TXT) / 2 * pyxel.FONT_WIDTH
                    
                else:
                    TXT = "Player 2 winner!"
                    CENTER_TXT = len(TXT) / 2 * pyxel.FONT_WIDTH
                    
                TXT2 = "Start to return"
                CENTER_TXT2 = len(TXT2) /2 * pyxel.FONT_WIDTH
                pyxel.text((self.CENTER_SCREEN_X - CENTER_TXT) +1, 20, TXT, pyxel.frame_count % 16)
                pyxel.text(self.CENTER_SCREEN_X - CENTER_TXT2, 28, TXT2, 7)

        if self.play:
            # Cálculo das posições dos pontos dos jogadores
            TXT1 = str(self.player1.scores)
            TXT2 = str(self.player2.scores)
            CENTER_PLAYER1_SCORE = len(TXT1) / 2 * pyxel.FONT_WIDTH
            CENTER_PLAYER2_SCORE = len(TXT2) / 2 * pyxel.FONT_WIDTH 
            pyxel.text(self.CENTER_SCREEN_X - 7 - CENTER_PLAYER1_SCORE, 10, TXT1, 7)
            pyxel.text(self.CENTER_SCREEN_X + 7 - CENTER_PLAYER2_SCORE, 10, TXT2, 7)

        else:
            CENTER_POSX = self.CENTER_SCREEN_X - 62 / 2
            CENTER_POSY = self.CENTER_SCREEN_Y - (20 / 2)
            pyxel.blt(CENTER_POSX, CENTER_POSY, 0, 0, 8, 62, 22)
            for btn in self.listButtons:
                btn.draw()

if __name__ == "__main__":
    Game()
