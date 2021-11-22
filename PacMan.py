#!/usr/bin/env python3


from random import choice
from time import time
from tkinter.constants import W
from typing import Tuple
from actor import Actor, Arena
class Biscotto(Actor):
    def __init__(self, type, arena, game, pos):
        self._x, self._y = pos
        self._arena = arena
        self._game = game
        
        #type 0 == super biscotto
        #type 1 == normale biscotto
        self._type = type
        if self._type == 0:
            self._w, self._h = 8, 8
        elif self._type == 1:
            self._w, self._h = 4, 4

        arena.add(self)

    def collide(self, other):
        if isinstance(other, PacMan):
            self._arena.remove(self)
            bonus_point = 0
            if self._type == 0:
                self._game.eat_biscotti()
                self._game.set_eating_time(self._game.get_eating_duration())
                self._game._audio.pacmanEatCoockie()
                bonus_point = 50
            else:
                bonus_point = 10
                
            self._game.inc_score(bonus_point)


    def move(self):
        pass
    def position(self):
        return self._x, self._y
    def size(self):
        return self._w, self._h
    def get_type(self):
        return self._type
    def symbol(self):
        sym_x, sym_y = 0,0
        if self._type == 0:
            sym_x, sym_y = 180,52
        elif self._type == 1:
            sym_x, sym_y = 166, 54
        return sym_x, sym_y


class Bonus(Actor):
    def __init__(self, arena, game, pos, sym_x_list, sym_y):
        self._x, self._y = pos
        self._arena = arena
        self._w, self._h = 16, 16

        self._game = game
        self._symbol_x_list = sym_x_list 
        self._symbol_y = sym_y
    
        self._symbol = choice(self._symbol_x_list), self._symbol_y

        self._visibility = True
        self._BONUSTIMER = self._game.get_bonus_time()

        arena.add(self)

    def collide(self, other):
        if self._visibility and isinstance(other, PacMan):
            self._game.inc_score(150)
            self._game.set_bonus_time(self._BONUSTIMER)
            self._visibility = False
            self._game._audio.pacmanEatBonus()
            self._symbol = choice(self._symbol_x_list), self._symbol_y

    def move(self):
        pass
    def position(self):
        return self._x, self._y

    def size(self):
        return self._w, self._h
    
    def symbol(self):
        bonus_timer = self._game.get_bonus_time()
        if bonus_timer > 0:
            self._game.set_bonus_time(bonus_timer-1)
        else:
            self._visibility = True

        if self._visibility: return self._symbol

