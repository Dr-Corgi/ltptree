# -*- coding: utf-8 -*-
from ltptree import tree_builder
from ltp_util import LTPUtil

def test_ltp_util():

    ltpUtil = LTPUtil()

    sentences = "Python才是世界上最好的编程语言。PHP不是。"

    # test sentence spliter
    sentList = ltpUtil.SentenceSplitter(sentences)
    print "========== Test 00 - Spliter ========="
    for item in sentList:
        print item
    print "======================================\n\n"

    sentence = "群众非常赞赏政府打击腐败的举措。"

    # test segment
    words = ltpUtil.Segmentor(sentence)
    print "========== Test 01 - Segment ========="
    for item in words:
        print item
    print "======================================\n\n"

    # test postage 01
    postags = ltpUtil.Postagger(words)
    print "========== Test 02 - POS words ========="
    pList = list(postags)
    for item in pList:
        print item
    print "========================================\n\n"

    # test postage 02
    postags = ltpUtil.Postagger(sent=sentence)
    print "========== Test 03 - POS sents ========="
    pList = list(postags)
    for item in pList:
        print item
    print "========================================\n\n"

    # test named entity recognizer 01
    ner = ltpUtil.NamedEntityRecognizer(words, postags)
    print "========== Test 04 - NER words ========="
    nList = list(ner)
    for item in nList:
        print item
    print "========================================\n\n"

    # test named entity recognizer 02
    ner = ltpUtil.NamedEntityRecognizer(sent=sentence)
    print "========== Test 05 - NER sents ========="
    nList = list(ner)
    for item in nList:
        print item
    print "========================================\n\n"

    # test parser 01
    arcs = ltpUtil.Parser(words, postags)
    print "========== Test 06 - PAR words ========="
    aList = list(arcs)
    for item in aList:
        print str(item.head) + ": " + item.relation
    print "========================================\n\n"

    # test parser 02
    arcs = ltpUtil.Parser(sent = sentence)
    print "========== Test 07 - PAR sents ========="
    aList = list(arcs)
    for item in aList:
        print str(item.head) + ": " + item.relation
    print "========================================\n\n"

def test_ltp_tree():
    sent = "群众非常赞赏政府打击腐败的举措。"

    tree = tree_builder(sent)

    for i in range(tree.getRIndex()):
        print tree.find(i+1).toString()

if __name__ == "__main__":

    test_ltp_util()
    #test_ltp_tree()