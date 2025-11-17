

def kddk_wrist_alt(pattern, starting_finger=None):
    layout = [1,0,0,1]
    if starting_finger is None:
        if pattern and pattern[0]:
            starting_finger = 0
        else:
            starting_finger = 1
    elif layout[starting_finger] != pattern[0]:
        raise ValueError('starting finger does not match pattern color')
    if starting_finger < 2:
        wrist = 0

    fingering = [starting_finger]
    for note in pattern[1:]:
        wrist = 1 - wrist
        if note:
            fingering.append(0 + 3 * wrist)
        else:
            fingering.append(1 + 1 * wrist)
    return layout, fingering


def kddk_full_roll(pattern, starting_finger=None):
    layout = [1,0,0,1]
    if starting_finger is None:
        wrist = 0
    else:
        if layout[starting_finger] != pattern[0]:
            raise ValueError('starting finger does not match pattern color')
        wrist = starting_finger // 2
    first_note = None
    
    fingering = []
    for note in pattern:
        if note == first_note:
            wrist = 1 - wrist

        if note:
            fingering.append(0 + 3 * wrist)
        else:
            fingering.append(1 + 1 * wrist)

        if first_note == None:
            first_note = note
        elif note != first_note:
            wrist = 1 - wrist
            first_note = None
    return layout, fingering


def global_rotation(layout, rotation, pattern):
    i = 0
    fingering = []
    for note in pattern:
        while not layout[rotation[i]] == note:
            i = (i + 1) % len(rotation)
        fingering.append(rotation[i])
        i = (i + 1) % len(rotation)
    return fingering


def kddk_half_roll(pattern, starting_finger=0):
    layout = [1,0,0,1]
    rotation = [0,1,3,2]
    if starting_finger < 2:
        starting_index = starting_finger
    else:
        starting_index = 5 - starting_finger
    rotation = rotation[starting_index:] + rotation[:starting_index]
    return layout, global_rotation(layout, rotation, pattern)


def kdkddkdk_half_roll(pattern, starting_finger=0):
    layout = [1,0,1,0,0,1,0,1]
    rotation = [0,1,2,3,7,6,5,4]
    if starting_finger < 4:
        starting_index = starting_finger
    else:
        starting_index = 11 - starting_finger
    rotation = rotation[starting_index:] + rotation[:starting_index]
    return layout, global_rotation(layout, rotation, pattern)


def dual_rotation(d_rotation, k_rotation, pattern):
    length = len(d_rotation) + len(k_rotation)
    if not all([(i in d_rotation or i in k_rotation) for i in range(length)]):
        raise ValueError('invalid d and k rotations')
    layout = [(i in k_rotation) for i in range(length)]
    d_i = 0
    k_i = 0
    fingering = []
    for note in pattern:
        if note:
            fingering.append(k_rotation[k_i])
            k_i = (k_i + 1) % len(k_rotation)
        else:
            fingering.append(d_rotation[d_i])
            d_i = (d_i + 1) % len(d_rotation)
    return layout, fingering


def handwise_dual_rotation(keys_per_hand, pattern, d_starting_finger=0, k_starting_finger=None):
    n = keys_per_hand
    if k_starting_finger is None:
        k_starting_finger = 2 * n - 1
    if d_starting_finger >= n:
        raise ValueError('starting finger does not match layout color')
    else:
        d_rotation = [(d_starting_finger + i) % n for i in range(n)]
    if k_starting_finger < n:
        raise ValueError('starting finger does not match layout color')
    else:
        k_rotation = [n + (k_starting_finger - n - i) % n for i in range(n)]
    return dual_rotation(d_rotation, k_rotation, pattern)


def ddkk_dual_rotation(pattern, d_starting_finger=0, k_starting_finger=3):
    return handwise_dual_rotation(2, pattern, d_starting_finger, k_starting_finger)


def ddddkkkk_dual_rotation(pattern, d_starting_finger=0, k_starting_finger=7):
    return handwise_dual_rotation(4, pattern, d_starting_finger, k_starting_finger)
    

four_key_styles = [
    kddk_wrist_alt,
    kddk_half_roll,
    kddk_full_roll,
    ddkk_dual_rotation
]
eight_key_styles = [
    kdkddkdk_half_roll,
    ddddkkkk_dual_rotation
]