class Ghost(Actor):
    def __init__(self, arena, game, sprite_number, start_timer, scatter_pos, behavor, pos):
        self._x, self._y = pos
        self._w, self._h = 16, 16

        self._speed = 2
        self._dx, self._dy, self._d, self._disabled_d =  0, 0, 2, ( 0, 0) 

        self._game = game
        self._arena = arena
        self._eatable = False
        self._symTimer = 0
        self._sprite_number = sprite_number
        self._start_timer = start_timer

        self._scatter_pos = scatter_pos
        self._chase_pos = (-1, -1)
        self._chase_timer_d = 200
        self._chase_timer = 0

        #0 Frightened
        #1 Scatter
        #2 Chase 
        self._behavor = behavor 
        arena.add(self)


    def euc_dis_move(self, direction, pos):
        #scatter controllare calcolo euc per singole coordinare
        x0, y0 = pos
        min_dir = direction[0]
        dx,dy = min_dir
        x,y = self._x+dx, self._y+dy
        min_euc_dis = abs(x- x0) + abs(y - y0)

        for d in direction:
            dx,dy = d
            x,y = self._x+dx, self._y+dy
            sc_eu_dis = abs(x- x0) + abs(y - y0)
            if sc_eu_dis < min_euc_dis:
                min_dir = d
                min_euc_dis = sc_eu_dis
        self._dx, self._dy = min_dir
    
    def chase_pos(self):
        actor = self._arena.actors()
        pacmans_pos = []
        for a in actor:
            if isinstance(a, PacMan):
                pacmans_pos.append(a.position())
        pacman_x, pacman_y = choice(pacmans_pos)
        self._chase_pos = (pacman_x , pacman_y)

        
    def move(self):    
        if self._behavor == 2 and self._chase_timer == 0:
            self.chase_pos()       
            self._chase_timer = self._chase_timer_d    
        elif self._behavor == 2:
            self._chase_timer -= 1
            
        if self._chase_pos == (-1,-1):
            self.chase_pos()
        #Ogni fantasma ha un tempo iniziale che deve attendere
        if self._start_timer > 0: 
            self._start_timer -= 1
        else:
            #Ad inizio game, il fantasma sceglie una direzione iniziale
            if self._x % 8 == 0 and self._y % 8 == 0 and self._dx == 0 and self._dy == 0:
                direction = [(0,self._speed),(0,-self._speed),(self._speed,0),(-self._speed,0)]
                if self._behavor == 1:
                    self.euc_dis_move(direction, self._scatter_pos)
                elif self._behavor == 2:
                    self.euc_dis_move(direction, self._chase_pos)
                else:
                    dx, dy = choice(direction)
                    self._dx, self._dy = dx, dy 

                self._disabled_d = (-self._dx,-self._dy)

            #Ogni volta che incontra delle coordinate multiple di 8, curba
            if self._x % 8 == 0 and self._y % 8 == 0:
                #Lista contenenti tutte le direzioni possibili [giu, su, destra, sinistra]
                direction = [(0,self._speed),(0,-self._speed),(self._speed,0),(-self._speed,0)]
                #rimuove la direzione da cui sta arrivando
                dx, dy = self._disabled_d
                direction.remove((dx,dy))
                

                dx, dy = 0,0
                for d in direction[:]:
                    dx, dy = d   
                    #verifica se la direzione presa in causa, porta ad un muro e quindi la elimina dalla lista
                    if self._game.in_wall(self._x + dx, self._y + dy):
                        direction.remove(d)
                    
                if self._behavor == 1:
                    self.euc_dis_move(direction, self._scatter_pos)
                elif self._behavor == 2:
                    self.euc_dis_move(direction, self._chase_pos)
                else:
                    #sceglie la direzione, dalla lista di quelle rimaste 
                    self._dx, self._dy = choice(direction)
                
                #Symbol Direction
                if self._dy == -self._speed:
                    self._d = 0 #su
                elif self._dy == self._speed:
                    self._d = 1 #giu
                elif self._dx == -self._speed:
                    self._d = 2 #sinistra
                elif self._dx == self._speed:
                    self._d = 3 #destra

            arena_w, arena_h = self._arena.size()
            #aggiorna la posizione disabilitata [quella da cui proviene]
            self._disabled_d = (-self._dx, -self._dy)

            #avanza
            self._y += self._dy
            self._x += self._dx

            #fix poszione in caso vada contro i bordi su e giu della arena [teleport dalla parte opposta]
            if self._y < 0:
                self._y = arena_h - self._h
            elif self._y > arena_h - self._h:
                self._y = 0

            #fix poszione in caso vada contro i bordi sinistra e destra della arena [teleport dalla parte opposta]
            if self._x <= 0:
                self._x = arena_w -self._w
            elif self._x >= arena_w - self._w:
                self._x = 0


    def eatable_status(self, status: bool):
        #imposta il fantasma puo o meno essere mangiato
        self._eatable = status

        if self._eatable: 
            self._behavor = 0
        else: 
            self.set_behavor()

    
    
        

    def collide(self, other):
        if self._eatable and isinstance(other, PacMan):
            self._arena.remove(self)
            self._game._audio.pacmanEatGhost()
            self._game.inc_score(100)
            #self._behavor = 0

    def position(self):
        return self._x, self._y

    def size(self):
        return self._w, self._h
    
    def symbol(self):
        sym = 0
        SYM_W = 64
        sprite_h = SYM_W + (self._h * self._sprite_number)
        #normali sprite fantasma
        if self._d == 0:
            sym = (64, sprite_h)

        if self._d == 1:
            sym = (96, sprite_h)
        
        if self._d == 2:
            sym = (32, sprite_h)
        
        if self._d == 3:
            sym = (0, sprite_h)

        #se esce dalla modalita eatable
        if not self._eatable: self._symTimer = 0

        #se entra in modalita eatable
        #velocita animazione
        eat_timer = self._game.get_eating_time()
        symin,symax = 0,0
        if  eat_timer < self._game.get_eating_duration() - self._game.get_eating_duration() // 4:
            symin,symax = 16,32
        elif  eat_timer < self._game.get_eating_duration() // 2:
            symin,symax = 2, 4
        
        if self._eatable and self._symTimer < symax:
            self._symTimer += 1
        elif self._eatable:
            self._symTimer = 1

        #animazione
        if eat_timer > 0:
            if self._symTimer <= symin or (symin,symax) == (0,0):
                sym = (128,64)
            elif self._symTimer <= symax:
                sym = (160,64)
            self._symTimer += 1
        return sym

    def get_direction(self) -> Tuple:
        return (self._dx, self._dy)

    def set_direction(self, direction: Tuple):
        self._dx, self._dy = direction
        self._disabled_d = (-self._dx, -self._dy)

        if direction == (0, -self._speed):
            self._d = 0 #su
        elif direction == (0, self._speed):
            self._d = 1 #giu
        elif direction == (-self._speed, 0):
            self._d = 2 #sinistra
        elif direction == (self._speed, 0):
            self._d = 3 #destra


    def set_behavor(self):
        self._behavor = choice([1,2])
        if self._behavor == 2:
            self.chase_pos()

    def get_start_timer(self)->int:
        return self._start_timer
    
    def set_start_timer(self, time:int):
        self._start_timer = time


