# Kazakh Finite-State Transducer

Two *sample* finite-state transducers for Kazakh. These use the proposed modified latin alphabet for Kazakh (2021), but could easily be modified if there were to be any more changes or if a Cyrillic version was to be added.

The first FST is a grapheme-to-phoneme transducer. This translates a given Kazakh word into IPA. For example, if **jaqsı** were used as an input, then **ʒaqsɯ** would be returned.


The second FST is a non-comprehensive generative morphology that handles vowel and consonant harmonies. A word is inputted to the FST with given grammatical tags and the inflected form of the word is returned. For example, if **bala+PLR** were used as an input, 
then **balalar** would be returned.
