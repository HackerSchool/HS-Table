NPLAYERS = 2
BOARDSIZE = 3

# create the board
Board = [-1 for i in range(0,BOARDSIZE * BOARDSIZE)]

def Play(player, spot):
    """ Handles a player play """

    # tried to play on not empty spot
    if Board[spot] != -1:
        return False

    else:
        Board[spot] = player
        # adicionar codigo para desenhar cruz/bola
        return True

def main():
    player = 0
    # adicionar o codigo para o pygame

    # game loop
    while True:
        print(Board)

        spot = int(input()) # receber o input
        # por a receber o input do rato/touch
        # converter as coords para uma das posições

        if Play(player, spot):
            # if played on valid spot increment player
            player += 1

            if player >= NPLAYERS:
                player = 0

if __name__ == "__main__":
    main()
