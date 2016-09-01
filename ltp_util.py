# -*- coding: utf-8 -*-
import pyltp

class LTPUtil:

    def __init__(self, seg_model_path = './model/cws.model', seg_lexicon_path = './lexicon/userLexicon.txt',
                 pos_model_path = './model/pos.model', rec_model_path = './model/ner.model',
                 par_model_path = './model/parser.model'):
        self.__segmentor = None
        self.__seg_model_path = seg_model_path
        self.__seg_lexicon_path = seg_lexicon_path
        self.__postagger = None
        self.__pos_model_path = pos_model_path
        self.__recognizer = None
        self.__rec_model_path = rec_model_path
        self.__parser = None
        self.__par_model_path = par_model_path

    # split sentences
    def SentenceSplitter(self, sents):
        sentList = pyltp.SentenceSplitter.split(sents)
        return sentList

    # segment
    def Segmentor(self, sent):
        if self.__segmentor == None:
            self.__segmentor = pyltp.Segmentor()
            if self.__seg_lexicon_path == None:
                self.__segmentor.load(self.__seg_model_path)
            else:
                self.__segmentor.load_with_lexicon(self.__seg_model_path, self.__seg_lexicon_path)
            print "Loaded Segmentor Model Success!"

        words = self.__segmentor.segment(sent)
        return words

    # postagger
    def Postagger(self, words = None, sent = None):
        if self.__postagger == None:
            self.__postagger = pyltp.Postagger()
            if self.__seg_lexicon_path == None:
                self.__postagger.load(self.__pos_model_path)
            else:
                self.__postagger.load_with_lexicon(self.__pos_model_path, self.__seg_lexicon_path)
            print "Loaded Postagger Model Success!"
        postags = None
        if sent != None:
            words = self.Segmentor(sent)
            postags = self.__postagger.postag(words)
        else:
            postags = self.__postagger.postag(words)
        return postags

    # named entity recognizer
    def NamedEntityRecognizer(self,words = None, postags = None, sent = None):
        if self.__recognizer == None:
            self.__recognizer = pyltp.NamedEntityRecognizer()
            self.__recognizer.load(self.__rec_model_path)
            print "Loaded Recognizer Model Success!"
        if sent != None:
            words = self.Segmentor(sent)
            postags = self.Postagger(words)
        netags = self.__recognizer.recognize(words, postags)
        return netags

    # parser
    def Parser(self, words = None, postags = None, sent = None):
        if self.__parser == None:
            self.__parser = pyltp.Parser()
            self.__parser.load(self.__par_model_path)
            print "Loaded Parser Model Success!"
        if sent != None:
            words = self.Segmentor(sent)
            postags = self.Postagger(words)
        arcs = self.__parser.parse(words, postags)
        return arcs

    def __del__(self):
        if self.__segmentor != None:
            self.__segmentor.release()
            print "Released Segmentor Model Success!"
        if self.__postagger != None:
            self.__postagger.release()
            print "Released Postagger Model Success!"
        if self.__recognizer != None:
            self.__recognizer.release()
            print "Released Recognizer Model Success!"
        if self.__parser != None:
            self.__parser.release()
            print "Released Parser Model Success!"


if __name__ == "__main__":

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