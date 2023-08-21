########
# PONG #
########
import pyxel

class Object(object):
    def __init__(self, x:int, y:int, w:int, h:int,col:int):
        self.x= x
        self.y= y
        self.w= w
        self.h = h
        self.col= col
        
    def move(self, cond1, cond2, cond3=None, cond4=None):
        if cond1 and self.y >3: self.y-=2                     
        if cond2 and self.y + self.h <= pyxel.height: self.y+=2 
        if cond3: self.x-=1                                  
        if cond4: self.x+=1                                     

    def check_collision(self, obj):
        if self.y >= obj.y and self.y<=obj.y +obj.h:
            if self.x +self.w >= obj.x and self.x<= obj.x + obj.w:
                return True

    def draw(self):
        pyxel.rect(self.x, self.y, self.w, self.h, self.col)

class Game:
    def __init__(self):
        pyxel.init(100,100,"Pong")
        self.play= False
        #Objetos
        self.player1= Object(3, pyxel.height/2 - (15/2), 5, 15, 7)
        self.player2= Object(pyxel.width -8, pyxel.height/2 - (15/2), 5, 15, 7)
        
        self.ball= Object(pyxel.width/2 -3, pyxel.height/2 -3, 3, 3, 7)
        self.ball.eixX1, self.ball.eixX2= False,True
        self.ball.eixY1, self.ball.eixY2= False,True
        self.listObject= [self.player1, self.player2, self.ball]
        
        pyxel.load("resources/pong.pyxres")
        pyxel.run(self.update, self.draw)
        
    def update(self):
        if self.play:
            self.player1.move(cond1= pyxel.btn(pyxel.KEY_W), cond2= pyxel.btn(pyxel.KEY_S))
            self.player2.move(cond1= pyxel.btn(pyxel.KEY_UP), cond2= pyxel.btn(pyxel.KEY_DOWN))
            self.ball.move(cond1= self.ball.eixY1, cond2= self.ball.eixY2,cond3= self.ball.eixX1, cond4= self.ball.eixX2)

            self.ball.check_collision(self.player1)
            self.ball.check_collision(self.player2)

            if self.ball.y >= pyxel.height - self.ball.h-3: 
                self.ball.eixY1= True
                self.ball.eixY2=False  
            if self.ball.y <= 3:
                self.ball.eixY1=False
                self.ball.eixY2 =True

            if self.ball.check_collision(self.player1):
                self.ball.eixX1=False
                self.ball.eixX2 =True   
            if self.ball.check_collision(self.player2): 
                self.ball.eixX1= True
                self.ball.eixX2=False  
               
            if pyxel.btn(pyxel.KEY_R):
                self.ball.x, self.ball.y= pyxel.width/2 -3, pyxel.height/2 -3
        else:
            if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):
                self.play= True
    def draw(self):
        pyxel.cls(0)
        pyxel.mouse(True)
        

        pyxel.rect(0,0,pyxel.width,3,7)
        pyxel.rect(0,pyxel.height-3,pyxel.width,3,7)
        
        for obj in self.listObject:
            obj.draw()
            
        if not self.play:
            pyxel.blt(pyxel.width/2 - 62/2,pyxel.height/2 - 22/2,0,0,0,62,20)
            pyxel.text(pyxel.width/2 - len("player1")/2 *4, pyxel.height/2 + 20,"player1",7)#pyxel.frame_count % 16)15
            pyxel.text(pyxel.width/2 - len("player2")/2 *4, pyxel.height/2 +30,"player2", 7)#pyxel.frame_count % 16)25


if __name__ == "__main__":
    Game()