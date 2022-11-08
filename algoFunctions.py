import random
import numpy as np
import pygame

# shape parameters
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 800
# animation parameters
SPEED = 20
#score parameter
max_score = 0

epsilon_min = 0.001
epsilon_decay = 0.9

Data = []
qTable = np.zeros([9,3])

def get_action(state, epsilon):
    global qTable
    if epsilon == 0:
        qTable = np.array( [[  0.       ,   21.10985742  , 0.        ],
                    [ 72.16789991 ,-69.32512334 ,  0.        ],
                    [  0.         , 24.11416627 , -0.203721  ],
                    [ 83.65503477 ,  0.          , 7.7331119 ],
                    [  0.         ,  0.         , 29.75941503],
                    [  6.70809565  , 3.74857549 ,  1.69514176],
                    [  0.          , 0.          , 0.        ],
                    [  0.         ,  0.          , 0.        ],
                    [ -0.105821   ,  0.9879      ,-0.89      ]])
        action = np.argmax(qTable[state.get_state(), :])
    else :  
        if random.uniform(0, 1) < epsilon:
            action = random.randrange(3)
        else:
            action = np.argmax(qTable[state.get_state(), :])
    return action


def get_reward(player, enemies):
    #Collision between the player and enemy
    if pygame.sprite.spritecollideany(player, enemies):
        return -100
    else :
        for enemy in enemies :
            #if the player is under the enemy
            if enemy.position == player.position :
                return -1
            #if the player skipped the enemy(car)
            elif enemy.rect.center[1] == SCREEN_HEIGHT * 0.9:
                return 2
            else :
                return 1 
   
class State:
    # we have 4 states
    def __init__(self, player, enemy):
        self.p = player.position 
        self.e = enemy.position

    def get_state(self):
        if self.p ==0 and self.e ==0 :
            return 0
        elif self.p ==0 and self.e ==1 :
            return 1
        elif self.p ==0 and self.e ==2 :
            return 2
        elif self.p ==1 and self.e ==0 :
            return 3
        elif self.p ==1 and self.e ==1 :
            return 4
        elif self.p ==1 and self.e ==2 :
            return 5
        elif self.p ==2 and self.e ==0 :
            return 6
        elif self.p ==2 and self.e ==1 :
            return 7
        elif self.p ==2 and self.e ==2 :
            return 8
        