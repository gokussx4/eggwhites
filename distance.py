import numpy as np
import operator
import collections

def spherical_dist(pos1, pos2, r=3958.75):
    pos1 = pos1 * np.pi / 180
    pos2 = pos2 * np.pi / 180
    cos_lat1 = np.cos(pos1[..., 0])
    cos_lat2 = np.cos(pos2[..., 0])
    cos_lat_d = np.cos(pos1[..., 0] - pos2[..., 0])
    cos_lon_d = np.cos(pos1[..., 1] - pos2[..., 1])
    return r * np.arccos(cos_lat_d - cos_lat1 * cos_lat2 * (1 - cos_lon_d))

def get_sorted_dist(distances):
    distanceAsMap = dict(enumerate(distances.flatten(), 1))
    sortedDistanceMap = sorted(distanceAsMap.items(), key=operator.itemgetter(1))
    return sortedDistanceMap

def get_distance_sorted_responders(pos1, pos2Dictionary):
    #initialize data
    #pos1=np.array([0, 0])
    #pos2Dictionary = collections.OrderedDict()
    #pos2Dictionary.update({'user1': [4, 4]})
    #pos2Dictionary.update({'user2': [3, 3]})
    #pos2Dictionary.update({'user3': [2, 2]})
    #pos2Dictionary.update({'user4': [0, 0]})
    #pos2Dictionary.update({'user5': [1, 1]})
    pos2 = np.array(pos2Dictionary.values())
    result = collections.OrderedDict()
    sorted = get_sorted_dist(spherical_dist(pos1, pos2))
    for k,v in sorted:
        result[pos2Dictionary.keys()[k-1]] = pos2Dictionary.values()[k-1]
    return result