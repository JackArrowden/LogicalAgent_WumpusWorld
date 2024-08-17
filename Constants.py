from dataclasses import dataclass

@dataclass(frozen = True)
class Constants:
    SAFE: int = 0
    WUMPUS: int = 100
    PIT: int = 200
    GAS: int = 300
    HEAL: int = 400
    GOLD: int = 500
    STENCH: int = 600
    BREEZE: int = 700
    WHIFF: int = 800
    GLOW: int = 900     
    RELIABLE: int = 1000 
    DELTA: list = ((1, 0), (0, 1), (-1, 0), (0, -1))

    CERTAINLY_GAS: tuple = (1, 0)
    CERTAINLY_HEAL: tuple = (-0.4, 0)
    ABLE_GAS: tuple = (0.5, 0)
    ABLE_HEAL: tuple = (-0.1, 0)
    NORMAL: tuple = (0, 0)
    VERIFY: tuple = (0, -4)

