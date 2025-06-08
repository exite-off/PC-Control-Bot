import ytmusicapi
import yt_dlp
import keyboard as kb
import pyautogui

# Download audio from YouTube music
async def download_audio(yt_url, query = 'result'):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
        'outtmpl': f'{query}.%(ext)s'
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([yt_url])

# configure yt_dlp
base_url = 'https://music.youtube.com/watch?v='
yt = ytmusicapi.YTMusic()

async def change_volume(vector: str) -> None:
    if vector == 'up':
        for i in range(5):
            kb.send("volume up")
    else:
        for i in range(5):
            kb.send("volume down")

def mute_pc_sound():
    kb.send("volume mute")

def take_screenshot(name: str = 'screenshot.png') -> None:
    image = pyautogui.screenshot()
    image.save(name)