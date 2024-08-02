import random
import time
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def run_race():
    track_length = 40
    snails = [0] * 6  # Six snails at the starting line
    clear_screen()

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

    while max(snails) < track_length:
        clear_screen()
        for i in range(len(snails)):
            if i == guess - 1:
                inc = random.randint(-1, 4)  # Each snail moves 0, 1, or 2 steps

            else:
                inc = random.randint(-2, 4)  # Each snail moves 0, 1, or 2 steps
            snails[i] += inc
            if snails[i] < 0:
                snails[i] = 0
            if inc < 0:
                flavor = "<derp"
            else:
                flavor = ''   

            if i == guess - 1:
                print(f"{i+1}: " + '*' * snails[i] + '🐌' + flavor + ' ' * (track_length - snails[i] - 1 - len(flavor)) + '|'  + 'X ' )
            else:
                print(f"{i+1}: " + '-' * snails[i] + '🐌' + flavor + ' ' * (track_length - snails[i] - 1 - len(flavor)) + '|')
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
