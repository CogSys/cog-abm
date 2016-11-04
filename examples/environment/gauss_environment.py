import numpy as np
from scipy.spatial import distance
import json

STIMULI_NUM = 600
STIM = (47,7,39)
COV = np.array([[1, 0, 0],
                [0, 1, 0],
                [0, 0, 1]])
STIMULI_FILE = '1269_munsell_chips.json'
DIST = 10.433935691395032


def fun(stimuli_file=STIMULI_FILE):
    with open(stimuli_file, 'r') as g:
        stimuli = json.load(g)
    chips = [i.values() for i in stimuli['stimuli']]
    min_dist = 0
    for chip in chips:
        dist = distance.cdist([chip], [i for i in chips if i!=chip], 'euclidean')
        if (min_dist <= np.min(dist)):
            min_dist = np.min(dist)
    return min_dist


def gauss_divide(output_name, stim=STIM, stimuli_num=STIMULI_NUM,
                 stimuli_file=STIMULI_FILE, cov=COV):
    with open(stimuli_file, 'r') as g:
        stimuli = json.load(g)
    chips = [i.values() for i in stimuli['stimuli']]
    random_chips = []
    i = 0
    while ( i < stimuli_num):
        x = np.random.multivariate_normal(stim, cov)
        if np.min(distance.cdist([x], chips, 'euclidean')) <= DIST:
            random_chips.append({"a": x[0], "L": x[1], "b": x[2]})
            i = i + 1

    with open(output_name+".json", 'w') as f:
        json.dump({"stimuli": random_chips, "type": "CIELab"}, f)


def find_focal_points(stimuli_file=STIMULI_FILE):
    with open(stimuli_file, 'r') as g:
        stimuli = json.load(g)
    print(stimuli['stimuli'][0]['L'], stimuli['stimuli'][0]['a'], stimuli['stimuli'][0]['b'], stimuli['stimuli'][0].values())
    chips = np.array([i.values() for i in stimuli['stimuli']])

    min_v, max_v = chips.max(axis=0), chips.min(axis=0)

    p1 = min_v + 0.33*(max_v-min_v)
    p2 = min_v + 0.66*(max_v-min_v)

    return p1, p2


if __name__ == "__main__":
    stim1, stim2 = find_focal_points()
    scale = np.abs(stim2 - stim1)*10

    cov = np.array([[scale[0], 0, 0], [0, scale[1], 0], [0, 0, scale[2]]])

    np.random.seed(13)
    gauss_divide("600_munsell_chips_gauss_1", stim=stim1, stimuli_num=600,
                 cov=cov)
    gauss_divide("600_munsell_chips_gauss_2", stim=stim2, stimuli_num=600,
                 cov=cov)