class PacMan(Actor):
    def __init__(self, arena,game, pos, controls):
        self._x, self._y = pos
        self._w, self._h = 16, 16
        self._speed = 2
        self._d, self._dx, self._dy = 2 , 0, 0
        self._controls = controls
        self._game = game
        self._last_collision = 0
        self._arena = arena
        self._count_face_status = 0

        self._eating_status = False
        self._death_sym = -1
        arena.add(self)


    def move(self):
        self._game._audio.pacmanWaka()
        #!Animazione sprite [rivedere]
        if self._arena.count() % 6 == 0: 
            self._count_face_status += 1
        if self._count_face_status == 2:  self._count_face_status = 0

        arena_w, arena_h = self._arena.size()    

        #se pacman incontra un muro si ferma         
        if self._game.in_wall(self._x + self._dx, self._y + self._dy) or self._death_sym != -1:
            self._dy = 0
            self._dx = 0
        
     
        self._y += self._dy
        self._x += self._dx

        #fix bordi [teleport]    
        if self._y < 0:
            self._y = arena_h - self._h
        elif self._y > arena_h - self._h:
            self._y = 0
        if self._x < 0:
            self._x = arena_w - self._w
        elif self._x > arena_w - self._w:
            self._x = 0
        

    def control(self, keys):
        #u, d, l, r = "ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight"
        #u, d, l, r = "w", "s", "a", "d"

        u, d, l, r = self._controls
        if self._game._startGameCounter > self._arena.count():
            return
            
        if (u in keys or d in keys or l in keys or r in keys) and self._death_sym == -1:
            self._game._audio.toggle_pacmanWaka(True)
        

        
        #quando incrocia coordinate multiple di 8
        if self._x % 8 == 0 and self._y % 8 == 0:
            #verifica il tasto premuto e se tale direzione porta ad un muro
            if u in keys and not self._game.in_wall(self._x, self._y -self._speed):
                self._d = 0
                self._dy = -self._speed
                self._dx = 0
            elif d in keys and not self._game.in_wall(self._x, self._y +self._speed):
                self._d = 1
                self._dy = self._speed
                self._dx = 0
            elif l in keys and not self._game.in_wall(self._x -self._speed, self._y):
                self._d = 2
                self._dx = -self._speed
                self._dy = 0
            elif r in keys and not self._game.in_wall(self._x + self._speed, self._y):
                self._d = 3
                self._dx = self._speed
                self._dy = 0
            
       
    def lives(self) -> int:
        pass

    def eating_status(self, status:bool):
        #imposta se puo mangiare i fantasmi
        self._eating_status = status

    def collide(self, other):
        if isinstance(other, Ghost):
            if not self._eating_status:
                if self._death_sym == -1:
                    self._game.remove_life()
                    self._death_sym = 0
                elif self._death_sym == 12:
                    self._arena.remove(self)
               
               

        elif isinstance(other, Biscotto):
            if other.get_type() == 0:
                self._eating_status = True
            pass
        
    def position(self):
        return self._x, self._y

    def size(self):
        return self._w, self._h

    def symbol(self):
        sym = 0,0
        spriteX = [0,16]
        i = self._count_face_status
        if self._death_sym == -1:
            if self._d == 0:
                sym = spriteX[i], 32

            if self._d == 1:
                sym = spriteX[i], 48
            
            if self._d == 2:
                sym = spriteX[i], 16
            
            if self._d == 3:
                sym = spriteX[i], 0
        else:
            sym = 32+(16*self._death_sym), 0
            if self._arena.count()%4 == 0:
                self._death_sym +=1
        return sym
    
    def set_direction(self, direction: Tuple):
        self._dx, self._dy = direction
        self._disabled_d = (-self._dx, -self._dy)

        if direction == (0, -self._speed):
            self._d = 0 #su
        elif direction == (0, self._speed):
            self._d = 1 #giu
        elif direction == (-self._speed, 0):
            self._d = 2 #sinistra
        elif direction == (self._speed, 0):
            self._d = 3 #destra

def print_arena(arena):
    for a in arena.actors():
        print(type(a).__name__, '@', a.position())

