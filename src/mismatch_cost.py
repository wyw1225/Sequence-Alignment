# use dict here, so that we can mismatch
# by using statement such as
# mismatch_cost['A']['T']
mismatch_cost = {
    'A': {
        'A': 0,
        'C': 110,
        'G': 48,
        'T': 94,
    },
    'C': {
        'A': 110,
        'C': 0,
        'G': 118,
        'T': 48,
    },
    'G': {
        'A': 48,
        'C': 118,
        'G': 0,
        'T': 110,
    },
    'T': {
        'A': 94,
        'C': 48,
        'G': 110,
        'T': 0,
    },
}

gap_cost = 30
