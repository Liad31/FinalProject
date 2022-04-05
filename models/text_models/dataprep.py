import numpy as np
import re
import gensim
import torch
import random
import os
import os.path as osp

def removeUnnecessarySpaces(text):
    return re.sub(r'[\n\t\ ]+', ' ', text)


def removeNonArabicChar(text):
    return re.sub(r'[^0-9\u0600-\u06ff\u0750-\u077f\ufb50-\ufbc1\ufbd3-\ufd3f\ufd50-\ufd8f\ufd50-\ufd8f\ufe70-\ufefc\uFDF0-\uFDFD.0-9]+', ' ', text)


def remove_numbers(text):
    return ''.join([i for i in text if not i.isdigit()])


def sentTokenize(text):
    return text.replace(".", ". \n- ")


def clean_str(text):
    search = ["@" ,"#","أ", "إ", "آ", "ة", "_", "-", "/", ".", "،", " و ", " يا ", '"', "ـ", "'", "ى", "\\", '\n', '\t',
              '&quot;', '?', '؟', '!']
    replace = ["","", "ا", "ا", "ا", "ه", " ", " ", "", "", "", " و", " يا", "", "", "", "ي", "", ' ', ' ', ' ', ' ? ', ' ؟ ',
               ' ! ']

    # remove tashkeel
    p_tashkeel = re.compile(r'[\u0617-\u061A\u064B-\u0652]')
    text = re.sub(p_tashkeel, "", text)

    # remove longation
    p_longation = re.compile(r'(.)\1+')
    subst = r"\1\1"
    text = re.sub(p_longation, subst, text)

    text = text.replace('وو', 'و')
    text = text.replace('يي', 'ي')
    text = text.replace('اا', 'ا')

    for i in range(0, len(search)):
        text = text.replace(search[i], replace[i])

    # trim
    text = text.strip()
    text = remove_numbers(text)
    return text


def clean(text):
    text = removeUnnecessarySpaces(text)
    text = removeNonArabicChar(text)
    text = clean_str(text)
    return removeUnnecessarySpaces(text)


# datas = np.load("data.npy", allow_pickle=True)
# tags = np.load("tag.npy")
# # print((datas))
# # print((tags))
#
# new_data = [(data['text'], tag) for (data, tag) in zip(datas, tags)]
#
# cleaner_data = []
# for (data, tag) in new_data:
#     cleaner = []
#     for word in data.split(' '):
#         if '#' not in word and '@' not in word:
#             cleaner.append(word)
#     cleaner = clean(' '.join(cleaner))
#     if cleaner != '' and cleaner != ' ':
#         cleaner_data.append((cleaner, tag))
#
# print(len(cleaner_data))
#
#
# t_model = gensim.models.Word2Vec.load('full_uni_sg_100_twitter.mdl')
# word_vectors = t_model.wv
# del t_model
#
# embedded_data = []
#
# for (data, tag) in cleaner_data:
#     embedded = [word_vectors[word] for word in data.split() if word in word_vectors]
#     embedded_data.append((embedded, tag))
#
# print(embedded_data)

def join_sentences(first, second):
    if first not in ["", " "] and second not in ["", " "]:
        return first + " . " + second
    return first + second


this_dir, this_filename = osp.split(__file__)
t_model = gensim.models.Word2Vec.load(osp.join(this_dir,'full_uni_sg_300_twitter.mdl'))
def prep_data(examples, labels):
    # load data
    new_data = [(example['text'], example['videoText'] if 'videoText' in example else "", 1 if label else 0) for (example, label) in zip(examples, labels)]

    # clean data
    cleaner_data = []
    for (text, video_text, tag) in new_data:
        cleaner_text = []
        for word in text.split(' '):
            if '#' not in word and '@' not in word:
                cleaner_text.append(word)
        cleaner_text = clean(' '.join(cleaner_text))
        cleaner_video_text = clean(video_text)
        cleaner = join_sentences(cleaner_text, cleaner_video_text)
        if cleaner != '' and cleaner != ' ':
            cleaner_data.append((cleaner, tag))
        else:
            cleaner_data.append((None, tag))

    # embed data
    print(os.getcwd())
    
    word_vectors = t_model.wv
    embedded_data = []
    for (text, tag) in cleaner_data:
        if text:
            embedded = [word_vectors[word] for word in text.split() if word in word_vectors]
            if embedded:
                embedded_data.append((embedded, tag))
            else:
                embedded_data.append((None, tag))
        else:
            embedded_data.append((None, tag))

    print(len(embedded_data))
    return embedded_data


