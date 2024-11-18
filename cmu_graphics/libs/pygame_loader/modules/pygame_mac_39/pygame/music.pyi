from typing import Optional

def load(filename: str) -> None: ...
def unload() -> None: ...
def play(
    loops: Optional[int] = 0, start: Optional[float] = 0.0, fade_ms: Optional[int] = 0
): ...
def rewind() -> None: ...
def stop() -> None: ...
def pause() -> None: ...
def unpause() -> None: ...
def fadeout(time: int) -> None: ...
def set_volume(volume: float) -> None: ...
def get_volume() -> float: ...
def get_busy() -> bool: ...
def set_pos(pos: float) -> None: ...
def get_pos() -> int: ...
def queue(filename: str) -> None: ...
def set_endevent(event_type: int) -> None: ...
def get_endevent() -> int: ...
