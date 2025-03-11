from os.path import abspath
from pathlib import Path

import pydantic
from pydantic import AnyHttpUrl, BaseModel, constr, Field


class MusicInitSchema(BaseModel):
    type: constr(regex='^music$') = Field(default='music', const=True)
    music_id: str
    file_path: Path  # This will ensure the path is valid
    url: AnyHttpUrl

    class Config:
        # Enforce immutability for the `type` field, making sure it always stays 'music'
        allow_mutation = False

class SoundInitSchema(BaseModel):
    type: constr(regex='^sound') = Field(default='sound', const=True)
    sound_id: str
    file_path: Path  # This will ensure the path is valid
    url: AnyHttpUrl

    class Config:
        # Enforce immutability for the `type` field, making sure it always stays 'music'
        allow_mutation = False

class SoundProgressSchema(pydantic.BaseModel):
    type: constr(regex='^sound') = Field(default='sound', const=True)
    sound_id: str
    class Config:
        # Enforce immutability for the `type` field, making sure it always stays 'music'
        allow_mutation = False


class MusicProgressSchema(pydantic.BaseModel):
    type: constr(regex='^music$') = Field(default='music', const=True)  # Default and required
    music_id: str
    class Config:
        # Enforce immutability for the `type` field, making sure it always stays 'music'
        allow_mutation = False

def create_music_init_data(music_id: str, file_path: str, github_raw_url: str):
    # assert file_path is valid
    return {
        "type": "music",
        "music_id": music_id,
        "file_path": file_path,
        "url": github_raw_url
    }


def create_sound_init_data(sound_id: str, file_path: str, github_raw_url: str):
    # assert file_path is valid
    return {
        "type": "sound",
        "sound_id": sound_id,
        "file_path": file_path,
        "url": github_raw_url
    }
