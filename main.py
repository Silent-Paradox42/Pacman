import pygame

# Initialize pygame
pygame.init()

# Set up screen dimensions
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pac-Man")

# Set up clock for controlling frame rate
clock = pygame.time.Clock()

# Main game loop
def main():
    running = True
    while running:
        clock.tick(60)  # Limit to 60 frames per second
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Fill the screen with black
        screen.fill((0, 0, 0))

        # TODO: Add player and map drawing here

        # Update the display
        pygame.display.update()

    # Quit pygame
    pygame.quit()

# Run the game
if __name__ == "__main__":
    main()
