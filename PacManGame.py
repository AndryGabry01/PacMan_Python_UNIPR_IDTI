#!/usr/bin/env python3

from random import choice
from time import time
from PacMan import Actor, Arena, Biscotto, Bonus, Ghost, PacMan

class PacManGame:
    def __init__(self):
        #mappa del gioco         
        self._board =  ["#############################",
                        "#             #             #",
                        "# ------------# ------------#",
                        "# -### -#### -# -#### -### -#",
                        "# +### -#### -# -#### -### +#",
                        "# -    -     -  -     -    -#",
                        "# --------------------------#",
                        "# -### -# -####### -# -### -#",
                        "# -    -# -   #    -# -    -#",
                        "# ------# ----# ----# ------#",
                        "###### -####  #  #### -######",
                        "###### -#           # -######",
                        "###### -#           # -######",
                        "###### -#  #######  # -######",
                        "       -   #######    -      ",
                        "       -   #######    -      ",
                        "###### -#  #######  # -######",
                        "###### -#           # -######",
                        "###### -#     $     # -######",
                        "###### -#  #######  # -######",
                        "#      -      #       -     #",
                        "# ------------# ------------#",
                        "# -### -#### -# -#### -### -#",
                        "# -  # -     -  -     -#   -#",
                        "# +--# -------  -------# --+#",
                        "### -# -# -####### -# -# -###",
                        "#   -  -# -   #    -# -  -  #",
                        "# ------# ----# ----# ------#",
                        "# -######### -# -######### -#",
                        "# -          -  -          -#",
                        "# --------------------------#",
                        "#############################"]
        #Game Setting
        self._arena = Arena((232, 256))
        self._eating_time = 0
        self._EATDURATION = 200
        self._bonus_time = 200
        self._heros_life = 2
        self.BEAV_GHOST_TIME = 500
        self._behavor_ghost_timer = self.BEAV_GHOST_TIME 

        #biscotto normale = 10 punt
        #super biscotto = 50
        #bonus = 150
        #eat_ghost = 100
        self._score = 0

        #Istance Biscotti +/-
        self.biscotti = self.biscotti_pos()
        nbiscotti = 0
        for biscotto in self.biscotti:
            type,pos = biscotto
            Biscotto(type, self._arena, self, pos)
            if type == 0:
                nbiscotti += 1
        self._remaining_biscotti = nbiscotti
        
        #Istance Bonus $
        bonuslist = self.bonus_pos()
        NUMERO_BONUS = 8
        BONUS_SYMBX_INIZIALE = 33
        SYMB_W = 16
        bonus_symbl_x_list = []
        BONUS_SYMVL_Y = 48
        for i in range(0, NUMERO_BONUS):
            bonus_symbl_x_list.append(BONUS_SYMBX_INIZIALE + (SYMB_W * i))
        for bonus in bonuslist:
            pos = bonus
            Bonus(self._arena, self, pos, bonus_symbl_x_list, BONUS_SYMVL_Y)

        #Istance Ghost        
        self._ghost = [
            #Ghost(self._arena, self, 0, 0, (20, 0), 1, (160,40)),
            Ghost(self._arena, self, 0, 0, (20, 0), 1, (112,88)),
            Ghost(self._arena, self, 1, 20, (210, 0), 2, (112,88)),
            Ghost(self._arena, self, 2, 40, (210, 256), 1, (112,88)),
            Ghost(self._arena, self, 3, 60, (20, 256), 2, (112,88))
        ]
        #Istance Heros
        self._heros =[
            PacMan(self._arena, self, (120, 184), ["ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight"]),
            PacMan(self._arena, self, (96, 184), ["w", "s", "a", "d"])
            ]

    
    def arena(self) -> Arena:
        return self._arena
    
    #Gestione Biscotti ed Eating time (tempo in cui i fantasmi possono essere mangiati)
    def get_eating_duration(self) -> int:
        return self._EATDURATION
        
    def eat_biscotti(self):
        if self._remaining_biscotti > 0:
            self._remaining_biscotti -= 1
    
    def set_eating_time(self, time: int):
        self._eating_time = time

    def get_eating_time(self) ->int:
        return self._eating_time 

    def eating_counter(self):
        if self._eating_time > 1:
            self._eating_time -= 1
            for ghost in self._ghost:
                ghost.eatable_status(True)
            for hero in self._heros:
                hero.eating_status(True)
        elif self._eating_time == 1:
            self._eating_time -= 1
            for hero in self._heros:
                hero.eating_status(False)
            for ghost in self._ghost:
                ghost.eatable_status(False)
        
    #Gestione bonus
    def set_bonus_time(self, time: int):
        self._bonus_time = time
    def get_bonus_time(self) ->int:
        return self._bonus_time 


    #Gestione Heros
    def hero(self, index) -> PacMan:
        return self._heros[index]
    def heros(self) -> list:
        return self._heros


    #Gestione Game
    def game_over(self) -> bool:
        return self._heros_life <= 0

    def game_won(self) -> bool:
        return self._remaining_biscotti == 0

    def remove_life(self) -> int:
        self._heros_life -= 1
    
    def remaining_life(self) -> int:
        return  self._heros_life

    def remaining_biscotti(self) -> int:
        return self._remaining_biscotti

    def behavor_ghost_timer(self):
        if self._behavor_ghost_timer == 0:
            self._behavor_ghost_timer = self.BEAV_GHOST_TIME
            for ghost in self._ghost:
                ghost.set_behavor()
        else:
            self._behavor_ghost_timer -=1
        

    def inc_score(self, add_score: int):
        self._score += add_score

    def get_score(self) -> int:
        return self._score
    


    #Gestione Mappa ed posizioni elementi in essa
    def in_wall(self, x: int, y: int) -> bool:
        #r, c, w, h = x//8, y//8, 3 if x%8 else 2, 3 if y%8 else 2
        c, r, w, h = x//8, y//8, 3 if x%8 else 2, 3 if y%8 else 2
        return "#" in "".join(line[c:c+w] for line in self._board[r:r+h])

    def biscotti_pos(self):
        listaBiscotti = []
        c,r = 0,0
        SPAZIO_POS = 8
        for line in self._board:
            c = 0
            for char in line:
                if char == "+":
                    cor_x, cor_y = 4,4
                    #0 = super biscotto
                    # #1 = normale biscotto
                    # #corregere xy di 2 px
                    x,y = c * SPAZIO_POS , r * SPAZIO_POS
                    listaBiscotti.append((0, (x - cor_x, y - cor_y)))
                elif char == "-":
                    #0 = super biscotto
                    #1 = normale biscotto
                    cor_x, cor_y = 2,2
                    x,y = c * SPAZIO_POS , r * SPAZIO_POS
                    listaBiscotti.append((1, (x - cor_x, y - cor_y)))

                c += 1
            r += 1
        return listaBiscotti

    def bonus_pos(self):
        listabonus = []
        c,r = 0,0
        SPAZIO_POS = 8
        for line in self._board:
            c = 0
            for char in line:
                if char == "$":
                    cor_x, cor_y = 4,8
                    x,y = c * SPAZIO_POS , r * SPAZIO_POS
                    listabonus.append((x - cor_x, y - cor_y))
                c += 1
            r += 1
        return listabonus

