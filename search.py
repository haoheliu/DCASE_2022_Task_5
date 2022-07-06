import os
from glob import glob
import json
import matplotlib.pyplot as plt
import collections
import pandas as pd


def read(fname):
    with open(fname, "r") as json_data:
        data = json_data.read().replace("\n", "")
        d = json.loads(data)
    return d


def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False


def boxplot(dict1):
    labels, data = [
        *zip(*dict1.items())
    ]  # 'transpose' items to parallel key, value lists

    # or backwards compatable
    labels, data = dict1.keys(), dict1.values()
    plt.figure(figsize=(15, 5))
    plt.boxplot(data)

    plt.xticks(range(1, len(labels) + 1), labels)

    for k, v in zip(labels, data):
        k = [k] * len(v)
        plt.scatter(k, v, s=3, c="black", alpha=0.3)

    plt.savefig("/vol/research/dcase2022/project/hhlab/temp.png")


# path = "/vol/research/dcase2022/project/hhlab/logs"
path = "/vol/research/dcase2022/project/hhlab/logs/experiments/runs"
prefix = "Evaluation_report_UoSurrey_unprocessed_VAL_"
folder = "0.9"

# for each in glob(os.path.join(path,"*/*/*/*/*.json")) + glob(os.path.join(path,"*/*/*/*/*/*.json")) + glob(os.path.join(path,"*/*/*/*/*/*/*.json")):
#     if(prefix not in each): continue
#     res = read(each)
#     if(res['overall_scores']['fmeasure'] > 60):
#         print(res['overall_scores']['fmeasure'], each)

res_dict = {}


def read_result(folder):
    json_file = glob(os.path.join(folder, "*.json"))
    if len(json_file) < 1:
        return None
    ret = []
    for each in json_file:
        # json_file = json_file[0]
        dic = read(each)["scores_per_subset"]
        if "PB" not in dic.keys():
            return None
        ret.append(dic["PB"]["f-measure"])
    return ret


result = {}
i = 0
for each in (
    glob(os.path.join(path, "*/%s" % folder))
    + glob(os.path.join(path, "*/*/%s" % folder))
    + glob(os.path.join(path, "*/*/*/%s" % folder))
    + glob(os.path.join(path, "*/*/*/*/%s" % folder))
    + glob(os.path.join(path, "*/*/*/*/*/%s" % folder))
    + glob(os.path.join(path, "*/*/*/*/*/*/%s" % folder))
):
    res = read_result(each)
    if res is None or max(res) < 40:
        print(res)
        continue

    i += 1
    if i > 20:
        break
    dirname = os.path.dirname(each)
    for folder in os.listdir(dirname):
        # print(folder, isfloat(folder))
        if isfloat(folder):
            if folder not in res_dict.keys():
                res_dict[folder] = []
            # print(dirname, folder)
            score = read_result(os.path.join(dirname, folder))
            if score is None:
                continue
            # print(max(score), dirname, folder)
            result[max(score)] = folder + "_" + dirname
            res_dict[folder].append(max(score))

res_dict = collections.OrderedDict(sorted(res_dict.items()))
result = collections.OrderedDict(sorted(result.items()))

# Serializing json
json_object = json.dumps(result, indent=4)
print(json_object)

# df = pd.DataFrame.from_dict(res_dict)
# df.to_csv("threshold.csv")
import ipdb

ipdb.set_trace()
boxplot(res_dict)
