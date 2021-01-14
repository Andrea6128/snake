import pyglet, random
from pathlib import Path
from pyglet.window import key


# IS_TITLE = True  # if first run, show title screen

def initial_settings():
    """ set global variables """

    global TILES_DIRECTORY
    global WINDOW_WIDTH
    global WINDOW_HEIGHT
    global TILE_SIZE
    global TILE_COUNT_X
    global TILE_COUNT_Y
    global SNAKE
    global FOOD
    global STEPS
    global PRESSED_KEYS
    global SCORE
    global DIRECTION
    global SPEED
    global IS_END
    # global IS_TITLE

    TILES_DIRECTORY = Path('assets/snake-tiles')
    WINDOW_WIDTH = 1000
    WINDOW_HEIGHT = 800
    TILE_SIZE = WINDOW_WIDTH // 20
    TILE_COUNT_X = (WINDOW_WIDTH // TILE_SIZE) - 1
    TILE_COUNT_Y = (WINDOW_HEIGHT // TILE_SIZE) - 1
    SNAKE = [(2, 2), (3, 2), (4, 2)]
    FOOD = [(2, 5)]
    STEPS = [0]
    PRESSED_KEYS = set()
    SCORE = [0]
    DIRECTION = (1, 0)  # default direction is to the right
    SPEED = .2
    IS_END = False
    # IS_TITLE = False


def collect_filenames():
    """ this makes a dict with picture names from the directory """

    all_png_files = list(TILES_DIRECTORY.glob('*.png'))
    pictures = {}
    for path in all_png_files:
        pictures[path.stem] = pyglet.image.load(path)

    return pictures


# TODO
def title_screen():
    global IS_TITLE
    IS_TITLE = True

    window.clear()
    pyglet.clock.unschedule(tik)

    label_title_text = pyglet.text.Label('TITLE SCREEN!',
                            font_name='Courier New',
                            font_size=32,
                            bold=True,
                            color=(230, 230, 230, 230),
                            x=window.width // 2, y=(window.height // 2) - 64,
                            anchor_x='center', anchor_y='center')
    label_title_text.draw()
    print("stop here")


def game_over(message):
    """ game over screen """

    global IS_END
    IS_END = True

    window.clear()
    pyglet.clock.unschedule(tik)
    label_game_over_score = pyglet.text.Label('Your score is '+str(SCORE[0]),
                            font_name='16bfZX',
                            font_size=48,
                            color=(230, 230, 230, 230),
                            x=window.width // 2, y=(window.height // 2) - 64,
                            anchor_x='center', anchor_y='center')
    label_game_over_score.draw()
    label_bye = pyglet.text.Label(message,
                            font_name='16bfZX',
                            font_size=32,
                            bold=True,
                            color=(220, 220, 220, 220),
                            x=window.width // 2, y=(window.height // 2) + 128,
                            anchor_x='center', anchor_y='center')
    label_bye.draw()
    label_escape = pyglet.text.Label('Press [ENTER] to play again or [ESC] to exit',
                            font_name='16bfZX',
                            font_size=32,
                            color=(170, 170, 170, 170),
                            x=window.width // 2, y=(window.height // 4),
                            anchor_x='center', anchor_y='center')
    label_escape.draw()

    game_over_picture.x = (window.width - game_over_picture.width) // 2
    game_over_picture.y = window.height // 2
    game_over_picture.draw()


def tik(t):
    """ sets time interval """

    # print("tik", t)

    STEPS[0] += 1

    # add new snake tile and delete last tile
    current_x = SNAKE[-1][0]
    current_y = SNAKE[-1][1]
    new_x = current_x + DIRECTION[0]
    new_y = current_y + DIRECTION[1]
    SNAKE.append((new_x, new_y))
    del SNAKE[0]

    if DIRECTION == (1, 0):
        snake.x = snake.x + 64
    if DIRECTION == (-1, 0):
        snake.x = snake.x - 64
    if DIRECTION == (0, 1):
        snake.y = snake.y + 64
    if DIRECTION == (0, -1):
        snake.y = snake.y - 64


def key_press(symbol, modificators):
    """ tests pressed keys (WSAD or arrows) """

    if symbol == key.W or symbol == key.UP:
        PRESSED_KEYS.add((0, 1))
    if symbol == key.S or symbol == key.DOWN:
        PRESSED_KEYS.add((0, -1))
    if symbol == key.A or symbol == key.LEFT:
        PRESSED_KEYS.add((-1, 0))
    if symbol == key.D or symbol == key.RIGHT:
        PRESSED_KEYS.add((1, 0))
    if symbol == key.RETURN and IS_END:
        restart_game()
    # if symbol == key.R and IS_TITLE:
    #     restart_game()


def key_release(symbol, modificators):
    """ tests released keys """

    if symbol == key.W or symbol == key.UP:
        PRESSED_KEYS.discard((0, 1))
    if symbol == key.S or symbol == key.DOWN:
        PRESSED_KEYS.discard((0, -1))
    if symbol == key.A or symbol == key.LEFT:
        PRESSED_KEYS.discard((-1, 0))
    if symbol == key.D or symbol == key.RIGHT:
        PRESSED_KEYS.discard((1, 0))


def playfield_collision_test():
    """ border collision test """

    reason_message = "The snake ran out of the playground"
    if SNAKE[-1][0] > TILE_COUNT_X or SNAKE[-1][0] < 0:
        game_over(reason_message)
        return True

    if SNAKE[-1][1] > TILE_COUNT_Y or SNAKE[-1][1] < 0:
        game_over(reason_message)
        return True

    return False


def eat_itself():
    """ if snake eats itself """

    if SNAKE[-1] in SNAKE[:-2]:
        print("snake ate itself")
        game_over("The snake ate itself")
        return True

    return False


def test_keys():
    """ assign pressed key to a direction """

    global DIRECTION
    if (1, 0) in PRESSED_KEYS:
        DIRECTION = (1, 0)
    if (-1, 0) in PRESSED_KEYS:
        DIRECTION = (-1, 0)
    if (0, 1) in PRESSED_KEYS:
        DIRECTION = (0, 1)
    if (0, -1) in PRESSED_KEYS:
        DIRECTION = (0, -1)


def eat_food():
    """ eat food function """

    new_food_x = random.randint(0, TILE_COUNT_X)
    new_food_y = random.randint(0, TILE_COUNT_Y)

    if SNAKE[-1] == FOOD[-1]:  # eat with snake's head

        # while the generated food is on snake's position, keep generating new one somewhere else
        if ((new_food_x, new_food_y)) in SNAKE[:-1]:
            new_food_x = random.randint(0, TILE_COUNT_X)
            new_food_y = random.randint(0, TILE_COUNT_Y)

        FOOD.append((new_food_x, new_food_y))
        del FOOD[0]

        # add piece of snake to the end
        SNAKE.insert(0, (SNAKE[0][0], SNAKE[0][1]))

        print(FOOD)
        SCORE[0] += 1


def get_image_name(index):
    """ gets tile name from filename """

    x_actual, y_actual = SNAKE[index]
    name_prev = 'tail'
    name_next = 'head'

    # test of current tile and previous tile
    if index == 0:  # if index is 0, it's always 'tail'
        name_prev = "tail"
    else:
        x_prev, y_prev = SNAKE[index - 1]  # else it sucks

        if x_actual == x_prev and y_actual == y_prev - 1:
            name_prev = "top"
        if x_actual == x_prev and y_actual == y_prev + 1:
            name_prev = "bottom"
        if x_actual == x_prev - 1 and y_actual == y_prev:
            name_prev = "right"
        if x_actual == x_prev + 1 and y_actual == y_prev:
            name_prev = "left"

    # test of current tile and next tile
    if index == len(SNAKE) - 1:  # if index is last, it's 'head'
        name_next = "head"
    else:
        x_actual, y_actual = SNAKE[index]  # else it sucks
        x_next, y_next = SNAKE[index + 1]

        if x_actual == x_next and y_actual == y_next - 1:
            name_next = "top"
        if x_actual == x_next and y_actual == y_next + 1:
            name_next = "bottom"
        if x_actual == x_next - 1 and y_actual == y_next:
            name_next = "right"
        if x_actual == x_next + 1 and y_actual == y_next:
            name_next = "left"

    return name_prev + "-" + name_next


def draw_score():
    """ draws score text """

    # font_size parameter reflects window size
    label_score = pyglet.text.Label(str(SCORE[0]),
                          font_name='16bfZX',
                          font_size=int(TILE_SIZE),
                          x=(window.width / 2) - int(TILE_SIZE // 2), y=window.height - (TILE_SIZE / 1.2))
    label_score.draw()

    label_steps = pyglet.text.Label(str(STEPS[0]),
                          font_name='16bfZX',
                          font_size=int(TILE_SIZE // 2),
                          color=(48, 114, 255, 255),
                          x=TILE_SIZE // 5, y=window.height - (TILE_SIZE // 2))
    label_steps.draw()


def draw_all():
    """ main draw function """

    window.clear()
    draw_score()

    # sprite's edges smoothing
    pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
    pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
 
    test_keys()
    eat_food()

    if playfield_collision_test() == False and eat_itself() == False:

        # draw snake
        # not mine :'(
        for index, value in enumerate(SNAKE):
            snake_piece_img_name = get_image_name(index)
            snake_cell = picture_names[snake_piece_img_name]
            snake_cell.blit(value[0] * TILE_SIZE, value[1] * TILE_SIZE, width=TILE_SIZE, height=TILE_SIZE)

        # draw food
        # copies snake drawing idea above, but uses "apple" image only
        for index, value in enumerate(FOOD):
            food_cell = picture_names["apple"]
            food_cell.blit(value[0] * TILE_SIZE, value[1] * TILE_SIZE, width=TILE_SIZE, height=TILE_SIZE)

           
def restart_game():
    """ sets all global variables again for game restart """

    initial_settings()

    window.clear()
    pyglet.clock.schedule_interval(tik, SPEED)


# first start
initial_settings()
window = pyglet.window.Window(width=WINDOW_WIDTH, height=WINDOW_HEIGHT)

picture_names = collect_filenames()  # get dict with tile names

snake = pyglet.sprite.Sprite(picture_names['left-dead'])
food = pyglet.sprite.Sprite(picture_names['apple'])
game_over_picture = pyglet.sprite.Sprite(picture_names['game_over'])

pyglet.font.add_file('assets/font/16bfZX.ttf')
my_font = pyglet.font.load('16bfZX, 16')


# main loop
if __name__ == "__main__":
    window.push_handlers(
    on_draw=draw_all,
    on_key_press=key_press,
    on_key_release=key_release,
    )

    pyglet.clock.schedule_interval(tik, SPEED)

    pyglet.app.run()
