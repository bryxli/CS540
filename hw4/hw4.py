import csv
import numpy as np
from scipy.cluster import hierarchy
import matplotlib.pyplot as plt

def load_data(filepath):
    with open(filepath, 'r') as pokemon:
        reader = csv.DictReader(pokemon)
        output = []
        for row in reader:
            safe_row = dict(row)
            stats = {
                'HP': safe_row['HP'],
                'Attack': safe_row['Attack'],
                'Defense': safe_row['Defense'],
                'Sp. Atk': safe_row['Sp. Atk'],
                'Sp. Def': safe_row['Sp. Def'],
                'Speed': safe_row['Speed']
            }
            output.append(stats)
        return output

def calc_features(row):
    return np.array([int(row['Attack']),int(row['Sp. Atk']),int(row['Speed']),int(row['Defense']),int(row['Sp. Def']),int(row['HP'])],dtype=np.int64)

def hac(features):
    # initialize data structures
    clustering = [[None for x in range(4)] for y in range(len(features) - 1)]
    points = {}
    for i in range(len(features)):
        points[str(i)] = None

    # populate clustering
    for row in range(len(clustering)):
        low = [None,None,None]
        # find clusters to merge
        for i in range(len(features)):
            for j in range(len(features)):
                # check to see points aren't the same or have not been initialized
                if (points[str(i)] != points[str(j)]) or (points[(str(i))] == None and points[(str(j))] == None):
                    duplicate = False
                    # calculate distance between two clusters
                    distance = np.linalg.norm(features[i] - features[j])
                    for clusters in clustering:
                        # check to see if point pair is already used
                        if (i == clusters[0] and j == clusters[1]) or (i == clusters[1] and j == clusters[0]):
                            duplicate = True
                        # calculate complete linkage
                        elif i == clusters[0]:
                            temp_distance = np.linalg.norm(clusters[1] - features[j])
                            if temp_distance > distance:
                                distance = temp_distance
                        elif i == clusters[1]:
                            temp_distance = np.linalg.norm(clusters[0] - features[j])
                            if temp_distance > distance:
                                distance = temp_distance
                        elif j == clusters[0]:
                            temp_distance = np.linalg.norm(clusters[1] - features[i])
                            if temp_distance > distance:
                                distance = temp_distance
                        elif j == clusters[1]:
                            temp_distance = np.linalg.norm(clusters[0] - features[i])
                            if temp_distance > distance:
                                distance = temp_distance
                    if not duplicate and i != j:
                        # if lower distance or not initalized
                        if low[2] is None or distance < low[2]:
                            low[0] = i
                            low[1] = j
                            low[2] = distance
                        # if tie
                        elif distance == low[2]:
                            # if first index lower
                            if i < low[0]:
                                low[0] = i
                                low[1] = j
                                low[2] = distance
                            elif i == low[0]:
                                # if second index lower
                                if j < low[1]:
                                    low[0] = i
                                    low[1] = j
                                    low[2] = distance

        # initialize clusters and points
        c1 = points[str(low[0])]
        c2 = points[str(low[1])]
        total = 2

        # create cluster
        if c1 == None:
            p1 = low[0]
            points[str(low[0])] = row
        else:
            p1 = c1 + len(features)
            total += clustering[c1][3] - 1
            for point in points:
                if points[point] == c1:
                    points[point] = row
        if c2 == None:
            p2 = low[1]
            points[str(low[1])] = row
        else:
            p2 = c2 + len(features)
            total += clustering[c2][3] - 1
            for point in points:
                if points[point] == c2:
                    points[point] = row

        # Z[i,0] < Z[i,1]
        if p1 < p2:
            clustering[row][0] = p1
            clustering[row][1] = p2
        else:
            clustering[row][1] = p1
            clustering[row][0] = p2
        
        # store rest of clustering data
        clustering[row][2] = low[2]
        clustering[row][3] = total

    return np.array(clustering)
        
def imshow_hac(Z):
    plt.figure()
    hierarchy.dendrogram(Z)
    plt.show()