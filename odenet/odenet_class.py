# Importe
from xml.etree import ElementTree as ET
import random
from random import *
import re
import networkx as nx
import matplotlib.pyplot as plt
import os
G=nx.Graph()


de_wn_file = os.path.join(os.path.dirname(__file__), f"wordnet/deWordNet.xml")
de_wn = open(de_wn_file,"r",encoding="utf-8")

#en_wn_file = os.path.join(os.path.dirname(__file__), f"..\..\..\..\English_WN\english-wordnet-2020.xml")
#en_wn = open(en_wn_file,"r",encoding="utf-8")

#out_wn = open(r"C:\Users\melaniesiegel\Documents\05_Projekte\WordNet\OdeNet\deWNaccess\odenet_oneline.xml","w",encoding="utf-8")

# You need to set the local path to PWN here:
# e.g.: get_english_wordnet_lexicon_local(r"C:\Users\melaniesiegel\Documents\05_Projekte\WordNet\English_WN\english-wordnet-2020.xml")

def get_english_wordnet_lexicon_local(pwnfile):
     en_wn = open(pwnfile,"r",encoding="utf-8")
     entree = ET.parse(en_wn)
     enroot = entree.getroot()
     enlexicon = enroot.find('Lexicon')
     return enlexicon


tree = ET.parse(de_wn)

root = tree.getroot()

lexicon = root.find('Lexicon')

de_wn.close()
#en_wn.close()

## Definitionen, die für die Methoden gebraucht werden

# Alle vorhandenen Informationen zu einem Wort zugreifen

def check_word_lemma(word_to_check):    
    for lexentry in lexicon.iter('LexicalEntry'):
        lemma = lexentry.find('Lemma')
        lemma_value = lemma.attrib['writtenForm']
        lemma_id = lexentry.attrib['id']
        if lemma_value == word_to_check:
            pos = lemma.attrib['partOfSpeech']
            senses = []
            for sense in lexentry.iter('Sense'):
                sense_id = sense.attrib['id']
                synset_id = sense.attrib['synset']
#                senserelation_type = lexentry.find('SenseRelation').attrib['relType']
#                senserelation_target = lexentry.find('SenseRelation').attrib['target']
                senses.append([sense_id,synset_id])
#            print("LEMMA: " + lemma_value + "\nPOS: " + pos + "\nSENSE ID: " + sense_id)
            return(lemma_id, lemma_value, pos, senses)

def words_in_synset(id):
    words = []
    for lexentry in lexicon.iter('LexicalEntry'):
        for sense in lexentry.iter('Sense'):
            if sense.attrib['synset'] == id:
                lemma = lexentry.find('Lemma').attrib['writtenForm']
                words.append(lemma)
    return(words)

def en_words_in_synset(id, enlexicon):
    words = []
    for lexentry in enlexicon.iter('LexicalEntry'):
        for sense in lexentry.iter('Sense'):
            if sense.attrib['synset'] == id:
                lemma = lexentry.find('Lemma').attrib['writtenForm']
                words.append(lemma)
    return(words)
'''
def en_words_in_ili(ili,pwnfile):
     enlexicon = get_english_wordnet_lexicon_local(pwnfile)
     words = []
     for synset in enlexicon.iter('Synset'):
          if ili == synset.attrib['ili']:
               id = synset.attrib['id']
               for lexentry in enlexicon.iter('LexicalEntry'):
                    for sense in lexentry.iter('Sense'):
                         if sense.attrib['synset'] == id:
                              lemma = lexentry.find('Lemma').attrib['writtenForm']
                              words.append(lemma)
     return(words)
'''     

def check_ili(ili):
     ili_synsets = []
     if len(ili) > 1:
          for synset in lexicon.iter('Synset'):  
               if ili == synset.attrib['ili']:
                    id = synset.attrib['id']
                    ili_synsets.append(id)
     return(ili_synsets)



def check_synset(id):
    words = words_in_synset(id)
    for synset in lexicon.iter('Synset'):
        if id == synset.attrib['id']:
            ili = synset.attrib['ili']
            try:
                en_definition = synset.attrib["{https://globalwordnet.github.io/schemas/dc/}description"]
            except KeyError:
                en_definition = []
            if synset.find('Definition') != None:
                de_definition = synset.find('Definition').text.strip()
            else:
                de_definition = []
            relations = []
            for relation in synset.iter('SynsetRelation'):
                reltype = relation.attrib['relType']
                reltarget = relation.attrib['target']
                relations.append((reltype,reltarget))
            ili_synsets = check_ili(ili)
            return(ili,en_definition,de_definition, relations, words, ili_synsets)

