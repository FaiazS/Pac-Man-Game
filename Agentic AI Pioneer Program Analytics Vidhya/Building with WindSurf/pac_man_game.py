# Import necessary modules
# Pygame for game development
# Random for random number generation
# Math for mathematical calculations
import pygame
import random
import math

# Initialize Pygame - this must be done before using any Pygame functions
pygame.init()

# Game Constants
# These values define the basic parameters of our game window and game mechanics
# WINDOW_WIDTH and WINDOW_HEIGHT determine the size of our game window
# GRID_SIZE is the size of each grid cell in pixels (32x32 pixels)
# FPS (Frames Per Second) controls how fast the game runs
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 32
FPS = 20  # Reduced speed for better control (30 FPS was too fast)

# Color Constants
# RGB color values for different elements in the game
# Each color is represented as a tuple (Red, Green, Blue)
BLACK = (0, 0, 0)      # Background color
WHITE = (255, 255, 255)  # Pellet color
YELLOW = (255, 255, 0)   # Pac-Man color
RED = (255, 0, 0)       # First ghost color
BLUE = (0, 0, 255)      # Second ghost color
ORANGE = (255, 165, 0)  # Third ghost color
PURPLE = (128, 0, 128)  # Fourth ghost color

# Direction Constants
# These tuples represent movement directions
# Each direction is a tuple (x_movement, y_movement)
# For example, UP = (0, -1) means move 0 pixels horizontally and -1 pixel vertically
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Game Setup
# Create the main game window
# Set the window title
# Create a clock object to control the frame rate
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Pac-Man")
clock = pygame.time.Clock()

# Player Class
# This class represents Pac-Man, the main character of the game
class Player:
    def __init__(self):
        # Initialize Pac-Man's starting position
        # Start in the middle of the screen, aligned with the grid
        self.x = GRID_SIZE * 5
        self.y = GRID_SIZE * 5
        
        # Set initial direction to RIGHT
        self.direction = RIGHT
        
        # Speed is equal to one grid cell per frame
        self.speed = GRID_SIZE
        
        # Initialize score to 0
        self.score = 0
        
        # Mouth animation variables
        # mouth_open controls whether the mouth is open or closed
        # mouth_timer controls the timing of the mouth animation
        # mouth_angle is used for smooth mouth movement
        self.mouth_open = False
        self.mouth_timer = 0
        self.mouth_angle = 0

    def move(self, direction):
        # Set Pac-Man's direction based on user input
        self.direction = direction

    def update(self):
        # Move Pac-Man based on current direction
        self.x += self.direction[0] * self.speed
        self.y += self.direction[1] * self.speed
        
        # Keep Pac-Man within the game boundaries
        # Use max() and min() to ensure Pac-Man doesn't go out of bounds
        self.x = max(0, min(WINDOW_WIDTH - GRID_SIZE, self.x))
        self.y = max(0, min(WINDOW_HEIGHT - GRID_SIZE, self.y))
        
        # Handle mouth animation
        # Increment mouth_timer to track animation frames
        self.mouth_timer += 1
        
        # Change mouth state every 10 frames
        if self.mouth_timer >= 10:
            self.mouth_open = not self.mouth_open
            self.mouth_timer = 0
            
            # Increment mouth angle for smoother animation
            self.mouth_angle += 20
            if self.mouth_angle >= 360:
                self.mouth_angle = 0

    def draw(self):
        # Draw Pac-Man with mouth animation
        # Calculate center position of Pac-Man
        center_x = self.x + GRID_SIZE//2
        center_y = self.y + GRID_SIZE//2
        radius = GRID_SIZE//2
        
        # Draw the yellow circle body
        pygame.draw.circle(screen, YELLOW, (center_x, center_y), radius)
        
        # Draw the mouth when it's open
        if self.mouth_open:
            # Calculate mouth points using trigonometry
            # Create 20 points around the circle to form a smooth curve
            angle = math.radians(self.mouth_angle)
            points = []
            for i in range(20):
                angle_i = angle + (i * 2 * math.pi / 20)
                x = center_x + radius * math.cos(angle_i)
                y = center_y + radius * math.sin(angle_i)
                points.append((x, y))
            
            # Add the center point to complete the mouth shape
            points.append((center_x, center_y))
            
            # Draw the black mouth polygon
            pygame.draw.polygon(screen, BLACK, points)

