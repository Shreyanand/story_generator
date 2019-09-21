# -*- coding: utf-8 -*-

'''
import subprocess

#p = subprocess.check_output(["python", "/Users/shrey/test.py"])
#p = subprocess.check_output(["echo" "hi"])
#p = subprocess.run(["echo $(python /Users/shrey/test.py)"], shell=True, stdout=subprocess.PIPE)
p1 = subprocess.run(['C:/Python27/python.exe', 'C:/Users/Amanul/Downloads/GM/Project/RNN code/story_cloze-master/skip_thought_vector.py'], stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
print (p1.stdout)
print(p1)
      
'''

from stanfordcorenlp import StanfordCoreNLP
import pandas as pd
from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize
import os
import sys
import json
from skip_thought_vector import skip_thought_vector
class interface:
    
    def __init__(self, host='http://localhost', port=9000):
        #self.file_path = 'ROCStories_winter2017 - ROCStories_winter2017.csv'
        self.file_path = 'process_data_final_.csv'
        self.nlp = StanfordCoreNLP(host, port=port, timeout=30000)
        self.props = {
            'annotators': 'tokenize,ssplit,pos,lemma,ner,parse,depparse,dcoref,relation',
            'pipelineLanguage': 'en',
            'outputFormat': 'json'
        }
    
    def annotate(self, sentence):
        return json.loads(self.nlp.annotate(sentence, properties=self.props))
    
    def get_ner_tags(self, ann_dict):
        person_list = dict()
        c = 1
        for sent in ann_dict['sentences']:
            for line in sent['tokens']:
                #print("line: " , line)
                if(line['ner'] == 'PERSON'):
                    #print("line : ", line)
                    name = line['word']
                    if(name not in person_list):
                        if(name == 'John' or name == 'Peter' or name == 'Jake' or name == 'David'):
                            person_list[line['word']] ='Male'
                        else:
                            person_list[line['word']] ='Female'
                        c+=1
                    #print("found ", line['word'])
        return(person_list)
        
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
    
    def replace_co_ref(self, ann_dict, person_list):
        sent_dict = self.sent_tokenized_dict(ann_dict)
        #for sent in ann_dict['sentences']:
        #    print(sent["tokens"])
        coref_dict = ann_dict['corefs']
        j = 1
        coref_flag = False
        for key in coref_dict:
            name = None
            #word_list = set()
            ref = coref_dict[key]
            #print("Ref [",j,"]: ", ref, "\n")
            
            if(len(ref) > 0 and (ref[0]['text'] in person_list) and ref[0]['type'] == 'PROPER'):
                coref_flag = True
                name = ref[0]['text']
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
            
        if(coref_flag != True):
            return None
            
        processed_text = []
        for key in sent_dict:
            #print("Key = ", key)
            #print(sent_dict[key])
            processed_text.append(" ".join(sent_dict[key]))
        return(processed_text)
    
    
    def find_character_details(self, sent):
        ann_dict = self.annotate(sent)
        person_list = self.get_ner_tags(ann_dict)
        return person_list
        
        
if __name__ == '__main__':
    
    story = []
    interf_ = interface()
    stv = skip_thought_vector()
    character_name = "Mohit"
    first_sentence = "John thought Peter should buy a trailer and haul it with his car."
    character_list = interf_.find_character_details(first_sentence)
    story = ["John thought Peter should buy a trailer and haul it with his car.",
             "Peter thought a truck would be better for what he needed.",
             "John pointed out two vehicles were much more expensive.",
             "Peter was set in his ways with conventional thinking.",
             "He ended up buying the truck he wanted despite John's advice."]
    '''
    for i in range(1,5):
        
        sentence = " ".join(story[0:i])
        ann_dict = interf_.annotate(sentence)
        processed_text = interf_.replace_co_ref(ann_dict, character_list)
        print(processed_text, " \n")   
      
    '''
    system_generated_sentences = ["Mohit was a man of principal and it would violate his principals to not do it even for a day.",
                                  "It was getting close to the end of day and Tyler was nowhere in sight.",
                                  "Finally his friend Amanul came to his rescue and gave him what he wanted.",
                                  "Mohit jumped with joy and was happy as never before."]
    
    print("Welcome to the world of imagination")
    
    print("How it works? \nThis is an interactive story generating system that uses human authoring along with",
          "the system's expertise to generate intriguing short stories. \n The system generates the first sentence",
          "for the story, following which it makes suggestions for the next sentence. You can choose from the",
          "suggestions you see in the list by typing the corresponding digit for your choosen next sentence, ",
          "or you can eneter a sentence which then becomes the part of the narration.\n This procedure continues till",
          " we have a short 5 sentence story.\n")
     
    print("Put your author hat one and get ready to help the system generate novel and interesting stories\n")
    print("This is a short story about", character_name)
    print("The story starts with this opening sentence \n\n'",first_sentence,"'\n")
    print("Choose either from the following system generated suggestions for the next sentence in the story or you can enter you own sentence here\n")
    print("To choose you just need to enter the digit corresponding to that suggestion\n")
    j = 1
    
    story = [first_sentence]
    character_list = interf_.find_character_details(first_sentence)
    system_generated_sentences = stv.generate_vector(story)  
    for sent in system_generated_sentences:
        print(j, "  ",sent)
        j += 1
    inp = input()
    while(1):
        if(len(inp) == 1 and int(inp) in range(5)):
            inp = int(inp)
            next_sentence = system_generated_sentences[inp-1]
            story.append(next_sentence)
            #story = story + str(system_generated_sentences[inp-1])
        else:
            next_sentence = str(inp)
            story.append(next_sentence)
            #story = story + " " + str(inp)
        j = 1
        print("Story so far")
        for st in story:
            print(st)
        
        sentence = " ".join(story[0:i])
        ann_dict = interf_.annotate(sentence)
        processed_story = interf_.replace_co_ref(ann_dict, character_list)
        
        system_generated_sentences = stv.generate_vector(processed_story)  
        for sent in system_generated_sentences:
            print(j, "  ",sent)
            j += 1
        
        if(len(story) == 5):
            break
        inp = input()
    
    print("\nFantastic! This is an amazing story. You should definitely try your hands on writing more stories, you could be the next Shakespeare")
    print("\n1final story: ")
    print(" ".join(story))