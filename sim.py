import pygame

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
    train_speed = (initial_train_x - target_train_x) / (5 * 60)  # Pixels per frame (5 seconds * 60 FPS)
    
    train = pygame.Rect(initial_train_x, train_y, train_width, train_height)
    top_platform = pygame.Rect([0, 0, 1280, 200])
    bot_platform = pygame.Rect([0, 520, 1280, 200])
    passenger_radius = 20
    seat_size = (50, 50)

    passenger_positions = [
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

    waiter_positions = [
        [100, 590], [100, 630], [100, 670], 
        [140, 590], [140, 630], [140, 670], 
        [180, 590], [180, 630], [180, 670], 
        [220, 590], [220, 630], [220, 670], 
        [260, 590], [260, 630], [260, 670], 
        [300, 590], [300, 630], [300, 670], 
        [340, 590], [340, 630], [340, 670], 
        [380, 590], [380, 630], [380, 670],
        [420, 590], [420, 630], [420, 670], 
        [460, 590], [460, 630], [460, 670],
        [820, 590], [820, 630], [820, 670],
        [860, 590], [860, 630], [860, 670],
        [900, 590], [900, 630], [900, 670], 
        [940, 590], [940, 630], [940, 670], 
        [980, 590], [980, 630], [980, 670], 
        [1020, 590], [1020, 630], [1020, 670], 
        [1060, 590], [1060, 630], [1060, 670], 
        [1100, 590], [1100, 630], [1100, 670],
        [1140, 590], [1140, 630], [1140, 670],
        [1180, 590], [1180, 630], [1180, 670]
    ]

    reached_target = False

    while running:
        # Poll for events
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                running = False

        # Update the train's position
        if train.x > target_train_x:
            train.x -= train_speed
            if train.x <= target_train_x:
                train.x = target_train_x
                reached_target = True

        # Fill the screen with a color to wipe away anything from last frame
        screen.fill("grey")

        # Draw the train
        pygame.draw.rect(screen, pygame.Color(255, 0, 0), train)

        # Determine door colors based on train position
        if train.x == target_train_x:
            exit_door_color = pygame.Color(0, 255, 0)
        else:
            exit_door_color = pygame.Color(255, 0, 0)

        # Draw the exit doors
        pygame.draw.line(screen, exit_door_color, [train.x + 90, 210], [train.x + 140, 210], 5)
        pygame.draw.line(screen, exit_door_color, [train.x + 860, 210], [train.x + 910, 210], 5)

        # Draw the entrance doors
        pygame.draw.line(screen, pygame.Color(255, 0, 0), [train.x + 90, 510], [train.x + 140, 510], 5)
        pygame.draw.line(screen, pygame.Color(255, 0, 0), [train.x + 860, 510], [train.x + 910, 510], 5)

        # Draw the platform
        pygame.draw.rect(screen, pygame.Color(175, 100, 0), top_platform)
        pygame.draw.rect(screen, pygame.Color(175, 100, 0), bot_platform)

        # Draw the yellow marker line
        pygame.draw.line(screen, pygame.Color(255, 255, 0), [0, 150], [1280, 150], 5)
        pygame.draw.line(screen, pygame.Color(255, 255, 0), [0, 570], [1280, 570], 5)

        # Draw the waiting passengers
        for pos in waiter_positions:
            # Draw waiting passenger
            pygame.draw.circle(screen, pygame.Color(255, 255, 255), pos, passenger_radius)

        # Move passengers to exit if the train has reached the target position
        if reached_target:
            for i, pos in enumerate(passenger_positions):
                if i < len(passenger_positions) // 2:
                    # Move to the left exit door
                    if pos[0] > train.x + 90:
                        pos[0] -= 1
                else:
                    # Move to the right exit door
                    if pos[0] < train.x + 910:
                        pos[0] += 1

        # Draw the seats
        for pos in seat_positions:
            # Adjust seat positions relative to the moving train
            seat_rect = pygame.Rect([pos[0] + (train.x - target_train_x), pos[1], seat_size[0], seat_size[1]])
            # Draw seat
            pygame.draw.rect(screen, pygame.Color(200, 200, 200), seat_rect)

        # Draw the passengers
        for pos in passenger_positions:
            # Adjust passenger positions relative to the moving train
            adjusted_pos = [pos[0] + (train.x - target_train_x), pos[1]]
            # Draw passenger
            pygame.draw.circle(screen, pygame.Color(255, 255, 255), adjusted_pos, passenger_radius)

        # Flip the display to put your work on screen
        pygame.display.flip()

        clock.tick(60)  # Limits FPS to 60
    pygame.quit()

main()
