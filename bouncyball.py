import pygame
import pymunk
import pymunk.pygame_util

def create_ball(space):
    body = pymunk.Body(1, pymunk.moment_for_circle(1, 0, 20))
    body.position = (400, 50)
    shape = pymunk.Circle(body, 20)
    shape.elasticity = 0.02
    space.add(body, shape)
    shape.color = (0, 0, 0, 255)  # Red color (RGBA)
    return body, shape

def create_line(space, angle):
    body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
    body.position = (400, 550)
    
    length = 400
    a = (-length//2, 0)
    b = (length//2, 0)
    
    shape = pymunk.Segment(body, a, b, 5)
    shape.elasticity = 1.0
    shape.friction = 0.8
    shape.color = (150, 75, 0, 255)  # Red color (RGBA)
    shape.body.angle = angle
    space.add(body, shape)
    return body, shape

def game():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    space = pymunk.Space()
    space.gravity = (0, 981)
    draw_options = pymunk.pygame_util.DrawOptions(screen)
    
    font = pygame.font.Font(None, 36)
    score = 0
    frame_count = 0
    
    # Load background image
    background = pygame.image.load("bg.jpg")
    background = pygame.transform.scale(background, (800, 600))
    
    ball_body, ball_shape = create_ball(space)
    line_body, line = create_line(space, angle=0.1)  # Line starts slightly slanted
    
    running = True
    game_over = False
    while running:
        screen.blit(background, (0, 0))  # Draw background
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        if not game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                line_body.angle -= 0.02
            if keys[pygame.K_RIGHT]:
                line_body.angle += 0.02
            
            space.step(1 / 60)
            space.debug_draw(draw_options)
            
            if ball_body.position.y > 600:
                game_over = True
            else:
                frame_count += 1
                if frame_count % 60 == 0:  # Increase score every second
                    score += 1
            
            score_text = font.render(f"Score: {score}", True, (0,0,0))
            screen.blit(score_text, (10, 10))
        else:
            screen.fill((0, 0, 0))
            game_over_text = font.render("Game Over!", True, (255, 0, 0))
            final_score_text = font.render(f"Final Score: {score}", True, (255, 255, 255))
            screen.blit(game_over_text, (350, 250))
            screen.blit(final_score_text, (350, 300))
            pygame.display.flip()
            pygame.time.delay(3000)
            running = False
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

game()
