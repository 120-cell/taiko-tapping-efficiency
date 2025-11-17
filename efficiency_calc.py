from tapping_styles import *
import math


def main():
    style_comparison(four_key_styles + eight_key_styles, 16, 3)


def style_comparison(style_list, max_pattern_length, decimal_places):
    name_len = max([len(style.__name__) for style in style_list])
    print('pattern length'.rjust(name_len) + ':\t',
          '\t'.join([str(i) for i in range(1, max_pattern_length + 1)]))
    for style in style_list:
        effs = [average_finger_eff(style, l) for l in range(1, max_pattern_length + 1)]
        print(f'{style.__name__.rjust(name_len)}:\t',
               '\t'.join([f'{eff:.{decimal_places}f}' for eff in effs]))


def average_finger_eff(tapping_style, pattern_length):
    efficiencies = []
    for i in range(2**pattern_length):
        pattern = [int(b) for b in bin(i)[2:].zfill(pattern_length)]
        efficiencies.append(min_finger_interval(tapping_style, pattern))
    average = sum(efficiencies) / 2**pattern_length
    return average


def min_finger_interval(tapping_style, pattern):
    layout, _ = tapping_style([])
    reps = 2 * math.ceil(len(layout) / len(pattern)) + 1
    pattern = pattern * reps
    _, fingering = tapping_style(pattern)
    distances = []
    for finger in range(len(layout)):
        indices = [i for i, x in enumerate(fingering) if x == finger]
        distances += [indices[i + 1] - indices[i] for i in range(len(indices) - 1)]
    return min(distances)


if __name__ == '__main__':
    main()