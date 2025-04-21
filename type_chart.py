type_chart = {
    "NORMAL": {
        "FIGHTING": 2.0, "GHOST": 0.0, "ROCK": 0.5, "STEEL": 0.5, "NORMAL": 1.0,
        "FIRE": 1.0, "WATER": 1.0, "ELECTRIC": 1.0, "GRASS": 1.0, "ICE": 1.0,
        "POISON": 1.0, "GROUND": 1.0, "FLYING": 1.0, "PSYCHIC": 1.0, "BUG": 1.0,
        "DRAGON": 1.0, "DARK": 1.0, "FAIRY": 1.0
    },
    "FIRE": {
        "WATER": 2.0, "ROCK": 2.0, "FIRE": 0.5, "GRASS": 0.5, "ICE": 0.5,
        "BUG": 0.5, "STEEL": 0.5, "DRAGON": 0.5, "NORMAL": 1.0, "FIGHTING": 1.0,
        "POISON": 1.0, "GROUND": 2.0, "FLYING": 1.0, "PSYCHIC": 1.0, "ELECTRIC": 1.0,
        "DARK": 1.0, "FAIRY": 0.5, "GHOST": 1.0
    },
    "WATER": {
        "ELECTRIC": 2.0, "GRASS": 2.0, "WATER": 0.5, "FIRE": 0.5, "ICE": 0.5,
        "STEEL": 0.5, "NORMAL": 1.0, "FIGHTING": 1.0, "POISON": 1.0, "GROUND": 1.0,
        "FLYING": 1.0, "PSYCHIC": 1.0, "BUG": 1.0, "ROCK": 1.0, "DRAGON": 1.0,
        "DARK": 1.0, "FAIRY": 1.0, "GHOST": 1.0
    },
    "ELECTRIC": {
        "GROUND": 2.0, "ELECTRIC": 0.5, "FLYING": 0.5, "STEEL": 0.5, "NORMAL": 1.0,
        "FIRE": 1.0, "WATER": 1.0, "GRASS": 1.0, "ICE": 1.0, "FIGHTING": 1.0,
        "POISON": 1.0, "PSYCHIC": 1.0, "BUG": 1.0, "ROCK": 1.0, "DRAGON": 1.0,
        "DARK": 1.0, "FAIRY": 1.0, "GHOST": 1.0
    },
    "GRASS": {
        "FIRE": 2.0, "ICE": 2.0, "POISON": 2.0, "FLYING": 2.0, "BUG": 2.0,
        "GRASS": 0.5, "WATER": 0.5, "ELECTRIC": 0.5, "GROUND": 0.5, "NORMAL": 1.0,
        "FIGHTING": 1.0, "PSYCHIC": 1.0, "ROCK": 1.0, "DRAGON": 1.0, "DARK": 1.0,
        "STEEL": 1.0, "FAIRY": 1.0, "GHOST": 1.0
    },
    "ICE": {
        "FIRE": 2.0, "FIGHTING": 2.0, "ROCK": 2.0, "STEEL": 2.0, "ICE": 0.5,
        "NORMAL": 1.0, "WATER": 1.0, "GRASS": 1.0, "ELECTRIC": 1.0, "POISON": 1.0,
        "GROUND": 1.0, "FLYING": 1.0, "PSYCHIC": 1.0, "BUG": 1.0, "DRAGON": 1.0,
        "DARK": 1.0, "FAIRY": 1.0, "GHOST": 1.0
    },
    "FIGHTING": {
        "FLYING": 2.0, "PSYCHIC": 2.0, "FAIRY": 2.0, "BUG": 0.5, "ROCK": 0.5,
        "DARK": 0.5, "NORMAL": 1.0, "FIRE": 1.0, "WATER": 1.0, "ELECTRIC": 1.0,
        "GRASS": 1.0, "ICE": 1.0, "FIGHTING": 1.0, "POISON": 1.0, "GROUND": 1.0,
        "STEEL": 1.0, "DRAGON": 1.0, "GHOST": 1.0
    },
    "POISON": {
        "GROUND": 2.0, "PSYCHIC": 2.0, "GRASS": 0.5, "FIGHTING": 0.5, "POISON": 0.5,
        "BUG": 0.5, "FAIRY": 0.5, "NORMAL": 1.0, "FIRE": 1.0, "WATER": 1.0,
        "ELECTRIC": 1.0, "ICE": 1.0, "FLYING": 1.0, "ROCK": 1.0, "DRAGON": 1.0,
        "DARK": 1.0, "STEEL": 1.0, "GHOST": 1.0
    },
    "GROUND": {
        "WATER": 2.0, "GRASS": 2.0, "ICE": 2.0, "POISON": 0.5, "ROCK": 0.5,
        "ELECTRIC": 0.0, "NORMAL": 1.0, "FIRE": 1.0, "GROUND": 1.0, "FLYING": 1.0,
        "PSYCHIC": 1.0, "BUG": 1.0, "DRAGON": 1.0, "DARK": 1.0, "STEEL": 1.0,
        "FAIRY": 1.0, "FIGHTING": 1.0, "GHOST": 1.0
    },
    "FLYING": {
        "ELECTRIC": 2.0, "ICE": 2.0, "ROCK": 2.0, "BUG": 0.5, "FIGHTING": 0.5,
        "GRASS": 0.5, "GROUND": 0.0, "NORMAL": 1.0, "FIRE": 1.0, "WATER": 1.0,
        "FLYING": 1.0, "PSYCHIC": 1.0, "POISON": 1.0, "DRAGON": 1.0, "DARK": 1.0,
        "STEEL": 1.0, "FAIRY": 1.0, "GHOST": 1.0
    },
    "PSYCHIC": {
        "BUG": 2.0, "DARK": 2.0, "GHOST": 2.0, "PSYCHIC": 0.5, "FIGHTING": 0.5,
        "NORMAL": 1.0, "FIRE": 1.0, "WATER": 1.0, "ELECTRIC": 1.0, "GRASS": 1.0,
        "ICE": 1.0, "POISON": 1.0, "GROUND": 1.0, "FLYING": 1.0, "ROCK": 1.0,
        "DRAGON": 1.0, "STEEL": 1.0, "FAIRY": 1.0
    },
    "BUG": {
        "FIRE": 2.0, "FLYING": 2.0, "ROCK": 2.0, "FIGHTING": 0.5, "GRASS": 0.5,
        "GROUND": 0.5, "BUG": 1.0, "NORMAL": 1.0, "WATER": 1.0, "ELECTRIC": 1.0,
        "ICE": 1.0, "POISON": 1.0, "PSYCHIC": 1.0, "DRAGON": 1.0, "DARK": 1.0,
        "STEEL": 1.0, "FAIRY": 1.0, "GHOST": 1.0
    },
    "ROCK": {
        "WATER": 2.0, "GRASS": 2.0, "FIGHTING": 2.0, "GROUND": 2.0, "STEEL": 2.0,
        "NORMAL": 0.5, "FIRE": 0.5, "POISON": 0.5, "FLYING": 0.5, "BUG": 0.5,
        "ROCK": 1.0, "ELECTRIC": 1.0, "ICE": 1.0, "PSYCHIC": 1.0, "DRAGON": 1.0,
        "DARK": 1.0, "FAIRY": 1.0, "GHOST": 1.0
    },
    "GHOST": {
        "GHOST": 2.0, "DARK": 2.0, "NORMAL": 0.0, "FIGHTING": 0.0, "BUG": 0.5,
        "POISON": 0.5, "NORMAL": 1.0, "FIRE": 1.0, "WATER": 1.0, "ELECTRIC": 1.0,
        "GRASS": 1.0, "ICE": 1.0, "GROUND": 1.0, "FLYING": 1.0, "PSYCHIC": 1.0,
        "ROCK": 1.0, "DRAGON": 1.0, "STEEL": 1.0, "FAIRY": 1.0
    },
    "DRAGON": {
        "ICE": 2.0, "DRAGON": 2.0, "FAIRY": 2.0, "NORMAL": 1.0, "FIRE": 1.0,
        "WATER": 1.0, "ELECTRIC": 1.0, "GRASS": 1.0, "FIGHTING": 1.0, "POISON": 1.0,
        "GROUND": 1.0, "FLYING": 1.0, "PSYCHIC": 1.0, "BUG": 1.0, "ROCK": 1.0,
        "DARK": 1.0, "STEEL": 1.0, "GHOST": 1.0
    },
    "DARK": {
        "BUG": 2.0, "FAIRY": 2.0, "FIGHTING": 2.0, "PSYCHIC": 0.0, "DARK": 0.5,
        "GHOST": 0.5, "NORMAL": 1.0, "FIRE": 1.0, "WATER": 1.0, "ELECTRIC": 1.0,
        "GRASS": 1.0, "ICE": 1.0, "POISON": 1.0, "GROUND": 1.0, "FLYING": 1.0,
        "DRAGON": 1.0, "ROCK": 1.0, "STEEL": 1.0
    },
    "STEEL": {
        "FIRE": 2.0, "FIGHTING": 2.0, "GROUND": 2.0, "NORMAL": 0.5, "GRASS": 0.5,
        "ICE": 0.5, "FLYING": 0.5, "BUG": 0.5, "ROCK": 0.5, "DRAGON": 0.5,
        "STEEL": 0.5, "FAIRY": 0.5, "WATER": 1.0, "ELECTRIC": 1.0, "POISON": 0.0,
        "PSYCHIC": 0.5, "DARK": 1.0, "GHOST": 1.0
    },
    "FAIRY": {
        "POISON": 2.0, "STEEL": 2.0, "BUG": 0.5, "DARK": 0.5, "FIGHTING": 0.5,
        "NORMAL": 1.0, "FIRE": 1.0, "WATER": 1.0, "ELECTRIC": 1.0, "GRASS": 1.0,
        "ICE": 1.0, "GROUND": 1.0, "FLYING": 1.0, "PSYCHIC": 1.0, "ROCK": 1.0,
        "DRAGON": 0.0, "FAIRY": 1.0, "GHOST": 1.0
    }
}