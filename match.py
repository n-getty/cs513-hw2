import pandas as pd
import numpy as np
import math


probe_data = "data/Partition6467ProbePoints.csv"
link_data = "data/Partition6467LinkData.csv"
matched_data = "results/Partition6467MatchedPoints.csv"

probe_df = pd.read_csv(probe_data, header=None, names=['sampleID', 'dateTime', 'sourceCode', 'latitude', 'longitude', 'altitude', 'speed', 'heading'])
link_df = pd.read_csv(link_data, header=None, usecols=[0,1,2,3,5,14,16], names=['linkPVID', 'refNodeID', 'nrefNodeID', 'length', 'directionOfTravel', 'shapeInfo', 'slopeInfo'])

link_df.shapeInfo = link_df.shapeInfo.str.split('|')
refLocs = []

for links in link_df.shapeInfo:
    loc = links[0].split('/')
    nloc = links[-1].split('/')
    refLocs.append((float(loc[0]),float(loc[1]),float(nloc[0]),float(nloc[1])))

link_df['refLocs'] = pd.Series(refLocs)


def calcDist(probe, link):
    refDist = math.sqrt((probe[0]-link[0]) ** 2 + (probe[1]-link[1]) ** 2)
    nrefDist = math.sqrt((probe[0]-link[2]) ** 2 + (probe[1]-link[3]) ** 2)

    if refDist < nrefDist:
        return [refDist, 'F']
    else:
        return [nrefDist, 'T']


uniIds = set(probe_df.sampleID)

for id in uniIds:
    probes = probe_df[probe_df.sampleID == id]
    for x in range(len(probes)-1):
        fp = probes.iloc[x]
        sp = probes.iloc[x+1]
        res = np.array([calcDist((fp.latitude, fp.longitude),l) for l in link_df.refLocs])
        all_dists = res[:,0]
        all_direc = res[:,1]
        idxs = all_dists==min(all_dists)
        candidates = all_dists[idxs]
        cand_direc = all_direc[idxs]


link_df.slopeInfo = link_df.slopeInfo.str.split('|')