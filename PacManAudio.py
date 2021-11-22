from g2d import play_audio, load_audio, pause_audio
class PacMan_PlayAudio():
    def __init__(self) -> None:
        self._pacman_waka = (False, False) #play waka?, is alredy play?
    def toggle_pacmanWaka(self, toogle):
        isplaying = self._pacman_waka[1]
        self._pacman_waka = (toogle, isplaying)
    def pacmanWaka(self):
        start_play, isplaying = self._pacman_waka 
        if start_play and not isplaying:
            play_audio("./sound/pacman_chomp.wav", True)
            self._pacman_waka = (start_play, True)
        elif not start_play:
            pause_audio("./sound/pacman_chomp.wav")

    def pacmanEatGhost(self):
        pause_audio("./sound/pacman_eatghost.wav")
        play_audio("./sound/pacman_eatghost.wav")

    def pacmanEatBonus(self):
        pause_audio("./sound/pacman_eatfruit.wav")
        play_audio("./sound/pacman_eatfruit.wav")

    def pacmanEatCoockie(self):
        pause_audio("./sound/pacman_intermission.wav")
        play_audio("./sound/pacman_intermission.wav")
    
    def pacmanGameOver():
        pause_audio("./sound/pacman_gameover.wav")
        play_audio("./sound/pacman_gameover.wav")

    def pacmanWon():
        pause_audio("./sound/pacman_won.wav")
        play_audio("./sound/pacman_won.wav")
        
    def stopActorSound(self):
        self._pacman_waka = (False, (False))
        pause_audio("./sound/pacman_chomp.wav")
        pause_audio("./sound/pacman_eatghost.wav")
        pause_audio("./sound/pacman_eatfruit.wav")
        pause_audio("./sound/pacman_intermission.wav")
