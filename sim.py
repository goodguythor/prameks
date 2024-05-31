import pygame
import random

def calculate_distance(x, y):
    return (x**2 + y**2) ** 0.5

def collision(passenger_positions, waiter_positions, collision_radius=20):
    # Check collision between passengers and waiters
    for passenger_pos in passenger_positions:
        for waiter_pos in waiter_positions:
            # Calculate distance between passenger and waiter
            distance_x = abs(passenger_pos[0] - waiter_pos[0])
            distance_y = abs(passenger_pos[1] - waiter_pos[1])
            distance = calculate_distance(distance_x, distance_y)

            # Check if the distance is less than the sum of their collision radii
            if distance < collision_radius * 2:
                return True
    return False

def update_train_pos(train, target_train_x, train_speed):
    # Update the train's position
    if train.x > target_train_x:
        train.x -= train_speed
        if train.x <= target_train_x:
            train.x = target_train_x

def move_waiter(waiter_positions, seat_positions, center, waiter_speed, train):
    for i, pos in enumerate(waiter_positions):
        # Calculate distance to left entrance door
        distance_x_left = abs(pos[0] - train.x - 105)

        # Calculate distance to right entrance door
        distance_x_right = abs(pos[0] - train.x - 885)

        if center[i]:
            if pos[0] < seat_positions[i][0] + 23:
                pos[0] += waiter_speed[i]
            elif pos[0] > seat_positions[i][0] + 27:
                pos[0] -= waiter_speed[i]
            elif pos[0] >= seat_positions[i][0] + 23 and pos[0] <= seat_positions[i][0] + 27:   
                if pos[1] < seat_positions[i][1] + 23:
                    pos[1] += waiter_speed[i]
                elif pos[1] > seat_positions[i][1] + 27:
                    pos[1] -= waiter_speed[i]
        elif distance_x_left <= distance_x_right:
            # Move to the left entrance door
            if pos[0] > train.x + 110:
                pos[0] -= waiter_speed[i]
            elif pos[0] < train.x + 100:
                pos[0] += waiter_speed[i]
            elif pos[0] <= train.x + 110 and pos[0] >= train.x + 100:
                pos[1] -= waiter_speed[i]
                if pos[1] >= train.y + 148 and pos[1] <= train.y + 152:
                    center[i] = True 
        else:
            # Move to the right entrance door
            if pos[0] < train.x + 880:
                pos[0] += waiter_speed[i]
            elif pos[0] > train.x + 890:
                pos[0] -= waiter_speed[i]
            elif pos[0] <= train.x + 890 and pos[0] >= train.x + 880:
                pos[1] -= waiter_speed[i]
                if pos[1] >= train.y + 148 and pos[1] <= train.y + 152:
                    center[i] = True

def move_passenger(passenger_positions, center_p, train, passenger_speed):
    for i, pos in enumerate(passenger_positions):
        distance_y = abs(pos[0] - train.y - 210)

        # Calculate distance to left exit door
        distance_x_left = abs(pos[0] - train.x - 105)
        distance_left = calculate_distance(distance_x_left, distance_y)

        # Calculate distance to right exit door
        distance_x_right = abs(pos[0] - train.x - 885)
        distance_right = calculate_distance(distance_x_right, distance_y)
        if not center_p[i]:
            if pos[1] < train.y + 148:
                pos[1] += passenger_speed[i]
            elif pos[1] > train.y + 152:
                pos[1] -= passenger_speed[i]
            elif pos[1] >= train.y + 148 and pos[1] <= train.y + 152:   
                center_p[i] = True
        elif distance_left <= distance_right:
            # Move to the left exit door
            if pos[0] > train.x + 110:
                pos[0] -= passenger_speed[i]
            elif pos[0] < train.x + 100:
                pos[0] += passenger_speed[i]
            elif pos[0] >= train.x + 100 and pos[0] <= train.x +110:
                pos[1] -= passenger_speed[i]
        else:
            # Move to the right exit door
            if pos[0] < train.x + 885:
                pos[0] += passenger_speed[i]
            elif pos[0] > train.x + 890:
                pos[0] -= passenger_speed[i]
            elif pos[0] >= train.x + 885 and pos[0] <= train.x + 890:
                pos[1] -= passenger_speed[i]

