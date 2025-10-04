# FileName: nighthawk.dll
# Sha256: 9a57919cc5c194e28acd62719487c563a8f0ef1205b65adbe535386e34e418b8

# @category Strings
# Use this script before Ghidra 11.4.1

# Author: Gabriel Toledo - 0xCH4S3
# Reference: https://github.com/0xCH4S3

from ghidra.program.model.data import StringDataInstance, TranslationSettingsDefinition
from ghidra.program.util import DefinedDataIterator
from ghidra.app.script import GhidraScript
from util import CollectionUtils

def translate_string(encoded_str):
    decoded_str = []
    cipher_alph = "cezH!g27E>?pnkI5ym6QG<wXr;ORhZDKY._:^u{UWt,j[9vasb*1/CBxF=q0d fo4)N]M}3ST(J$8PiA+LVl"
    plaintext_alph = " wPXJ}?IeL7y!SaKxkr,sOOTjl4_hf:C{W.>c$!Hg^u=GYD+Bni<v62z8d3bpRJ(q9MZ/*oNU][AQmV5tE&;-E"

    for character in encoded_str:
        if character in cipher_alph:
            char_loc = cipher_alph.find(character)
            translated_char = plaintext_alph[char_loc]
            decoded_str.append(translated_char)
        else:
            decoded_str.append(character)

    return ''.join(decoded_str)

count = 0
listing = currentProgram.getListing()
num_defined_data = listing.getNumDefinedData()

monitor.initialize(num_defined_data)
monitor.setMessage("Translating strings")

for data in CollectionUtils.asIterable(DefinedDataIterator.definedStrings(currentProgram, currentSelection)):
    if monitor.isCancelled():
        break
    str_data_instance = StringDataInstance.getStringDataInstance(data)
    s = str_data_instance.getStringValue()
    
    if s is not None:
        TranslationSettingsDefinition.TRANSLATION.setTranslatedValue(data, translate_string(s))
        TranslationSettingsDefinition.TRANSLATION.setShowTranslated(data, True)
        count += 1
        monitor.incrementProgress(1)

println("Translated " + str(count) + " strings.")


