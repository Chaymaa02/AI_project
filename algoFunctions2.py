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

qTable2 = np.zeros([27,3])

def get_action2(state, epsilon):
    global qTable2

    if epsilon == 0:
        qTable2 = np.array(   [[ -96.056632  ,  -77.937414   , -11.33747557],
                    [-126.12966848, -102.06198048 , -92.16756566],
                    [ -99.49102144,  -22.50396454 , -92.98547718],
                    [ -99.49102144 ,-101.82287278 ,  -9.74982887],
                    [ -12.56384913 , -14.94017472 , -17.87802068],
                    [ -12.45743696 , -93.53436545 ,-108.86076329],
                    [-168.0154613  , -11.48168025, -172.2263347 ],
                    [ -19.50480973 , -95.67005955, -104.60405515],
                    [ -17.76304439 , -68.20484732,  -72.29080771],
                    [-107.51986511 , -21.12997911 ,-101.42265311],
                    [-199.54008588, -198.75772376 ,-174.65808387],
                    [ -72.59822244 , -19.3235447  ,-106.59110196],
                    [-135.63812472, -132.49693141 , -18.17928435],
                    [ -14.176632 ,   -14.176632   , -13.56779871],
                    [ -20.89034224 , -20.89034224 ,  -6.32808631],
                    [ -21.4392027 ,  -99.7649144 , -104.63062653],
                    [ -14.05102144 , -14.05102144 , -13.03822543],
                    [ -81.4128132  , -85.72160864 , -14.92175882],
                    [ -30.39554591 , -96.21004118,  -34.95043571],
                    [-105.40216511 ,-125.0097597,   -85.19018536],
                    [-134.9270712  , -31.52537139, -132.49693141],
                    [ -26.71179376 , -92.40298507,  -26.28441485],
                    [ -19.0660289  , -15.36867586 , -25.76067715],
                    [-141.8368903 ,  -15.74794281, -138.75136141],
                    [-121.11550919 , -30.50023762, -124.13681472],
                    [ -20.89034224 , -15.65428168, -104.38398624],
                    [ -28.10204288 , -23.53961653, -103.05045998]])
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
