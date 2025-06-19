from aiogram.types import (Message, FSInputFile, InlineQuery,
                           InlineQueryResultArticle, InputTextMessageContent,
                           CallbackQuery)
from aiogram import F, Router
from backend.keyboards import main_keyboard, media_keyboard, on_music_keyboard
import os
import hashlib
import functions
from pydub import AudioSegment
import win32api
import pyautogui
from win32con import *
import backend.transcriber as tr
from config import whitelist

router = Router()

# voice converter function
async def voice_send(message: Message) -> None:
    # get info about file
    audio = message.audio
    duration: int = audio.duration
    file_id: str = audio.file_id
    # download file and write to disk
    file_info = await message.bot.get_file(file_id)
    file_path: str | None = file_info.file_path
    downloaded_file = await message.bot.download_file(file_path)
    with open(f'{file_id}.mp3', 'wb') as f:
        f.write(downloaded_file.getvalue())
        f.close()
    # convert file to .ogg, send it as voice message
    sound = AudioSegment.from_mp3(f'{file_id}.mp3')
    sound.export('result.ogg', format='ogg', codec="libopus")
    voice = FSInputFile('result.ogg')
    await message.answer_voice(voice=voice, duration=duration)
    # remove temp files
    os.remove('result.ogg')
    os.remove(f'{file_id}.mp3')

# Function for downloading audio from message
async def download_audiofile(message: Message,
                             audioname: str = None, is_voice: bool = False) -> None:
    if is_voice:
        audio = message.voice
        file_id: str = audio.file_id
        audio_name: str = audioname
    else:
        audio = message.audio
        file_id: str = audio.file_id
        audio_name: str | None = audio.file_name
    if not audio_name:
        audio_name = f'{hashlib.md5(file_id.encode()).hexdigest()}.mp3'
    file_info = await message.bot.get_file(file_id)
    file_path: str | None = file_info.file_path
    downloads_path = os.path.join(os.environ['USERPROFILE'], 'Downloads', audio_name)
    downloaded_file = await message.bot.download_file(file_path)
    with open(downloads_path, 'wb') as f:
        f.write(downloaded_file.getvalue())

# Handler for command /start
@router.message((F.text == '/start') & F.from_user.id.in_(whitelist))
async def start(message: Message) -> None:
    await message.answer('Glad to see you here <3', reply_markup=main_keyboard)

# Handler for command /music
@router.message(F.text.contains('/music') & F.text.startswith('/')
                & F.from_user.id.in_(whitelist))
async def download_music(message: Message) -> None:
    if len(message.text) > 7:
        query: str = message.text[7:]
        await message.answer(f'Searching for {query}')
        search_res: list[dict] = functions.yt.search(query=query, filter='videos',
                                                     limit=1)
        mus_id: str = search_res[0]['videoId']
        url: str = functions.base_url + mus_id
        await functions.download_audio(url, query)
        await message.reply(f'Downloaded, sending!\n{url}')
        try:
            await message.answer_audio(audio=FSInputFile(f'{query}.mp3'))
        except Exception as e:
            await message.answer(f'Error: {e}')
        os.remove(f'{query}.mp3')
    else:
        await message.answer('No query provided')

# Handler for voice to text converter
@router.message(F.content_type.in_({'voice'}))
async def voice_to_text(message: Message) -> None:
    await message.answer('Downloading voice message...')
    try:
        await download_audiofile(message, audioname='voice.ogg', is_voice=True)
    except Exception as e:
        await message.answer(f'Error downloading voice message: {e}')
        return
    await message.answer('Extracting text...')
    try:
        downloads_path: str = os.path.join(os.environ['USERPROFILE'],
                                           'Downloads', 'voice.ogg')
        res: str = tr.extract_text(downloads_path)
        os.remove(downloads_path)
        await message.answer(res)
    except Exception as e:
        await message.answer(f'Error while extracting text: {e}')

# Handler for command /help
@router.message((F.text == '/help') & F.from_user.id.in_(whitelist))
async def help_command(message: Message) -> None:
    await message.answer('There is no help in this world!')