def embed_text(model, data, labels):
    embedded_data = prep_data(data, labels)
    for x, embed_x in zip(data, embedded_data):
        if embed_x[0]:
            m = torch.from_numpy(np.array(embed_x[0]))
            z = torch.permute(torch.unsqueeze(m, 0), (1, 0, 2))
            y = model.forward_to_last_layer(z)
            x["text_embeded"] = y
            x["text"] = 1
        else:
            x["text_embeded"] = torch.tensor([0]*64)
            x["text"] = 0


def lengths_clones(samples):
    d = {}
    for (s, tag) in samples:
        if len(s) in d.keys():
            d[len(s)].append((s, tag))
        else:
            d[len(s)] = [(s, tag)]
    # print(d)
    return d


def split_to_batches(samples, batch_size):
    batches = list()
    samples = lengths_clones(samples)
    for size in samples.keys():
        i = 0
        batch = []
        tags = []
        for (example, tag) in samples[size]:
            if i == batch_size:
                # print(batch)
                batches.append((torch.permute(torch.from_numpy(np.array(batch)), (1, 0, 2)), torch.tensor(tags)))
                # batches.append((np.array(batch), tags))
                batch = []
                tags = []
                i = 0
            batch.append(example)
            tags.append([tag])
            i += 1
        if batch:
            batches.append((torch.permute(torch.from_numpy(np.array(batch)), (1, 0, 2)), torch.tensor(tags)))
        # batches.append((np.array(batch), tags))
    return batches


def load_my_data(file):
    return np.load(file, allow_pickle=True)


if __name__ == '__main__':
    # pre_data = load_my_data("my_data_300_sg.npy")
    # data = np.load('train_val_300_sg.npy', allow_pickle=True)
    # test = np.load('test_300_sg.npy', allow_pickle=True)
    # print("bye")
    # count = 0
    # for i in range(len(pre_data)):
    #     for j in range(len(data)):
    #         if pre_data[i][0][0][0] == data[j][0][0][1] and pre_data[i][0][0][0] == data[j][0][0][1]:
    # for i in pre_data:
    #     for j in data:
    #         if len(i[0]) == len(j[0]):
    #             flag = 1
    #             for k in range(len(i[0])):
    #                 if not np.array_equal(np.array(i[0][k]), np.array(j[0][k])):
    #                     flag = 0
    #                     break
    #             count += flag
    # print(count)

    # data_size = int(0.8 * len(pre_data))
    # data, test_set = torch.utils.data.random_split(pre_data, [data_size, len(pre_data) - data_size])
    # data, test_set = list(data), list(test_set)
    # np.save('train_val_300_sg', data)
    # np.save('test_300_sg', test_set)
    x_train = np.load('x_train.npy', allow_pickle=True)
    y_train = np.load('y_train.npy', allow_pickle=True)
    # x_val = np.load('../hashtags_models/x_val.npy', allow_pickle=True)
    # y_val = np.load('../hashtags_models/y_val.npy', allow_pickle=True)
    x_test = np.load('x_test.npy', allow_pickle=True)
    y_test = np.load('y_test.npy', allow_pickle=True)
    train = prep_data(x_train, y_train)
    train = [x for x in train if x[0] is not None]
    # val = prep_data(x_val, y_val)
    # val = [x for x in val if x[0] is not None]
    test = prep_data(x_test, y_test)
    test = [x for x in test if x[0] is not None]
    np.save('train', np.array(train, dtype=object))
    # np.save('val', np.array(val, dtype=object))
    np.save('test', np.array(test, dtype=object))

# if __name__ == '__main__':
#     x_train = np.load('../hashtags_models/x_train.npy', allow_pickle=True)
#     y_train = np.load('../hashtags_models/y_train.npy', allow_pickle=True)
#     x_val = np.load('../hashtags_models/x_val.npy', allow_pickle=True)
#     y_val = np.load('../hashtags_models/y_val.npy', allow_pickle=True)
#     x_test = np.load('../hashtags_models/x_test.npy', allow_pickle=True)
#     y_test = np.load('../hashtags_models/y_test.npy', allow_pickle=True)
#     x_train = x_train[y_train != 2]
#     y_train = y_train[y_train != 2]
#     x_val = x_val[y_val != 2]
#     y_val = y_val[y_val != 2]
#     x_test = x_test[y_test != 2]
#     y_test = y_test[y_test != 2]
#     np.save('../hashtags_models/x_train.npy', x_train)
#     np.save('../hashtags_models/y_train.npy', y_train)
#     np.save('../hashtags_models/x_val.npy', x_val)
#     np.save('../hashtags_models/y_val.npy', y_val)
#     np.save('../hashtags_models/x_test.npy', x_test)
#     np.save('../hashtags_models/y_test.npy', y_test)


