from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.core.window import Window

class PongBall(Widget):

    # velocity of the ball on x and y axis
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)

    # referencelist property so we can use ball.velocity as
    # a shorthand, just like e.g. w.pos for w.x and w.y
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    # ``move`` function will move the ball one step. This
    # will be called in equal intervals to animate the ball
    def move(self):
        # self.velocity_y -= 0.4
        self.pos = Vector(*self.velocity) + self.pos

class PongPaddle(Widget):
    score = NumericProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            speedup = 1.1
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * speedup
            ball.velocity = vel.x, vel.y + offset

class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)
    # inside_box_y = True
    w_key = False
    s_key = False
    up_key = False
    down_key = False

    def __init__(self, **kwargs):
        super(PongGame, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_key_down)
        self._keyboard.bind(on_key_up=self._on_key_up)
    
    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_key_down)
        self._keyboard.unbind(on_key_up=self._on_key_up)
        self._keyboard = None

    def _on_key_down(self, keyboard, keycode, text, modifiers):
        move_speed = 30
        if keycode[1] == 'w':
            self.w_key = True
            # self.player1.center_y += move_speed
        elif keycode[1] == 's':
            self.s_key = True
            # self.player1.center_y -= move_speed
        elif keycode[1] == 'up':
            self.up_key = True
            # self.player2.center_y += move_speed
        elif keycode[1] == 'down':
            self.down_key = True
            # self.player2.center_y -= move_speed
        return True
    
    def _on_key_up(self, keyboard, keycode):
        if keycode[1] == 'w':
            self.w_key = False
        elif keycode[1] == 's':
            self.s_key = False
        elif keycode[1] == 'up':
            self.up_key = False
        elif keycode[1] == 'down':
            self.down_key = False
        return True

    def serve_ball(self, vel=(4,0)):
        self.ball.center = self.center
        self.ball.velocity = vel


    def update(self, dt):

        self.ball.move()

        # move paddles with keyboard
        move_speed = 4
        if self.w_key:
            self.player1.center_y += move_speed
        if self.s_key:
            self.player1.center_y -= move_speed
        if self.up_key:
            self.player2.center_y += move_speed
        if self.down_key:
            self.player2.center_y -= move_speed

        # bounce off paddles
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

        # bounce off top and bottom
        if (self.ball.y < 0) or (self.ball.top > self.height):
            # if (self.inside_box_y):
                # self.inside_box_y = False
            self.ball.velocity_y *= -1
            # self.ball.velocity_y += 1
        # else:
        #     self.inside_box_y = True
        
        # score if off side left and right
        if (self.ball.x < self.x):
            self.player2.score += 1
            self.serve_ball(vel=(4,0))

        if (self.ball.right > self.width):
            self.player1.score += 1
            self.serve_ball(vel=(-4,0))           
    
    def on_touch_move(self, touch):
        if touch.x < self.width/3:
            self.player1.center_y = touch.y
        if touch.x > self.width - self.width/3:
            self.player2.center_y = touch.y
    
    def on_key_down(window, keycode, text, modifiers):
        self.player1.score += 1

class PongApp(App):
    def build(self):
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0/60.0)
        return game
    
if __name__ == '__main__':
    PongApp().run()