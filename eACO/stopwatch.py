import time


class Stopwatch:
    digits: int

    def __init__(self, digits: int = 2):
        self.digits = digits

        self._start = time.perf_counter()
        self._end = None

    @property
    def duration(self) -> float:
        return (
            self._end - self._start if self._end else time.perf_counter() - self._start
        )

    @property
    def running(self) -> bool:
        return not self._end

    def restart(self) -> None:
        self._start = time.perf_counter()
        self._end = None

    def reset(self) -> None:
        self._start = time.perf_counter()
        self._end = self._start

    def start(self) -> None:
        if not self.running:
            self._start = time.perf_counter() - self.duration
            self._end = None

    def stop(self) -> None:
        if self.running:
            self._end = time.perf_counter()

    def __str__(self) -> str:
        time = self.duration

        if time >= 1:
            return "{:.{}f}s".format(time, self.digits)

        if time >= 0.01:
            return "{:.{}f}ms".format(time * 1000, self.digits)

        return "{:.{}f}μs".format(time * 1000 * 1000, self.digits)
