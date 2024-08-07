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
        if cond1 and self.y > 7:
            self.y -= 2
        if cond2 and self.y + self.h <= pyxel.height - 9:
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
        self.btnPlayer1 = Object(pyxel.width / 2 - 14, pyxel.height / 2 + 20, 0, 32, 35, 32, 6)
        self.btnPlayer2 = Object(pyxel.width / 2 - 14, pyxel.height / 2 + 30, 0, 0, 45, 32, 6)
        self.listButtons = [self.btnPlayer1, self.btnPlayer2]

        # Objetos
        self.player1 = Object(3, pyxel.height / 2 - (15 / 2), 0, 64, 8, 5, 15)
        self.player2 = Object(pyxel.width - 8, pyxel.height / 2 - (15 / 2), 0, 64, 8, 5, 15)
        self.ball = Object(pyxel.width / 2 - 3, pyxel.height / 2 - 3, 0, 70, 8, 6, 6)
        self.ball.eixX1 = False
        self.ball.eixX2 = True
        self.ball.eixY1 = False
        self.ball.eixY2 = True

        self.listObjects = [self.player1, self.player2, self.ball]

        pyxel.load("assets/pong.pyxres")
        pyxel.run(self.update, self.draw)

    def reset(self):
        """Reinicia o jogo para o estado inicial."""
        self.ball.x, self.ball.y = pyxel.width / 2 - 3, pyxel.height / 2 - 3
        self.player1.y = pyxel.height / 2 - (15 / 2)
        self.player2.y = pyxel.height / 2 - (15 / 2)
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

    def update(self):
        """Atualiza o estado do jogo e trata a entrada do jogador."""
        if self.play:
            if not self.pause:
                self.player1.move(
                    cond1=pyxel.btn(pyxel.KEY_W),
                    cond2=pyxel.btn(pyxel.KEY_S)
                )

                if self.modePlayer1:
                    self.player2.move(
                        cond1=self.player2.y + 7 > self.ball.y,
                        cond2=self.player2.y + 7 < self.ball.y
                    )
                elif self.modePlayer2:
                    self.player2.move(
                        cond1=pyxel.btn(pyxel.KEY_UP),
                        cond2=pyxel.btn(pyxel.KEY_DOWN)
                    )

                self.ball.move(
                    cond1=self.ball.eixY1,
                    cond2=self.ball.eixY2,
                    cond3=self.ball.eixX1,
                    cond4=self.ball.eixX2
                )

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

                if self.ball.x < -3:
                    self.ball.x, self.ball.y = pyxel.width / 2 - 3, pyxel.height / 2 - 3
                    self.player2.scores += 1
                    pyxel.play(1, 1)

                if self.ball.x > pyxel.width:
                    self.ball.x, self.ball.y = pyxel.width / 2 - 3, pyxel.height / 2 - 3
                    self.player1.scores += 1
                    pyxel.play(1, 1)

                for obj in self.listObjects:
                    obj.draw()
                    if obj.scores == 5:
                        self.pause = True

            if pyxel.btn(pyxel.KEY_R):
                self.reset()

        else:
            if (pyxel.btnp(pyxel.KEY_UP) or
                pyxel.btnp(pyxel.KEY_W)):
                
                self.btnPlayer1.imgx = 32
                self.btnPlayer2.imgx = 0
                self.modePlayer2 = False
                self.modePlayer1 = True
                pyxel.play(0, 0)

            if (pyxel.btnp(pyxel.KEY_DOWN) or
                pyxel.btnp(pyxel.KEY_S)):
                
                self.btnPlayer2.imgx = 32
                self.btnPlayer1.imgx = 0
                self.modePlayer1 = False
                self.modePlayer2 = True
                pyxel.play(0, 0)

            if pyxel.btnr(pyxel.KEY_RETURN):
                self.play = True

    def draw(self):
        """Desenha o estado atual do jogo na tela."""
        pyxel.cls(1)
        pyxel.blt(0, 0, 0, 0, 0, 110, 7)
        pyxel.blt(0, pyxel.height - 7, 0, 0, 0, 110, 7)

        for obj in self.listObjects:
            obj.draw()
            if obj.scores == 5:
                if obj.x < pyxel.width / 2:
                    TXT = "Player 1 Ganhou!"
                    CENTER_TXT = len(TXT) / 2 * pyxel.FONT_WIDTH
                else:
                    TXT = "Player 2 Ganhou!"
                    CENTER_TXT = len(TXT) / 2 * pyxel.FONT_WIDTH
                
                pyxel.text(pyxel.width / 2 + 2 - CENTER_TXT, 20, TXT, pyxel.frame_count % 16)

        if self.play:
            # Cálculo das posições dos pontos dos jogadores
            TXT1 = str(self.player1.scores)
            TXT2 = str(self.player2.scores)
            CENTER_PLAYER1_SCORE = len(TXT1) / 2 * pyxel.FONT_WIDTH
            CENTER_PLAYER2_SCORE = len(TXT2) / 2 * pyxel.FONT_WIDTH 
            pyxel.text(pyxel.width / 2 - 7 - CENTER_PLAYER1_SCORE, 10, TXT1, 7)
            pyxel.text(pyxel.width / 2 + 7 - CENTER_PLAYER2_SCORE, 10, TXT2, 7)

        else:
            pyxel.blt(pyxel.width / 2 - 62 / 2, pyxel.height / 2 - (20 / 2), 0, 0, 8, 62, 22)
            for btn in self.listButtons:
                btn.draw()

if __name__ == "__main__":
    Game()