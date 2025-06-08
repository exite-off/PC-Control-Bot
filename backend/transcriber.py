import whisper
import torch

device = 'cuda' if torch.cuda.is_available() else 'cpu'

def extract_text(audio_path: str = 'E:\\projects\\PythonAI\\totext.ogg', model: str = 'turbo') -> str:
    model = whisper.load_model(model).to(device)
    result = model.transcribe(audio_path)

    return str(result['text'])