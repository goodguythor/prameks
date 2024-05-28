import pygame

def main():
    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True

    train = pygame.Rect([140, 210, 1000, 300])
    seat_size = (50, 50)
    passenger_radius = 20

    # List of passenger positions
    passenger_positions = [
        [180, 240], [180, 300], [180, 420], [180, 480],
        [330, 240], [330, 300], [330, 420], [330, 480],
        [400, 240], [400, 300], [400, 420], [400, 480],
        [470, 240], [470, 300], [470, 420], [470, 480],
        [540, 240], [540, 300], [540, 420], [540, 480],
        [610, 240], [610, 300], [610, 420], [610, 480],
        [710, 240], [710, 300], [710, 420], [710, 480],
        [780, 240], [780, 300], [780, 420], [780, 480],
        [850, 240], [850, 300], [850, 420], [850, 480],
        [920, 240], [920, 300], [920, 420], [920, 480],
        [990, 240], [990, 300], [990, 420], [990, 480],
        [1100, 240], [1100, 300], [1100, 420], [1100, 480]
    ]

    while running:
        # Poll for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Fill the screen with a color to wipe away anything from last frame
        screen.fill("black")

        # Draw the train
        pygame.draw.rect(screen, pygame.Color(255, 0, 0), train)

        # Draw the seats and passengers
        for pos in passenger_positions:
            # Draw seat
            seat_rect = pygame.Rect(pos[0] - seat_size[0] // 2, pos[1] - seat_size[1] // 2, seat_size[0], seat_size[1])
            pygame.draw.rect(screen, pygame.Color(200, 200, 200), seat_rect)

            # Draw passenger
            pygame.draw.circle(screen, pygame.Color(255, 255, 255), pos, passenger_radius)

        # Flip the display to put your work on screen
        pygame.display.flip()

        clock.tick(60)  # Limits FPS to 60
    pygame.quit()

main()
