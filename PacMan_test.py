import unittest
from PacMan import Arena, Ghost, PacMan
from PacManGame import PacManGame


class GhostTest(unittest.TestCase):
    def test_collide_eating_pacman(self):
        a = Arena((232, 256))
        game = PacManGame()
        g = Ghost(a, game, 0, 0, (112, 88), 1, (89,88))

        p = PacMan(a, game, (96, 184), ["w", "s", "a", "d"])

        g.eatable_status(True)
        p.eating_status(True)
        
        g.collide(p)
        self.assertTrue(g not in a.actors() and game.get_score() > 0)

    def test_collide_not_eating_pacman(self):
        a = Arena((232, 256))
        game = PacManGame()
        g = Ghost(a, game, 0, 0, (112, 88), 1, (112,88))

        p = PacMan(a, game, (96, 184), ["w", "s", "a", "d"])
        
        g.collide(p)
        self.assertTrue(g in a.actors() and game.get_score() == 0)
    
    def test_muri(self):
        a = Arena((232, 256))
        game = PacManGame()
        #posizionato davanti ad un muro
        PacMan(a, game, (96, 184), ["w", "s", "a", "d"])

        g = Ghost(a, game, 0, 0, (72, 88), 0, (112,88))

        g.set_start_timer(0)
        #lo dirigo verso il muro
        g.set_direction((-2,0))

        g.move()

        x,y = g.position()        
        self.assertTrue(not game.in_wall(x,y))

    def test_incorci(self):
        a = Arena((232, 256))
        game = PacManGame()
        PacMan(a, game, (96, 184), ["w", "s", "a", "d"])

        #posizionato davanti ad un muro
        g = Ghost(a, game, 0, 0, (88, 88), 1, (88,88))
        g2 = Ghost(a, game, 0, 0, (89, 88), 1, (89,88))

        g.set_start_timer(0)
        g2.set_start_timer(0)
        g.move()
        g2.move()

        g.move()
        g2.move()

        g.move()
        g2.move()
      
        #se un fantasma viene posizionato in un incrocio, inevitabilmente si muovera, se no manterra la posizione iniziale
        self.assertTrue(g.position() != (88,88) and g2.position() == (89,88))

    def test_sprite(self):
        a = Arena((232, 256))
        game = PacManGame()
        SU,GIU,SIN,DES = (0,-2),(0,2),(-2,0),(2,0)

        SYM_NUM = 0        
        GHOST_H = 16
        SYM_W = 64
        sprite_h = SYM_W + (GHOST_H * SYM_NUM)
        SU_SYM,GIU_SYM,SIN_SYM,DES_SYM = (64, sprite_h), (96, sprite_h), (32, sprite_h), (0, sprite_h)
        
        #posizionato davanti ad un muro
        g = Ghost(a, game, SYM_NUM, 0, (88, 88), 1, (112,88))

        g.set_direction(SU)
        su = g.symbol()

        g.set_direction(GIU)
        giu = g.symbol()

        g.set_direction(DES)
        des = g.symbol()

        g.set_direction(SIN)
        sin = g.symbol()
      
        #se un fantasma viene posizionato in un incrocio, inevitabilmente si muovera, se no manterra la posizione iniziale
        self.assertTrue(su == SU_SYM and giu == GIU_SYM and sin == SIN_SYM and des == DES_SYM)



            


class PacManTest(unittest.TestCase):
    def test_collide_eatable_ghost(self):
        a = Arena((232, 256))
        game = PacManGame()
        g = Ghost(a, game, 0, 0, (112, 88), 1, (89,88))
        p = PacMan(a, game, (96, 184), ["w", "s", "a", "d"])

        g.eatable_status(True)
        p.eating_status(True)

        p.collide(g)
        g.collide(g)
        self.assertTrue(p in a.actors())

    def test_collide_not_eatable_ghost(self):
        a = Arena((232, 256))
        game = PacManGame()
        g = Ghost(a, game, 0, 0, (112, 88), 1, (112,88))
        p = PacMan(a, game, (96, 184), ["w", "s", "a", "d"])
        
        p.collide(g)
        self.assertTrue(g in a.actors() and p not in a.actors())
    
    def test_muri(self):
        a = Arena((232, 256))
        game = PacManGame()
        #posizionato davanti ad un muro
        p = PacMan(a, game, (72,88), ["w", "s", "a", "d"])
        #lo dirigo verso il muro
        p.set_direction((-2,0))

        p.move()

        x,y = p.position()        
        self.assertTrue(not game.in_wall(x,y))

    def test_incorci(self):
        a = Arena((232, 256))
        game = PacManGame()
        #posizionato davanti ad un muro
        p = PacMan(a, game, (88, 88), ["w", "s", "a", "d"])

        p2 = PacMan(a, game, (89, 88), ["w", "s", "a", "d"])
        p.set_direction((-2,0))
        p2.set_direction((-2,0))

        p.move()
        p2.move()

        p.move()
        p2.move()

        p.move()
        p2.move()
      
        #se un fantasma viene posizionato in un incrocio, inevitabilmente si muovera, se no manterra la posizione iniziale
        self.assertTrue(p.position() != (88,88) and not p2.position() == (89,88))

    def test_sprite(self):
        a = Arena((232, 256))
        game = PacManGame()
        SU,GIU,SIN,DES = (0,-2),(0,2),(-2,0),(2,0)

        SYM_NUM = 0        
        GHOST_H = 16
        SYM_W = 64
        sprite_h = SYM_W + (GHOST_H * SYM_NUM)
        SU_SYM,GIU_SYM,SIN_SYM,DES_SYM = (64, sprite_h), (96, sprite_h), (32, sprite_h), (0, sprite_h)
        
        #posizionato davanti ad un muro
        g = Ghost(a, game, SYM_NUM, 0, (88, 88), 1, (112,88))

        g.set_direction(SU)
        su = g.symbol()

        g.set_direction(GIU)
        giu = g.symbol()

        g.set_direction(DES)
        des = g.symbol()

        g.set_direction(SIN)
        sin = g.symbol()
      
        #se un fantasma viene posizionato in un incrocio, inevitabilmente si muovera, se no manterra la posizione iniziale
        self.assertTrue(su == SU_SYM and giu == GIU_SYM and sin == SIN_SYM and des == DES_SYM)
            
if __name__ == '__main__':
    unittest.main()
