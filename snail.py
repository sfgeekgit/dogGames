import random
import time
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def run_race():
    track_length = 40
    snails = [0] * 6  # Six snails at the starting line
    clear_screen()
    bomb_display = '💣' 
    bang_display = '💥'

    # Ask the player for their guess with error handling
    while True:
        try:
            guess = int(input("Which snail do you think will win? Enter a number (1-6): "))
            if 1 <= guess <= 6:
                break
            else:
                print("Please enter a number between 1 and 6.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")


    # Initialize bomb
    #bomb_snail = random.randint(1, 6)  # Choose one snail randomly
    #bomb_position = random.randint(5, 25)  # Bomb position between 5 and 25

    bombs = {}
    for i in range(random.randint(1, 3)):
        lane = random.randint(1, 6)
        while lane in bombs:
            lane = random.randint(1, 6)
        position = random.randint(5, 25)
        bombs[lane] = position


    derp_snail = random.randint(1, 6)    
    while derp_snail == guess:
        derp_snail = random.randint(1, 6)

    inch_snail = random.randint(1, 6)
    while inch_snail == guess or inch_snail == derp_snail:
        inch_snail = random.randint(1, 6)



    while max(snails) < track_length:
        clear_screen()
        for i in range(len(snails)):

            # defaults for all snails
            trail = '-'
            finish_line = '|'
            flavor = ''

            if i == guess - 1:
                inc = random.randint(-2, 5)  
                trail = '*'
                finish_line = 'X'
            elif i == derp_snail - 1:
                trail = '~'
                inc = random.randint(-4, 3)
                if inc > 2:
                    inc = 10
            elif i == inch_snail - 1:
                inc = 1
                trail = '.'
            else:
                inc = random.randint(-2, 4)  

            if i+1 in bombs:
                if (snails[i] >= bombs[i+1]) or (snails[i] + inc >= bombs[i+1]):
                    inc = 0
                    snails[i] = bombs[i+1]
            #if i == bomb_snail -1  and inc < 0 and snails[i] >= bomb_position:
            #    inc = 0
            #    snails[i] = bomb_position

            snails[i] += inc
            if snails[i] < 0:
                snails[i] = 0
            if inc < 0:
                flavor = "<derp"



            #if i == bomb_snail -1:
            if i+1 in bombs:
                bomb_position = bombs[i+1]
                if snails[i] >= bombs[i+1]:
                    print(f"{i+1}: " + trail * bomb_position + bang_display + ' ' * (track_length - bomb_position - 1) + finish_line)
                else:
                    print(f"{i+1}: " + trail * snails[i] + '🐌' + flavor + ' ' * (bomb_position - snails[i] - 1 - len(flavor)) + bomb_display + ' ' * (track_length - bomb_position - 2) + finish_line)
            else:
                print(f"{i+1}: " + trail * snails[i] + '🐌' + flavor + ' ' * (track_length - snails[i] - 1 - len(flavor)) + finish_line)

        print(snails)
        time.sleep(0.5)

    winner = snails.index(max(snails)) + 1
    print(f"Snail {winner} wins the race!")

    # Check if the player's guess was correct
    if winner == guess:
        print("Congratulations! Your guess was correct!")
    else:
        print(f"Sorry, your guess was incorrect. Snail {winner} won the race.")


if __name__ == "__main__":
    run_race()
