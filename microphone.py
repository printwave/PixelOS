import pyaudio
import wave

def record_audio(filename, duration=5, channels=2, sample_rate=44100, chunk=1024):
    """
    Record audio from the microphone and save it to a WAV file.

    Args:
    - filename (str): Name of the output WAV file.
    - duration (int): Recording duration in seconds (default: 5).
    - channels (int): Number of audio channels (default: 2).
    - sample_rate (int): Sampling frequency in Hz (default: 44100).
    - chunk (int): Number of frames per buffer (default: 1024).
    """
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16,
                        channels=channels,
                        rate=sample_rate,
                        input=True,
                        frames_per_buffer=chunk)
    
    frames = []
    print("Recording...")
    for _ in range(int(sample_rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)
    print("Recording complete.")

    stream.stop_stream()
    stream.close()
    audio.terminate()

    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(sample_rate)
        wf.writeframes(b''.join(frames))
    print(f"Audio saved as {filename}")

if __name__ == "__main__":
    record_audio("recorded_audio.wav")
