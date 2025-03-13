import pygame
import pymunk
import pymunk.pygame_util

def create_ball(space):
    body = pymunk.Body(1, pymunk.moment_for_circle(1, 0, 20))
    body.position = (400, 50)
    shape = pymunk.Circle(body, 20)
    shape.elasticity = 1.0
    space.add(body, shape)
    return body, shape

def create_line(space, angle):
    body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
    body.position = (400, 550)
    
    length = 200
    a = (-length//2, 0)
    b = (length//2, 0)
    
    shape = pymunk.Segment(body, a, b, 5)
    shape.elasticity = 1.0
    shape.friction = 0.8
    shape.body.angle = angle
    space.add(body, shape)
    return body, shape

def create_walls(space):
    top_wall = pymunk.Segment(space.static_body, (0, 0), (800, 0), 5)
    top_wall.elasticity = 1.0
    static_body = space.static_body
    left_wall = pymunk.Segment(static_body, (0, 0), (0, 600), 5)
    right_wall = pymunk.Segment(static_body, (800, 0), (800, 600), 5)
    left_wall.elasticity = 1.0
    right_wall.elasticity = 1.0
    space.add(left_wall, right_wall, top_wall)

def game():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    space = pymunk.Space()
    space.gravity = (0, 981)
    draw_options = pymunk.pygame_util.DrawOptions(screen)
    
    ball_body, ball_shape = create_ball(space)
    line_body, line = create_line(space, angle=0.1)  # Line starts slightly slanted
    create_walls(space)  # Add walls to bounce back the ball
    
    running = True
    while running:
        bg = pygame.image.load('bg.jpg')
        screen.blit(bg, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    ball_body.velocity = (ball_body.velocity.x, -700)  # Boost ball upwards
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            line_body.angle -= 0.05
        if keys[pygame.K_RIGHT]:
            line_body.angle += 0.05
        
        space.step(1 / 60)
        space.debug_draw(draw_options)
        pygame.display.flip()
        clock.tick(60)
        
        # Game Over Condition
        if ball_body.position.y > 600:
            print("Game Over!")
            running = False
    
    pygame.quit()

game()
