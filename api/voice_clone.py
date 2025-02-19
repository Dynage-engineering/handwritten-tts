# load all the functions
# from voice_cloning.generation import *
from styletts2 import tts


def voice_clone(sound_path, speech_text, output_file="output.wav"):
    my_tts = tts.StyleTTS2()
    out = my_tts.inference(
        speech_text,
        target_voice_path=sound_path,
        output_wav_file=output_file,
    )

    return out

#     generated_wav = speech_generator(
#         voice_type="western",  # supports "indian" & "western"
#         sound_path=sound_path,
#         speech_text=speech_text,
#     )

#     return generated_wav


## Play and save the sound with noise-reduction capabilities

# play the generated sound
# play_sound(generated_wav)

# save the file
# save_sound(generated_wav, filename="voice output", noise_reduction=True)