def check_word_id(word_id):    
    for lexentry in lexicon.iter('LexicalEntry'):
        lemma = lexentry.find('Lemma')
        lemma_value = lemma.attrib['writtenForm']
        lemma_id = lexentry.attrib['id']
        if lemma_id == word_id:
            pos = lemma.attrib['partOfSpeech']
            senses = []
            for sense in lexentry.iter('Sense'):
                sense_id = sense.attrib['id']
                synset_id = sense.attrib['synset']
                senses.append([sense_id,synset_id])
            print("LEMMA: " + lemma_value + "\nPOS: " + pos + "\nSENSE ID: " + sense_id)

def find_all_lexentries(word_to_check):
    for lexentry in lexicon.iter('LexicalEntry'):
        lemma = lexentry.find('Lemma')
        lemma_value = lemma.attrib['writtenForm']
        lemma_id = lexentry.attrib['id']
        word_id_list = []
        if lemma_value == word_to_check:
            word_id_list.append(lemma_id)
        for wid in word_id_list:
            check_word_id(wid)            
        
def hypernyms_word(word):
    try:
        lemma_id, lemma, pos, senses = check_word_lemma(word)
    except:
        return(None)
    hyp_list = []
    for sense in senses:
        (ili,definition,de_definition, relations, words,ili_list) = check_synset(sense[1])
        for relation in relations:
            if relation[0] == "hypernym":
                hypernym_synset = relation[1]
                hypernym_words = words_in_synset(relation[1])
#            else:
#                hypernym_synset = []
#                hypernym_words = []               
                hyp_list.append((sense[0],hypernym_synset,hypernym_words))
    return(hyp_list)

def hypernyms(sense):
    hyp_list = []
    (ili,definition,de_definition, relations, words,ili_list) = check_synset(sense)
    if check_synset(sense)!= None:
         for relation in relations:
             if relation[0] == "hypernym":
                 hypernym_synset = relation[1]
                 hypernym_words = words_in_synset(relation[1])
                 hyp_list.append((hypernym_synset,hypernym_words))
             else:
                  hyp_list = hyp_list
    return(hyp_list)

def hypernyms_path(synset,hyp_list):
    if len(synset) > 0:
        hyper=hypernyms(synset)
        if len(hyper) > 0:
            hyp = hyper[0][0]
            hyp_list.append(hyp)
            synset = hyp
            hypernyms_path(synset,hyp_list)
        else:
            hyp_list = hyp_list
    else:
        hyp_list = hyp_list
    return(hyp_list)

def hyponyms(sense):
    hyp_list = []
    (ili,definition,de_definition, relations, words,ili_list) = check_synset(sense)
    for relation in relations:
        if relation[0] == "hyponym":
            hyponym_synset = relation[1]
            hyponym_words = words_in_synset(relation[1])
            hyp_list.append((hyponym_synset,hyponym_words))
    return(hyp_list)

def hyponyms_word(word):
    try:
        lemma_id, lemma, pos, senses = check_word_lemma(word)
    except:
        return(None)
    hyp_list = []
    for sense in senses:
        (ili,definition,de_definition, relations, words,ili_list) = check_synset(sense[1])
        for relation in relations:
            if relation[0] == "hyponym":
                hyponym_synset = relation[1]
                hyponym_words = words_in_synset(relation[1])
 #           else:
 #               hyponym_synset = []
 #               hyponym_words = []               
                hyp_list.append((sense[0],hyponym_synset,hyponym_words))
    return(hyp_list)

def meronyms_word(word):
    try:
        lemma_id, lemma, pos, senses = check_word_lemma(word)
    except:
        return(None)
    mero_list = []
    for sense in senses:
        (ili,definition,de_definition, relations, words,ili_list) = check_synset(sense[1])
        for relation in relations:
            if relation[0] == "mero_part":
                meronym_synset = relation[1]
                meronym_words = words_in_synset(relation[1])
                mero_list.append((sense[0],meronym_synset,meronym_words))
    return(mero_list)

