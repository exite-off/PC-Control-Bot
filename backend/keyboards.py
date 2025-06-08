from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                     InlineKeyboardMarkup, InlineKeyboardButton)

main_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='🔈Volume Down'), KeyboardButton(text='🔇Mute'), KeyboardButton(text='🔊Volume Up')],
    [KeyboardButton(text='⏯Media control')],
    [KeyboardButton(text='📷Screenshot'), KeyboardButton(text='🖥️Show Desktop')],
],
resize_keyboard=True,
input_field_placeholder='Main menu')

media_keyboard = ReplyKeyboardMarkup(keyboard = [
    [KeyboardButton(text='⏮️Previous'), KeyboardButton(text='⏯Play/Stop'), KeyboardButton(text='⏭Next')],
    [KeyboardButton(text='🏠Main Menu')],
],
resize_keyboard=True,
input_field_placeholder='Media menu')

on_music_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text = 'Download', callback_data = 'download'),
                     InlineKeyboardButton(text = 'Convert', callback_data = 'convert')]
                    ])