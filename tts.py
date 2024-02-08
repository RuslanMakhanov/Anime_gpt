from pathlib import Path
import openai


def tts_gpt(text):
    speech_file_path = Path(__file__).parent / "speech.mp3"
    response = openai.audio.speech.create(
      model="tts-1",
      voice="nova",
      input=text
    )
    response.stream_to_file(speech_file_path)
    return speech_file_path

tts_gpt("Конничива, PilotAski! Привет, Серега! Желаю тебе прекрасного дня и отличного настроения на работе! Пусть все задачи выполняются легко и без проблем, а коллеги окружают тебя поддержкой и улыбками. Ты молодец, и я верю, что у тебя все получится! Гамбарэте, Серега! 💪😊")