# Handler for Screenshot button
@router.message((F.text == '📷Screenshot') & F.from_user.id.in_(whitelist))
async def screenshot_command(message: Message) -> None:
    functions.take_screenshot()
    photo = FSInputFile('screenshot.png')
    await message.answer_photo(photo=photo)
    os.remove('screenshot.png')

# Handler for Show Desktop button
@router.message((F.text == '🖥️Show Desktop') & F.from_user.id.in_(whitelist))
async def show_desktop_command(message: Message) -> None:
    pyautogui.hotkey('win', 'd')
    await message.answer('Switched to desktop')

# Handler for Medio control button
@router.message((F.text == '⏯Media control') & F.from_user.id.in_(whitelist))
async def media_kb_send(message: Message) -> None:
    await message.answer('Media controller', reply_markup=media_keyboard)

# Handler for Main menu button
@router.message((F.text == '🏠Main Menu') & F.from_user.id.in_(whitelist))
async def main_menu_send(message: Message) -> None:
    await message.answer('Main menu', reply_markup=main_keyboard)

# Handler for Volume Up button
@router.message((F.text == '🔊Volume Up') & F.from_user.id.in_(whitelist))
async def volume_up_command(message: Message) -> None:
    await functions.change_volume('up')
    await message.answer('Volume up')

# Handler for Volume Down button
@router.message((F.text == '🔈Volume Down') & F.from_user.id.in_(whitelist))
async def volume_down_command(message: Message) -> None:
    await functions.change_volume('down')
    await message.answer('Volume down')

# Handler for Mute button
@router.message((F.text == '🔇Mute') & F.from_user.id.in_(whitelist))
async def mute_command(message: Message) -> None:
    win32api.keybd_event(VK_VOLUME_MUTE, 0xAD, KEYEVENTF_EXTENDEDKEY, 0)
    await message.answer('Mute')

# Handler for previous media button
@router.message((F.text == '⏮️Previous') & F.from_user.id.in_(whitelist))
async def previous_media_command(message: Message) -> None:
    win32api.keybd_event(VK_MEDIA_PREV_TRACK, 0xB1, KEYEVENTF_EXTENDEDKEY, 0)
    await message.answer('Previous media is starting!')

# Handler for next media button
@router.message((F.text == '⏭Next') & F.from_user.id.in_(whitelist))
async def next_media_command(message: Message) -> None:
    win32api.keybd_event(VK_MEDIA_NEXT_TRACK, 0xB3, KEYEVENTF_EXTENDEDKEY, 0)
    await message.answer('Next media is starting!')

# Handler for play/stop media button
@router.message((F.text == '⏯Play/Stop') & F.from_user.id.in_(whitelist))
async def play_stop_media_command(message: Message) -> None:
    win32api.keybd_event(VK_MEDIA_PLAY_PAUSE, 0xB0, KEYEVENTF_EXTENDEDKEY, 0)
    await message.answer('Media is playing/stopping!')


# Handler for audio
@router.message(F.audio & F.from_user.id.in_(whitelist))
async def convert_to_voice(message: Message) -> None:
    await message.reply('What do you want to do with audio?',
                        reply_markup=on_music_keyboard)

# Handler for inline convert button
@router.callback_query((F.data == 'convert') & F.from_user.id.in_(whitelist))
async def convert_to_voice_callback(callback_query: CallbackQuery) -> None:
    await voice_send(callback_query.message.reply_to_message)

# Handler for inline download button
@router.callback_query((F.data == 'download') & F.from_user.id.in_(whitelist))
async def download_music_callback(callback_query: CallbackQuery) -> None:
    await download_audiofile(callback_query.message.reply_to_message)
    await callback_query.message.edit_text('Done!')

@router.message(F.text.contains('music.youtube.com') & F.from_user.id.in_(whitelist))
async def download_music_from_link(message: Message) -> None:
    url: str = message.text
    await functions.download_audio(url)
    await message.answer_audio(audio=FSInputFile('result.mp3'))
    os.remove('result.mp3')