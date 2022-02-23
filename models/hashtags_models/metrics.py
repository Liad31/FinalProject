import numpy as np

# correlation_dict = {'a':0.6,'b':0.5, 'c':0.9, 'd':-0.3,'e':-0.7,'f':-0.8}
# {'a': [],}       => correlation_dict
# {'a': [-1, 1] }


def cut(hashtags1, hashtags2, correlation_dict):
    return np.tanh(len(list(set(hashtags1).intersection(hashtags2))))


def cut_union(hashtags1, hashtags2, correlation_dict):
    return (len(list(set(hashtags1).intersection(hashtags2))))/len(set(hashtags1 + hashtags2))


def cut_union_corr(hashtags1, hashtags2, correlation_dict):
    cut = list(set(hashtags1).intersection(hashtags2))
    cut_corr_sum = 0
    for hash in cut:
        if hash in correlation_dict:
            cut_corr_sum += abs(correlation_dict[hash])

    union = set(hashtags1 + hashtags2)
    union_corr_sum = 0
    for hash in union:
        if hash in correlation_dict:
            union_corr_sum += abs(correlation_dict[hash])

    return cut_corr_sum/union_corr_sum


def cut_union_corr_sum(hashtags1, hashtags2, correlation_dict):
    cut = list(set(hashtags1).intersection(hashtags2))
    cut_corr_sum = 0
    for hash in cut:
        if hash in correlation_dict:
            cut_corr_sum += abs(correlation_dict[hash])

    sum_corr_first = 0
    for hash in hashtags1:
        if hash in correlation_dict:
            sum_corr_first += correlation_dict[hash]

    sum_corr_second = 0
    for hash in hashtags2:
        if hash in correlation_dict:
            sum_corr_second += correlation_dict[hash]

    if cut_corr_sum > 0 and sum_corr_first - sum_corr_second == 0:
        return 1
    return np.tanh(cut_corr_sum / abs(sum_corr_first - sum_corr_second))



# def cut_union_corr_avg(hashtags1, hashtags2, correlation_dict):
#     cut = list(set(hashtags1).intersection(hashtags2))
#     cut_corr_sum = 0
#     for hash in cut:
#         cut_corr_sum += abs(correlation_dict[hash])
#     cut_corr_sum /= len(cut)
#
#     avg_corr_first = 0
#     for hash in hashtags1:
#         avg_corr_first += correlation_dict[hash]
#     avg_corr_first /= len(hashtags1)
#
#     avg_corr_second = 0
#     for hash in hashtags2:
#         avg_corr_second += correlation_dict[hash]
#     avg_corr_second /= len(hashtags2)
#
#     if cut_corr_sum > 0 and avg_corr_first - avg_corr_second == 0:
#         return 1
#
#     return cut_corr_sum / abs(avg_corr_first - avg_corr_second)



