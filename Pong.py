########
# PONG #
########
import pyxel

class Object(object):
    def __init__(self, x:int, y:int, img:int, imgx:int, imgy:int, w:int, h:int):
        self.x= x
        self.y= y
        self.img= img
        self.imgx= imgx
        self.imgy= imgy
        self.w= w
        self.h= h
        
    def move(self, cond1, cond2, cond3=None, cond4=None):
        if cond1 and self.y >7: self.y-=2                     
        if cond2 and self.y + self.h <= pyxel.height-9: self.y+=2 
        if cond3: self.x-=1                                  
        if cond4: self.x+=1                                     

    def check_collision(self, obj):
        if self.y >= obj.y and self.y<= obj.y +obj.h:
            if self.x +self.w >= obj.x and self.x<= obj.x + obj.w:
                return True

    def draw(self):
        pyxel.blt(self.x, self.y, self.img, self.imgx, self.imgy, self.w, self.h)

class Game:
    def __init__(self):
        pyxel.init(100,100,"Pong")
        
        self.play= False
        self.modePlayer1= True
        self.modePlayer2= False
        self.btnPlayer1= Object(pyxel.width/2 - 14, pyxel.height/2 + 20, 0, 32, 35, 32, 6)
        self.btnPlayer2= Object(pyxel.width/2 - 14, pyxel.height/2 + 30, 0, 0, 45, 32, 6)
        self.listButtons= [self.btnPlayer1, self.btnPlayer2]
        #Objetos
        self.player1= Object(3, pyxel.height/2 - (15/2),0, 64, 8, 5, 15)
        self.player2= Object(pyxel.width -8, pyxel.height/2 - (15/2), 0, 64, 8, 5, 15)
        self.ball= Object(pyxel.width/2 -3, pyxel.height/2 -3, 0, 70, 8, 6, 6)
        self.ball.eixX1= False
        self.ball.eixX2= True
        self.ball.eixY1= False
        self.ball.eixY2= True
        self.listObject= [self.player1, self.player2, self.ball]
        
        pyxel.load("resources/pong.pyxres")
        pyxel.run(self.update, self.draw)
        
    def reset(self):
        self.ball.x, self.ball.y= pyxel.width/2 -3, pyxel.height/2 -3
        self.player1.y= pyxel.height/2 - (15/2)
        self.player2.y= pyxel.height/2 - (15/2)
        self.play= False
        
    def update(self):
        if self.play:
            self.player1.move(cond1= pyxel.btn(pyxel.KEY_W), cond2= pyxel.btn(pyxel.KEY_S))
            if self.modePlayer1: self.player2.move(cond1= self.player2.y+ 7 > self.ball.y, cond2= self.player2.y+7 < self.ball.y)
            if self.modePlayer2: self.player2.move(cond1= pyxel.btn(pyxel.KEY_UP), cond2= pyxel.btn(pyxel.KEY_DOWN))
            self.ball.move(cond1= self.ball.eixY1, cond2= self.ball.eixY2,cond3= self.ball.eixX1, cond4= self.ball.eixX2)

            self.ball.check_collision(self.player1)
            self.ball.check_collision(self.player2)

            if self.ball.y >= pyxel.height - self.ball.h-7: 
                self.ball.eixY1= True
                self.ball.eixY2=False  
                
            if self.ball.y <= 7:
                self.ball.eixY1=False
                self.ball.eixY2 =True

            if self.ball.check_collision(self.player1):
                self.ball.eixX1=False
                self.ball.eixX2 =True   
                
            if self.ball.check_collision(self.player2): 
                self.ball.eixX1= True
                self.ball.eixX2=False 
                
            if pyxel.btn(pyxel.KEY_R):
                self.reset()
        else:

            if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.KEY_W):
                self.btnPlayer1.imgx=32
                self.btnPlayer2.imgx=0
                self.modePlayer2= False  
                self.modePlayer1= True  

            if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.KEY_S):
                self.btnPlayer2.imgx=32
                self.btnPlayer1.imgx=0
                self.modePlayer1=False
                self.modePlayer2=True
                
            if pyxel.btnr(pyxel.KEY_KP_ENTER):
                self.play= True
                
    def draw(self):
        pyxel.cls(1)
        pyxel.blt(0,0,0,0,0,110,7)
        pyxel.blt(0,pyxel.height-7,0,0,0,110,7)
        
        for obj in self.listObject:
            obj.draw()
            
        if not self.play:
            pyxel.blt(pyxel.width/2 - 62/2,pyxel.height/2 - (20/2),0,0,8,62,22)
            for btn in self.listButtons:
                btn.draw()
            
if __name__ == "__main__":
    Game()