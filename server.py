import socket
import random
import json
import os
import sys

LEADERBOARD_FILE = 'leaderboard.json'

def load_leaderboard():
    if os.path.exists(LEADERBOARD_FILE):
        with open(LEADERBOARD_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_leaderboard(leaderboard):
    with open(LEADERBOARD_FILE, 'w') as f:
        json.dump(leaderboard, f, indent=4)

def update_leaderboard(username, score, difficulty, leaderboard):
    leaderboard[username] = {'score': score, 'difficulty': difficulty}
    save_leaderboard(leaderboard)

def display_leaderboard(leaderboard):
    sorted_leaderboard = sorted(leaderboard.items(), key=lambda x: x[1]['score'])
    print("\nLeaderboard:")
    for rank, (username, data) in enumerate(sorted_leaderboard, start=1):
        print(f"{rank}. {username} - {data['score']} tries, Difficulty: {data['difficulty']}")
    print("\n")

def play_game(conn, username, leaderboard):
    while True:
        conn.sendall(b"Select difficulty (easy, medium, hard): ")
        difficulty = conn.recv(1024).decode('utf-8').strip().lower()

        if difficulty not in ['easy', 'medium', 'hard']:
            conn.sendall(b"Invalid difficulty level. Defaulting to medium.\n")
            difficulty = 'medium'

        if difficulty == 'easy':
            max_number = 50
        elif difficulty == 'medium':
            max_number = 100
        elif difficulty == 'hard':
            max_number = 500

        number_to_guess = random.randint(1, max_number)
        conn.sendall(f"Guess a number between 1 and {max_number}: ".encode('utf-8'))

        tries = 0
        while True:
            guess = conn.recv(1024).decode('utf-8').strip()
            if not guess.isdigit():
                conn.sendall(b"Please enter a valid number: ")
                continue
            
            tries += 1
            guess = int(guess)
            if guess < number_to_guess:
                conn.sendall(b"Too low! Try again: ")
            elif guess > number_to_guess:
                conn.sendall(b"Too high! Try again: ")
            else:
                conn.sendall(f"Congratulations! You guessed the right number in {tries} tries!\n".encode('utf-8'))
                update_leaderboard(username, tries, difficulty, leaderboard)
                break
        
        display_leaderboard(leaderboard)
        conn.sendall(b"Do you want to play again? (yes/no): ")
        play_again = conn.recv(1024).decode('utf-8').strip().lower()
        if play_again != 'yes':
            conn.sendall(b"Goodbye!\n")
            break
    sys.exit("Server has been stopped.")

def start_server(host='127.0.0.1', port=65432):
    leaderboard = load_leaderboard()
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Server started. Listening on {host}:{port}")
        
        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                conn.sendall(b"Enter your username: ")
                username = conn.recv(1024).decode('utf-8').strip()
                
                if username in leaderboard:
                    welcome_message = f"Welcome back, {username}!\n"
                else:
                    welcome_message = f"Welcome, {username}!\n"
                
                conn.sendall(welcome_message.encode('utf-8'))
                
                play_game(conn, username, leaderboard)

if __name__ == "__main__":
    start_server()
