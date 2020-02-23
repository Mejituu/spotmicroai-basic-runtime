#!/usr/bin/env python3


class SpotMicro:
    _spanish_bark = "guau-guau"
    _japanese_bark = "wan-wan"
    _german_bark = "wuff-wuff"
    _english_bark = "woof-woof"

    def bark_in_spanish(self):
        return self._spanish_bark

    def bark_in_japanese(self):
        return self._japanese_bark

    def bark_in_german(self):
        return self._german_bark

    def bark_in_english(self):
        return self._english_bark


if __name__ == '__main__':
    spotmicro = SpotMicro()

    print('Ladrar: ' + spotmicro.bark_in_spanish())
    print('樹皮: ' + spotmicro.bark_in_japanese())
    print('Bellen: ' + spotmicro.bark_in_german())
    print('To bark: ' + spotmicro.bark_in_english())
