# load all the functions
# from voice_cloning.generation import *
from styletts2 import tts
from resemble import Resemble
import os
import uuid
from faker import Faker

fake = Faker()

Resemble.api_key(os.getenv("RESEMBLE_API_KEY"))
CONSENT = "I am aware that recordings of my voice will be used by Resemble AI to train and create a synthetic version of my voice by Resemble AI."


def voice_clone(sound_path, speech_text, output_file="output.wav"):
    my_tts = tts.StyleTTS2()
    out = my_tts.inference(
        speech_text,
        target_voice_path=sound_path,
        output_wav_file=output_file,
    )

    return out


def voice_clone_with_resemble(sample_audio, body):

    # Resemble Voice creation step

    # Create a voice using the "Create a voice" endpoint and omit the dataset_url attribute.
    name = fake.name() + "Voice"

    response = Resemble.v2.voices.create(name, consent=CONSENT, callback_uri="http://example.com/cb")
    # voice = response["item"]
    # Use the instructions on the "Create a recording" page to upload recordings to your voice.
    voice_uuid = uuid.uuid4()
    name = fake.name() + "recording"
    text = fake.sentence()
    is_active = True
    emotion = "neutral"

    with open(sample_audio, "rb") as file:
        response = Resemble.v2.recordings.create(
            voice_uuid, file, name, text, is_active, emotion
        )
        # recording = response["item"]
    # Upon uploading at least 3 recordings, follow the Build a voice documentation to start training.

    response = Resemble.v2.voices.build(voice_uuid)

    # get project ID
    project_uuid = Resemble.v2.projects.all(1, 10)["items"][0]["uuid"]

    # create a voice
    # use the newly created voice to product the output clip

    response = Resemble.v2.clips.create_sync(
        project_uuid,
        body,
        voice_uuid="",
        title=None,
        sample_rate=None,
        output_format=None,
        precision=None,
        include_timestamps=None,
        is_archived=None,
        raw=None,
    )

    print(response["audio_src"])

    return response
