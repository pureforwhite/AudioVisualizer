#Thanks for watching this coding video
#Please do not forget to subscribe my youtube channel and like my videos, share them
#This source code will be publish under below(including the music)
#if you have any question you can comment below or contact me through every platform
#Love you guys thanks :D

import sys, math, wave, numpy, pygame
from pygame.locals import *
from scipy.fftpack import dct

Number = 30 # number of bars
HEIGHT = 600 # HEIGHT of a bar
WIDTH = 40 #WIDTH of a bar
FPS = 10

file_name = sys.argv[0]
status = 'stopped'
fpsclock = pygame.time.Clock()

#screen init, music playback

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode([Number * WIDTH, 50 + HEIGHT])
pygame.display.set_caption('Audio Visualizer')
my_font = pygame.font.SysFont('consolas', 16)
pygame.mixer.music.load("Nevada.wav")
pygame.mixer.music.play()
pygame.mixer.music.set_endevent()
pygame.mixer.music.set_volume(0.2)
status = "Playing"

#process wave data

f = wave.open("Nevada.wav", 'rb')
params = f.getparams()
nchannels, sampwidth, framerate, nframes = params[:4]
str_data = f.readframes(nframes)
f.close()
wave_data = numpy.fromstring(str_data, dtype = numpy.short)
wave_data.shape = -1, 2
wave_data = wave_data.T

num = nframes

def Visualizer(nums):
    num = int(nums)
    h = abs(dct(wave_data[0][nframes - num:nframes - num + Number]))
    h = [min(HEIGHT, int(i**(1 / 2.5) * HEIGHT / 100)) for i in h]
    draw_bars(h)

def vis(status):
    global num
    if status == "stopped":
        num = nframes
        return
    elif status == "paused":
        Visualizer(num)
    else:
        num -= framerate / FPS
        if num > 0:
            Visualizer(num)

def get_time():
    seconds = max(0, pygame.mixer.music.get_pos() / 1000)
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    hms = ("%02d:%02d:%02d" % (h, m, s))
    return hms

def controller(key):
    global status
    if status == "stopped":
        if key == K_RETURN:
            pygame.mixer_music.play()
            status = "playing"
    elif status == "paused":
        if key == K_RETURN:
            pygame.mixer_music.stop()
            status = "stopped"
        elif key == K_SPACE:
            pygame.mixer.music.unpause()
            status = "playing"
    elif status == "playing":
        if key == K_RETURN:
            pygame.mixer.music.stop()
            status = "stopped"
        elif key == K_SPACE:
            pygame.mixer.music.pause()
            status = "paused"

def draw_bars(h):
    bars = []
    for i in h:
        bars.append([len(bars) * WIDTH , 50 + HEIGHT - i, WIDTH - 1, i])
    for i in bars:
        pygame.draw.rect(screen, [255,255,255], i, 0)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == KEYDOWN:
            controller(event.key)

    if num <= 0:
        status = "stopped"

    name = my_font.render(file_name, True, (255,255,255))
    info = my_font.render(status.upper() + "" + get_time(), True, (255,255,255))
    screen.fill((0,0,0))
    screen.blit(name,(0,0))
    screen.blit(info,(0, 18))
    fpsclock.tick(FPS)
    vis(status)
    pygame.display.update()