from musicpy import *

guitar = (
    C('G', 2, 1)^2 |
    C('Bm', 2, 1)^2 |
    C('C', 2, 1)^2 |
    C('D', 2, 1)^2 |
    C('Em', 2, 1)^2 |
    C('Bm', 2, 1)^2 |
    C('Em', 2, 1/2)^2 |
    C('D', 2, 1/2)^2 |

    C('G', 2, 1)^2 |
    C('Bm', 2, 1)^2 |
    C('C', 2, 1)^2 |
    C('D', 2, 1)^2 |
    C('Em', 2, 1)^2 |
    C('D/F#', 2, 1)^2 |
    C('Am', 2, 1)^2 |
    C('Am', 2, 1)^2 |
    C('C', 2, 1)^2 |
    C('D', 2, 1)^2 |
    C('G', 2, 1)^2
)
play(guitar, bpm=155, instrument=25, wait=True)

