import asyncio
import platform
import pygame
import math
import random
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Initialize Pygame
try:
    pygame.init()
except pygame.error as e:
    logger.error(f"Pygame initialization failed: {e}")
    raise SystemExit

# Screen settings
WIDTH, HEIGHT = 800, 600
try:
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Water Droplet from Leaf")
except pygame.error as e:
    logger.error(f"Failed to set display mode: {e}")
    raise SystemExit

# Colors
SKY_TOP = (150, 200, 255)  # Light blue
SKY_BOTTOM = (200, 220, 255)  # Pale blue
GROUND_BROWN = (139, 69, 19)  # Earthy brown
LEAF_GREEN = (34, 139, 34)  # Vibrant green
LEAF_DARK_GREEN = (20, 80, 20)  # Darker green for gradient
VEIN_YELLOW = (154, 205, 50)  # Yellow-green veins
WATER_BLUE = (100, 150, 255, 200)  # Semi-transparent blue
SPLASH_BLUE = (135, 206, 235, 150)  # Lighter blue for splash
SHADOW_GRAY = (50, 50, 50, 100)  # Semi-transparent shadow

# Leaf parameters
LEAF_X, LEAF_Y = WIDTH // 2, HEIGHT // 4
LEAF_WIDTH, LEAF_HEIGHT = 120, 40
TIP_X, TIP_Y = LEAF_X + LEAF_WIDTH * 0.8, LEAF_Y + LEAF_HEIGHT * 0.5

# Droplet parameters
droplets = []
splash_particles = []
DROP_INTERVAL = 3  # Seconds between drops
DROP_GROWTH_RATE = 0.4  # Faster growth for larger droplets
MAX_DROP_SIZE = 10  # Increased droplet size
GRAVITY = 0.3
SPLASH_Y = HEIGHT - 50  # Ground level for splash

FPS = 60

def draw_leaf(surface):
    try:
        # Leaf shape (elongated, asymmetric oval with pointed tip)
        leaf_points = []
        for i in range(50):
            t = i / 50.0
            angle = t * math.pi
            x = LEAF_X + LEAF_WIDTH * math.cos(angle) * (1 - t * 0.5)  # Taper towards tip
            y = LEAF_Y + LEAF_HEIGHT * math.sin(angle) * (1 + t * 0.2)  # Slight curve
            leaf_points.append((x, y))
        for i in range(50):
            t = (50 - i) / 50.0
            angle = (1 - t) * math.pi + math.pi
            x = LEAF_X + LEAF_WIDTH * math.cos(angle) * (1 - t * 0.5)
            y = LEAF_Y + LEAF_HEIGHT * math.sin(angle) * (1 + t * 0.2)
            leaf_points.append((x, y))
        
        # Shadow
        shadow_points = [(x + 5, y + 5) for x, y in leaf_points]
        shadow_surface = pygame.Surface((300, 100), pygame.SRCALPHA)
        pygame.draw.polygon(shadow_surface, SHADOW_GRAY, shadow_points)
        surface.blit(shadow_surface, (LEAF_X - 150, LEAF_Y - 50))
        
        # Draw leaf with gradient
        pygame.draw.polygon(surface, LEAF_GREEN, leaf_points)
        inner_points = [(p[0] * 0.95 + LEAF_X * 0.05, p[1] * 0.95 + LEAF_Y * 0.05) for p in leaf_points]
        pygame.draw.polygon(surface, LEAF_DARK_GREEN, inner_points)
        
        # Veins (curved, more detailed)
        for i in range(-3, 4):
            start_x = LEAF_X
            start_y = LEAF_Y
            control_x = LEAF_X + LEAF_WIDTH * 0.4 * math.cos(math.radians(i * 15))
            control_y = LEAF_Y + LEAF_HEIGHT * 0.4 * math.sin(math.radians(i * 15))
            end_x = LEAF_X + LEAF_WIDTH * 0.7 * math.cos(math.radians(i * 15))
            end_y = LEAF_Y + LEAF_HEIGHT * 0.7 * math.sin(math.radians(i * 15))
            points = []
            for t in range(20):
                u = t / 19.0
                x = (1 - u) ** 2 * start_x + 2 * (1 - u) * u * control_x + u ** 2 * end_x
                y = (1 - u) ** 2 * start_y + 2 * (1 - u) * u * control_y + u ** 2 * end_y
                points.append((x, y))
            pygame.draw.lines(surface, VEIN_YELLOW, False, points, 1)
    except Exception as e:
        logger.error(f"Error drawing leaf: {e}")