def holonyms_word(word):
    try:
        lemma_id, lemma, pos, senses = check_word_lemma(word)
    except:
        return(None)
    holo_list = []
    for sense in senses:
        (ili,definition,de_definition, relations, words,ili_list) = check_synset(sense[1])
        for relation in relations:
            if relation[0] == "holo_part" or relation[0] == "holo_member":
                holo_synset = relation[1]
                holo_words = words_in_synset(relation[1])
                holo_list.append((sense[0],holo_synset,holo_words))
    return(holo_list)

def antonyms_word(word):
    try:
        lemma_id, lemma, pos, senses = check_word_lemma(word)
    except:
        return(None)
    anto_list = []
    for sense in senses:
        (ili,definition,de_definition, relations, words,ili_list) = check_synset(sense[1])
        for relation in relations:
            if relation[0] == "antonym":
                antonym_synset = relation[1]
                antonym_words = words_in_synset(relation[1])
                anto_list.append((sense[0],antonym_synset,antonym_words))
    return(anto_list)

def synonyms_word(word):
    try:
        lemma_id, lemma, pos, senses = check_word_lemma(word)
    except:
        return(None)
    syn_list = []
    for sense in senses:
        (ili,definition,de_definition, relations, words,ili_list) = check_synset(sense[1])
        words.remove(word)
        syn_list.append(words)
 #       for w in words:
 #           syn_list.append(w)
#    syn_list.remove(word)
#    return(sorted(set(syn_list)))
    return(syn_list)


def words2ids(wordlist):
    word_id_list = []
    for word in wordlist:
        try:
            lemma_id, lemma, pos, senses = check_word_lemma(word)
            word_id_list.append(lemma_id)
        except:
            print(word + " NOT IN ODENET")
    return(word_id_list)
    


# Visualisierungen

seen = set()

def recurse_hyper(s,word):
    if not s in seen:
        seen.add(s)
        G.add_node(word)
        hypers = hypernyms(s)
        print(str(hypers))
#        if len(hypers) > 0:
        for h in hypers:
            G.add_node(h[1][0])
            G.add_edge(word,h[1][0])
            recurse_hyper(h[0],h[1][0])

def recurse_hypo(s,word):
    if not s in seen:
        seen.add(s)
        G.add_node(word)
        hypos = hyponyms(s)
        for h in hypos:
            G.add_node(h[1][0])
            G.add_edge(word,h[1][0])
            recurse_hypo(h[0],h[1][0])

def recurse(s,word):
    if not s in seen:
        seen.add(s)
        G.add_node(word)
        hypers = hypernyms(s)
        hypos = hyponyms(s)
        print(str(hypers))
        print(str(hypos))
#        if len(hypers) > 0:
        for h in hypers:
            G.add_node(h[1][0])
            G.add_edge(word,h[1][0])
            recurse_hyper(h[0],h[1][0])
        for h in hypos:
            G.add_node(h[1][0])
            G.add_edge(word,h[1][0])
            recurse_hypo(h[0],h[1][0])

#recurse_hyper(sense,word)

#recurse_hypo(sense,word)

def visualize_hypernyms():
    word = input("Welches Wort? ")
    lemma, pos, senses = check_word_lemma(word)
    print("Ich habe diese Senses dafür: ")
    for s in senses:
        print("SYNSET: " + s[1])
        print(check_synset(s[1]))
    sense = input("Welcher Sense? ")      
    recurse_hyper(sense,word)
    print (G.nodes(data=True))
    nx.draw_networkx(G, width=2, with_labels=True)
    plt.show()

def visualize_hyponyms():
    word = input("Welches Wort? ")
    lemma, pos, senses = check_word_lemma(word)
    print("Ich habe diese Senses dafür: ")
    for s in senses:
        print("SYNSET: " + s[1])
        print(check_synset(s[1]))
    sense = input("Welcher Sense? ")
    recurse_hypo(sense,word)
    print (G.nodes(data=True))
    nx.draw_networkx(G, width=2, with_labels=True)
    plt.show()

def give_all_senses(word):
    try:
        lemma_id, lemma, pos, senses = check_word_lemma(word)
        for sense in senses:
            print("SYNSET: " + sense[1])
            print(check_synset(sense[1]))
    except TypeError:
        print("No entry for word " + word)


