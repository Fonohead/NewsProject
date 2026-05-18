from django import template

register = template.Library()

# Фильтр слов
forbidden_words = ['бармаглот', 'бармаглота', 'шорьки', 'концерт']

@register.filter()
def censor(text):
    if not isinstance(text, str):
        raise TypeError("Требуется строка, получено: " + str(type(text).__name__))

    words = text.split()
    result = []

    for word in words:
        clean_word = ""
        punctuation = ""
        for char in word:
            if char.isalpha():
                clean_word += char
            else:
                punctuation += char

        if not clean_word:
            result.append(word)
            continue

        if clean_word.lower() in forbidden_words and clean_word[1:].islower():
            censored = clean_word[0] + '*' * (len(clean_word) - 1)
            result.append(censored + punctuation)
        else:
            result.append(word)

    return " ".join(result)




