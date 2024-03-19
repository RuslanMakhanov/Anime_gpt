from misc import *
from aiogram.types import Voice
import io
from pydub import AudioSegment
import openai
import os

client = openai.OpenAI()


async def save_voice_as_mp3(voice: Voice) -> str:
    """Скачивает голосовое сообщение и сохраняет в формате mp3."""
    voice_file_info = await bot.get_file(voice.file_id)
    voice_ogg = io.BytesIO()
    await bot.download_file(voice_file_info.file_path, voice_ogg)

    voice_mp3_path = f"voice_files/voice-{voice.file_unique_id}.mp3"
    AudioSegment.from_file(voice_ogg, format="ogg").export(
        voice_mp3_path, format="mp3"
    )
    return voice_mp3_path


async def audio_to_text(file_path: str) -> str:
    """Принимает путь к аудио файлу, возвращает текст файла."""
    with open(file_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )

    delete_file(file_path)

    return transcription.text


def delete_file(file_path):
    try:
        os.remove(file_path)
        print(f"Файл {file_path} успешно удален.")
    except FileNotFoundError:
        print(f"Файл {file_path} не найден.")
    except PermissionError:
        print(f"Недостаточно прав для удаления файла {file_path}.")
    except Exception as e:
        print(f"Произошла ошибка при удалении файла {file_path}: {e}")
