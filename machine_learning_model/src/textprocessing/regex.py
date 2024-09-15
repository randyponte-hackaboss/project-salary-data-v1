import re
from src.textprocessing.preprocess import join_contexts, remove_punctuation, normalize_text


def salary_range(text):
    range_re = re.compile("[0-9]+[k|eur]?\s?[-|up to]\s*?[0-9]+[k|eur]?")
    return range_re.findall(text)

def number_regex(text):
    number_re = re.compile("[0-9]+")
    return number_re.findall(text)

def found_signal_words(contexts:list, signal_words:list):
    signal_word_present_in_context = False
    for signal_word in signal_words:
        if signal_word in join_contexts(contexts):
            signal_word_present_in_context = True
            break

    return signal_word_present_in_context

def get_context_from_numbers_in_text(text, ngrams=3, overlap_limit=0.3, remove_stop_words=False):
    contexts = []
    found_numbers = number_regex(remove_punctuation(normalize_text(text, remove_stop_words=remove_stop_words)))
    tokens_from_original_text = re.sub("\s\s+", " ", " ".join(normalize_text(text, remove_stop_words=remove_stop_words).replace("\n", " ").replace("\t", "").split(" "))).split(" ")
    
    for number in found_numbers:
        for index, token in enumerate(tokens_from_original_text):
            number_in_token = number_regex(remove_punctuation(normalize_text(token, remove_stop_words=remove_stop_words)).strip())
            
            if len(number_in_token)>0 and number_in_token[0] == number:
                lower_boud = index-ngrams if index-ngrams>=0 else 0
                upper_boud = index+ngrams+1 if index+ngrams+1<= len(tokens_from_original_text) else len(tokens_from_original_text)
                new_context = tokens_from_original_text[lower_boud:upper_boud]

                # I need to check all of them for overlaping If I find any overlap over the threshold I need to flag it so I do not add it.
                overlaps_with_any_previous_context=False
                for saved_context in contexts:
                    overlaping_count = len(list(set(saved_context) & set(new_context)))
                    if (overlaping_count/(overlaping_count+len(new_context))) >= overlap_limit:
                        overlaps_with_any_previous_context = True
                        break

                if not overlaps_with_any_previous_context:
                    contexts.append(new_context)

    return found_numbers, contexts
