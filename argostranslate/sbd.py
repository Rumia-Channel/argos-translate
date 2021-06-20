from difflib import SequenceMatcher

from argostranslate import package, settings
from argostranslate.utils import info, error

DETECT_SENTENCE_BOUNDARIES_TOKEN = "<detect-sentence-boundaries>"
SENTENCE_BOUNDARY_TOKEN = "<sentence-boundary>"


def get_sbd_package():
    packages = package.get_installed_packages()
    for pkg in packages:
        if pkg.type == "sbd":
            return pkg
    return None


def detect_sentence(input_text, sbd_translation, sentence_guess_length=150):
    """Given input text, return the index after the end of the first sentence.

    Args:
        input_text (str): The text to detect the first sentence of.
        sbd_translation (translate.ITranslation): An ITranslation for detecting sentences.
        sentence_guess_length (int): Estimated number of chars > than most sentences.

    Returns:
        int: The index of the character after the end of the sentence.
                -1 if not found.
    """
    # TODO: Cache
    sentence_guess = input_text[:sentence_guess_length]
    info("sentence_guess:", sentence_guess)
    sbd_translated_guess = sbd_translation.translate(
        DETECT_SENTENCE_BOUNDARIES_TOKEN + sentence_guess
    )
    sbd_translated_guess_index = sbd_translated_guess.find(SENTENCE_BOUNDARY_TOKEN)
    if sbd_translated_guess_index != -1:
        sbd_translated_guess = sbd_translated_guess[:sbd_translated_guess_index]
        info("sbd_translated_guess:", sbd_translated_guess)
        best_index = None
        best_ratio = 0.0
        for i in range(len(input_text)):
            candidate_sentence = input_text[:i]
            sm = SequenceMatcher()
            sm.set_seqs(candidate_sentence, sbd_translated_guess)
            ratio = sm.ratio()
            if best_index is None or ratio > best_ratio:
                best_index = i
                best_ratio = ratio
        return best_index
    else:
        return -1
