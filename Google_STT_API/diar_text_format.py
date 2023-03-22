from config import Config


def formatter(text: list) -> str:
    text = [line.strip().split(', ') for line in text]

    spk_idxs = [str(i) for i in range(1, Config.diarization_config['max_speaker_count'] + 1)]
    spk_letters = [chr(ord("A") + i) for i in range(len(spk_idxs))]
    spk_idx_letter_map = dict(zip(spk_idxs, spk_letters))

    reformated_text = f'Speaker: {spk_idx_letter_map[text[0][1]]} \n'
    reformated_text += f'{text[0][0]} '
    for i in range(1, len(text)):
        if text[i][1] != text[i - 1][1]:
            reformated_text += f'\n\nSpeaker: {spk_idx_letter_map[text[i][1]]} \n'
        reformated_text += f'{text[i][0]} '
    return reformated_text
