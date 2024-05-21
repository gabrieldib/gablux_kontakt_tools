# You need ffmpeg installed
# get it at https://ffmpeg.org/download.html

#  - go through a folder structure
#  - if a wav file is found, normalize it and save a new version
#  - delete the original wav
#  - convert to ogg

#  by Gablux 2024.02.18

import os
import soundfile as sf
import pyloudnorm as pyln
from platform import system
import logging


def normalize_wav_file(wav_file, output_path):
    # Load audio
    data, rate = sf.read(wav_file)

    # Measure the loudness first
    meter = pyln.Meter(rate)  # Create BS.1770 meter
    loudness_before = meter.integrated_loudness(data)
    print(f"Source file loudness: {loudness_before:.2f} LUFS")

    # Loudness normalize the peak normalized audio to -19 dB LUFS
    target_loudness = -19.0
    loudness_normalized_audio = pyln.normalize.loudness(data, loudness_before, target_loudness)

    # Measure the loudness after normalization
    loudness_after = meter.integrated_loudness(loudness_normalized_audio)
    print(f"    Normalized file loudness: {loudness_after:.2f} LUFS")

    print("    writing normalized file into ", output_path)
    # Save the loudness normalized audio
    sf.write(output_path, loudness_normalized_audio, rate)


def main(folder_to_process, keep_original=True, keep_normalized_wavs=True):
    original_wavs = []
    normalized_wavs = []
    files_to_convert = []

    for root, dirs, files in os.walk(folder_to_process):
        for file in files:
            if ".wav" in file:
                normalize_wav_file(root + "\\" + file, root + "\\" + file.replace(".wav", "_norm.wav"))
                original_wavs.append(root + "\\" + file)
                normalized_wavs.append(root + "\\" + file.replace(".wav", "_norm.wav"))
                files_to_convert.append(root + "\\" + file.replace(".wav", "_norm.wav"))

    for file in files_to_convert:
        system_call = "ffmpeg" + \
                      ' -i "' + file + \
                      '" -ar ' + '44100' + \
                      ' -codec:a libvorbis ' + \
                      ' -aq ' + '5' + \
                      ' "' + file.replace("_norm.wav", ".ogg") + '"'

        if system() == 'Darwin' or system() == 'Windows':
            os.system(system_call)
        else:
            logging.error("Are you on Linux?")

    if not keep_original:
        for file in original_wavs:
            os.remove(file)

    if not keep_normalized_wavs:
        for file in normalized_wavs:
            os.remove(file)


if __name__ == "__main__":

    TARGET_FOLDER = "input your folder path here"

    KEEP_ORIGINAL_WAVS   = False
    KEEP_NORMALIZED_WAVs = False

    main(TARGET_FOLDER, KEEP_ORIGINAL_WAVS, KEEP_NORMALIZED_WAVs)
