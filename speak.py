# #!/usr/bin/env python

# from  AppKit import NSSpeechSynthesizer
# import time
# import sys


# if len(sys.argv) < 2:
#    text = raw_input('> ')
# else:
#    text = sys.argv[1]

# nssp = NSSpeechSynthesizer

# ve = nssp.alloc().init()

# voices = ["com.apple.speech.synthesis.voice.Alex",
# "com.apple.speech.synthesis.voice.Vicki",
# "com.apple.speech.synthesis.voice.Victoria",
# "com.apple.speech.synthesis.voice.Zarvox" ]

# # for voice in nssp.availableVoices():
# for voice in voices:
#    ve.setVoice_(voice)
#    print voice
#    ve.startSpeakingString_(text)
#    while ve.isSpeaking():
#       time.sleep(1)


# from Cocoa import NSSpeechSynthesizer

# sp = NSSpeachSynthesizer.alloc().initWithVoice_(None) # use default voice
# sp.startSpeakingString_("hello world")


import pyttsx
engine = pyttsx.init()
engine.say('Sally sells seashells by the seashore.')
engine.say('The quick brown fox jumped over the lazy dog.')
engine.runAndWait()