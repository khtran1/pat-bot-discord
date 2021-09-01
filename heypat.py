import numpy as np

import driveAuth as auth


def updateBrain(text):
    filesList = auth.drive.ListFile({'q': "trashed=false"}).GetList()
    for files in filesList:
        if files['title'] == 'patbrain.txt':
            files.GetContentFile("patbrain.txt")
            update = files.GetContentString() + " ||| " + text
            files.SetContentString(update)
            files.Upload()
            break


def deleteBrain():
    filesList = auth.drive.ListFile({'q': "trashed=false"}).GetList()
    for files in filesList:
        if files['title'] == 'patbrain.txt':
            files.GetContentFile("patbrain.txt")
            update = " "
            files.SetContentString(update)
            files.Upload()
            break


def readBrain():
    filesList = auth.drive.ListFile({'q': "trashed=false"}).GetList()
    for files in filesList:
        if files['title'] == 'patbrain.txt':
            brainfile = files.GetContentString("patbrain.txt")
            return brainfile


rawText = readBrain()


# For markov chain
def build_transition_matrix(rawText):
    rawText = rawText.split(' ')
    transitions = {}
    for k in range(0, len(rawText)):
        word = rawText[k]
        if k != len(rawText) - 1:  # Deal with last word
            next_word = rawText[k+1]
        else:
            next_word = rawText[0]  # To loop back to the beginning

        if word not in transitions:
            transitions[word] = []

        transitions[word].append(next_word)
    return transitions


def sample_sentence(rawText, sentence_length, burn_in=1000):
    rawText = rawText
    sentence = []

    transitions = build_transition_matrix(rawText)

    # Make a sentence that is 50 words long
    # We sample the sentence after running through the chain 1000 times to hope
    # to near a stationary distribution.
    current_word = np.random.choice(rawText.split(' '), size=1)[0]
    for k in range(0, burn_in + sentence_length):
        # Sample from the lists with an equal chance for each entry
        # This chooses a word with the correct probability distribution
        # in the transition matrix.
        current_word = np.random.choice(transitions[current_word], size=1)[0]

        if k >= burn_in:
            sentence.append(current_word)

        if "|||" in sentence:
            sentence = sentence[:-1]
            print('found |||')
            break

        if any(('.' or '!' or '?') in s for s in sentence):
            print('found end of sentence')
            break

    if len(sentence) == 0:
        print('legngth 0')
        sample_sentence(rawText, np.random.randint(100, 150), 1000)

    return ' '.join(sentence)


def updateTransitions():
    global rawText
    rawText = readBrain()
