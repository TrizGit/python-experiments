# This script will play music based on the playlist on "musicPL"
# A few things need to be clarified:
# - This whole thing is completely unnecessary unless you have a broken media player. (Not me)
# - Looks nicer if the "Title", "Contributing Artist", and "Genre" is filled.
# - Song order based on the number on the filename, so a NaN completely stops the script. 

import pygame
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
import os, sys
import time
import psutil

os.environ['SDL_VIDEO_WINDOW_POS'] = '0,0'

# Initialize pygame and the mixer
pygame.init()
pygame.mixer.init()

# Screen setup
screen = pygame.display.set_mode((500, 150), pygame.NOFRAME | pygame.SRCALPHA)
pygame.display.set_caption("USB Playlist")

# Define colors and font
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
L_BLUE = (0, 255, 255)
RED = (255, 0, 0)
PURPLE = (255, 0, 255)
D_PURPLE = (200, 0, 200)
ORANGE = (255, 155, 0)
IDK = (255, 155, 255)
DGRAY = (10, 10, 10)

# Font setup
font1 = pygame.font.SysFont('MARIO Font v3_2 Solid', 14, False) # For title
font2 = pygame.font.SysFont('MARIO Font v3_2 Solid', 11, False) # For artists and time
font3 = pygame.font.SysFont('MARIO Font v3_2 Solid', 10, False) # Anything else

# Get the directory of the script
drive_letter = 'D:'
script_dir = drive_letter + "\\piton\\music thingymajig\\musicPL"

# Define number of songs
num_songs = len(os.listdir(script_dir))
songs = [os.path.join(script_dir, f"{i}.mp3") for i in range(1, num_songs + 1)]

# Set initial volume and playback settings
volume = 0.2
pygame.mixer.music.set_volume(volume)
start_time = 0
current_duration = 0
loop_enabled = 0
current_song_index = 0
text_x = 5
text_y = 5
script_start = time.time()
seconds = 0
minutes = 0
hours = 0
is_muted = False
current_artist_info = ""


def get_audio_info(file_path):
    try:
        audio = MP3(file_path, ID3=EasyID3)
        title = audio.get('title', [os.path.basename(file_path)])[0]
        artist = audio.get('artist', ["???"])[0]
        subtitle = audio.get('genre', ['??'])[0]
        combined = f"{artist} | {subtitle}" if subtitle else f"{artist}"
        duration = int(audio.info.length)
        return title, combined, duration
    except Exception as e:
        return os.path.basename(file_path), "Unknown Artist", "Unknown"

def play_song(song_index):
    global start_time, current_duration, current_artist_info
    try:
        song_path = songs[song_index]
        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play()
        title, artist_info, duration = get_audio_info(song_path)
        current_duration = duration
        start_time = time.time()
        current_artist_info = artist_info
        return title
    except Exception as e:
        sys.exit(f"Uh oh! Error encountered: {e}")

def play_next_song():
    global current_song_index
    if loop_enabled == 1:
        return play_song(current_song_index)
    else:
        current_song_index = (current_song_index + 1) % len(songs)
        return play_song(current_song_index)

