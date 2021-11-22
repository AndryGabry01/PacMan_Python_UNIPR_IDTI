#!/usr/bin/env python3
from typing import Text
import g2d
from PacManGame import PacManGame
from PacManAudio import PacMan_PlayAudio as audio 

class PacManGui:
    def __init__(self):
        self._game = PacManGame()
        self._info_rect_size_h = 40
        self._ishero_sound_1 = True 
        arena_w, arena_h = self._game.arena().size()
        self._win_w, self._win_h = arena_w ,arena_h + self._info_rect_size_h
        g2d.init_canvas((self._win_w, self._win_h))

        self._sprites = g2d.load_image("./img/pac_man.png")
        g2d.play_audio("./sound/pacman_start.wav")
        g2d.main_loop(self.tick)
    
    def tick(self):
        heros = self._game.heros()
        for hero in heros:
            hero.control(g2d.current_keys())
        arena = self._game.arena()
        arena.move_all()  # Game logic
        g2d.clear_canvas()

        #pacman map
        g2d.draw_image("./img/pac_man_bg.png", (0,0))
        
        #draw Disegna la tabella contenente le informazioni
        self.tabella_info()
        
        for a in arena.actors():
            if a.symbol() != None:
                g2d.draw_image_clip(self._sprites, a.symbol(), a.size(), a.position())
        #Decrementa il tempo rimanente per mangiare i fantasmi
        self._game.eating_counter()
        self._game.behavor_ghost_timer()

        #Game Over
        if self._game.game_over():
            g2d.clear_canvas()
            g2d.draw_image("./img/pac_man_gameover.png", (0,0))
            self.tabella_info()
            audio.pacmanGameOver()
            g2d.alert("Click for close window")

            g2d.close_canvas()
        elif self._game.game_won():
            g2d.clear_canvas()
            g2d.draw_image("./img/pac_man_gamewon.png", (0,0))
            self.tabella_info()
            audio.pacmanWon()
            g2d.alert("Click for close window")

            g2d.close_canvas()
    
    def tabella_info(self):
        #Info_rect
        arena_w, arena_h = self._game.arena().size()
        g2d.set_color((0,0,0))
        g2d.fill_rect((0, arena_h),(arena_w, self._info_rect_size_h))
        #Tabella informazioni
        TEXT_SIZE = 22
        RECT_PADDING_W = 5

        Biscotti = "Biscotti: " + str(self._game.remaining_biscotti())
        Score = "Score: " + str(self._game.get_score())

        g2d.set_color((255,255,255))
        sprite_sym_clip_pos = 16,0
        sprite_sym_size = 16, 16
        sprite_sym_pos = RECT_PADDING_W, arena_h

        for i in range(0, self._game.remaining_life()):
            g2d.draw_image_clip(self._sprites, sprite_sym_clip_pos, sprite_sym_size, sprite_sym_pos)
            w = sprite_sym_size[0]
            x,y = sprite_sym_pos
            x += w
            sprite_sym_pos = x, y
        g2d.draw_text(Biscotti +" | "+ Score, (RECT_PADDING_W, arena_h +TEXT_SIZE), TEXT_SIZE)
        g2d.set_color((255,0,0))
        
gui = PacManGui()