def draw_droplets(surface):
    try:
        for drop in droplets:
            pygame.draw.circle(surface, WATER_BLUE, (int(drop['x']), int(drop['y'])), int(drop['size']))
    except Exception as e:
        logger.error(f"Error drawing droplets: {e}")

def draw_splash_particles(surface):
    try:
        for particle in splash_particles:
            pygame.draw.circle(surface, SPLASH_BLUE, (int(particle['x']), int(particle['y'])), int(particle['size']))
    except Exception as e:
        logger.error(f"Error drawing splash particles: {e}")

def draw_background(surface):
    try:
        # Sky gradient
        for y in range(HEIGHT // 2):
            r = SKY_TOP[0] + (SKY_BOTTOM[0] - SKY_TOP[0]) * y / (HEIGHT // 2)
            g = SKY_TOP[1] + (SKY_BOTTOM[1] - SKY_TOP[1]) * y / (HEIGHT // 2)
            b = SKY_TOP[2] + (SKY_BOTTOM[2] - SKY_TOP[2]) * y / (HEIGHT // 2)
            pygame.draw.line(surface, (r, g, b), (0, y), (WIDTH, y))
        
        # Ground
        pygame.draw.rect(surface, GROUND_BROWN, (0, HEIGHT // 2, WIDTH, HEIGHT // 2))
    except Exception as e:
        logger.error(f"Error drawing background: {e}")

async def main():
    clock = pygame.time.Clock()
    last_drop_time = pygame.time.get_ticks() / 1000.0
    
    def setup():
        logger.info("Setting up water droplet animation")
    
    def update_loop():
        nonlocal last_drop_time
        try:
            # Create new droplet
            current_time = pygame.time.get_ticks() / 1000.0
            if current_time - last_drop_time > DROP_INTERVAL:
                droplets.append({
                    'x': TIP_X,
                    'y': TIP_Y,
                    'size': 0,
                    'vy': 0,
                    'state': 'growing'
                })
                last_drop_time = current_time
            
            # Update droplets
            for drop in droplets[:]:
                if drop['state'] == 'growing':
                    drop['size'] += DROP_GROWTH_RATE
                    if drop['size'] >= MAX_DROP_SIZE:
                        drop['state'] = 'falling'
                elif drop['state'] == 'falling':
                    drop['vy'] += GRAVITY
                    drop['y'] += drop['vy']
                    if drop['y'] >= SPLASH_Y:
                        # Create splash particles
                        for _ in range(7):  # More particles for larger drop
                            angle = random.uniform(0, math.pi)
                            speed = random.uniform(3, 6)
                            splash_particles.append({
                                'x': drop['x'],
                                'y': SPLASH_Y,
                                'vx': math.cos(angle) * speed,
                                'vy': -math.sin(angle) * speed,
                                'size': random.uniform(2, 4),  # Larger particles
                                'life': 0.6
                            })
                        droplets.remove(drop)
            
            # Update splash particles
            for particle in splash_particles[:]:
                particle['x'] += particle['vx']
                particle['y'] += particle['vy']
                particle['vy'] += GRAVITY / 2
                particle['life'] -= 1.0 / FPS
                if particle['life'] <= 0:
                    splash_particles.remove(particle)
            
            # Draw
            draw_background(screen)
            draw_leaf(screen)
            draw_droplets(screen)
            draw_splash_particles(screen)
            
            pygame.display.flip()
        except Exception as e:
            logger.error(f"Error in update loop: {e}")
    
    setup()
    running = True
    while running:
        try:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            update_loop()
            clock.tick(FPS)
            await asyncio.sleep(1.0 / FPS)
        except Exception as e:
            logger.error(f"Error in main loop: {e}")
            running = False
    
    pygame.quit()

if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())