def update_display(title, elapsed, total_duration):
    screen.fill(DGRAY)
    current_date = time.strftime("%a, %d %b %Y | %I:%M:%S %p")
    battery = psutil.sensors_battery()
    battery_percentage = battery.percent
    plugged = battery.power_plugged
    battery_status = "(Plugged In)" if plugged else ""
    is_shift_pressed = False
    
    # Render texts
    song_text = font1.render(title, True, PURPLE)
    artist_text = font2.render(f"{current_artist_info}", True, D_PURPLE)
    duration_text = "?" if title.startswith("USB disconnected") else f"{elapsed // 60}:{elapsed % 60:02d} / {total_duration // 60}:{total_duration % 60:02d} | Song #{current_song_index + 1}/{len(songs)}"
    elapsed_text = font3.render(f"{duration_text} {'[<- Prev | Next ->]' if loop_enabled == 0 else '[Restart ->]'}", True, L_BLUE)
    volume_text = font3.render(f"{int(volume * 100)}% {'(Muted) ' if is_muted else ''}(-|0|+)", True, YELLOW)
    loop_text = font3.render(f"{'[V] (Q)' if loop_enabled == 1 else '[X] (Q)'}", True, RED if loop_enabled == 0 else GREEN)
    time_text = font3.render(f"It's been ~{hours}h {minutes % 60}m {seconds % 60}s." if hours > 0 else f"It's been ~{minutes % 60}m {seconds % 60}s." if minutes > 0 else f"It's been ~{seconds % 60}s.", True, WHITE)
    date_text = font3.render(f"{current_date}", True, ORANGE)
    battery_text = font3.render(f"Battery: {battery_percentage}% {battery_status}", True, ORANGE)
    
    screen.blit(song_text, (text_x, text_y))
    screen.blit(artist_text, (text_x, text_y + 16.5))
    screen.blit(elapsed_text, (text_x, text_y + 30))
    screen.blit(volume_text, (text_x, text_y + 50))
    screen.blit(loop_text, (text_x + 80, text_y + 50))
    screen.blit(time_text, (text_x, text_y + 80))
    screen.blit(date_text, (text_x, text_y + 105))
    screen.blit(battery_text, (text_x, text_y + 125))
    pygame.display.flip()

def adjust_volume(change, is_shift_pressed=False):
    global volume, is_muted
    volume += change * 10 if is_shift_pressed else change
    if volume < 0:
        volume = 0
    elif volume > 1:
        volume = 1
    title, artist_info, duration = get_audio_info(songs[current_song_index])
    elapsed = int(time.time() - start_time)
    pygame.mixer.music.set_volume(volume)
    update_display(title, elapsed, current_duration)

def is_usb_connected():
    return os.path.exists(script_dir)

def event_check():
    global script_start, seconds, minutes, hours, current_title, current_song_index, running, loop_enabled, start_time, is_muted, volume, current_duration, elapsed
    for event in pygame.event.get():
        if event.type == pygame.USEREVENT: 
            current_title = play_next_song()  
        elif event.type == pygame.QUIT:    
            running = False
            pygame.mixer.music.stop()
        elif event.type == pygame.KEYDOWN:
            mods = pygame.key.get_mods()  # Get modifier keys
            is_shift_pressed = mods & pygame.KMOD_SHIFT  # Check if Shift is held

            if event.key == pygame.K_RIGHT:  
                current_title = play_next_song()
            elif event.key == pygame.K_LEFT and loop_enabled != 1:  
                current_song_index = (current_song_index - 1) % len(songs)
                current_title = play_song(current_song_index)
            elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                if volume < 1:
                    adjust_volume(0.01, is_shift_pressed)  # Increase volume
                    is_muted = False
                    update_display(current_title, elapsed, current_duration)
            elif event.key == pygame.K_0:
                pygame.mixer.music.set_volume(0)
                is_muted = True
            elif event.key == pygame.K_MINUS:
                if volume < 0.011:
                    volume = 0
                    pygame.mixer.music.set_volume(volume)
                    is_muted = True
                elif volume > 0:
                    adjust_volume(-0.01, is_shift_pressed)  # Decrease volume
                    is_muted = False
                update_display(current_title, elapsed, current_duration)
            elif event.key == pygame.K_q:      
                loop_enabled = (loop_enabled + 1) % 2  
                elapsed = int(time.time() - start_time)
            elif event.key == pygame.K_0:
                pygame.mixer.music.set_volume(0.0)
                is_muted = True
            update_display(current_title, elapsed, current_duration)

    if pygame.mixer.music.get_busy():
        elapsed = int(time.time() - start_time)
        seconds = int(time.time() - script_start)
        if seconds >= 60:
            script_start = time.time()
            seconds = 0
            minutes += 1
        if minutes >= 60:
            minutes = 0
            hours += 1
        update_display(current_title, elapsed, current_duration)

current_title = play_song(current_song_index)
pygame.mixer.music.set_endevent(pygame.USEREVENT)
running = True

while running:
    usb_connected = is_usb_connected()
    if not usb_connected:
        pygame.mixer.music.stop()
        print("USB was disconnected. Exiting program.")
        running = False
        break
    event_check()
pygame.quit()