def en_ili_words(ili,pwnfile):
         enlexicon = get_english_wordnet_lexicon_local(pwnfile)
         words = []
         for synset in enlexicon.iter('Synset'):
              if ili == synset.attrib['ili']:
                   id = synset.attrib['id']
                   for lexentry in enlexicon.iter('LexicalEntry'):
                        for sense in lexentry.iter('Sense'):
                             if sense.attrib['synset'] == id:
                                  lemma = lexentry.find('Lemma').attrib['writtenForm']
                                  words.append(lemma)
         return words
               
## Die Klasse für den Zugriff auf OdeNet

class OdeNet(object):
    def word_info(object):
        try:
            lemma_id, lemma_value, pos, senses = check_word_lemma(object)
        except:
            return(None)
        print (lemma_value + " " + pos + " ")
        print("------------------------")
        for sense in senses:
            (ili,definition,de_definition, relations, words,ili_list) = check_synset(sense[1])
            print("SENSE: " + str(sense[1]))
            print("ILI: " + str(ili) + ' ' + str(en_ili_words(ili, r"C:\Users\Melanie Siegel\Documents\05_Projekte\OdeNet\English_WN\english-wordnet-2021.xml")))
            if len(ili_list) > 1:
                 print("MULTIPLE SENSES FOR ILI " + str(ili) + ": " + str(ili_list))
            print("DEFINITION: " + str(definition))
            print("DE_DEFINITION: " + str(de_definition))
            print("WORDS: " + str(words))
            print("RELATIONS: ")
            for relation in relations:
                 rel_words = words_in_synset(relation[1])
                 print(str(relation) + ': ' + str(rel_words))
#            print("RELATIONS: " + str(relations))
            print("------------------------")
#            print("SENSE: " + str(sense[1]) + "  " + str(check_synset(sense[1])) + "\n")
#        print("HYPERNYMS: " + str(hypernyms_word(object)))
#        print("HYPONYMS: " + str(hyponyms_word(object)))
#        print("MERONYMS: " + str(meronyms_word(object)))
#        print("HOLONYMS: " + str(holonyms_word(object)))
#        print("ANTONYMS: " + str(antonyms_word(object)))
        find_all_lexentries(object)                       
    pass
    def check_ili_in_pwn(object,pwnfile):
         enlexicon = get_english_wordnet_lexicon_local(pwnfile)
         for lexentry in enlexicon.iter('LexicalEntry'):
             lemma = lexentry.find('Lemma')
             lemma_value = lemma.attrib['writtenForm']
             if lemma_value == object:
                 pos = lemma.attrib['partOfSpeech']
                 senses = []
                 for sense in lexentry.iter('Sense'):
                     synset_id = sense.attrib['synset']
                     senses.append(synset_id)
                 for sense in senses:
                     words = en_words_in_synset(sense,enlexicon)
                     print(str(words))
                     for synset in enlexicon.iter('Synset'):
                         if sense == synset.attrib['id']:
                             ili = synset.attrib['ili']
                             print(str(ili))
                             definition = synset.find('Definition').text.strip()
                             print(str(definition))
    pass
    def en_words_in_ili(ili,pwnfile):
         enlexicon = get_english_wordnet_lexicon_local(pwnfile)
         words = []
         for synset in enlexicon.iter('Synset'):
              if ili == synset.attrib['ili']:
                   id = synset.attrib['id']
                   for lexentry in enlexicon.iter('LexicalEntry'):
                        for sense in lexentry.iter('Sense'):
                             if sense.attrib['synset'] == id:
                                  lemma = lexentry.find('Lemma').attrib['writtenForm']
                                  words.append(lemma)
         print("ENGLISH WORDS FOR THIS ILI: " + str(words))
         return words
    pass
    def de_words_in_ili(ili):
         ili_synsets = check_ili(ili)
         for synset in ili_synsets:
              print(str(synset) + ": " + str(words_in_synset(synset)))
    def word_id(object):
         try:
              lemma_id, lemma, pos, senses = check_word_lemma(object)
         except:
              return(None)
         return lemma_id
    pass
    def visualize(object):
        try:
            lemma_id, lemma, pos, senses = check_word_lemma(object)
        except:
            return(None)
        if len(senses) == 1:
            sense = senses[0][1]
        else:
            print("Ich habe diese Senses dafür: ")
            for s in senses:
                print("SYNSET: " + s[1])
                print(check_synset(s[1]))
            sense = input("Welcher Sense? ")      
        recurse(sense,object)
        print (G.nodes(data=True))
        nx.draw_networkx(G, width=2, with_labels=True)
        plt.show()
    pass

