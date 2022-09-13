import csv
import os

import scipy
import torch
import numpy as np
from collections import defaultdict
import random
from sklearn.preprocessing import normalize
from collections import OrderedDict
from scipy import sparse
from scipy.spatial.distance import pdist
from scipy.sparse import dok_matrix
import logging

class DataLoader:
    def __init__(self, task_dir, n_sample):
        self.inPath = task_dir
        self.n_sample = n_sample
        self.feature_size = 0

        print("The toolkit is importing datasets.\n")
        with open(os.path.join(self.inPath, "relation2id.txt")) as f:
            tmp = f.readline()
            self.n_rel = int(tmp.strip())
            print("The total of relations is {}".format(self.n_rel))

        with open(os.path.join(self.inPath, "entity2id.txt"), encoding='utf-8') as f:
            tmp = f.readline()
            self.n_ent = int(tmp.strip())
            print("The total of entities is {}".format(self.n_ent))

        self.train_head, self.train_tail, self.train_rela = self.read_data("train2id.txt")
        self.valid_head, self.valid_tail, self.valid_rela = self.read_data("valid2id.txt")
        self.test_head,  self.test_tail,  self.test_rela  = self.read_data("test2id.txt")

    def read_data(self, filename):
        allList = []
        head = []
        tail = []
        rela = []
        with open(os.path.join(self.inPath, filename)) as f:
            tmp = f.readline()
            total = int(tmp.strip())
            for i in range(total):
                tmp = f.readline()
                h, t, r = tmp.strip().split()
                h, t, r = int(h), int(t), int(r)
                allList.append((h, t, r))

        allList.sort(key=lambda l:(l[0], l[1], l[2]))

        head.append(allList[0][0])
        tail.append(allList[0][1])
        rela.append(allList[0][2])

        for i in range(1, total):
            if allList[i] != allList[i-1]:
                h, t, r = allList[i]
                head.append(h)
                tail.append(t)
                rela.append(r)
        return head, tail, rela

    def graph_size(self):
        return (self.n_ent, self.n_rel)

    def load_data(self, index):
        if index == 'train':
            return self.train_head, self.train_tail, self.train_rela
        elif index == 'valid':
            return self.valid_head, self.valid_tail, self.valid_rela
        else:
            return self.test_head,  self.test_tail,  self.test_rela

    def heads_tails(self):
        all_heads = self.train_head + self.valid_head + self.test_head
        all_tails = self.train_tail + self.valid_tail + self.test_tail
        all_relas = self.train_rela + self.valid_rela + self.test_rela

        heads = defaultdict(lambda: set())
        tails = defaultdict(lambda: set())
        for h, t, r in zip(all_heads, all_tails, all_relas):
            tails[(h, r)].add(t)
            heads[(t, r)].add(h)

        #get feature size
        heads_train = defaultdict(lambda: set())
        tails_train = defaultdict(lambda: set())
        for h, t, r in zip(self.train_head, self.train_tail, self.train_rela):
            tails_train[(h, r)].add(t)
            heads_train[(t, r)].add(h)
        self.feature_size = len(tails_train) + len(heads_train)

        heads_sp = {}
        tails_sp = {}
        for k in heads.keys():
            heads_sp[k] = torch.sparse.FloatTensor(torch.LongTensor([list(heads[k])]),
                                                   torch.ones(len(heads[k])), torch.Size([self.n_ent]))

        for k in tails.keys():
            tails_sp[k] = torch.sparse.FloatTensor(torch.LongTensor([list(tails[k])]),
                                                   torch.ones(len(tails[k])), torch.Size([self.n_ent]))
        print("heads/tails size:", len(tails), len(heads))

        return heads_sp, tails_sp

    def get_cache_list(self):
        head_cache = {}
        tail_cache = {}
        head_pos = []
        tail_pos = []
        head_idx = []
        tail_idx = []
        count_h = 0
        count_t = 0
        for h, t, r in zip(self.train_head, self.train_tail, self.train_rela):
            if not (t,r) in head_cache:
                head_cache[(t,r)] = count_h
                head_pos.append([h])
                count_h += 1
            else:
                head_pos[head_cache[(t,r)]].append(h)

            if not (h,r) in tail_cache:
                tail_cache[(h,r)] = count_t
                tail_pos.append([t])
                count_t += 1
            else:
                tail_pos[tail_cache[(h,r)]].append(t)

            head_idx.append(head_cache[(t,r)])
            tail_idx.append(tail_cache[(h,r)])

        #一些常见数据statistic获取方法#
        # self.getrelationfeature(head_cache,tail_cache)
        # self.getnodefeaturedegree()
        # self.settemperature(head_cache, tail_cache, head_pos, tail_pos)
        self.gethrdistributionandsimilarentity(head_cache, tail_cache, head_pos, tail_pos)
        head_idx = np.array(head_idx, dtype=int)
        tail_idx = np.array(tail_idx, dtype=int)
        head_cache = np.random.randint(low=0, high=self.n_ent, size=(count_h, self.n_sample))
        tail_cache = np.random.randint(low=0, high=self.n_ent, size=(count_t, self.n_sample))
        print('head/tail_idx: head/tail_cache', len(head_idx), len(tail_idx), head_cache.shape, tail_cache.shape, len(head_pos), len(tail_pos))


        return head_idx, tail_idx, head_cache, tail_cache, head_pos, tail_pos

    def get_relation_temp(self):
        edges = defaultdict(lambda: defaultdict(lambda: set()))
        rev_edges = defaultdict(lambda: defaultdict(lambda: set()))
        for h, t, r in zip(self.train_head, self.train_tail, self.train_rela):
            edges[r][h].add(t)
            rev_edges[r][t].add(h)
        file = open(self.inPath + '/' + 'relationdis.txt', 'a')
        for k in edges.keys():
            right = sum(len(tails) for tails in edges[k].values()) / len(edges[k])
            left = sum(len(heads) for heads in rev_edges[k].values()) / len(rev_edges[k])
            file.write(str(right) + '\t')
            file.write(str(left) + '\t')

        file.close()

    def get_new_cache_list(self):
        head_cache = {}
        tail_cache = {}
        head_pos = []
        tail_pos = []
        head_idx = []
        tail_idx = []

        entity_in = np.zeros(self.n_ent, dtype=int)
        entity_out = np.zeros(self.n_ent, dtype=int)
        for h, t, r in zip(self.train_head, self.train_tail, self.train_rela):
            entity_out[h] = entity_out[h] + 1
            entity_in[t] = entity_in[t] + 1

        entity_in_size,_, entity_in_q = np.unique(entity_in, return_index=True, return_inverse=True)
        entity_out_size, _, entity_out_q = np.unique(entity_out, return_index=True, return_inverse=True)

        entity_in_cate = {}
        entity_out_cate = {}
        # write to pretain.txt
        if not os.path.exists(self.inPath + '/relation_in.txt'):
            entity_in_cate, entity_out_cate = self.writeToTxt(entity_in, entity_in_size, entity_out, entity_out_size)
        else:
            entity_in_cate, entity_out_cate = self.readFromTxt()

        need_add = []
        random_idx = []
        list = []
        head_cache = {}
        head_cache1 = np.zeros((self.n_ent, self.n_sample),dtype = int)
        tail_cache1 = np.zeros((self.n_ent, self.n_sample),dtype = int)
        head_cache2 = np.zeros((self.n_ent, self.n_ent), dtype=int)
        head_cache2[:][:] = -1
        head_cache3 = np.random.randint(self.n_ent, size = (self.n_ent, self.n_sample), dtype=int)

        tail_cache2 = np.zeros((self.n_ent, self.n_ent), dtype=int)
        tail_cache2[:][:] = -1
        tail_cache3 = np.random.randint(self.n_ent, size = (self.n_ent, self.n_sample), dtype=int)

        for i, j in entity_in_cate.items():
            # list = j.copy()
            # arr = np.copy(list)
            # random.shuffle(list)
            # if self.n_sample < len(list):
            #     tail_cache3[arr, :self.n_sample] = list[ :self.n_sample]
            # else:
            #     tail_cache3[arr, :len(list)] = list[:len(list)]
            if len(j) <= (self.n_sample):
                for k in j:
                    list = j.copy()
                    list.remove(k)
                    cut = list.copy()
                    need_add = np.random.randint(self.n_ent, size=( 1 + self.n_sample - len(j)))
                    list = list + need_add.tolist()
                    random.shuffle(list)
                    tail_cache1[k][:self.n_sample] = list[:self.n_sample]
                    tail_cache2[k][:len(cut)] = cut[:len(cut)]
            else:
                for k in j:
                    list = j.copy()
                    #list.remove(k)
                    cut = list.copy()
                    random.shuffle(list)
                    tail_cache1[k][:self.n_sample] = list[:self.n_sample]
                    tail_cache2[k][:len(cut)] = cut[:len(cut)]

        for i, j in entity_out_cate.items():
            # list = j.copy()
            # arr = np.copy(list)
            # random.shuffle(list)
            # if self.n_sample < len(list):
            #     head_cache3[arr, :self.n_sample] = list[:self.n_sample]
            # else:
            #     head_cache3[arr, :len(list)] = list[:len(list)]
            if len(j) <= (self.n_sample):
                for k in j:
                    list = j.copy()
                    #list.remove(k)
                    cut = list.copy()
                    need_add = np.random.randint(self.n_ent, size=(1+ self.n_sample - len(j)))
                    list = list + need_add.tolist()
                    random.shuffle(list)
                    head_cache1[k][:self.n_sample] = list[:self.n_sample]
                    head_cache2[k][:len(cut)] = cut[:len(cut)]
            else:
                for k in j:
                    list = j.copy()
                    #list.remove(k)
                    cut = list.copy()
                    random.shuffle(list)
                    head_cache1[k][:self.n_sample] = list[:self.n_sample]
                    head_cache2[k][:len(cut)] = cut[:len(cut)]


        tail_cache = head_cache1
        head_cache = tail_cache1





        print('head/tail_idx: head/tail_cache', len(head_idx), len(tail_idx), head_cache.shape, tail_cache.shape, len(head_pos), len(tail_pos))
        return head_idx, tail_idx, head_cache, tail_cache, head_pos, tail_pos

    def get_ver2_cache_list(self,args):
        head_pos = []
        tail_pos = []
        head_idx = []
        tail_idx = []

        entity_in = np.zeros(self.n_ent, dtype=int)
        entity_out = np.zeros(self.n_ent, dtype=int)
        for h, t, r in zip(self.train_head, self.train_tail, self.train_rela):
            entity_out[h] = entity_out[h] + 1
            entity_in[t] = entity_in[t] + 1

        entity_in_size,_, entity_in_q = np.unique(entity_in, return_index=True, return_inverse=True)
        entity_out_size, _, entity_out_q = np.unique(entity_out, return_index=True, return_inverse=True)

        # write to pretain.txt
        if not os.path.exists(self.inPath + '/relation_in.txt'):
            entity_in_cate, entity_out_cate, max_in, max_out = self.writeToTxt(entity_in, entity_in_size, entity_out, entity_out_size)
        else:
            entity_in_cate, entity_out_cate, max_in, max_out = self.readFromTxt()


        head_cache = np.random.randint(self.n_ent, size = (self.n_ent, max_out), dtype=int)
        tail_cache = np.random.randint(self.n_ent, size = (self.n_ent, max_in), dtype=int)

        for i, j in entity_in_cate.items():
            list = j.copy()
            arr = np.copy(list)
            tail_cache[arr, :len(list)] = list[:len(list)]
        for i, j in entity_out_cate.items():
            list = j.copy()
            arr = np.copy(list)
            head_cache[arr, :len(list)] = list[:len(list)]

        hh = np.reshape(np.arange(self.n_ent), (self.n_ent, 1))
        tt = np.reshape(np.arange(self.n_ent), (self.n_ent, 1))

        tail_cache = np.where(tt != tail_cache, tail_cache, np.random.randint(self.n_ent, size=tail_cache.shape))
        head_cache = np.where(hh != head_cache, head_cache, np.random.randint(self.n_ent, size=head_cache.shape))






        print('head/tail_idx: head/tail_cache', len(head_idx), len(tail_idx), head_cache.shape, tail_cache.shape, len(head_pos), len(tail_pos))
        return head_idx, tail_idx, head_cache, tail_cache, head_pos, tail_pos

    def get_ver3_cache_list(self,args):
        head_cache = {}
        tail_cache = {}
        head_pos = []
        tail_pos = []
        head_idx = []
        tail_idx = []



        entity_in_cate = {}
        entity_out_cate = {}
        # write to pretain.txt
        if not os.path.exists(self.inPath + '/relation_in.txt'):
            entity_in_cate, entity_out_cate, max_in, max_out = self.writeToTxt()
        else:
            entity_in_cate, entity_out_cate, max_in, max_out = self.readFromTxt()

        # group the candidate with min_size and step_in

        entity_in_cate,entity_out_cate = self.group_generate(args, entity_in_cate, entity_out_cate, max_in, max_out)

        # add the size of cache
        if(args.task_dir == './KG_Data/FB15K') or (args.task_dir == './KG_Data/FB15K237'):
            max_in = 10000
            max_out = 10000

        head_cache3 = np.random.randint(self.n_ent, size = (self.n_ent, max_out), dtype=int)

        tail_cache3 = np.random.randint(self.n_ent, size = (self.n_ent, max_in), dtype=int)

        count = 0
        for i, j in entity_in_cate.items():
            count += len(j)
            list = j.copy()
            arr = np.copy(list)
            tail_cache3[arr, :len(list)] = list[:len(list)]
        count = 0
        for i, j in entity_out_cate.items():
            count += len(j)
            list = j.copy()
            arr = np.copy(list)
            head_cache3[arr, :len(list)] = list[:len(list)]

        h = np.reshape(np.arange(self.n_ent), (self.n_ent, 1))
        t = np.reshape(np.arange(self.n_ent), (self.n_ent, 1))

        tail_cache3 = np.where(t != tail_cache3, tail_cache3, random.randint(0,self.n_ent))
        head_cache3 = np.where(h != head_cache3, head_cache3, random.randint(0,self.n_ent))

        ## shuffle them
        shuffle_helper_in = np.argsort(np.random.rand(self.n_ent, max_in), axis=1)
        shuffle_helper_out = np.argsort(np.random.rand(self.n_ent, max_out), axis=1)

        tail_cache = tail_cache3[np.arange(shuffle_helper_in.shape[0])[:, None], shuffle_helper_in]
        head_cache = head_cache3[np.arange(shuffle_helper_out.shape[0])[:, None], shuffle_helper_out]
        # tail_cache = tail_cache3
        # head_cache = head_cache3





        print('head/tail_idx: head/tail_cache', len(head_idx), len(tail_idx), head_cache.shape, tail_cache.shape, len(head_pos), len(tail_pos))
        return head_idx, tail_idx, head_cache, tail_cache, head_pos, tail_pos

    # select from the around 3 step
    def get_ver5_cache_list(self,args):

        head_pos = []
        tail_pos = []
        head_idx = []
        tail_idx = []



        entity_in_cate = {}
        entity_out_cate = {}
        # write to pretain.txt
        if not os.path.exists(self.inPath + '/relation_in.txt'):
            entity_in_cate, entity_out_cate, max_in, max_out = self.writeToTxt()
        else:
            entity_in_cate, entity_out_cate, max_in, max_out = self.readFromTxt()

        # group the candidate with min_size and step_in

        #entity_in_cate,entity_out_cate = self.group_generate(args, entity_in_cate, entity_out_cate, max_in, max_out)
        head_cache = np.zeros((self.n_ent, 3*max_out), dtype=int)
        head_cache[:][:] = -1
        tail_cache = np.zeros((self.n_ent, 3*max_in), dtype=int)
        tail_cache[:][:] = -1

        count = 0
        pre_list = []
        pre_arr = []
        for i, j in entity_in_cate.items():

            list = j.copy()
            arr = np.copy(list)
            #this round
            tail_cache[arr, max_in :max_in + len(list)] = list[:len(list)]
            if(count != 0):
                #pre round
                tail_cache[pre_arr, 2* max_in: 2* max_in + len(list)] = list[: len(list)]
                tail_cache[arr, : len(pre_list)] = pre_list[: len(pre_list)]

            count += 1
            pre_list = j.copy()
            pre_arr = arr.copy()

        count = 0
        pre_list = []
        pre_arr = []
        for i, j in entity_out_cate.items():

            list = j.copy()
            arr = np.copy(list)
            # this round
            head_cache[arr, max_out:max_out + len(list)] = list[:len(list)]
            if (count != 0):
                # pre round
                head_cache[pre_arr, 2 * max_out: 2 * max_out + len(list)] = list[: len(list)]
                head_cache[arr, : len(pre_list)] = pre_list[: len(pre_list)]

            count += 1
            pre_list = j.copy()
            pre_arr = arr.copy()

        hh = np.reshape(np.arange(self.n_ent), (self.n_ent, 1))
        tt = np.reshape(np.arange(self.n_ent), (self.n_ent, 1))

        tail_cache = np.where(tt != tail_cache, tail_cache, np.random.randint(self.n_ent, size=tail_cache.shape))
        head_cache = np.where(hh != head_cache, head_cache, np.random.randint(self.n_ent, size=head_cache.shape))


        print('head/tail_idx: head/tail_cache', len(head_idx), len(tail_idx), head_cache.shape, tail_cache.shape, len(head_pos), len(tail_pos))
        return head_idx, tail_idx, head_cache, tail_cache, head_pos, tail_pos

    def get_relational_cache_list(self,args):
        head_pos = []
        tail_pos = []
        head_idx = []
        tail_idx = []

        head = {}
        tail = {}
        relation_in = {}
        relation_out = {}
        graph_out = np.zeros((self.n_ent, self.n_rel), dtype= int)
        graph_in = np.zeros((self.n_ent, self.n_rel), dtype=int)

        propability_in = np.zeros((self.n_ent, self.n_ent), dtype=float)
        propability_out = np.zeros((self.n_ent, self.n_ent), dtype=float)




        if os.path.exists(self.inPath + '/propability_in.npy'):
            propability_in = np.load(self.inPath + '/propability_in.npy')
            propability_out = np.load(self.inPath + '/propability_out.npy')
        else:
            for h, t, r in zip(self.train_head, self.train_tail, self.train_rela):
                graph_out[h,r] = graph_out[h,r] + 1
                graph_in[t,r] = graph_in[t,r] + 1

            if not os.path.exists(self.inPath + '/whole_in.npy'):
                np.save(self.inPath + '/whole_in', graph_in)
                np.save(self.inPath + '/whole_out', graph_out)
            # calculate the probability of entities
            for e1_index in range(graph_in.shape[0]):
                for e2_index in range(e1_index + 1 , graph_in.shape[0]):
                    distance_in = np.abs(graph_in[e1_index] - graph_in[e2_index])
                    distance_in = np.mean(distance_in)
                    propability_in[e1_index, e2_index] = distance_in
                    propability_in[e2_index, e1_index] = distance_in

                    distance_out = np.abs(graph_out[e1_index] - graph_out[e2_index])
                    distance_out = np.mean(distance_out)
                    propability_out[e1_index, e2_index] = distance_out
                    propability_out[e2_index, e1_index] = distance_out

            np.save(self.inPath + '/propability_in', propability_in)
            np.save(self.inPath + '/propability_out', propability_out)

        index = range(0, self.n_ent)
        propability_in[index, index] = 50000
        propability_out[index, index] = 50000
        head_cache = np.random.randint(low=0, high=self.n_ent, size=(self.n_ent, self.n_sample))
        tail_cache = np.random.randint(low=0, high=self.n_ent, size=(self.n_ent, self.n_sample))

        print('head/tail_idx: head/tail_cache', len(head_idx), len(tail_idx), head_cache.shape, tail_cache.shape, len(head_pos), len(tail_pos))
        return propability_in,propability_out, head_idx, tail_idx, head_cache, tail_cache, head_pos, tail_pos

    def get_graph_relation_add_node(self,args):
        head_r = {}
        tail_r = {}
        out_r =  defaultdict(list)
        in_r =  defaultdict(list)
        r_head = defaultdict()
        r_tail = defaultdict()
        head_cache = {}
        tail_cache = {}
        head_pos = []
        tail_pos = []
        head_idx = []
        tail_idx = []

        for h, t, r in zip(self.train_head, self.train_tail, self.train_rela):
            if not (h, r) in head_r:
                head_r[(h, r)] = []
                # get the size of (t, r) with a r
                if not r in r_head:
                    r_head[r] = 0
                r_head[r] = r_head[r] + 1
            if not (t, r) in tail_r:
                tail_r[(t, r)] = []
                if not r in r_tail:
                    r_tail[r] = 0
                r_tail[r] = r_tail[r] + 1



            head_r[(h, r)].append(t)
            tail_r[(t, r)].append(h)


            if r not in out_r[h]:
                out_r[h].append(r)
            if r not in in_r[t]:
                in_r[t].append(r)


        # through head_cache and tail_cache calculate (r,t) similarity
        propability_in = np.zeros((self.n_ent, self.n_ent), dtype=float)

        propability_out = np.zeros((self.n_ent, self.n_ent), dtype=float)

        count11 = 0
        count22 = 0
        if os.path.exists(self.inPath + '/simi_head.npz'):
            propability_in = scipy.sparse.load_npz(self.inPath + '/simi_tail.npz')
            propability_in = sparse.csr_matrix(propability_in).toarray()
            propability_out = scipy.sparse.load_npz(self.inPath + '/simi_head.npz')
            propability_out = sparse.csr_matrix(propability_out).toarray()
            # propability_in = (propability_in + propability_out).toarray()
        else:
            row, col = propability_in.nonzero()
            propability_in_scipy = sparse.csr_matrix((propability_in[propability_in.nonzero()], (row, col)),
                                                     shape=propability_in.shape)
            propability_in = propability_in_scipy.tolil()
            row, col = propability_out.nonzero()
            propability_out_scipy = sparse.csr_matrix((propability_out[propability_out.nonzero()], (row, col)),
                                                      shape=propability_out.shape)
            propability_out = propability_out_scipy.tolil()
            for e1_idx in range(self.n_ent):
                print("the entity now is: " + str(e1_idx) + ' in ' + str(self.n_ent))
                for dist in range(self.n_ent - e1_idx - 1):
                    both_r = set(out_r[e1_idx]).intersection(out_r[e1_idx + dist + 1])
                    count1 = 0
                    for r in both_r:
                        if (e1_idx, r) in head_r and (e1_idx + dist + 1, r) in head_r:
                            both = set(head_r[(e1_idx, r)]).intersection(head_r[(e1_idx + dist + 1, r)])
                            propability_out[e1_idx, e1_idx + dist + 1] = propability_out[e1_idx, e1_idx + dist + 1] + len(both)
                            propability_out[e1_idx + dist + 1, e1_idx] = propability_out[e1_idx + dist + 1, e1_idx] + len(both)
                            if len(both) == len(head_r[(e1_idx, r)])  and len(both) == len(head_r[(e1_idx + dist + 1, r)]):
                                count1 += 1
                    ## all relation are the same
                    if len(both_r) != 0 and count1 == len(both_r) and len(both_r) == len(out_r[e1_idx]) and len(both_r) == len(out_r[e1_idx + dist + 1]):
                        propability_out[e1_idx, e1_idx + dist + 1] = 0
                        propability_out[e1_idx + dist + 1, e1_idx] = 0
                        count11 += 1

                    both_r = set(in_r[e1_idx]).intersection(in_r[e1_idx + dist + 1])
                    count2 = 0
                    for r in both_r:
                        if (e1_idx, r) in tail_r and (e1_idx + dist + 1, r) in tail_r:
                            both = set(tail_r[(e1_idx, r)]).intersection(tail_r[(e1_idx + dist + 1, r)])
                            propability_in[e1_idx, e1_idx + dist + 1] = propability_in[e1_idx, e1_idx + dist + 1] + len(both)
                            propability_in[e1_idx + dist + 1, e1_idx] = propability_in[e1_idx + dist + 1, e1_idx] + len(both)
                            if len(both) == len(tail_r[(e1_idx, r)]) and len(both) == len(tail_r[(e1_idx + dist + 1, r)]):
                                count2 += 1
                    ## all relation are the same
                    if len(both_r) != 0 and count2 == len(both_r) and len(both_r) == len(in_r[e1_idx]) and len(both_r) == len(
                            in_r[e1_idx + dist + 1]):
                        propability_in[e1_idx, e1_idx + dist + 1] = 0
                        propability_in[e1_idx + dist + 1, e1_idx] = 0
                        count22 += 1
            # row, col = propability_in.nonzero()
            # propability_in_scipy = sparse.csr_matrix((propability_in[propability_in.nonzero()], (row, col)),
            #                                    shape=propability_in.shape)
            scipy.sparse.save_npz(self.inPath + '/propability_in.npz', propability_in.tocsr())

            # row, col = propability_out.nonzero()
            # propability_out_scipy = sparse.csr_matrix((propability_out[propability_out.nonzero()], (row, col)),
            #                                    shape=propability_out.shape)
            scipy.sparse.save_npz(self.inPath + '/propability_out.npz', propability_out.tocsr())
            propability_in = propability_in.tolil()
            propability_out = propability_out.tolil()
            # propability_in = (propability_in + propability_out).toarray()

        print('count1=' + str(count11) + 'count2=' + str(count22))

        head_topk, head_topk_idx = self.topk_(propability_out, args.topk, axis=1)
        tail_topk, tail_topk_idx = self.topk_(propability_in, args.topk, axis=1)

        propability_out.fill(0)
        propability_in.fill(0)

        propability_out[np.repeat(np.arange(propability_out.shape[0]), args.topk).reshape(
            head_topk_idx.shape), head_topk_idx] = head_topk
        propability_in[np.repeat(np.arange(propability_out.shape[0]), args.topk).reshape(
            head_topk_idx.shape), tail_topk_idx] = tail_topk

        row, col = propability_in.nonzero()
        propability_in_scipy = sparse.csr_matrix((propability_in[row,col], (row, col)),
                                                 shape=propability_in.shape)
        scipy.sparse.save_npz(self.inPath + '/propability_in' + str(args.topk) + 'sep.npz', propability_in_scipy)

        row, col = propability_out.nonzero()
        propability_out_scipy = sparse.csr_matrix((propability_out[row,col], (row, col)),
                                                 shape=propability_out.shape)
        scipy.sparse.save_npz(self.inPath + '/propability_out' + str(args.topk) + 'sep.npz', propability_out_scipy)

        head_cache = np.random.randint(low=0, high=self.n_ent, size=(self.n_ent, self.n_sample))
        tail_cache = np.random.randint(low=0, high=self.n_ent, size=(self.n_ent, self.n_sample))
        print('head/tail_idx: head/tail_cache', len(head_idx), len(tail_idx), head_cache.shape, tail_cache.shape,
              len(head_pos), len(tail_pos))
        return propability_in,propability_out, head_idx, tail_idx, head_cache, tail_cache, head_pos, tail_pos

    # def get_graph_relation_add_node_topk(self,args):
    #     head_r = {}
    #     tail_r = {}
    #     out_r =  defaultdict(list)
    #     in_r =  defaultdict(list)
    #     r_head = defaultdict()
    #     r_tail = defaultdict()
    #     head_cache = {}
    #     tail_cache = {}
    #     head_pos = []
    #     tail_pos = []
    #     head_idx = []
    #     tail_idx = []
    #
    #     for h, t, r in zip(self.train_head, self.train_tail, self.train_rela):
    #         if not (h, r) in head_r:
    #             head_r[(h, r)] = []
    #             # get the size of (t, r) with a r
    #             if not r in r_head:
    #                 r_head[r] = 0
    #             r_head[r] = r_head[r] + 1
    #         if not (t, r) in tail_r:
    #             tail_r[(t, r)] = []
    #             if not r in r_tail:
    #                 r_tail[r] = 0
    #             r_tail[r] = r_tail[r] + 1
    #
    #
    #
    #         head_r[(h, r)].append(t)
    #         tail_r[(t, r)].append(h)
    #
    #
    #         if r not in out_r[h]:
    #             out_r[h].append(r)
    #         if r not in in_r[t]:
    #             in_r[t].append(r)
    #
    #
    #     # through head_cache and tail_cache calculate (r,t) similarity
    #     propability_in = np.zeros((self.n_ent, self.n_ent), dtype=float)
    #
    #     propability_out = np.zeros((self.n_ent, self.n_ent), dtype=float)
    #
    #     count11 = 0
    #     count22 = 0
    #     if os.path.exists(self.inPath + '/propability_in.npz'):
    #         # propability_in = np.load(self.inPath + '/propability_in.npy')
    #         # propability_out = np.load(self.inPath + '/propability_out.npy')
    #         propability_in = scipy.sparse.load_npz(self.inPath + '/propability_in.npz')
    #         propability_in = sparse.csr_matrix(propability_in).toarray()
    #         tail_topk, tail_topk_idx = self.topk_(propability_in, args.topk, axis=1)
    #         propability_in_idx = torch.from_numpy(tail_topk_idx).type(torch.LongTensor).cuda()
    #         propability_in_value = torch.from_numpy(tail_topk).type(torch.LongTensor).cuda()
    #         # _, t_new = torch.topk(propability_in, args.topk, dim=-1)
    #         # t_idx = torch.arange(0, self.n_ent).type(torch.LongTensor).unsqueeze(1).expand(-1, args.topk)
    #         # propability_in = propability_in[t_idx, t_new]
    #
    #
    #         propability_out = scipy.sparse.load_npz(self.inPath + '/propability_out.npz')
    #         propability_out = sparse.csr_matrix(propability_out).toarray()
    #         head_topk, head_topk_idx = self.topk_(propability_out, args.topk, axis=1)
    #         propability_out_idx = torch.from_numpy(head_topk_idx).type(torch.LongTensor).cuda()
    #         propability_out_value = torch.from_numpy(head_topk).type(torch.LongTensor).cuda()
    #     else:
    #         for e1_idx in range(self.n_ent):
    #             for dist in range(self.n_ent - e1_idx - 1):
    #                 both_r = set(out_r[e1_idx]).intersection(out_r[e1_idx + dist + 1])
    #                 count1 = 0
    #                 for r in both_r:
    #                     if (e1_idx, r) in head_r and (e1_idx + dist + 1, r) in head_r:
    #                         both = set(head_r[(e1_idx, r)]).intersection(head_r[(e1_idx + dist + 1, r)])
    #                         propability_out[e1_idx, e1_idx + dist + 1] = propability_out[e1_idx, e1_idx + dist + 1] + len(both)
    #                         propability_out[e1_idx + dist + 1, e1_idx] = propability_out[e1_idx + dist + 1, e1_idx] + len(both)
    #                         if len(both) == len(head_r[(e1_idx, r)])  and len(both) == len(head_r[(e1_idx + dist + 1, r)]):
    #                             count1 += 1
    #                 ## all relation are the same
    #                 if len(both_r) != 0 and count1 == len(both_r) and len(both_r) == len(out_r[e1_idx]) and len(both_r) == len(out_r[e1_idx + dist + 1]):
    #                     propability_out[e1_idx, e1_idx + dist + 1] = 0
    #                     propability_out[e1_idx + dist + 1, e1_idx] = 0
    #                     count11 += 1
    #
    #                 both_r = set(in_r[e1_idx]).intersection(in_r[e1_idx + dist + 1])
    #                 count2 = 0
    #                 for r in both_r:
    #                     if (e1_idx, r) in tail_r and (e1_idx + dist + 1, r) in tail_r:
    #                         both = set(tail_r[(e1_idx, r)]).intersection(tail_r[(e1_idx + dist + 1, r)])
    #                         propability_in[e1_idx, e1_idx + dist + 1] = propability_in[e1_idx, e1_idx + dist + 1] + len(both)
    #                         propability_in[e1_idx + dist + 1, e1_idx] = propability_in[e1_idx + dist + 1, e1_idx] + len(both)
    #                         if len(both) == len(tail_r[(e1_idx, r)]) and len(both) == len(tail_r[(e1_idx + dist + 1, r)]):
    #                             count2 += 1
    #                 ## all relation are the same
    #                 if len(both_r) != 0 and count2 == len(both_r) and len(both_r) == len(in_r[e1_idx]) and len(both_r) == len(
    #                         in_r[e1_idx + dist + 1]):
    #                     propability_in[e1_idx, e1_idx + dist + 1] = 0
    #                     propability_in[e1_idx + dist + 1, e1_idx] = 0
    #                     count22 += 1
    #         row, col = propability_in.nonzero()
    #         propability_in_scipy = sparse.csr_matrix((propability_in[propability_in.nonzero()], (row, col)),
    #                                            shape=propability_in.shape)
    #         scipy.sparse.save_npz(self.inPath + '/propability_in.npz', propability_in_scipy)
    #
    #         row, col = propability_out.nonzero()
    #         propability_out_scipy = sparse.csr_matrix((propability_out[propability_out.nonzero()], (row, col)),
    #                                            shape=propability_out.shape)
    #         scipy.sparse.save_npz(self.inPath + '/propability_out.npz', propability_out_scipy)
    #
    #         # np.save(self.inPath + '/propability_in', propability_in)
    #         # np.save(self.inPath + '/propability_out', propability_out)
    #     print('count1=' + str(count11) + 'count2=' + str(count22))
    #
    #     #propability_in[propability_in.nonzero()] = 1
    #     #propability_out[propability_out.nonzero()] = 1
    #
    #
    #
    #
    #     # inss = propability_in.copy()
    #     # outss = propability_out.copy()
    #     # propability_out.fill(0)
    #     # propability_in.fill(0)
    #
    #     #propability_out[np.repeat(np.arange(propability_out.shape[0]), args.topk).reshape(head_topk_idx.shape) ,head_topk_idx] = head_topk
    #     #propability_in[np.repeat(np.arange(propability_out.shape[0]), args.topk).reshape(head_topk_idx.shape), tail_topk_idx] = tail_topk
    #
    #
    #
    #
    #     # if (inss == propability_in).all():
    #     #     print("in same")
    #     # if (outss == propability_out).all():
    #     #     print("out same")
    #     # print(str((propability_in-inss).nonzero()))
    #     # print(str((propability_out - outss).nonzero()))
    #
    #
    #     head_cache = np.random.randint(low=0, high=self.n_ent, size=(self.n_ent, self.n_sample))
    #     tail_cache = np.random.randint(low=0, high=self.n_ent, size=(self.n_ent, self.n_sample))
    #     print('head/tail_idx: head/tail_cache', len(head_idx), len(tail_idx), head_cache.shape, tail_cache.shape,
    #           len(head_pos), len(tail_pos))
    #     return propability_in_idx,propability_out_idx, propability_in_value,propability_out_value, head_idx, tail_idx, head_cache, tail_cache, head_pos, tail_pos

    def get_graph_relation_add_node_topk(self,args):
        head_r = {}
        tail_r = {}
        out_r =  defaultdict(list)
        in_r =  defaultdict(list)
        r_head = defaultdict()
        r_tail = defaultdict()
        head_cache = {}
        tail_cache = {}
        head_pos = []
        tail_pos = []
        head_idx = []
        tail_idx = []

        for h, t, r in zip(self.train_head, self.train_tail, self.train_rela):
            if not (h, r) in head_r:
                head_r[(h, r)] = []
                # get the size of (t, r) with a r
                if not r in r_head:
                    r_head[r] = 0
                r_head[r] = r_head[r] + 1
            if not (t, r) in tail_r:
                tail_r[(t, r)] = []
                if not r in r_tail:
                    r_tail[r] = 0
                r_tail[r] = r_tail[r] + 1



            head_r[(h, r)].append(t)
            tail_r[(t, r)].append(h)


            if r not in out_r[h]:
                out_r[h].append(r)
            if r not in in_r[t]:
                in_r[t].append(r)


        # through head_cache and tail_cache calculate (r,t) similarity
        propability_in = np.zeros((self.n_ent, self.n_ent), dtype=float)

        propability_out = np.zeros((self.n_ent, self.n_ent), dtype=float)

        count11 = 0
        count22 = 0
        if os.path.exists(self.inPath + '/propability_in.npz'):
            propability_in = scipy.sparse.load_npz(self.inPath + '/propability_in.npz')
            propability_in = sparse.csr_matrix(propability_in).toarray()
            propability_out = scipy.sparse.load_npz(self.inPath + '/propability_out.npz')
            propability_out = sparse.csr_matrix(propability_out).toarray()

            propability_in = propability_in + propability_out

        else:
            for e1_idx in range(self.n_ent):
                for dist in range(self.n_ent - e1_idx - 1):
                    both_r = set(out_r[e1_idx]).intersection(out_r[e1_idx + dist + 1])
                    count1 = 0
                    for r in both_r:
                        if (e1_idx, r) in head_r and (e1_idx + dist + 1, r) in head_r:
                            both = set(head_r[(e1_idx, r)]).intersection(head_r[(e1_idx + dist + 1, r)])
                            propability_out[e1_idx, e1_idx + dist + 1] = propability_out[e1_idx, e1_idx + dist + 1] + len(both)
                            propability_out[e1_idx + dist + 1, e1_idx] = propability_out[e1_idx + dist + 1, e1_idx] + len(both)
                            if len(both) == len(head_r[(e1_idx, r)])  and len(both) == len(head_r[(e1_idx + dist + 1, r)]):
                                count1 += 1
                    ## all relation are the same
                    if len(both_r) != 0 and count1 == len(both_r) and len(both_r) == len(out_r[e1_idx]) and len(both_r) == len(out_r[e1_idx + dist + 1]):
                        propability_out[e1_idx, e1_idx + dist + 1] = 0
                        propability_out[e1_idx + dist + 1, e1_idx] = 0
                        count11 += 1

                    both_r = set(in_r[e1_idx]).intersection(in_r[e1_idx + dist + 1])
                    count2 = 0
                    for r in both_r:
                        if (e1_idx, r) in tail_r and (e1_idx + dist + 1, r) in tail_r:
                            both = set(tail_r[(e1_idx, r)]).intersection(tail_r[(e1_idx + dist + 1, r)])
                            propability_in[e1_idx, e1_idx + dist + 1] = propability_in[e1_idx, e1_idx + dist + 1] + len(both)
                            propability_in[e1_idx + dist + 1, e1_idx] = propability_in[e1_idx + dist + 1, e1_idx] + len(both)
                            if len(both) == len(tail_r[(e1_idx, r)]) and len(both) == len(tail_r[(e1_idx + dist + 1, r)]):
                                count2 += 1
                    ## all relation are the same
                    if len(both_r) != 0 and count2 == len(both_r) and len(both_r) == len(in_r[e1_idx]) and len(both_r) == len(
                            in_r[e1_idx + dist + 1]):
                        propability_in[e1_idx, e1_idx + dist + 1] = 0
                        propability_in[e1_idx + dist + 1, e1_idx] = 0
                        count22 += 1
            row, col = propability_in.nonzero()
            propability_in_scipy = sparse.csr_matrix((propability_in[propability_in.nonzero()], (row, col)),
                                               shape=propability_in.shape)
            scipy.sparse.save_npz(self.inPath + '/propability_in.npz', propability_in_scipy)

            row, col = propability_out.nonzero()
            propability_out_scipy = sparse.csr_matrix((propability_out[propability_out.nonzero()], (row, col)),
                                               shape=propability_out.shape)
            scipy.sparse.save_npz(self.inPath + '/propability_out.npz', propability_out_scipy)

            # np.save(self.inPath + '/propability_in', propability_in)
            # np.save(self.inPath + '/propability_out', propability_out)
        print('count1=' + str(count11) + 'count2=' + str(count22))



        head_topk, head_topk_idx = self.topk_(propability_out, args.topk, axis=1)
        tail_topk, tail_topk_idx = self.topk_(propability_in, args.topk, axis=1)

        propability_out.fill(0)
        propability_in.fill(0)

        propability_out[np.repeat(np.arange(propability_out.shape[0]), args.topk).reshape(head_topk_idx.shape) ,head_topk_idx] = head_topk
        propability_in[np.repeat(np.arange(propability_out.shape[0]), args.topk).reshape(head_topk_idx.shape), tail_topk_idx] = tail_topk

        head_cache = np.random.randint(low=0, high=self.n_ent, size=(self.n_ent, self.n_sample))
        tail_cache = np.random.randint(low=0, high=self.n_ent, size=(self.n_ent, self.n_sample))
        print('head/tail_idx: head/tail_cache', len(head_idx), len(tail_idx), head_cache.shape, tail_cache.shape,
              len(head_pos), len(tail_pos))
        return propability_in,propability_out, head_idx, tail_idx, head_cache, tail_cache, head_pos, tail_pos

    def get_graph_relation_add_node_set(self, args):
        head_r = defaultdict(set)
        tail_r = defaultdict(set)
        out_r = defaultdict(set)
        in_r = defaultdict(set)
        head_conf = defaultdict(set)
        tail_conf = defaultdict(set)

        for h, t, r in zip(self.train_head, self.train_tail, self.train_rela):
            head_r[(h, r)].add(t)
            tail_r[(t, r)].add(h)

            head_conf[h].add((r, t))
            tail_conf[t].add((r, h))

            if r not in out_r[h]:
                out_r[h].add(r)
            if r not in in_r[t]:
                in_r[t].add(r)

        #############IF EXISTS, READ THE ENTITY SIMILARITY FILES#############
        if os.path.exists(self.inPath + '/simi_head.npz'):
            print("Load Similar Entities (Local).")
            simi_head = scipy.sparse.load_npz(self.inPath + '/simi_head.npz')
            simi_head = sparse.csr_matrix(simi_head).tolil()
            simi_tail = scipy.sparse.load_npz(self.inPath + '/simi_tail.npz')
            simi_tail = sparse.csr_matrix(simi_tail).tolil()
        ############ELSE GENERATE SIMILAR ENTITIES FIRST#####################
        else:
            print("Fail to Load Similar Entities (Local) and Begin to Generate.")
            simi_head = sparse.csr_matrix((self.n_ent, self.n_ent))
            simi_head = simi_head.tolil()
            simi_tail = sparse.csr_matrix((self.n_ent, self.n_ent))
            simi_tail = simi_tail.tolil()
            for e1_idx in range(self.n_ent):
                print("the entity now is: " + str(e1_idx) + ' in ' + str(self.n_ent))
                for dist in range(self.n_ent - e1_idx - 1):
                    head_score = head_conf[e1_idx].intersection(head_conf[e1_idx + dist + 1])
                    tail_score = tail_conf[e1_idx].intersection(tail_conf[e1_idx + dist + 1])
                    if len(head_score) != 0 and not (
                            len(head_score) == len(head_conf[e1_idx]) and len(head_score) == len(
                            head_conf[e1_idx + dist + 1])):
                        simi_head[e1_idx, e1_idx + dist + 1] = len(head_score)
                        simi_head[e1_idx + dist + 1, e1_idx] = len(head_score)
                    if len(tail_score) != 0 and not (
                            len(tail_score) == len(tail_conf[e1_idx]) and len(tail_score) == len(
                            tail_conf[e1_idx + dist + 1])):
                        simi_tail[e1_idx, e1_idx + dist + 1] = len(tail_score)
                        simi_tail[e1_idx + dist + 1, e1_idx] = len(tail_score)

            scipy.sparse.save_npz(self.inPath + '/simi_tail.npz', simi_tail.tocsr())
            scipy.sparse.save_npz(self.inPath + '/simi_head.npz', simi_head.tocsr())

        ################get top k similar entities###############
        if args.topk != 0:
            ent = 0
            for data, row in zip(simi_head.data, simi_head.rows):
                if args.topk < len(row):
                    d, r = zip(*sorted(zip(data, row), reverse=True)[:args.topk])
                    simi_head.data[ent] = list(d)
                    simi_head.rows[ent] = list(r)
                ent += 1
            ent = 0
            for data, row in zip(simi_tail.data, simi_tail.rows):
                if args.topk < len(row):
                    d, r = zip(*sorted(zip(data, row), reverse=True)[:args.topk])
                    simi_tail.data[ent] = list(d)
                    simi_tail.rows[ent] = list(r)
                ent += 1
        return simi_tail, simi_head
    def get_graph_relation_add_node2(self, args):
        head_r = {}
        tail_r = {}
        out_r = defaultdict(list)
        in_r = defaultdict(list)
        r_head = defaultdict()
        r_tail = defaultdict()
        head_cache = {}
        tail_cache = {}
        head_pos = []
        tail_pos = []
        head_idx = []
        tail_idx = []

        for h, t, r in zip(self.train_head, self.train_tail, self.train_rela):
            if not (h, r) in head_r:
                head_r[(h, r)] = []
                # get the size of (t, r) with a r
                if not r in r_head:
                    r_head[r] = 0
                r_head[r] = r_head[r] + 1
            if not (t, r) in tail_r:
                tail_r[(t, r)] = []
                if not r in r_tail:
                    r_tail[r] = 0
                r_tail[r] = r_tail[r] + 1

            head_r[(h, r)].append(t)
            tail_r[(t, r)].append(h)

            if r not in out_r[h]:
                out_r[h].append(r)
            if r not in in_r[t]:
                in_r[t].append(r)

        # through head_cache and tail_cache calculate (r,t) similarity
        # propability_in = np.zeros((self.n_ent, self.n_ent), dtype=float)

        # propability_out = np.zeros((self.n_ent, self.n_ent), dtype=float)

        count11 = 0
        count22 = 0
        if os.path.exists(self.inPath + '/propability_in.npz'):
            propability_in = scipy.sparse.load_npz(self.inPath + '/propability_in.npz')
            propability_in = sparse.csr_matrix(propability_in)
            propability_out = scipy.sparse.load_npz(self.inPath + '/propability_out.npz')
            propability_out = sparse.csr_matrix(propability_out)
            # propability_in = np.load(self.inPath + '/propability_in.npy')
            # propability_out = np.load(self.inPath + '/propability_out.npy')
            # row, col = propability_in.nonzero()
            # c_in = sparse.coo_matrix((propability_in[propability_in.nonzero()], (row, col)), shape=propability_in.shape)
            # row1, col1 = propability_out.nonzero()
            # c_out = sparse.coo_matrix((propability_out[propability_out.nonzero()], (row1, col1)), shape=propability_out.shape)
            # scipy.sparse.save_npz(self.inPath + '/propability_in.npz', c_in)
            # scipy.sparse.save_npz(self.inPath + '/propability_out.npz', c_out)


        else:
            propability_in = sparse.lil_matrix((self.n_ent, self.n_ent), dtype=np.float32)
            propability_out = sparse.lil_matrix((self.n_ent, self.n_ent), dtype=np.float32)
            for e1_idx in range(self.n_ent):
                if (e1_idx % 10 == 0):
                    with open(args.perf_file, 'a') as f:
                        f.write('entityID:' + str(e1_idx))
                for dist in range(self.n_ent - e1_idx - 1):
                    both_r = set(out_r[e1_idx]).intersection(out_r[e1_idx + dist + 1])
                    count1 = 0
                    for r in both_r:
                        if (e1_idx, r) in head_r and (e1_idx + dist + 1, r) in head_r:
                            both = set(head_r[(e1_idx, r)]).intersection(head_r[(e1_idx + dist + 1, r)])
                            propability_out[e1_idx, e1_idx + dist + 1] = propability_out[
                                                                             e1_idx, e1_idx + dist + 1] + len(both)
                            propability_out[e1_idx + dist + 1, e1_idx] = propability_out[
                                                                             e1_idx + dist + 1, e1_idx] + len(both)
                            if len(both) == len(head_r[(e1_idx, r)]) and len(both) == len(
                                    head_r[(e1_idx + dist + 1, r)]):
                                count1 += 1
                    ## all relation are the same
                    if len(both_r) != 0 and count1 == len(both_r) and len(both_r) == len(out_r[e1_idx]) and len(
                            both_r) == len(out_r[e1_idx + dist + 1]):
                        propability_out[e1_idx, e1_idx + dist + 1] = 0
                        propability_out[e1_idx + dist + 1, e1_idx] = 0
                        count11 += 1

                    both_r = set(in_r[e1_idx]).intersection(in_r[e1_idx + dist + 1])
                    count2 = 0
                    for r in both_r:
                        if (e1_idx, r) in tail_r and (e1_idx + dist + 1, r) in tail_r:
                            both = set(tail_r[(e1_idx, r)]).intersection(tail_r[(e1_idx + dist + 1, r)])
                            propability_in[e1_idx, e1_idx + dist + 1] = propability_in[e1_idx, e1_idx + dist + 1] + len(
                                both)
                            propability_in[e1_idx + dist + 1, e1_idx] = propability_in[e1_idx + dist + 1, e1_idx] + len(
                                both)
                            if len(both) == len(tail_r[(e1_idx, r)]) and len(both) == len(
                                    tail_r[(e1_idx + dist + 1, r)]):
                                count2 += 1
                    ## all relation are the same
                    if len(both_r) != 0 and count2 == len(both_r) and len(both_r) == len(in_r[e1_idx]) and len(
                            both_r) == len(
                            in_r[e1_idx + dist + 1]):
                        propability_in[e1_idx, e1_idx + dist + 1] = 0
                        propability_in[e1_idx + dist + 1, e1_idx] = 0
                        count22 += 1
            row, col = propability_in.nonzero()
            propability_in = sparse.csr_matrix((propability_in.toarray()[propability_in.nonzero()], (row, col)),
                                               shape=propability_in.shape)
            row, col = propability_out.nonzero()
            propability_out = sparse.csr_matrix((propability_out.toarray()[propability_out.nonzero()], (row, col)),
                                                shape=propability_out.shape)
            scipy.sparse.save_npz(self.inPath + '/propability_in.npz', propability_in)
            scipy.sparse.save_npz(self.inPath + '/propability_out.npz', propability_out)
            # np.save(self.inPath + '/propability_in', propability_in)
            # np.save(self.inPath + '/propability_out', propability_out)
        print('count1=' + str(count11) + 'count2=' + str(count22))

        # propability_in[propability_in.nonzero()] = 1
        # propability_out[propability_out.nonzero()] = 1

        # propability_in = propability_in + 0.000001
        # propability_out = propability_out + 0.000001

        # propability_in.nonzero()

        head_cache = np.random.randint(low=0, high=self.n_ent, size=(self.n_ent, self.n_sample))
        tail_cache = np.random.randint(low=0, high=self.n_ent, size=(self.n_ent, self.n_sample))
        print('head/tail_idx: head/tail_cache', len(head_idx), len(tail_idx), head_cache.shape, tail_cache.shape,
              len(head_pos), len(tail_pos))
        return propability_in, propability_out, head_idx, tail_idx, head_cache, tail_cache, head_pos, tail_pos

    def getnodefeaturedegree(self):
        head_cache = {}
        tail_cache = {}
        head_pos = []
        tail_pos = []
        head_idx = []
        tail_idx = []
        count_h = 0
        count_t = 0
        for h, t, r in zip(self.train_head, self.train_tail, self.train_rela):
            if not h in head_cache:
                head_cache[h] = 0
            head_cache[h] += 1

            if not t in tail_cache:
                tail_cache[t] = 0
            tail_cache[t] += 1

        file = open(self.inPath + '/' + 'nodefeaturedegree.txt', 'a')

        for index, value in head_cache.items():
            file.write(str(value) + '\t')

        for index, value in tail_cache.items():
            file.write(str(value) + '\t')
        file.close()

    def getrelationfeature(self, head_cache,tail_cache):
        head_feature = {}
        tail_feature = {}
        for key, value in head_cache.items():
            if key[1] not in head_feature:
                head_feature[key[1]] = []
                head_feature[key[1]].append(key[0])
            else:
                if key[0] not in head_feature[key[1]]:
                    head_feature[key[1]].append(key[0])
        for key, value in tail_cache.items():
            if key[1] not in tail_feature:
                tail_feature[key[1]] = []
                tail_feature[key[1]].append(key[0])
            else:
                if key[0] not in tail_feature[key[1]]:
                    tail_feature[key[1]].append(key[0])
        file = open(self.inPath + '/' + 'relationfeature.txt', 'a')

        for index, value in head_feature.items():
            file.write(str(len(value)) + '\t')

        for index, value in tail_feature.items():
            file.write(str(len(value)) + '\t')
        file.close()



    def settemperature(self,head_cache, tail_cache, head_pos, tail_pos):
        head_temp = []
        tail_temp = []
        self.head_temp = []
        self.tail_temp = []
        for key, value in head_cache.items():
            ##(t, r)##
            head_temp.append(len(head_pos[value]))
        for key, value in tail_cache.items():
            ##(h, r)##
            tail_temp.append(len(tail_pos[value]))
        self.head_temp = head_temp
        self.tail_temp = tail_temp
        file = open(self.inPath + '/' + 'featuredis.txt', 'a')
        # for i in distribution:
        #     file.write(str(i) + '\t')
        # file.close()
        for index, value in enumerate(head_temp):
            file.write(str(value) + '\t')

        for index, value in enumerate(tail_temp):
            file.write(str(value) + '\t')
        file.close()
        self.tail_temp = np.array(self.tail_temp)
        self.head_temp = np.array(self.head_temp)


    def gethrdistributionandsimilarentity(self,head_cache, tail_cache, head_pos, tail_pos):

        if os.path.exists(self.inPath + '/simi_tail.npz'):
            simi_tail = scipy.sparse.load_npz(self.inPath + '/simi_tail.npz')
            simi_tail = sparse.csr_matrix(simi_tail).toarray()
            simi_head = scipy.sparse.load_npz(self.inPath + '/simi_head.npz')
            simi_head = sparse.csr_matrix(simi_head).toarray()
        head_temp = []
        tail_temp = []
        head_simi = []
        tail_simi = []
        self.head_temp = []
        self.tail_temp = []
        for key, value in head_cache.items():
            ##(t, r)##
            head_temp.append(len(head_pos[value]))
            head_simi.append(simi_head[np.array(head_pos[value])].nonzero()[0].shape[0]/len(head_pos[value]))
        for key, value in tail_cache.items():
            ##(h, r)##
            tail_temp.append(len(tail_pos[value]))
            tail_simi.append(simi_tail[np.array(tail_pos[value])].nonzero()[0].shape[0]/ len(tail_pos[value]))
        self.head_temp = head_temp
        self.tail_temp = tail_temp
        file = open(self.inPath + '/' + 'featuredis.txt', 'a')
        # for i in distribution:
        #     file.write(str(i) + '\t')
        # file.close()
        for index, value in enumerate(head_temp):
            file.write(str(value) + '\t')

        for index, value in enumerate(tail_temp):
            file.write(str(value) + '\t')
        file.close()

        file = open(self.inPath + '/' + 'similarentityaccordinghr.txt', 'a')
        # for i in distribution:
        #     file.write(str(i) + '\t')
        # file.close()
        for index, value in enumerate(head_simi):
            file.write(str(value) + '\t')

        for index, value in enumerate(tail_simi):
            file.write(str(value) + '\t')
        file.close()
        self.tail_temp = np.array(self.tail_temp)
        self.head_temp = np.array(self.head_temp)



    def get_graph_normalization(self,args):
        head_r = {}
        tail_r = {}
        out_r =  defaultdict(list)
        in_r =  defaultdict(list)
        r_head = defaultdict()
        r_tail = defaultdict()
        head_cache = {}
        tail_cache = {}
        head_pos = []
        tail_pos = []
        head_idx = []
        tail_idx = []
        for h, t, r in zip(self.train_head, self.train_tail, self.train_rela):

            if not (h, r) in head_r:
                head_r[(h, r)] = []
                # get the size of (t, r) with a r
                if not r in r_head:
                    r_head[r] = 0
                r_head[r] = r_head[r] + 1
            if not (t, r) in tail_r:
                tail_r[(t, r)] = []
                if not r in r_tail:
                    r_tail[r] = 0
                r_tail[r] = r_tail[r] + 1



            head_r[(h, r)].append(t)
            tail_r[(t, r)].append(h)


            if r not in out_r[h]:
                out_r[h].append(r)
            if r not in in_r[t]:
                in_r[t].append(r)


        # through head_cache and tail_cache calculate (r,t) similarity
        propability_in = np.zeros((self.n_ent, self.n_ent), dtype=np.float32)

        propability_out = np.zeros((self.n_ent, self.n_ent), dtype=np.float32)


        if os.path.exists(self.inPath + '/propability_in.npy'):
            propability_in = np.load(self.inPath + '/propability_in.npy')
            propability_out = np.load(self.inPath + '/propability_out.npy')
        else:
            for e1_idx in range(self.n_ent):
                for dist in range(self.n_ent - e1_idx - 1):
                    for r in set(out_r[e1_idx]).intersection(out_r[e1_idx + dist + 1]):
                        if (e1_idx, r) in head_r and (e1_idx + dist + 1, r) in head_r:
                            both = set(head_r[(e1_idx, r)]).intersection(head_r[(e1_idx + dist + 1, r)])
                            propability_out[e1_idx, e1_idx + dist + 1] = propability_out[e1_idx, e1_idx + dist + 1] + len(both)
                            propability_out[e1_idx + dist + 1, e1_idx] = propability_out[e1_idx + dist + 1, e1_idx] + len(both)
                    for r in set(in_r[e1_idx]).intersection(in_r[e1_idx + dist + 1]):
                        if (e1_idx, r) in tail_r and (e1_idx + dist + 1, r) in tail_r:
                            both = set(tail_r[(e1_idx, r)]).intersection(tail_r[(e1_idx, r)])
                            propability_in[e1_idx, e1_idx + dist + 1] = propability_in[e1_idx, e1_idx + dist + 1] + len(both)
                            propability_in[e1_idx + dist + 1, e1_idx] = propability_in[e1_idx + dist + 1, e1_idx] + len(both)

            np.save(self.inPath + '/propability_in', propability_in)
            np.save(self.inPath + '/propability_out', propability_out)

        # head_idx = np.array(head_idx, dtype=int)
        # tail_idx = np.array(tail_idx, dtype=int)

        propability_in = propability_in
        propability_out = propability_out

        # nomalization
        # def normalization(data):
        #     _range = np.max(data) - np.min(data)
        #     return (data - np.min(data)) / _range
        #
        # def standardization(data):
        #     mu = np.mean(data, axis=0)
        #     sigma = np.std(data, axis=0)
        #     return (data - mu) / sigma

        propability_in = normalize(propability_in, axis=1, norm='max')
        propability_out = normalize(propability_out, axis=1, norm='max')

        head_cache = np.random.randint(low=0, high=self.n_ent, size=(self.n_ent, self.n_sample))
        tail_cache = np.random.randint(low=0, high=self.n_ent, size=(self.n_ent, self.n_sample))
        print('head/tail_idx: head/tail_cache', len(head_idx), len(tail_idx), head_cache.shape, tail_cache.shape,
              len(head_pos), len(tail_pos))
        return propability_in,propability_out, head_idx, tail_idx, head_cache, tail_cache, head_pos, tail_pos


    def get_graph_get_top2000(self,args):
        head_r = {}
        tail_r = {}
        out_r =  defaultdict(list)
        in_r =  defaultdict(list)

        head_cache = {}
        tail_cache = {}
        head_pos = []
        tail_pos = []
        head_idx = []
        tail_idx = []

        for h, t, r in zip(self.train_head, self.train_tail, self.train_rela):
            # get matrix of e and r
            if not (h, r) in head_r:
                head_r[(h, r)] = []
            if not (t, r) in tail_r:
                tail_r[(t, r)] = []

            head_r[(h, r)].append(t)
            tail_r[(t, r)].append(h)


            if r not in out_r[h]:
                out_r[h].append(r)
            if r not in in_r[t]:
                in_r[t].append(r)

        # calculate r similarity


        # through head_cache and tail_cache calculate (r,t) similarity
        propability_in = np.zeros((self.n_ent, self.n_ent), dtype=float)

        propability_out = np.zeros((self.n_ent, self.n_ent), dtype=float)

        if os.path.exists(self.inPath + '/propability_in.npy'):
            propability_in = np.load(self.inPath + '/propability_in.npy')
            propability_out = np.load(self.inPath + '/propability_out.npy')
        else:
            for e1_idx in range(self.n_ent):
                for dist in range(self.n_ent - e1_idx - 1):
                    for r in set(out_r[e1_idx]).intersection(out_r[e1_idx + dist + 1]):
                        if (e1_idx, r) in head_r and (e1_idx + dist + 1, r) in head_r:
                            both = set(head_r[(e1_idx, r)]).intersection(head_r[(e1_idx + dist + 1, r)])
                            propability_out[e1_idx, e1_idx + dist + 1] = propability_out[e1_idx, e1_idx + dist + 1] + len(both)
                            propability_out[e1_idx + dist + 1, e1_idx] = propability_out[e1_idx + dist + 1, e1_idx] + len(both)
                    for r in set(in_r[e1_idx]).intersection(in_r[e1_idx + dist + 1]):
                        if (e1_idx, r) in tail_r and (e1_idx + dist + 1, r) in tail_r:
                            both = set(tail_r[(e1_idx, r)]).intersection(tail_r[(e1_idx, r)])
                            propability_in[e1_idx, e1_idx + dist + 1] = propability_in[e1_idx, e1_idx + dist + 1] + len(both)
                            propability_in[e1_idx + dist + 1, e1_idx] = propability_in[e1_idx + dist + 1, e1_idx] + len(both)

            np.save(self.inPath + '/propability_in', propability_in)
            np.save(self.inPath + '/propability_out', propability_out)

        # head_idx = np.array(head_idx, dtype=int)
        # tail_idx = np.array(tail_idx, dtype=int)

        propability_in = propability_in + 0.0001
        propability_out = propability_out + 0.0001
        # propability_in = torch.from_numpy(propability_in).cuda() + 0.0001
        # propability_out = torch.from_numpy(propability_out).cuda() + 0.0001

        topk = args.top_num
        if os.path.exists(self.inPath + '/head_cache.npy'):
            head_top2000 = np.load(self.inPath + '/head_cache.npy')
            if head_cache.shape[1] == topk:
                tail_top2000 = np.load(self.inPath + '/tail_cache.npy')
                head_top2000 = torch.from_numpy(head_top2000).cuda()
                tail_top2000 = torch.from_numpy(tail_top2000).cuda()
            else:
                head_cache = self.topk_(head_cache, topk, axis=1)
                tail_cache = self.topk_(tail_cache, topk, axis=1)
                np.save(self.inPath + '/head_cache', head_cache)
                np.save(self.inPath + '/tail_cache', tail_cache)
        else:
            head_cache = self.topk_(head_cache,topk,axis=1)
            tail_cache = self.topk_(tail_cache,topk,axis=1)
            np.save(self.inPath + '/head_cache', head_cache)
            np.save(self.inPath + '/tail_cache', tail_cache)




        # p_in = torch.from_numpy(propability_in).cuda()
        # p_out = torch.from_numpy(propability_out).cuda()
        ## average candidate
        # _, head_cache = p_out.topk(2000, dim = 1, largest=True)
        # _, tail_cache = p_in.topk(2000, dim = 1, largest= True)
        #
        # head_cache = head_cache.cpu().numpy()
        # tail_cache = tail_cache.cpu().numpy()
        # np.save(self.inPath + '/head_cache', head_cache)
        # np.save(self.inPath + '/tail_cache', tail_cache)


        head_cache = np.random.randint(low=0, high=self.n_ent, size=(self.n_ent, self.n_sample))
        tail_cache = np.random.randint(low=0, high=self.n_ent, size=(self.n_ent, self.n_sample))
        print('head/tail_idx: head/tail_cache', len(head_idx), len(tail_idx), head_cache.shape, tail_cache.shape,
              len(head_pos), len(tail_pos))
        return propability_in,propability_out, head_idx, tail_idx, head_cache, tail_cache, head_pos, tail_pos, head_top2000, tail_top2000

    def topk_(self, matrix, K, axis=1):
        if axis == 0:
            row_index = np.arange(matrix.shape[1 - axis])
            topk_index = np.argpartition(matrix, K, axis=axis)[0:K, :]
            topk_data = matrix[topk_index, row_index]
            topk_index_sort = np.argsort(-topk_data, axis=axis)
            topk_data_sort = topk_data[topk_index_sort, row_index]
            topk_index_sort = topk_index[0:K, :][topk_index_sort, row_index]
        else:
            column_index = np.arange(matrix.shape[1 - axis])[:, None]
            topk_index = np.argpartition(-matrix, K, axis=axis)[:, 0:K]
            topk_data = matrix[column_index, topk_index]
            topk_index_sort = np.argsort(-topk_data, axis=axis)
            topk_data_sort = topk_data[column_index, topk_index_sort]
            topk_index_sort = topk_index[:, 0:K][column_index, topk_index_sort]
        return topk_data_sort, topk_index_sort


    def get_graph_structure_right(self,args):
        head_r = {}
        tail_r = {}
        out_r =  defaultdict(list)
        in_r =  defaultdict(list)

        head_cache = {}
        tail_cache = {}
        head_pos = []
        tail_pos = []
        head_idx = []
        tail_idx = []

        for h, t, r in zip(self.train_head, self.train_tail, self.train_rela):
            # get matrix of e and r
            if not (h, r) in head_r:
                head_r[(h, r)] = []
            if not (t, r) in tail_r:
                tail_r[(t, r)] = []

            head_r[(h, r)].append(t)
            tail_r[(t, r)].append(h)


            if r not in out_r[h]:
                out_r[h].append(r)
            if r not in in_r[t]:
                in_r[t].append(r)

        # calculate r similarity


        # through head_cache and tail_cache calculate (r,t) similarity
        propability_in = np.zeros((self.n_ent, self.n_ent), dtype=float)

        propability_out = np.zeros((self.n_ent, self.n_ent), dtype=float)

        graph1 = np.zeros((self.n_ent + self.n_rel * 2, 100), dtype=float)
        # with open('../GraphWaveMachine-master/output' + '/FB15K237.csv') as csvfile:
        #     csv_reader_lines = csv.reader(csvfile)
        #     for one_line in csv_reader_lines:
        #         graph1[int(one_line[0])] = [float(i) for i in one_line[1:]]
        # graph1 = torch.from_numpy(graph1).type(torch.FloatTensor).cuda()

        if os.path.exists('../GraphSAGE-master/graphsage/unsup-FB15K237/graphsage_maxpool_big_0.001000' + '/val.npy'):
            # with open('../GraphSAGE-master/graphsage/graphsage_maxpool_big_0.001000' + '/val.npy') as csvfile:
            #     csv_reader_lines = csv.reader(csvfile)
            #     for one_line in csv_reader_lines:
            #         graph1[int(one_line[0])] = [float(i) for i in one_line[1:]]
            graph1 = np.load('../GraphSAGE-master/graphsage/unsup-FB15K237/graphsage_maxpool_big_0.001000' + '/val.npy')
            graph1 = torch.from_numpy(graph1).type(torch.FloatTensor).cuda()
                # graph1 = torch.from_numpy(graph1).type(torch.FloatTensor).cuda()


        head_idx = np.array(head_idx, dtype=int)
        tail_idx = np.array(tail_idx, dtype=int)
        head_cache = np.random.randint(low=0, high=self.n_ent, size=(self.n_ent, self.n_sample))
        tail_cache = np.random.randint(low=0, high=self.n_ent, size=(self.n_ent, self.n_sample))
        print('head/tail_idx: head/tail_cache', len(head_idx), len(tail_idx), head_cache.shape, tail_cache.shape,
              len(head_pos), len(tail_pos))
        return graph1,propability_in,propability_out, head_idx, tail_idx, head_cache, tail_cache, head_pos, tail_pos



    def get_graph_structure(self, args):
        # the orginal version
        head_cache = {}
        tail_cache = {}
        head_pos = []
        tail_pos = []
        head_idx = []
        tail_idx = []
        count_h = 0
        count_t = 0
        graph_out = np.zeros((self.n_ent, self.n_rel), dtype=int)
        graph_in = np.zeros((self.n_ent, self.n_rel), dtype=int)
        entity = np.zeros((self.n_ent, self.n_ent), dtype=int)

        for h, t, r in zip(self.train_head, self.train_tail, self.train_rela):
            entity[h, t] = entity[h, t] + 1
            graph_out[h, r] = graph_out[h, r] + 1
            graph_in[t, r] = graph_in[t, r] + 1
            if not (t, r) in head_cache:
                head_cache[(t, r)] = count_h
                head_pos.append([h])
                count_h += 1
            else:
                head_pos[head_cache[(t, r)]].append(h)

            if not (h, r) in tail_cache:
                tail_cache[(h, r)] = count_t
                tail_pos.append([t])
                count_t += 1
            else:
                tail_pos[tail_cache[(h, r)]].append(t)

            head_idx.append(head_cache[(t, r)])
            tail_idx.append(tail_cache[(h, r)])
        head_idx = np.array(head_idx, dtype=int)
        tail_idx = np.array(tail_idx, dtype=int)
        head_cache = np.random.randint(low=0, high=self.n_ent, size=(count_h, self.n_sample))
        tail_cache = np.random.randint(low=0, high=self.n_ent, size=(count_t, self.n_sample))

        # propability_in = np.zeros((1, 1), dtype=float)
        # propability_out = np.zeros((1, 1), dtype=float)
        propability_in = np.zeros((self.n_ent, self.n_ent), dtype=float)
        propability_out = np.zeros((self.n_ent, self.n_ent), dtype=float)
        if os.path.exists(self.inPath + '/propability_in.npy'):
            propability_in = np.load(self.inPath + '/propability_in.npy')
            propability_out = np.load(self.inPath + '/propability_out.npy')
        else:
            # calculate the probability of entities
            for e1_index in range(graph_in.shape[0]):
                for e2_index in range(e1_index + 1, graph_in.shape[0]):
                    distance_in = 1 - pdist(np.vstack([graph_in[e1_index],graph_in[e2_index]]),'cosine')
                    propability_in[e1_index, e2_index] = distance_in[0]
                    propability_in[e2_index, e1_index] = distance_in[0]

                    distance_out = 1 - pdist(np.vstack([graph_out[e1_index],graph_out[e2_index]]),'cosine')
                    propability_out[e1_index, e2_index] = distance_out[0]
                    propability_out[e2_index, e1_index] = distance_out[0]
            propability_in[np.isnan(propability_in)] = 0
            propability_out[np.isnan(propability_out)] = 0
            np.save(self.inPath + '/propability_in', propability_in)
            np.save(self.inPath + '/propability_out', propability_out)





        print('head/tail_idx: head/tail_cache', len(head_idx), len(tail_idx), head_cache.shape, tail_cache.shape,
              len(head_pos), len(tail_pos))
        return graph_in, graph_out, propability_in, propability_out, entity, head_idx, tail_idx, head_cache, tail_cache, head_pos, tail_pos

    def get_graph_structure2(self, args):
        # the orginal version
        head_cache = {}
        tail_cache = {}
        head_pos = []
        tail_pos = []
        head_idx = []
        tail_idx = []
        count_h = 0
        count_t = 0
        graph1 = np.zeros((self.n_ent + self.n_rel * 2, 100), dtype=float)
        graph = np.zeros((self.n_ent, self.n_rel*2), dtype=float)
        graph_sec = np.zeros((self.n_ent, self.n_rel * 2), dtype=float)

        entity = np.zeros((self.n_ent, self.n_ent), dtype=int)

        for h, t, r in zip(self.train_head, self.train_tail, self.train_rela):
            entity[h, t] = entity[h, t] + 1
            graph[h, r] = graph[h, r] + 1
            graph[t, r + self.n_rel] = graph[t, r + self.n_rel] + 1
            if not (t, r) in head_cache:
                head_cache[(t, r)] = count_h
                head_pos.append([h])
                count_h += 1
            else:
                head_pos[head_cache[(t, r)]].append(h)

            if not (h, r) in tail_cache:
                tail_cache[(h, r)] = count_t
                tail_pos.append([t])
                count_t += 1
            else:
                tail_pos[tail_cache[(h, r)]].append(t)

            head_idx.append(head_cache[(t, r)])
            tail_idx.append(tail_cache[(h, r)])

        for h, t, r in zip(self.train_head, self.train_tail, self.train_rela):
            graph_sec[h] = graph_sec[h] + graph[t]
            graph_sec[t] = graph_sec[t] + graph[h]

        head_idx = np.array(head_idx, dtype=int)
        tail_idx = np.array(tail_idx, dtype=int)
        head_cache = np.random.randint(low=0, high=self.n_ent, size=(self.n_ent, self.n_sample))
        tail_cache = np.random.randint(low=0, high=self.n_ent, size=(self.n_ent, self.n_sample))

        propability_in = np.zeros((1, 1), dtype=float)
        propability_out = np.zeros((1, 1), dtype=float)

        with open('../GraphWaveMachine-master/output' + '/FB15K237.csv') as csvfile:
            csv_reader_lines = csv.reader(csvfile)
            for one_line in csv_reader_lines:
                graph1[int(one_line[0])] = [float(i) for i in one_line[1:]]
        graph1 = torch.from_numpy(graph1).type(torch.FloatTensor).cuda()

        # if os.path.exists('../GraphSAGE-master/graphsage/unsup-FB15K237/n2v_big_0.001000' + '/val.npy'):
        #     # with open('../GraphSAGE-master/graphsage/graphsage_maxpool_big_0.001000' + '/val.npy') as csvfile:
        #     #     csv_reader_lines = csv.reader(csvfile)
        #     #     for one_line in csv_reader_lines:
        #     #         graph1[int(one_line[0])] = [float(i) for i in one_line[1:]]
        #     graph1 = np.load('../GraphSAGE-master/graphsage/unsup-FB15K237/n2v_big_0.001000' + '/val.npy')
        #     graph1 = torch.from_numpy(graph1).type(torch.FloatTensor).cuda()
        #         # graph1 = torch.from_numpy(graph1).type(torch.FloatTensor).cuda()

        print('head/tail_idx: head/tail_cache', len(head_idx), len(tail_idx), head_cache.shape, tail_cache.shape,
              len(head_pos), len(tail_pos))
        return graph1, propability_in, propability_out, entity, head_idx, tail_idx, head_cache, tail_cache, head_pos, tail_pos





    def get_graph_adjacent(self, args):
        # the orginal version
        head_cache = {}
        tail_cache = {}
        head_pos = []
        tail_pos = []
        head_idx = []
        tail_idx = []
        count_h = 0
        count_t = 0
        graph_out = np.zeros((self.n_ent, self.n_rel), dtype=int)
        graph_in = np.zeros((self.n_ent, self.n_rel), dtype=int)
        entity = np.zeros((self.n_ent, self.n_ent), dtype=int)

        for h, t, r in zip(self.train_head, self.train_tail, self.train_rela):
            entity[h, t] = entity[h, t] + 1
            graph_out[h, r] = graph_out[h, r] + 1
            graph_in[t, r] = graph_in[t, r] + 1
            if not (t, r) in head_cache:
                head_cache[(t, r)] = count_h
                head_pos.append([h])
                count_h += 1
            else:
                head_pos[head_cache[(t, r)]].append(h)

            if not (h, r) in tail_cache:
                tail_cache[(h, r)] = count_t
                tail_pos.append([t])
                count_t += 1
            else:
                tail_pos[tail_cache[(h, r)]].append(t)

            head_idx.append(head_cache[(t, r)])
            tail_idx.append(tail_cache[(h, r)])
        head_idx = np.array(head_idx, dtype=int)
        tail_idx = np.array(tail_idx, dtype=int)
        head_cache = np.random.randint(low=0, high=self.n_ent, size=(count_h, self.n_sample))
        tail_cache = np.random.randint(low=0, high=self.n_ent, size=(count_t, self.n_sample))

        propability_in = np.zeros((1, 1), dtype=float)
        propability_out = np.zeros((1, 1), dtype=float)
        # propability_in = np.zeros((self.n_ent, self.n_ent), dtype=float)
        # propability_out = np.zeros((self.n_ent, self.n_ent), dtype=float)
        # if os.path.exists(self.inPath + '/propability_in.npy'):
        #     propability_in = np.load(self.inPath + '/propability_in.npy')
        #     propability_out = np.load(self.inPath + '/propability_out.npy')
        # else:
        #     # calculate the probability of entities
        #     for e1_index in range(graph_in.shape[0]):
        #         for e2_index in range(e1_index + 1, graph_in.shape[0]):
        #             distance_in = 1 - pdist(np.vstack([graph_in[e1_index],graph_in[e2_index]]),'cosine')
        #             propability_in[e1_index, e2_index] = distance_in[0]
        #             propability_in[e2_index, e1_index] = distance_in[0]
        #
        #             distance_out = 1 - pdist(np.vstack([graph_out[e1_index],graph_out[e2_index]]),'cosine')
        #             propability_out[e1_index, e2_index] = distance_out[0]
        #             propability_out[e2_index, e1_index] = distance_out[0]
        #     propability_in[np.isnan(propability_in)] = 0
        #     propability_out[np.isnan(propability_out)] = 0
        #     np.save(self.inPath + '/propability_in', propability_in)
        #     np.save(self.inPath + '/propability_out', propability_out)
        #
        #



        print('head/tail_idx: head/tail_cache', len(head_idx), len(tail_idx), head_cache.shape, tail_cache.shape,
              len(head_pos), len(tail_pos))
        return graph_in, graph_out, propability_in, propability_out, entity, head_idx, tail_idx, head_cache, tail_cache, head_pos, tail_pos


    def generateCache(self, args, relation_in, relation_out):
        head_cache = np.zeros((self.n_ent, args.cache_size), dtype=int)
        head_cache[:,:] = -1
        tail_cache = np.zeros((self.n_ent, args.cache_size), dtype=int)
        tail_cache[:,:] = -1
        relation_o = {}
        relation_i = {}
        relation_index = 0
        max_size = 0


        for i in range(self.n_rel):
            relation_o[i] = list(set(relation_out[i]))
            relation_i[i] = list(set(relation_in[i]))
            # head_cache[relation_o[i], relation_index: relation_index + len(relation_o[i])] = relation_o[i]
            # tail_cache[relation_i[i], relation_index: relation_index + len(relation_i[i])] = relation_i[i]
            # relation_index += max(len(relation_o[i]), len(relation_i[i]))
            if max_size < max(len(relation_o[i]), len(relation_i[i])):
                max_size = max(len(relation_o[i]), len(relation_i[i]))

        with open(self.inPath + '/relation2_in.txt', 'w+') as f:
            for i in range(self.n_rel):
                f.write(str(i) + '\t' + str(len(relation_i[i])))
                f.write('\n')

        with open(self.inPath + '/relation2_out.txt', 'w+') as f:
            for i in range(self.n_rel):
                f.write(str(i) + '\t' + str(len(relation_o[i])))
                f.write('\n')

        print('max_size:', str(max_size))
        return head_cache, tail_cache

    def group_generate(self,args, entity_in_cate, entity_out_cate, max_in, max_out):
        min_size = args.min_size
        step_len = args.step_len
        entity_in_cate_new = {}
        entity_out_cate_new = {}
        temp = []
        step = 0
        count = 0
        pre = 0
        for i, j in entity_in_cate.items():
            if count == len(entity_in_cate) - 1 :
                entity_in_cate_new[i] = (temp + j).copy()
            elif len(j) < min_size:
                if not len(temp):
                    step = i
                if len(j) + len(temp) <= max_in and (int(i) - step ) <= step_len:
                    temp = temp + j
                    pre = i
                else:
                    entity_in_cate_new[pre]= temp.copy()
                    step = i
                    temp.clear()
                    temp = temp + j
            else:
                entity_in_cate_new[i] = j
            count += 1

        step = 0
        count = 0
        pre = 0
        temp.clear()
        for i, j in entity_out_cate.items():
            if count == len(entity_out_cate) - 1:
                entity_out_cate_new[i] = (temp + j).copy()
            elif len(j) < min_size:
                if not len(temp):
                    step = i
                if len(j) + len(temp) <= max_out and (int(i) - step) <= step_len:
                    temp = temp + j
                    pre = i
                else:
                    entity_out_cate_new[pre] = temp.copy()
                    step = i
                    temp.clear()
                    temp = temp + j
            else:
                entity_out_cate_new[i] = j
            count += 1

        return entity_in_cate_new, entity_out_cate_new

    def saveResult(self, propability):
       np.save(self.inPath + '/propability', propability)



    def writeToTxt(self):
        entity_in = np.zeros(self.n_ent, dtype=int)
        entity_out = np.zeros(self.n_ent, dtype=int)
        for h, t, r in zip(self.train_head, self.train_tail, self.train_rela):
            entity_out[h] = entity_out[h] + 1
            entity_in[t] = entity_in[t] + 1

        entity_in_size, _, entity_in_q = np.unique(entity_in, return_index=True, return_inverse=True)
        entity_out_size, _, entity_out_q = np.unique(entity_out, return_index=True, return_inverse=True)
        entity_in_cate = {}
        entity_out_cate = {}
        max_in = []
        max_out = []
        with open(self.inPath + '/relation_in.txt', 'w+') as f:
            for i, m in enumerate(entity_in_size.tolist()):
                count_in = 0
                f.write(str(i) + '\t')
                entity_in_cate[i] = []
                for j, k in enumerate(entity_in.tolist()):
                    if k == m:
                        entity_in_cate[i].append(j)
                        f.write(str(j) + '\t')
                        count_in += 1
                max_in.append(count_in)
                f.write('\n')
        with open(self.inPath + '/relation_out.txt', 'w+') as f:
            for i, m in enumerate(entity_out_size.tolist()):
                count_out = 0
                f.write(str(i) + '\t')
                entity_out_cate[i] = []
                for j, k in enumerate(entity_out.tolist()):
                    if k == m:
                        entity_out_cate[i].append(j)
                        f.write(str(j) + '\t')
                        count_out += 1
                max_out.append(count_out)
                f.write('\n')
        return entity_in_cate,entity_out_cate, max(max_in), max(max_out)


    def readFromTxt(self):
        entity_in_cate = {}
        entity_out_cate = {}
        max_in = []
        max_out = []

        with open(self.inPath + '/relation_in.txt', 'r') as f:
            tmp = f.readlines()
            for line in tmp:
                count = 0
                line = line.split()
                for en in line:
                    entity = en.strip().split()
                    if count==0:
                        size = entity
                        entity_in_cate[int(size[0])] = []
                    else:
                        entity_in_cate[int(size[0])].append(int(entity[0]))
                    count += 1
                max_in.append(count-1)

        with open(self.inPath + '/relation_out.txt', 'r') as f:
            tmp = f.readlines()
            for line in tmp:
                count = 0
                line = line.split()
                for en in line:
                    entity = en.strip().split()
                    if count==0:
                        size = entity
                        entity_out_cate[int(size[0])] = []
                    else:
                        entity_out_cate[int(size[0])].append(int(entity[0]))
                    count += 1
                max_out.append(count - 1)

        return entity_in_cate, entity_out_cate, max(max_in), max(max_out)







