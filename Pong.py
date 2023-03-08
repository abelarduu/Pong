########
# PONG #
########
#Importações necessárias
import pyxel

#Objetos
""" 
    #OBJECTS
    
    Classe padronizada para criação de:
        .Players
        .ball
"""
class Object(object):
    def __init__(self, x:int, y:int, width:int, height:int, color:int):
        self.x, self.y = x,y
        self.width, self.height= width, height
        self.color, self.score= color, 0
        self.flipX,self.flipY = False, False
    
    """
        #FUNÇÂO DE MOVIMENTAÇÃO DO OBJETO
        Se o objeto sair dos limites da tela, mova-o para dentro.
        (limita a movimentação do objeto apenas dentro dos limites da tela)
        Ex:     
            Se houver interações para movimentação do Objeto para cima e se ele estiver nos limites superior da tela:
                mova-o para cima
                
            Se houver interações para movimentação do Objeto para Baixo e se ele estiver nos limites superior da tela:
                mova-o para baixo
    """
    def move(self, cond1, cond2,cond4=None, cond5=None):
        #Button Up
        if cond1 and self.y >= 0:
            self.y-=2
        #Button Down
        if cond2 and self.y + self.height <= pyxel.height:
            self.y+=2
            

    """
        #FUNÇÃO DE VERIFICAÇÃO DE COLISÃO
        Verifica se há colisões com o objeto no eixo X/Y
        Ex: 
            Para cada objeto contido na Lista de objetos:
                Se a direção do objeto não foi virado:
                    Se o objeto colidir com algo no eixo Y:
                        se o objeto com algo no eixo X:
                            Vire/Mude a direção
                            
                Se a direção do objeto já foi virado:
                    Se o objeto colidir com algo no eixo Y:
                        se o objeto com algo no eixo X:
                            Vire/Mude a direção
    """
    def collision(self,objList: list):
        #Verificação de colisão com cada objeto da lista
        for obj in objList:
            #Verificação de colisão no eixo X
            if self.flipX:
                if self.y >= obj.y and self.y <= obj.y + obj.height:
                    if self.x>= obj.x and self.x <= obj.x + obj.width:
                        self.flipX = False
            else: 
                if self.y >= obj.y and self.y < obj.y + obj.height:
                    if self.x>= obj.x and self.x <= obj.x + obj.width:
                        self.flipX= True
            #Verificação de colisão no eixo Y
            if self.y<= 0: self.flipY=True
            if self.y>= pyxel.height:self.flipY=False
            #inversão das direções no eixo X
            if self.flipX: self.x+=0.5
            elif not self.flipX: self.x-=0.5
            #inversão das direções no eixo Y
            if self.flipY:
                self.y+=0.5
            elif not self.flipY:
                self.y-=0.5
    """
        #FUNÇÃO DE ATUALIZAÇÃO DO OBJETO NA INTERFACE
        Desenha e atualiza o objeto na interface a cada quadro
    """
    def draw(self):
        pyxel.rect(self.x,self.y,self.width,self.height, self.color)
#======================================================================================================================================================================================
# Main
#======================================================================================================================================================================================
class Game:
    def __init__(self):
        #Inicializa o aplicativo Pyxel e seus Módulos
        pyxel.init(100,100,title="Pong")
        #Declarando variáveis
        self.player1= Object(5,40, 5,15,7)
        self.player2= Object(pyxel.width -10, 40, 5,15,7)
        self.ball=Object(pyxel.width/2,pyxel.height/2, 3,3,7)
        self.entityList= [self.player1, self.player2, self.ball]
        #Ligando métodos principais
        pyxel.run(self.update, self.draw)

    #Verificação de interação por quadro
    def update(self):
        #Movimento/interações
        self.player1.move(cond1= pyxel.btn(pyxel.KEY_W),cond2= pyxel.btn(pyxel.KEY_S))
        self.player2.move(cond1= pyxel.btn(pyxel.KEY_UP), cond2= pyxel.btn(pyxel.KEY_DOWN))
        self.ball.collision([self.player1,self.player2])
        
    #Atualização da interface a cada quadro
    def draw(self):
        pyxel.cls(0)
        #Iserindo/Desenhando Objetos na tela
        for entity in self.entityList:
            entity.draw()
##########################################
#Verificação da execução direta do módulo#
##########################################
if __name__== "__main__":
    Game()
'''
    ##################################
    #copia do pong criado em 11/11/22#
    ##################################
'''