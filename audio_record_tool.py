import pyaudio
import wave


class AudioRecord:
    def __init__(self, WAVE_OUTPUT_FILENAME, RECORD_DURATIONS):
        # self.path = WAVE_OUTPUT_FILENAME
        # self.durations = RECORD_DURATIONS
        CHUNK = 8192
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100

        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        input_device_index=1,
                        frames_per_buffer=CHUNK)

        print("* recording")

        frames = []
        for i in range(0, int(RATE / CHUNK * RECORD_DURATIONS) + 1):
            data = stream.read(CHUNK)
            frames.append(data)
        print("* done")

        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()


if __name__ == '__main__':
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("-p", required=True,
                    help="wav file path")
    ap.add_argument("-t", required=True,
                    help="seconds of record duration")

    args = vars(ap.parse_args())
    # # path, result_path, lang, auth
    AudioRecord(WAVE_OUTPUT_FILENAME=args['p'], RECORD_DURATIONS=int(args['t']))
    # AudioRecord(WAVE_OUTPUT_FILENAME='E:/output3.wav', RECORD_DURATIONS=10)