def main():
    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True

    initial_train_x = 1280  # Start position (off-screen to the right)
    target_train_x = 140  # Target position
    train_y = 210  # Fixed Y position
    train_width = 1000
    train_height = 300
    train_speed = 5
    
    train = pygame.Rect(initial_train_x, train_y, train_width, train_height)
    top_platform = pygame.Rect([0, 0, 1280, 200])
    bot_platform = pygame.Rect([0, 520, 1280, 200])
    passenger_radius = 20
    seat_size = (50, 50)

    open_door_color = pygame.Color(0, 255, 0)
    closed_door_color = pygame.Color(255, 0, 0)

    full_passenger_positions = [
        [180, 240], [180, 300], [180, 420], [180, 480],
        [330, 240], [330, 300], [330, 420], [330, 480],
        [400, 240], [400, 300], [400, 420], [400, 480],
        [470, 240], [470, 300], [470, 420], [470, 480],
        [540, 240], [540, 300], [540, 420], [540, 480],
        [610, 240], [610, 300], [610, 420], [610, 480],
        [670, 240], [670, 300], [670, 420], [670, 480],
        [740, 240], [740, 300], [740, 420], [740, 480],
        [810, 240], [810, 300], [810, 420], [810, 480],
        [880, 240], [880, 300], [880, 420], [880, 480],
        [950, 240], [950, 300], [950, 420], [950, 480],
        [1100, 240], [1100, 300], [1100, 420], [1100, 480]
    ]

    # Randomize the quantity of waiter positions
    passenger_positions = random.sample(full_passenger_positions, random.randint(1, len(full_passenger_positions)))

    seat_positions = [
        [155, 215], [155, 275], [155, 395], [155, 455],
        [305, 215], [305, 275], [305, 395], [305, 455],
        [375, 215], [375, 275], [375, 395], [375, 455],
        [445, 215], [445, 275], [445, 395], [445, 455],
        [515, 215], [515, 275], [515, 395], [515, 455],
        [585, 215], [585, 275], [585, 395], [585, 455],
        [645, 215], [645, 275], [645, 395], [645, 455],
        [715, 215], [715, 275], [715, 395], [715, 455],
        [785, 215], [785, 275], [785, 395], [785, 455],
        [855, 215], [855, 275], [855, 395], [855, 455],
        [925, 215], [925, 275], [925, 395], [925, 455],
        [1075, 215], [1075, 275], [1075, 395], [1075, 455]
    ]

    full_waiter_positions = [
        [140, 590], [140, 630], [140, 670],
        [180, 590], [180, 630], [180, 670], 
        [220, 590], [220, 630], [220, 670], 
        [260, 590], [260, 630], [260, 670], 
        [300, 590], [300, 630], [300, 670], 
        [340, 590], [340, 630], [340, 670], 
        [380, 590], [380, 630], [380, 670],
        [420, 590], [420, 630], [420, 670],
        [860, 590], [860, 630], [860, 670],  
        [900, 590], [900, 630], [900, 670], 
        [940, 590], [940, 630], [940, 670], 
        [980, 590], [980, 630], [980, 670], 
        [1020, 590], [1020, 630], [1020, 670], 
        [1060, 590], [1060, 630], [1060, 670], 
        [1100, 590], [1100, 630], [1100, 670],
        [1140, 590], [1140, 630], [1140, 670]
    ]

    # Randomize the quantity of waiter positions
    waiter_positions = random.sample(full_waiter_positions, random.randint(1, len(full_waiter_positions)))

    # Variable to check if the waiter is already reach the center of the train
    center = [False for i in range(48)] 

    # Variable to check if the passenger is already reach the center of the train
    center_p = [False for i in range(48)]

    # Assign random speed to passengers and waiters
    passenger_speed = [random.randint(1, 3) for i in range(len(passenger_positions))]
    waiter_speed = [random.randint(1, 3) for i in range(len(waiter_positions))]

    # Define person color by speed
    person_colors = [pygame.Color(255, 127, 0), pygame.Color(255, 63, 0), pygame.Color(255, 0, 0)]

    # Assign color to each passenger
    passenger_color = [person_colors[i-1] for i in passenger_speed]
    
    # Assign color to each waiter
    waiter_color = [person_colors[i-1] for i in waiter_speed]

    reached_target = False

    open_entrance = False

    paused = False

    # Define font for the message
    font = pygame.font.Font(None, 36)

    # Copy the seat positions
    available_seats = seat_positions.copy()
    assigned_seats = []

    # Assign every waiter to a random seats
    for _ in waiter_positions:
        seat = random.choice(available_seats)
        assigned_seats.append(seat)
        available_seats.remove(seat)

    while running:
        # Poll for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (paused and event.type == pygame.KEYUP):
                running = False
            if reached_target and event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                open_entrance = True

        if not paused:
            # Fill the screen with a color to wipe away anything from last frame
            screen.fill(pygame.Color(150, 75, 0))

            # Draw the train
            pygame.draw.rect(screen, pygame.Color(255, 253, 100), train)

            # Update train position
            update_train_pos(train, target_train_x, train_speed)
            if train.x == target_train_x:
                reached_target = True

            # Draw the entrance doors
            if not open_entrance:
                pygame.draw.line(screen, closed_door_color, [train.x + 90, 510], [train.x + 140, 510], 5)
                pygame.draw.line(screen, closed_door_color, [train.x + 860, 510], [train.x + 910, 510], 5)
            else:
                pygame.draw.line(screen, open_door_color, [train.x + 90, 510], [train.x + 140, 510], 5)
                pygame.draw.line(screen, open_door_color, [train.x + 860, 510], [train.x + 910, 510], 5)
                if reached_target:
                    move_waiter(waiter_positions, assigned_seats, center, waiter_speed, train)

            # Draw the platform
            pygame.draw.rect(screen, pygame.Color(20, 20, 20), top_platform)
            pygame.draw.rect(screen, pygame.Color(20, 20, 20), bot_platform)

            # Draw the yellow marker line
            pygame.draw.line(screen, pygame.Color(255, 255, 0), [0, 150], [1280, 150], 5)
            pygame.draw.line(screen, pygame.Color(255, 255, 0), [0, 570], [1280, 570], 5)

            # Draw the seats
            for pos in seat_positions:
                # Adjust seat positions relative to the moving train
                seat_rect = pygame.Rect([pos[0] + (train.x - target_train_x), pos[1], seat_size[0], seat_size[1]])
                # Draw seat
                pygame.draw.rect(screen, pygame.Color(200, 200, 100), seat_rect)

            # Move passengers to exit if the train has reached the target position
            if reached_target:
                # Draw the exit doors
                pygame.draw.line(screen, open_door_color, [train.x + 90, 210], [train.x + 140, 210], 5)
                pygame.draw.line(screen, open_door_color, [train.x + 860, 210], [train.x + 910, 210], 5)
                move_passenger(passenger_positions, center_p, train, passenger_speed)
            else:
                # Draw the exit doors
                pygame.draw.line(screen, closed_door_color, [train.x + 90, 210], [train.x + 140, 210], 5)
                pygame.draw.line(screen, closed_door_color, [train.x + 860, 210], [train.x + 910, 210], 5)

            # Draw the passengers
            for i,pos in enumerate(passenger_positions):
                # Adjust passenger positions relative to the moving train
                adjusted_pos = [pos[0] + (train.x - target_train_x), pos[1]]
                # Draw passenger
                pygame.draw.circle(screen, passenger_color[i], adjusted_pos, passenger_radius)

            # Draw the waiting passengers
            for i,pos in enumerate(waiter_positions):
                # Draw waiting passenger
                pygame.draw.circle(screen, waiter_color[i], pos, passenger_radius)

            if collision(passenger_positions, waiter_positions):
                # Display message on screen
                message = font.render("Collision between passenger and waiter!", True, (255, 255, 255))
                screen.blit(message, (400, 50))  # Adjust position as needed
                paused = True

        # Flip the display to put your work on screen
        pygame.display.flip()

        clock.tick(60)  # Limits FPS to 60
    pygame.quit()

main()