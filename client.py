import socket

def start_client(host='127.0.0.1', port=65432):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        
        while True:
            data = s.recv(1024)
            print(data.decode('utf-8'))
            
            username = input()
            s.sendall(username.encode('utf-8'))
            
            welcome_message = s.recv(1024)
            print(welcome_message.decode('utf-8'))
            
            play_game(s)

def play_game(s):
    while True:
        difficulty_prompt = s.recv(1024)
        print(difficulty_prompt.decode('utf-8'))
        
        difficulty = input()
        s.sendall(difficulty.encode('utf-8'))
        
        guess_prompt = s.recv(1024)
        print(guess_prompt.decode('utf-8'))
        
        while True:
            guess = input()
            s.sendall(guess.encode('utf-8'))
            
            response = s.recv(1024)
            print(response.decode('utf-8'))
            
            if "Congratulations" in response.decode('utf-8'):
                break
            
        play_again_prompt = s.recv(1024)
        print(play_again_prompt.decode('utf-8'))
        play_again = input().strip().lower()
        s.sendall(play_again.encode('utf-8'))
        
        if play_again != 'yes':
            break

if __name__ == "__main__":
    start_client()
