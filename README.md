# GuintanganGuessingGame



## Features

- Players can select difficulty levels: The project can be done in a easy, medium, or hard way.
- The numbers that are produced randomly and are based on the difficulty level that you have chosen.
- Leaderboard is the tool that tracks player scores and difficulty levels.
- It supports multiple parallel connections through TCP/IP sockets.

## Getting Started

1. You can either clone the repository or download the server. py file.
2. Check if you have Python installed on your system.
3. Start the server script with the command python server. py.
4. Join the server by a TCP client (e.g. a web browser). g. , Telnet) to the specified host and port.

## Usage

- When you are connecting to the server, you should input a username when the server asks for it.
- You should choose a difficulty level (easy, medium, or hard) when the prompt asks you to do so.
- Try to guess a number in the given range.
- The server will give a response to the guess which will either say that it is too low or too high.
- After the right number is guessed, the server will show the number of attempts and update the leaderboard.
- Players can either opt to play again or leave the game.
