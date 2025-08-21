import nltk
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize

# Download necessary data
nltk.download('wordnet')
nltk.download('punkt')

def get_synonyms(word):
    synonyms = []
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.append(lemma.name())
    return set(synonyms)

def refactor_text(text):
    words = word_tokenize(text)
    refactored_words = []
    for word in words:
        synonyms = get_synonyms(word)
        if synonyms:
            # Choose the first synonym that is not the same as the original word
            synonym = next((syn for syn in synonyms if syn.lower() != word.lower()), word)
            refactored_words.append(synonym)
        else:
            refactored_words.append(word)
    return ' '.join(refactored_words)

if __name__ == "__main__":
    text = "The quick brown fox jumps over the lazy dog."
    refactored_text = refactor_text(text)
    print("Original text:", text)
    print("Refactored text:", refactored_text)