# Ghost Class
# Represents the enemies in the game
class Ghost:
    def __init__(self, color, start_pos):
        # Initialize ghost position
        self.x, self.y = start_pos
        
        # Random initial direction
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        
        # Set ghost color
        self.color = color
        
        # Ghost moves slower than Pac-Man
        self.speed = GRID_SIZE * 0.5
        
        # Variables for movement logic
        self.target = None
        self.target_timer = 0
        self.movement_timer = 0

    def update(self):
        # Update target position every 30 frames (about once per second)
        self.target_timer += 1
        if self.target_timer >= 30:
            # Choose a random target position within the game boundaries
            self.target = (random.randint(0, WINDOW_WIDTH//GRID_SIZE) * GRID_SIZE,
                         random.randint(0, WINDOW_HEIGHT//GRID_SIZE) * GRID_SIZE)
            self.target_timer = 0

        # Move towards target
        if self.target:
            target_x, target_y = self.target
            
            # Move every 5 frames for smoother animation
            self.movement_timer += 1
            if self.movement_timer >= 5:
                self.movement_timer = 0
                
                # Move in grid-aligned steps
                # Use max() and min() to keep ghost within bounds
                if target_x < self.x:
                    self.x = max(0, self.x - self.speed)
                elif target_x > self.x:
                    self.x = min(WINDOW_WIDTH - GRID_SIZE, self.x + self.speed)
                
                if target_y < self.y:
                    self.y = max(0, self.y - self.speed)
                elif target_y > self.y:
                    self.y = min(WINDOW_HEIGHT - GRID_SIZE, self.y + self.speed)

    def draw(self):
        # Draw ghost as a colored circle
        pygame.draw.circle(screen, self.color, (self.x + GRID_SIZE//2, self.y + GRID_SIZE//2), GRID_SIZE//2)

# Level Class
# Manages game progression and level-specific elements
class Level:
    def __init__(self, level_number):
        # Store current level number
        self.level_number = level_number
        
        # Calculate number of ghosts based on level
        # Maximum of 4 ghosts
        self.ghost_count = min(4, level_number + 1)
        
        # Colors for different ghosts
        self.ghost_colors = [RED, BLUE, ORANGE, PURPLE]
        
        # Track number of pellets
        self.pellet_count = 0
        
        # Timer for level completion text
        self.level_text_timer = 0

    def create_ghosts(self):
        # Create ghosts at specific starting positions
        ghosts = []
        positions = [
            # Top-left corner
            (GRID_SIZE * 2, GRID_SIZE * 2),
            # Top-right corner
            (WINDOW_WIDTH - GRID_SIZE * 3, GRID_SIZE * 2),
            # Bottom-left corner
            (GRID_SIZE * 2, WINDOW_HEIGHT - GRID_SIZE * 3),
            # Bottom-right corner
            (WINDOW_WIDTH - GRID_SIZE * 3, WINDOW_HEIGHT - GRID_SIZE * 3)
        ]
        
        # Create ghosts up to the current level's ghost count
        for i in range(self.ghost_count):
            ghosts.append(Ghost(self.ghost_colors[i], positions[i]))
        return ghosts

    def create_pellets(self):
        pellets = []
        # Create pellets in a grid pattern with spacing
        # Start from GRID_SIZE to avoid edge collisions
        for x in range(GRID_SIZE, WINDOW_WIDTH - GRID_SIZE, GRID_SIZE * 2):
            for y in range(GRID_SIZE, WINDOW_HEIGHT - GRID_SIZE, GRID_SIZE * 2):
                # Don't place pellets where ghosts start
                # Check distance from all ghost starting positions
                ghost_positions = [
                    (GRID_SIZE * 2, GRID_SIZE * 2),
                    (WINDOW_WIDTH - GRID_SIZE * 3, GRID_SIZE * 2),
                    (GRID_SIZE * 2, WINDOW_HEIGHT - GRID_SIZE * 3),
                    (WINDOW_WIDTH - GRID_SIZE * 3, WINDOW_HEIGHT - GRID_SIZE * 3)
                ]
                
                # Only add pellet if it's far enough from ghost positions
                if all(abs(x - g[0]) > GRID_SIZE * 2 and abs(y - g[1]) > GRID_SIZE * 2 for g in ghost_positions):
                    pellets.append((x, y))
        
        # Store total number of pellets
        self.pellet_count = len(pellets)
        return pellets

# Game Initialization Function
def initialize_game():
    # Create and return all game objects
    player = Player()
    level = Level(1)
    ghosts = level.create_ghosts()
    pellets = level.create_pellets()
    return player, level, ghosts, pellets

# Main Game Loop Function
def main():
    # Game state variables
    running = True
    current_level = 1
    show_level_text = True
    level_text_timer = 0
    
    # Initialize all game objects
    player, level, ghosts, pellets = initialize_game()
    
    while running:
        # Event Handling
        for event in pygame.event.get():
            # Check if user wants to quit
            if event.type == pygame.QUIT:
                running = False
            
            # Handle keyboard input
            elif event.type == pygame.KEYDOWN:
                # Change Pac-Man's direction based on arrow keys
                if event.key == pygame.K_UP:
                    player.move(UP)
                elif event.key == pygame.K_DOWN:
                    player.move(DOWN)
                elif event.key == pygame.K_LEFT:
                    player.move(LEFT)
                elif event.key == pygame.K_RIGHT:
                    player.move(RIGHT)

        # Update Game State
        # Update Pac-Man's position
        player.update()
        
        # Update all ghosts
        for ghost in ghosts:
            ghost.update()

        # Collision Detection
        # Check pellet collection
        player_pos = (player.x, player.y)
        for pellet in pellets[:]:  # Use [:] to create a copy of the list for safe removal
            # Check if Pac-Man is close enough to a pellet
            if abs(pellet[0] - player.x) < GRID_SIZE and abs(pellet[1] - player.y) < GRID_SIZE:
                # Remove pellet and increase score
                pellets.remove(pellet)
                player.score += 10

        # Check ghost collision
        for ghost in ghosts:
            # If Pac-Man collides with a ghost, game over
            if abs(ghost.x - player.x) < GRID_SIZE and abs(ghost.y - player.y) < GRID_SIZE:
                print(f"Game Over! Score: {player.score}")
                running = False

        # Level Progression
        # When all pellets are collected, move to next level
        if len(pellets) == 0:
            current_level += 1
            print(f"Level {current_level} completed!")
            # Reset game with new level
            player, level, ghosts, pellets = initialize_game()
            show_level_text = True

        # Drawing
        # Clear screen with black background
        screen.fill(BLACK)
        
        # Draw all pellets
        for pellet in pellets:
            # Draw white pellets at each pellet position
            pygame.draw.circle(screen, WHITE, (pellet[0] + GRID_SIZE//2, pellet[1] + GRID_SIZE//2), 2)
        
        # Draw Pac-Man and all ghosts
        player.draw()
        for ghost in ghosts:
            ghost.draw()
        
        # Draw UI Elements
        # Create font for text rendering
        font = pygame.font.Font(None, 36)
        
        # Draw score
        score_text = font.render(f"Score: {player.score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        
        # Draw level number
        level_text = font.render(f"Level: {current_level}", True, WHITE)
        screen.blit(level_text, (10, 50))

        # Show level completion message
        if show_level_text:
            # Create and center level completion text
            level_text = font.render(f"Level {current_level}!", True, WHITE)
            text_rect = level_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
            screen.blit(level_text, text_rect)
            
            # Timer to hide the message after 2 seconds (60 frames at 30 FPS)
            level_text_timer += 1
            if level_text_timer >= 60:
                show_level_text = False
                level_text_timer = 0

        # Update Display
        # Flip the display buffer to show all drawn elements
        pygame.display.flip()
        
        # Control frame rate
        clock.tick(FPS)

    # Clean up
    pygame.quit()

# Entry Point
# This ensures the game only runs when the script is executed directly
if __name__ == "__main__":
    main()
