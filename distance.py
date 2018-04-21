import numpy as np

def spherical_dist(pos1, pos2, r=3958.75):
    pos1 = pos1 * np.pi / 180
    pos2 = pos2 * np.pi / 180
    cos_lat1 = np.cos(pos1[..., 0])
    cos_lat2 = np.cos(pos2[..., 0])
    cos_lat_d = np.cos(pos1[..., 0] - pos2[..., 0])
    cos_lon_d = np.cos(pos1[..., 1] - pos2[..., 1])
    return r * np.arccos(cos_lat_d - cos_lat1 * cos_lat2 * (1 - cos_lon_d))

def main():
    pos1=np.array([39.956755, -86.01335])
    pos2=np.array([[39.956755, -86.01335],[38.956755, -86.01335],[39.956755, -86.01335],[39.956755, -86.01335]])
    print(spherical_dist(pos1, pos2))

if __name__=="__main__":
    main()