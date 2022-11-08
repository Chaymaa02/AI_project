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
qTable2 = np.zeros([27,3])

def get_action2(state, epsilon):
    global qTable2

    if epsilon == 0:
        qTable2 = np.array( [[  0.       ,   21.10985742  , 0.        ],
                    [ 72.16789991 ,-69.32512334 ,  0.        ],
                    [  0.         , 24.11416627 , -0.203721  ],
                    [ 83.65503477 ,  0.          , 7.7331119 ],
                    [  0.         ,  0.         , 29.75941503],
                    [  6.70809565  , 3.74857549 ,  1.69514176],
                    [  0.          , 0.          , 0.        ],
                    [  0.         ,  0.          , 0.        ],
                    [ -0.105821   ,  0.9879      ,-0.89      ]])
        action = np.argmax(qTable2[state.get_state(), :])
    else :  
        if random.uniform(0, 1) < epsilon:
            action = random.randrange(3)
        else:
            action = np.argmax(qTable2[state.get_state(), :])
    return action


def get_reward2(player, enemies):
    reward = 0
    #Collision between the player and enemy
    if pygame.sprite.spritecollideany(player, enemies):
        return -100
    else :
        for enemy in enemies :
            #if the player is under the enemy
            if enemy.position == player.position :
                reward -= 4

            # #if the player is under the enemy
            # if enemies.sprites()[0].position == player.position :
            #     return -1
            # elif enemies.sprites()[1].position == player.position :
            #     return -1 

            #if the player skipped the enemy(car)
            elif enemies.sprites()[0].rect.center[1] == SCREEN_HEIGHT * 0.85:
                reward = 10
            else :
                reward += 0
        return reward

   

class State2:
    # we have 27 states
    def __init__(self, player, enemies):
        self.p = player.position
        self.e1 = enemies.sprites()[0].position
        self.e2 = enemies.sprites()[1].position

    def get_state(self):
        if self.p ==0 and self.e1 ==0 and self.e2==0 :
            return 0
        if self.p ==0 and self.e1 ==1 and self.e2==0 :
            return 1
        if self.p ==0 and self.e1 ==2 and self.e2==0 :
            return 2

        if self.p ==0 and self.e1 ==0 and self.e2==1 :
            return 3
        if self.p ==0 and self.e1 ==1 and self.e2==1 :
            return 4
        if self.p ==0 and self.e1 ==2 and self.e2==1 :
            return 5
        
        if self.p ==0 and self.e1 ==0 and self.e2==2 :
            return 6
        if self.p ==0 and self.e1 ==1 and self.e2==2 :
            return 7
        if self.p ==0 and self.e1 ==2 and self.e2==2 :
            return 8
        ##
        if self.p ==1 and self.e1 ==0 and self.e2==0 :
            return 9
        if self.p ==1 and self.e1 ==1 and self.e2==0 :
            return 10
        if self.p ==1 and self.e1 ==2 and self.e2==0 :
            return 11

        if self.p ==1 and self.e1 ==0 and self.e2==1 :
            return 12
        if self.p ==1 and self.e1 ==1 and self.e2==1 :
            return 13
        if self.p ==1 and self.e1 ==2 and self.e2==1 :
            return 14
        
        if self.p ==1 and self.e1 ==0 and self.e2==2 :
            return 15
        if self.p ==1 and self.e1 ==1 and self.e2==2 :
            return 16
        if self.p ==1 and self.e1 ==2 and self.e2==2 :
            return 17
        ##
        if self.p ==2 and self.e1 ==0 and self.e2==0 :
            return 18
        if self.p ==2 and self.e1 ==1 and self.e2==0 :
            return 19
        if self.p ==2 and self.e1 ==2 and self.e2==0 :
            return 20

        if self.p ==2 and self.e1 ==0 and self.e2==1 :
            return 21
        if self.p ==2 and self.e1 ==1 and self.e2==1 :
            return 22
        if self.p ==2 and self.e1 ==2 and self.e2==1 :
            return 23
        
        if self.p ==2 and self.e1 ==0 and self.e2==2 :
            return 24
        if self.p ==2 and self.e1 ==1 and self.e2==2 :
            return 25
        if self.p ==2 and self.e1 ==2 and self.e2==2 :
            return 26
