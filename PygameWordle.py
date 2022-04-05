import pygame
from pygame import gfxdraw

from WordleGame import WordleGame
from EvilWordleGame import EvilWordleGame

pygame.init()
game = WordleGame()

# TODO: implement color_flash and color_flash_timer (see the K_RETURN code)

# things to tweak
bigfontsize = 48
smallfontsize = 18
fontwewant = "couriernew"
mycolors = [(0,    43,  54),  # bg color
            (238, 232, 213),  # font color
            (88,  110, 117),  # input word bubble color
            (88,  110, 117),  # guessed word bubble color
            (181, 137,   0),  # guessed word bubble color (correct character)
            (133, 153,   0),  # guessed word bubble color (correct position)
            (88,  110, 117),  # keyboard word bubble color
            (203,  75,  22),  # keyboard word bubble color (bad)
            (133, 153,   0),  # keyboard word bubble color (good)
            (203,  75,  22),  # input word bubble color (invalid word)
            ]

width = 640
height = 520
size = (width, height)
screen = pygame.display.set_mode(size)


# font initialization
fontlist = pygame.font.get_fonts()
if fontwewant in fontlist:
    fontpath = pygame.font.match_font(fontwewant, bold=True)
    bigfont = pygame.font.Font(fontpath, bigfontsize)
    smallfont = pygame.font.Font(fontpath, smallfontsize)
else:
    message = """You do not have %s installed.
    You may change the default monospace font \
    in the code under the variable fontwewant.""" % fontwewant
    raise pygame.error(message)


def drawRoundedRect(surface, color, rect, rad=None):
    if rad is None:
        rad = min(rect[2], rect[3])//3

    pygame.draw.rect(surface, color,
                     [rect[0]+rad, rect[1], rect[2]-(rad*2), rect[3]])
    pygame.draw.rect(surface, color,
                     [rect[0], rect[1]+rad, rect[2], rect[3]-(rad*2)])

    circlecenters = [(rect[0]+rad, rect[1]+rad),
                     (rect[0]+rect[2]-(rad+1), rect[1]+rad),
                     (rect[0]+rad, rect[1]+rect[3]-(rad+1)),
                     (rect[0]+rect[2]-(rad+1), rect[1]+rect[3]-(rad+1))]

    for cc in circlecenters:
        pygame.gfxdraw.aacircle(surface, cc[0], cc[1], rad, color)
        pygame.gfxdraw.filled_circle(surface, cc[0], cc[1], rad, color)


# scale is width
# scale*1.5 is height
# bcolor -> bubble color
# fcolor -> font color
def drawBubbleWord(surface, word, corner, scale, bcolor, fcolor, spacing=None):
    if spacing is None:
        spacing = scale//5

    for i in range(len(word)):
        rect = (corner[0]+(scale+spacing)*i, corner[1], scale, int(scale*1.5))
        drawRoundedRect(surface, bcolor[i], rect)

        if scale > 30:
            renderedfont = bigfont.render(word[i], True, fcolor)
        else:
            renderedfont = smallfont.render(word[i], True, fcolor)

        fontcorner = [rect[0]+((scale-renderedfont.get_width())//2),
                      rect[1]+((int(scale*1.5)-renderedfont.get_height())//2)]
        surface.blit(renderedfont, fontcorner)


def keyboardColor(char, used_letters, good_letters):
    if char in good_letters:
        return mycolors[8]
    elif char in used_letters:
        return mycolors[7]
    else:
        return mycolors[6]


flag = True
current_word = ""
displayed_guesses = 6

clock = pygame.time.Clock()

color_flash = (0, 0, 0)
color_flash_timer = 0

while flag:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            flag = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                flag = False
            elif event.key in [pygame.K_DELETE, pygame.K_BACKSPACE]:
                if len(current_word) > 0:
                    current_word = current_word[:-1]
            elif event.key == pygame.K_RETURN:
                if len(current_word) == 5:
                    print(current_word)
                    dist = game.guessWord(current_word)
                    if dist is not None:
                        if all([el == 2 for el in dist]):
                            print("used %d guesses" % len(game.getState()))
                            color_flash_timer = -1
                            color_flash = mycolors[4]
                        else:
                            current_word = ""
                    else:
                        color_flash_timer = 300
                        color_flash = mycolors[9]
                        print("invalid word")
            elif pygame.K_a <= event.key <= pygame.K_z:
                if len(current_word) < 5 and not game.gameWon():
                    current_word += event.unicode.upper()

    screen.fill(mycolors[0])

    # draw the input
    padded_word = current_word+" "*(5-len(current_word))
    if color_flash_timer == 0:
        bcolors = [mycolors[2]]*5
    else:
        bcolors = [color_flash]*5
        color_flash_timer = color_flash_timer - clock.get_time()
        if color_flash_timer < 0:
            color_flash_timer = 0

    drawBubbleWord(screen, padded_word, (320, 25), 50, bcolors, mycolors[1])

    # draw your current guesses
    game_state = game.getState()
    for i in range(displayed_guesses):
        corner = (30, 30 + (80*i))
        if i < len(game_state):
            index = i + max(0, len(game_state)-displayed_guesses)
            bcolors = [mycolors[3+game_state[index][1][j]] for j in range(5)]
            word = game_state[index][0]
            drawBubbleWord(screen, word, corner, 40, bcolors, mycolors[1])
        else:
            drawBubbleWord(screen, " "*5, corner, 40, [mycolors[3]]*5, mycolors[1])

    # draw the keyboard
    ul = game.getUsedLetters()
    bl = game.getGoodLetters()
    kcolors = [keyboardColor(char, ul, bl) for char in "QWERTYUIOP"]
    drawBubbleWord(screen, "QWERTYUIOP", (360, 350), 20, kcolors, mycolors[1])
    kcolors = [keyboardColor(char, ul, bl) for char in "ASDFGHJKL"]
    drawBubbleWord(screen, "ASDFGHJKL", (372, 385), 20, kcolors, mycolors[1])
    kcolors = [keyboardColor(char, ul, bl) for char in "ZXCVBNM"]
    drawBubbleWord(screen, "ZXCVBNM", (384, 420), 20, kcolors, mycolors[1])

    # frame stuff
    pygame.display.flip()
    clock.tick(50)  # run the game at <50 frames a sec
    # pygame.time.wait(10)

pygame.quit()
