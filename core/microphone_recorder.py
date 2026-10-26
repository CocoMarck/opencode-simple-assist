import sounddevice

class MicrophoneRecorder:
    def __init__( self, sample_rate: int, blocksize: int = 8000):
        self.sample_rate = sample_rate
        self.blocksize = blocksize
        self._stream = None
        self._buffer = bytearray()

        self._external_callback = None

    @property
    def buffer(self):
        return self._buffer

    def get_duration_in_seconds(self, duration_in_seconds: float):
        return int(duration_in_seconds * self.sample_rate)

    def _callback(self, indata, frames, time, status):
        if status:
            print(status)
        data = indata.tobytes()
        self._buffer.extend(data)
        if self._external_callback is not None:
            try:
                self._external_callback(indata, frames, time, status)
            except Exception as e:
                print(e)

    def start(self):
        self._buffer.clear()
        self._stream = sounddevice.InputStream(
            samplerate=self.sample_rate,
            channels=1,
            dtype='int16',
            device=None,
            blocksize=self.blocksize,
            callback=self._callback
        )
        self._stream.start()
        print("Recording without limits with sounddevice...")

    def stop(self) -> bytearray:
        '''
        # Retorna el `bytearray` del espacio en memoria del audio del micrófono.
        '''
        if self._stream is not None:
            self._external_callback = None
            self._stream.stop()
            self._stream.close()
            self._stream = None
            print("Stopping recording with no limits in sounddevice...")
        return self._buffer

    def sync_with_duration(self, duration_in_seconds: float) -> bytes:
        '''
        Grabación sincronizada con duración especificada.
        '''
        audio = sounddevice.rec(
            self.get_duration_in_seconds(duration_in_seconds),
            samplerate=self.sample_rate,
            channels=1,
            dtype="int16",
            device=None
        )
        sounddevice.wait()
        return audio.tobytes()
    
    def start_with_callback(self, external_callback=None):
        '''
        External callback, tiene que recibir bytes
        '''
        print("Recording with external callback with sounddevice...")
        self._buffer.clear()
        self._external_callback = external_callback
        self._stream = sounddevice.InputStream(
            samplerate=self.sample_rate,
            channels=1,
            dtype="int16",
            device=None,
            blocksize=self.blocksize,
            callback=self._callback
        )
        self._stream.start()