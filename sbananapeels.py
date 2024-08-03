'''
Game Jam
Theme: Small banana peels

Player uses arrow keys to move around a maze
If they step on a banana peel, they slide
They might be chased by a jealous monkey
'''

import curses
import sys
import time
import random  # Import at the top of your file

# Maze layout: '#' represents walls, ' ' represents paths, 'b' represents banana peels
def initialize_maze():
    return [
        "####################",
        "#   b      b      b#",
        "#b ######  #########",
        "#  #      b#       #",
        "#b #  ######  #####",
        "#b #  #        #   #",
        "#b ###  ####  ##   #",
        "#     #      #     #",
        "#     #      #     #",
        "##### ################",
        "#                   #",
        "#                   E",
        "####################"
    ]

# Duration of each tick in seconds
tick_duration = 0.4

def draw_maze(win, maze):
    max_y, max_x = win.getmaxyx()  # Get the maximum y and x for the window
    for y, line in enumerate(maze):
        for x, char in enumerate(line):
            if y < max_y and x < max_x - 1:  # Ensure you're within the bounds, minus 1 on x to avoid the bottom-right corner
                win.addch(y, x, char)
    win.addstr(y+2,0,f"Run the maze. \"b\" are banana peels which make you slide. \nAvoid the jealous monkies.\nTime is running out.")

def add_monkey(maze):
    empty_positions = [(y, x) for y, row in enumerate(maze) for x, char in enumerate(row) if char == ' ']
    if empty_positions:
        my, mx = random.choice(empty_positions)
        maze_row = list(maze[my])
        maze_row[mx] = 'M'
        maze[my] = ''.join(maze_row)

def main(stdscr):
    tick_count = 0  # Initialize tick counter
    MAZE = initialize_maze()  # Initialize the maze
    score = 100  # Initialize score

    while True:  # Add a loop to allow restarting the game
        player_char = '@'
        max_y, max_x = stdscr.getmaxyx()
        required_y, required_x = len(MAZE), len(MAZE[0])
        if max_y < required_y or max_x < required_x:
            raise ValueError(f"Terminal window is too small for the maze, please resize to at least {required_x}x{required_y} and try again.")

        # Initialize curses
        curses.curs_set(0)  # Hide cursor
        stdscr.keypad(True)  # Enable keypad mode
        curses.noecho()  # Turn off auto echoing of key presses
        curses.cbreak()  # React to keys instantly without requiring the Enter key

        # Starting position of the player
        x, y = 1, 1
        stdscr.addch(y, x, player_char)

        stdscr.timeout(int(tick_duration * 1000))  # Set timeout for getch in milliseconds

        while True:
            tick_count += 1  # Increment tick counter each loop

            start_time = time.time()  # Record start time of the tick

            # Clear any previous input
            curses.flushinp()

            key = stdscr.getch()

            # Initialize new_x and new_y to current x and y
            new_x, new_y = x, y

            # Determine the new position based on the key pressed
            if key == curses.KEY_UP:
                new_y -= 1
            elif key == curses.KEY_DOWN:
                new_y += 1
            elif key == curses.KEY_LEFT:
                new_x -= 1
            elif key == curses.KEY_RIGHT:
                new_x += 1

            # Check for slipping on a banana peel
            if 0 <= new_y < len(MAZE) and 0 <= new_x < len(MAZE[0]) and MAZE[new_y][new_x] == 'b':
                # Remove the banana peel immediately after stepping on it
                maze_row = list(MAZE[new_y])  # Convert the string to a list to modify it
                maze_row[new_x] = ' '  # Replace 'b' with ' '
                MAZE[new_y] = ''.join(maze_row)  # Convert list back to string and update the maze

                # Increase score by 10
                score += 10

                # Move additional 3 steps in the same direction
                for _ in range(3):
                    if key == curses.KEY_UP and new_y > 0 and MAZE[new_y-1][new_x] != '#':
                        new_y -= 1
                    elif key == curses.KEY_DOWN and new_y < len(MAZE)-1 and MAZE[new_y+1][new_x] != '#':
                        new_y += 1
                    elif key == curses.KEY_LEFT and new_x > 0 and MAZE[new_y][new_x-1] != '#':
                        new_x -= 1
                    elif key == curses.KEY_RIGHT and new_x < len(MAZE[0])-1 and MAZE[new_y][new_x+1] != '#':
                        new_x += 1

            # Check if the player has stepped on 'M'
            if MAZE[new_y][new_x] == 'M' or score <= 0:
                stdscr.clear()  # Clear the screen before displaying the lose message
                stdscr.addstr(0, 0, "You lost! Press Y to play again or Q to quit.")
                stdscr.refresh()
                while True:  # Loop to handle post-game options
                    response = stdscr.getch()
                    if response in [ord('y'), ord('Y')]:
                        MAZE = initialize_maze()  # Reset the maze
                        score = 100  # Reset score
                        break  # Break the inner loop to restart the game
                    elif response in [ord('q'), ord('Q')]:
                        return  # Return from the function to exit
                break  # Break the game loop to restart the game

            # Validate movement within maze boundaries and not into walls
            if 0 <= new_y < len(MAZE) and 0 <= new_x < len(MAZE[0]) and MAZE[new_y][new_x] != '#':
                x, y = new_x, new_y  # Update player's position only if it's a valid move

            # Decrease score each tick
            score -= 1

            # Check if the player has reached the exit
            if x == 19 and y == 11:  # Coordinates of the exit
                stdscr.clear()  # Clear the screen before displaying the win message
                stdscr.addstr(0, 0, f"You've escaped the maze! Final score: {score}. Press Y to play again or Q to quit.")
                stdscr.refresh()
                while True:  # Loop to handle post-game options
                    response = stdscr.getch()
                    if response in [ord('y'), ord('Y')]:
                        break  # Break the inner loop to restart the game
                    elif response in [ord('q'), ord('Q')]:
                        return  # Return from the function to exit
                break  # Break the game loop to restart the game

            # Add 'M' to a random empty spot every few ticks
            if tick_count % 7 == 1:
                add_monkey(MAZE)

            # Redraw the player at the new position
            stdscr.clear()
            draw_maze(stdscr, MAZE)
            stdscr.addch(y, x, player_char)

            # Display the score
            stdscr.addstr(0, len(MAZE[0]) + 2, f"Score: {score}")

            # Refresh the screen to update the display
            stdscr.refresh()

            # Calculate remaining time in the tick and sleep if necessary
            elapsed_time = time.time() - start_time
            if elapsed_time < tick_duration:
                time.sleep(tick_duration - elapsed_time)

if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        sys.exit()


