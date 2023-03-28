import random
import re

import human

# prefixes
prefixes = ["A mon avis ",
            "Je pense que ",
            "Je dirais que ",
            "Je crois que ",
            "j'ai bien réfléchi et en vrai "]

# prefixes to use when the coming sentence starts with a vowel
prefixes_vowel = ["A mon avis ",
                    "Je pense qu'",
                    "Je dirais qu'",
                    "Je crois qu'",
                    "j'ai bien réfléchi et en vrai "]

# suffixes
suffixes = [" en vrai",
            " je pense",
            " je crois",
            " je dirais",
            " non ?"]

# define the function that will be called when a message contains "quoi"
async def respond_feur(message):
    # simulate thinking
    await human.simulate(message)

    text = message.content

    # clean the text
    text = strip_feur(text)

    # if "pourquoi" is in the message, replace it with " feur"
    if "pourquoi" in text:
        text = text.replace("pourquoi", "pour feur")
    text = text.replace("quoi", "feur")

    # Handle the pronouns (might not work for all cases)
    text = pronouns_feur(text)

    # remove evrything on the right of the first feur
    text = text.split("feur")[0] + "feur"

    # surround the text with a prefix or a suffix and send it
    await message.channel.send(surround_feur(text))

def pronouns_feur(text):
    text = text.replace("tu", "je")
    text = text.replace("m'", "t'")
    return text

def surround_feur(text):
    # choose either a prefix or a suffix
    if random.randint(0, 1) == 0:
        if text[0] in "aeiouy":
            prefix = random.choice(prefixes_vowel)
        else:
            prefix = random.choice(prefixes)
        text = prefix + text
        
    else:
        suffix = random.choice(suffixes)
        text = text + suffix
    return text


# Handles some cases where message would make no sense if
# we just use the above method
# Example:
#   "Mais pourquoi tu fais ça ?" -> "En vrai mais pour feur" (not good)
#   "Mais pourquoi tu fais ça ?" -> "En vrai pour feur" (better)
def strip_feur(text):
    if text.startswith("mais "):
        text = text.replace("mais ", "", 1)
    if text.startswith("et "):
        text = text.replace("et ", "", 1)
    # remove any mention matchin regex "<@*>""
    text = re.sub(r"<@.*>", "", text)

    return text
