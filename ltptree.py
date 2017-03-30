# -*- coding: utf-8 -*-
from ltputil import LTPUtil

ltpUtil = LTPUtil()

class Node:
    def __init__(self, index, relation, head, postag, context, polarity, lchild=None, rchild=None):
        self.index = index
        self.head = head
        self.relation = relation
        self.postag = postag
        self.context = context
        self.polarity = polarity
        self.lindex = index
        self.rindex = index
        self.lchild = lchild
        self.rchild = rchild

class LTPTree:
    def __init__(self, index, relation, head, postag, context, polarity=0.0):
        self.root = Node(index, relation, head, postag, context, polarity)

    def addChild(self, child_tree):
        if child_tree.root.index < self.root.index:
            if self.root.lindex > child_tree.root.lindex:
                self.root.lindex = child_tree.root.lindex
            if self.root.lchild == None:
                self.root.lchild = list()
                self.root.lchild.append(child_tree)
            else:
                added_flag = False

                for iter in range(len(self.root.lchild))[::-1]:
                    if self.root.lchild[iter].root.head == child_tree.root.index:
                        sub_tree = self.root.lchild[iter]
                        child_tree.addChild(self.root.lchild[iter])
                        self.root.lchild.remove(sub_tree)
                if (child_tree.root.lchild != None):
                    child_tree.root.lchild.sort(lambda x,y:cmp(x.root.index,y.root.index))


                for iter in range(len(self.root.lchild)):
                    if child_tree.root.head == self.root.lchild[iter].root.index:
                        added_flag = True
                        self.root.lchild[iter].addChild(child_tree)
                    elif self.root.lchild[iter].inrange(child_tree.root.head):
                        added_flag = True
                        self.root.lchild[iter].addChild(child_tree)
                if added_flag == False:
                    self.root.lchild.append(child_tree)
                self.root.lchild.sort(lambda x,y:cmp(x.root.index,y.root.index))

        else:
            if self.root.rindex < child_tree.root.rindex:
                self.root.rindex = child_tree.root.rindex
            if self.root.rchild == None:
                self.root.rchild = list()
                self.root.rchild.append(child_tree)
            else:
                added_flag = False
                for iter in range(len(self.root.rchild))[::-1]:
                    if self.root.rchild[iter].root.head == child_tree.root.index:
                        sub_tree = self.root.rchild[iter]
                        child_tree.addChild(self.root.rchild[iter])
                        self.root.rchild.remove(sub_tree)
                # 如果出现顺序错误，可能要修改这里。
                if (child_tree.root.rchild != None):
                    child_tree.root.rchild.sort(lambda x, y: cmp(x.root.index, y.root.index))
                for iter in range(len(self.root.rchild)):
                    if self.root.rchild[iter].root.index == child_tree.root.head:
                        added_flag = True
                        self.root.rchild[iter].addChild(child_tree)
                    elif self.root.rchild[iter].inrange(child_tree.root.head):
                        added_flag = True
                        self.root.rchild[iter].addChild(child_tree)
                if added_flag == False:
                    self.root.rchild.append(child_tree)
                self.root.rchild.sort(lambda x, y: cmp(x.root.index, y.root.index))

    def getLIndex(self):
        return self.root.lindex

    def getRIndex(self):
        return self.root.rindex

    def toString(self):
        return "====================\n" + \
               "head: " + str(self.root.head) + "\n" + \
               "index: " + str(self.root.index) + "\n" + \
               "relation: " + self.root.relation + "\n" + \
               "postage: " + self.root.postag + "\n" + \
               "context: " + self.root.context + "\n" + \
               "polarity: " + str(self.root.polarity) + "\n" + \
               "lindex: " + str(self.root.lindex) + "\n" + \
               "rindex: " + str(self.root.rindex) + "\n" + \
               "====================\n"

    def find(self, index):
        if index < self.root.lindex or index > self.root.rindex:
            print "Error! Out of range!"
        if index == self.root.index:
            return self
        elif index < self.root.index:
            for tree in self.root.lchild:
                if tree.inrange(index):
                    return tree.find(index)
        else:
            for tree in self.root.rchild:
                if tree.inrange(index):
                    return tree.find(index)

    def inrange(self,index):
        return (self.root.lindex <= index and self.root.rindex >= index)


def tree_builder(sentence):
    words = ltpUtil.Segmentor(sentence)
    postags = ltpUtil.Postagger(words)
    arcs = ltpUtil.Parser(words, postags)

    head_index = -1
    for i in range(len(arcs)):
        if arcs[i].head == 0: head_index = i+1

    # 属性polarity默认使用0.0,按需修改
    tree = LTPTree(head_index, 'HED', 0, postags[head_index-1], words[head_index-1])

    for i in range(len(arcs)):
        if i+1 != head_index:
            p_tree = LTPTree(i+1, arcs[i].relation, arcs[i].head, postags[i], words[i])
            tree.addChild(p_tree)

    return tree