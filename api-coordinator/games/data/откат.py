import socket
import pygame

def start_server(port):
    class Paddle:
        def __init__(self, x, y):
            self.rect = pygame.Rect(x, y, 15, 80)

    class Ball:
        def __init__(self):
            self.rect = pygame.Rect(400, 300, 15, 15)
            self.speed = [1, 1]

        def move_ball(self):
            self.rect.move_ip(self.speed)
            if self.rect.left < 0 or self.rect.right > 800:
                self.speed[0] = -self.speed[0]
            if self.rect.top < 35 or self.rect.bottom > 600:
                self.speed[1] = -self.speed[1]

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('95.163.25.189', port))
    server.listen(2)

    print("Server Started. Waiting for connection...")

    p1, addr1 = server.accept()
    player_id_1 = p1.recv(1024).decode()  # Получаем id игрока 1
    print(f"Player {player_id_1} connected from", addr1)
    p1.sendall(b'1')  # Отправляем игроку номер 1

    p2, addr2 = server.accept()
    player_id_2 = p2.recv(1024).decode()  # Получаем id игрока 2
    print(f"Player {player_id_2} connected from", addr2)
    p2.sendall(b'2')  # Отправляем игроку номер 2

    paddle1 = Paddle(50, 250)
    paddle2 = Paddle(735, 250)
    ball = Ball()

    while True:
        data1 = p1.recv(1024).decode()
        data2 = p2.recv(1024).decode()

        paddle1.rect.x, paddle1.rect.y = map(int, data1.split(',')[:2])
        paddle2.rect.x, paddle2.rect.y = map(int, data2.split(',')[:2])

        if paddle1.rect.colliderect(ball.rect) or paddle2.rect.colliderect(ball.rect):
            ball.speed[0] = -ball.speed[0] * 1.1  # 10 процентов

        ball.move_ball()

        if ball.rect.left < 0:
            winner = '2'
            break
        elif ball.rect.right > 800:
            winner = '1'
            break

        data = f"{paddle1.rect.x},{paddle1.rect.y},{paddle2.rect.x},{paddle2.rect.y},{ball.rect.x},{ball.rect.y}"
        p1.sendall(data.encode())
        p2.sendall(data.encode())

    print(f"Player {winner} wins!") # КОГДА ИГРОК ПОБЕЖДАЕТ
