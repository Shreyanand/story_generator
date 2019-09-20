# -*- coding: utf-8 -*-
'''
author: Amanul Haque
'''

from stanfordcorenlp import StanfordCoreNLP
import logging
import json
from pprint import pprint
import sys
import pandas as pd

class data_preprocessing:
    
    def __init__(self, host='http://localhost', port=9000):
        #self.file_path = 'ROCStories_winter2017 - ROCStories_winter2017.csv'
        self.file_path = 'process_data_final_.csv'
        self.nlp = StanfordCoreNLP(host, port=port, timeout=30000)
        self.props = {
            'annotators': 'tokenize,ssplit,pos,lemma,ner,parse,depparse,dcoref,relation',
            'pipelineLanguage': 'en',
            'outputFormat': 'json'
        }
        self.male_names = ['Bill', 'Ivan', 'Ida', 'Mac', 'Xavier', 'Orlando', 'Gizmo', 'Koa', 'Cal', 'Geb', 'Rover', 'Nio', 'Kio', 'Regis',]
        self.female_names = ['Genie', 'Bea', 'Ana', 'Sia', 'Pia', 'Minerva', 'Sky', 'Bebe', 'Peta', 'Frances', 'Chariot', 'Kana', 'Gia', 'Loris', 'Terra', 'Jasmine']
        
        self.universal_male_names = ['John', 'Peter', 'Jake', 'David']
        self.universal_female_names = ['Emily', 'Rachel', 'Sarah', 'Molly']
        self.u_count = 0
        self.unknown_geneder_name = set()

    def word_tokenize(self, sentence):
        return self.nlp.word_tokenize(sentence)

    def pos(self, sentence):
        return self.nlp.pos_tag(sentence)

    def ner(self, sentence):
        return self.nlp.ner(sentence)

    def parse(self, sentence):
        return self.nlp.parse(sentence)

    def dependency_parse(self, sentence):
        return self.nlp.dependency_parse(sentence)

    def annotate(self, sentence):
        return json.loads(self.nlp.annotate(sentence, properties=self.props))
  
    def get_data(self):
        data = pd.read_csv(self.file_path)
        return data
    
    def write_to_csv(self, df):
        df = pd.DataFrame([df])
        with open('process_data_final_.csv', 'a') as f:
            df.to_csv(f, header=False)
            
    def write_to_text_file(self, data, filename):
        with open(filename, "a") as myfile:
            myfile.write(data)
            myfile.write("\n")
        
    def process(self, data):
        
        count = 0        
        person_list = dict()
        #num_col = len(data.iloc[0])
        df = dict()
        for index, row in data.iterrows():
            #if(index not in indx):
            count += 1
            story_id = row[0]
            story_title = row[1]
            sent_list = [row[i] for i in range(2, len(row))]
            #print("sent List before Processing ", sent_list)
            sent_list = self.replace_neutral_names(sent_list)
            #print("sent List after Processing ", sent_list)
            sentence = " ".join(sent_list)
            #if('!' in sentence):
            #    sentence = sentence.replace('!','.')
            #print("Initial sentence is : " , sentence)
            ann_dict = self.annotate(sentence)
            person_list = self.get_ner_tags(ann_dict)
            #print("person_list", person_list)
            #self.list_of_nuetral_names(ann_dict, person_list, index)
            #print(count)
            processed_text = self.replace_co_ref(ann_dict, person_list)
            df[0] = story_id
            df[1] = story_title
            if(processed_text != None):
                for i in range(len(processed_text)):
                    df[i+2] = processed_text[i]
    
                #self.write_to_csv(df)
                #print(df)
            print(count)
            
        #print(df)
        return df

    
    def replace_neutral_names(self, sent_list):
        new_sent_list = []
        #print("old sentence list: ", sent_list)
        for sent in sent_list:
            for name in self.male_names:
                if(name in sent):
                    sent = sent.replace(name, 'John')
            for name in self.female_names:
                if(name in sent):
                    sent = sent.replace(name, 'Emily')
            new_sent_list.append(sent)
        #print("new_sent_list : ", new_sent_list)
        return new_sent_list
                    
        
    def list_of_nuetral_names(self, ann_dict, person_list, index):
        
        coref_dict = ann_dict['corefs']
        j = 1
        for key in coref_dict:
            ref = coref_dict[key]
            
            if(len(ref) > 0 and (ref[0]['text'] in person_list) and ref[0]['type'] == 'PROPER'):
                #name = person_list[ref[0]['text']]
                if((ref[0]['type'] == 'PROPER' or ref[0]['type'] == 'PRONOMINAL') and (ref[0]['gender'] == 'UNKNOWN' or ref[0]['gender'] == 'NEUTRAL')):
                    print("Name ", ref[0]['text'])
                    if(ref[0]['text'] not in self.unknown_geneder_name):
                        self.unknown_geneder_name.add(ref[0]['text'])
                        self.write_to_text_file(ref[0]['text'], "unkown_gender_names_3.txt")
                        self.write_to_text_file(str(index), "index_list_1.txt")
                    
                    self.u_count+=1
                    j+=1
        #print("\n")
        
        
    def sent_tokenized_dict(self, ann_dict):
        sent_dict = {}
        i_sent = 1
        for sent in ann_dict['sentences']:
            sent_dict[i_sent] = []
            #w_index = 0
            #print(len(sent['tokens']))
            for line in sent['tokens']:
                #print(line)
                #if(line["word"] != '.'):
                sent_dict[i_sent].append(line["word"])
                    #w_index += 1
            #sent_dict[i_sent].append('.')
            i_sent+=1   
        #print(sent_dict)
        return sent_dict
    
    def get_ner_tags(self, ann_dict):
        person_list = dict()
        c = 1
        for sent in ann_dict['sentences']:
            for line in sent['tokens']:
                #print("line: " , line)
                if(line['ner'] == 'PERSON'):
                    #print("line : ", line)
                    if(line['word'] not in person_list):
                        person_list[line['word']] ='Person' + str(c)
                        c+=1
                    #print("found ", line['word'])
        return(person_list)
        
    
    def replace_co_ref(self, ann_dict, person_list):
        sent_dict = self.sent_tokenized_dict(ann_dict)
        #for sent in ann_dict['sentences']:
        #    print(sent["tokens"])
        used_names = set()
        coref_dict = ann_dict['corefs']
        j = 1
        coref_flag = False
        for key in coref_dict:
            name = None
            #word_list = set()
            ref = coref_dict[key]
            #print("Ref [",j,"]: ", ref, "\n")
            
            #for ref in coref_dict[key]:
            #    word_list.add(ref['text'])
                
            #print("Word List :", word_list)
            #print("person_list ", person_list)
            if(len(ref) > 0 and (ref[0]['text'] in person_list) and ref[0]['type'] == 'PROPER'):
                coref_flag = True
                if(ref[0]['gender'] == 'MALE'):
                    name = [n for n in self.universal_male_names if n not in used_names][0]
                    used_names.add(name)
                elif(ref[0]['gender'] == 'FEMALE'):
                    name = [n for n in self.universal_female_names if n not in used_names][0]
                    used_names.add(name)
                else:
                    name = 'UNKNOWN'
                    used_names.add(name)
                    self.u_count += 1
                    
                #print("Name = ", name)
                for ref in coref_dict[key]:
                    if(ref['type'] == 'PROPER' or ref['type'] == 'PRONOMINAL'):
                        #print("REF word ", ref['text'], "\t", ref['sentNum'], "\t", ref['startIndex'])
                        sent_num = ref['sentNum']
                        start_index = ref['startIndex']-1
                        #end_index = ref['endIndex']-1
                        #for index in range(start_index, end_index):
                        if(ref['text'] == 'his' or ref['text'] == 'her' or ref['text'] == 'His' or ref['text'] == 'Her'):
                            sent_dict[sent_num][start_index] = name +str("'s")
                        else:
                            sent_dict[sent_num][start_index] = name
            j+=1
            
        if(coref_flag == False):
            print("sent ", sent_dict)
            sys.exit()
        
        if(coref_flag != True):
            return None
            
        processed_text = []
        #sys.exit()
        #print("sent_dict" , sent_dict)
        for key in sent_dict:
            #print("Key = ", key)
            #print(sent_dict[key])
            processed_text.append(" ".join(sent_dict[key]))
        return(processed_text)
    
    def find_unknown_cases(self, data):
        count = 0
        count_ = 0
        loop_counter = 0
        
        for index, row in data.iterrows():
            loop_counter += 1
            flag = 0
            story_id = row[0]
            story_title = row[1]
            sent_list = [row[i] for i in range(2, len(row))]
            #print(sent_list)
            for sent in sent_list:
                if(' he ' in sent or 'He' in sent):
                    flag = 1
                    break
                if(' she ' in sent or 'She' in sent):
                    flag = 1
                    break
                if(' his ' in sent or 'His ' in sent or ' him ' in sent or 'His ' in sent):
                    flag = 1
                    break
                if('Her ' in sent or ' her ' in sent):
                    flag = 1
                    break
       
            if(flag == 0):
                count_ += 1
                self.write_to_csv(row)
            else:
                count += 1
        print("COUNT = ", count)
        print("Other count = ", count_)
        print("loop_counter = ", loop_counter)
                
    def find_unknown_case(self, data):
        unknowns = 0
        he = 0
        she = 0
        his = 0
        her = 0
        
        for index, row in data.iterrows():
            flag = 0
            story_id = row[0]
            story_title = row[1]
            sent_list = [row[i] for i in range(3, len(row))]
            #print(sent_list)
            for sent in sent_list:
                if('UNKNOWN' in sent):
                    unknowns += 1
                    break
                if(' he ' in sent or 'He' in sent):
                    he += 1
                    break
                if(' she ' in sent or 'She' in sent):
                    she += 1
                    break
                if(' his ' in sent or 'His ' in sent or ' him ' in sent or 'His ' in sent):
                    his += 1
                    break
                if('Her ' in sent or ' her ' in sent):
                    her += 1
                    break
                
        print("UNKNOW ", unknowns)
        print("HE ", he)
        print("SHE ", she)
        print("HER ", her)
        print("HIS ", his)
    
    def replace_unknowns(self, data):
        
        for index, row in data.iterrows():
            story_id = row[0]
            story_title = row[1]
            sent_list = [row[i] for i in range(2, len(row))]
            new_row = [story_id, story_title]
            for sent in sent_list:
                while('UNKNOWN' in sent):
                    sent = sent.replace('UNKNOWN', 'Emily')
                new_row.append(sent)
            #print(new_row)
            #sys.exit()
            self.write_to_csv(new_row)
                    
        
        
                
if __name__ == '__main__':
    #f = open("abc.txt", "w")
    dp = data_preprocessing()
    data = dp.get_data()
    #print(data.shape)
    #sys.exit()
    
    #print(data.iloc[8:9,2:7])
    dp.find_unknown_case(data)
    #dp.replace_unknowns(data)
    #print(data.iloc[55:56,:])
    #df = dp.process(data.iloc[32:40,:])
    #print(df)    
