import kill_game
import run_game
import invite_team
import time

def restart():
    kill_game.kill_game()
    time.sleep(5)  # Attendre un peu après la fermeture
    run_game.run_game()
    time.sleep(90)  # 1 minute 30 secondes d'attente
    invite_team.invite()