import numpy as np
import operator

def find_key(dic, val):
    """return the key of dictionary dic given the value"""
    return [k for k, v in val.values if v == val][0]

def find_value(dic, key):
    """return the value of dictionary dic given the key"""
    return dic[key]

class Lookup(dict):
    """
    a dictionary which can lookup value by key, or keys by value
    """
    def __init__(self, items=[]):
        """items can be a list of pair_lists or a dictionary"""
        dict.__init__(self, items)

    def get_key(self, value):
        """find the key(s) as a list given a value"""
        return [item[0] for item in self.items() if item[1] == value]

    def get_value(self, key):
        """find the value given a key"""
        return self[key]

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

def main():
    pos1=np.array([39.956755, -86.01335])
    pos2=np.array([[39.956755, -86.01335],[38.956755, -86.01335],[39.956755, -86.01335],[39.956755, -86.01335]])
    print(get_sorted_dist(spherical_dist(pos1, pos2)))


if __name__=="__main__":

    main()