from bs4 import BeautifulSoup
import requests

import os

from gtts import gTTS
from playsound import playsound

import sys
sys.dont_write_bytecode = True
import rainbow_divider_lib as rdl

import genanki
import random
import time

def progress(count, total, suffix=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '#' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', suffix))
    sys.stdout.flush()  # As suggested by Rom Ruben
    if percents == 100:
        print("")


def remove_repeated_element(test_list):
    res = []
    for i in test_list:
        if i not in res:
            res.append(i)
    return res


def search_vocab_en(word, exactly_mode=False,
                    src="NECTEC Lexitron Dictionary EN-TH"):
    url = requests.get("https://dict.longdo.com/mobile.php?search="+word)
    soup = BeautifulSoup(url.content, "html.parser")
    target_src_exist = soup.find("b", string=src)
    if target_src_exist is not None:
        data = soup.find("b", string=src).next_sibling
        # print(data)
        '''
        print(data.prettify())
        print(data.tr.td)
        print(data.tr.td.contents)
        print(data.tr.td.text)

        print(data.tr.children)
        print(list(data.tr.children))
        '''

        result_lst = []
        for tr in data:
            tr_lst = []
            for td in tr:
                tr_lst.append(td.text)
            if exactly_mode is True:
                if tr_lst[0] == word:
                    result_lst.append(tr_lst)
            else:
                result_lst.append(tr_lst)

        for idx, text in enumerate(result_lst):
            if text[1].find(', Syn.') != -1:
                result_lst[idx][1] = text[1][:text[1].find(', Syn.')]
            # print(text)
        return result_lst
    else:
        return None

    # soup = BeautifulSoup(data)
    # table = soup.find("table", attrs={"class":"result-table"})


def search_vocab_jp(word, exactly_mode=False):
    '''search_mode = 'Start', 'End', 'Between', 'Exact' '''
    if exactly_mode is True:
        search_mode = 'Exact'
    else:
        search_mode = 'Between'
    url = requests.get("https://j-doradic.com/?searchPosition=search"
                       + search_mode + "&q=" + word)
    soup = BeautifulSoup(url.content, "html.parser")
    target_exist = soup.find("table", class_="table table-striped")
    # print(data.prettify())
    if target_exist is not None:
        data = soup.find("table", class_="table table-striped").tbody
        descendant_lst = []
        for d in data.descendants:
            if d.name == "a" and d.text != "thumb_up" and len(d.attrs) == 1:
                descendant_lst.append(d.text.replace('\n', ' ')
                                      .replace('\r', ''))
                # print(d.text.replace('\n', ' ').replace('\r', ''))

        if len(descendant_lst) % 3 == 0:
            result_lst = []
            for i in range(len(descendant_lst)//3):
                kanji = descendant_lst[i*3]
                hiragana = descendant_lst[i*3+1]
                thai_meaning = descendant_lst[i*3+2]

                if kanji.count('•') > 0:
                    hiragana_copy = hiragana
                    for i in range(kanji.count('•')):
                        hiragana = hiragana + '•' + hiragana_copy
                if kanji.count('・') > 0:
                    hiragana_copy = hiragana
                    for i in range(kanji.count('・')):
                        hiragana = hiragana + '・' + hiragana_copy

                meaning_lst = ["<ruby>"+kanji+"<rt>"
                               + hiragana+"</rt></ruby>", thai_meaning]
                '''
                meaning_lst = [descendant_lst[i*3],
                               descendant_lst[i*3+1],
                               descendant_lst[i*3+2]]
                '''
                if exactly_mode is True:
                    if descendant_lst[i*3] == word:
                        result_lst.append(meaning_lst)
                else:
                    result_lst.append(meaning_lst)

            return result_lst
        else:
            print("error")
            return None
    else:
        return None


def read_txt(file_name):
    f = open(file_name, "r", encoding="utf8")
    vocab_lst = f.read().strip('\n').split('\n')
    return vocab_lst


def find_text_between(text, start, end):
    return text[text.find(start)+len(start):text.rfind(end)]


def text_convert(meaning_lst, vocab):
    text = ''
    exactly_text = ''
    rgb_lst = rdl.divider2str(len(meaning_lst))
    for idx, meaning in enumerate(meaning_lst):
        # print(meaning[1])
        # found_vocab = '<p style="color:rgb(255, 99, 71);">'+meaning[0]+'</p>'
        if '<ruby>' in meaning[0]:  # is firigana
            is_exactly_vocab = bool(find_text_between(
                                    meaning[0], '<ruby>', '<rt>') == vocab)
        else:
            is_exactly_vocab = bool(meaning[0] == vocab)
        if is_exactly_vocab:
            found_vocab = '<span style="color:rgb(102, 255, 153); font-size:30px">'+meaning[0]+'</span>'
            found_meaning = '<span style="color:rgb(102, 255, 153); font-size:30px">'+meaning[1]+'</span>'
            exactly_text = '<span style="color:rgb(233, 253, 226); font-size:50px">'+meaning[0]+'</span>'
        else:
            found_vocab = '<span style="color:rgb'+ rgb_lst[idx] +'; font-size:20px">'+meaning[0]+'</span>'
            found_meaning = '<span style="color:rgb'+ rgb_lst[idx] +'; font-size:20px">'+meaning[1]+'</span>'
        new_text = found_vocab + ' : ' + found_meaning

        if is_exactly_vocab:
            text = new_text + '<br>' + text
        else:
            text = text + new_text + '<br>'

    return text, exactly_text


def text2sound(vocab, sound_number, parent_path, sound_lang):
    if sound_lang == "jp":
        sound_lang = "ja"
    tts = gTTS(text=vocab, lang=sound_lang)
    tts.save(parent_path + '/output/sound/#' + sound_number + '.mp3')


def ankiTH(input_text, gen_sound=False, exactly_mode=False, lang_select="jp"):

    parent_path = os.path.dirname(os.path.dirname(input_text))
    input_text_file_name = os.path.basename(input_text)
    input_text_file_name = os.path.splitext(input_text_file_name)[0]

    vocab_lst = read_txt(input_text)
    output = open(parent_path + "/output/" + input_text_file_name +'_output.txt', "w", encoding="utf8")
    fail_output = open(parent_path + "/output/" + input_text_file_name +'_fail_output.txt', "w", encoding="utf8")

    for vocab_cnt, vocab in enumerate(vocab_lst):
        if 'jp' in lang_select:
            meaning_lst = search_vocab_jp(vocab, exactly_mode)
            if exactly_mode is False:
                meaning_lst_exact = search_vocab_jp(vocab, True)
                if meaning_lst is not None and meaning_lst_exact is not None:
                    meaning_lst = meaning_lst_exact + meaning_lst
                    meaning_lst = remove_repeated_element(meaning_lst)
            furigana_offset = "</br>"
        elif 'en' in lang_select:
            meaning_lst = search_vocab_en(vocab, exactly_mode)
            furigana_offset = ""
        else:
            break
        if meaning_lst is not None:
            # print(search_vocab_en(vocab))
            meaning_text, furigana = text_convert(meaning_lst, vocab)
            if gen_sound is True:
                sound_number = input_text_file_name + '_' + str(vocab_cnt)
                sound_call_name = '[sound:#' + sound_number + '.mp3]'
                text2sound(vocab, sound_number, parent_path, lang_select)
            else:
                sound_call_name = ''
            vocab = '<span style="color:rgb(233, 253, 226); font-size:50px">' \
                    + "<ruby>" + vocab + "<rt>" + furigana_offset \
                    + "</rt></ruby>" + '</span>'
            if furigana == '':
                furigana = vocab
            output.write(vocab + '@' + meaning_text + sound_call_name
                         + '@' + furigana + '\n')
        else:
            fail_output.write(vocab + '\n')
        progress(vocab_cnt+1, len(vocab_lst))
    output.close()
    # search_vocab_en('carrot')

def gen_apkg(path="data/output/text_temp_output.txt"):
    # need to run from cd reference ( run from outer will can't use relative path)
    # where run script, that is workspace path
    # ankiTH("data/input/text_temp.txt", gen_sound=True, exactly_mode=False, lang_select="jp") 
    parent_path = os.path.dirname(path)
    
    model_id = random.randrange(1 << 30, 1 << 31)
     
    my_model = genanki.Model(
                    model_id,
                    'Simple Model with Media',
                    fields=[
                        {'name': 'หน้า'},
                        {'name': 'ย้อนกลับ'},
                        {'name': 'furigana'},
                    ],
                    templates=[
                        {
                        'name': 'anki_th_web_app_card',
                        'qfmt': '{{หน้า}}',
                        'afmt': '{{furigana}}<hr>{{ย้อนกลับ}}',
                        },
                    ],
                    css='.card {font-family: arial;font-size: 20px;text-align: center;color: black;background-color: white;}'
                    )
    my_deck = genanki.Deck(model_id, 'anki_th')
    my_package = genanki.Package(my_deck)
    
    deck_list = read_txt(path)
    for card in deck_list:
        card_list = card.split("@")
        element_list = []
        for element in card_list: # หน้า หลัง furigana
            element_list.append(element)
        my_note = genanki.Note(model=my_model, fields=element_list)
        my_deck.add_note(my_note)
        if ".mp3]@" in card:
            sound_file_name = card[card.find("[sound:")+len("[sound:"):card.find(".mp3]@")]
            my_package.media_files.append(parent_path+'/sound/'+sound_file_name+'.mp3')
    my_package.write_to_file(parent_path+'/output.apkg')
    
    

def main():

    do_list = [
             #  'N3_100_jp.txt',
             #  'N3_500_jp.txt',
             #  'N3_full_jp.txt',
               'vocab_en.txt',
               'vocab_jp.txt'
               ]
    directory = 'data/input/'
    for filename in os.listdir(directory):
        if filename.endswith(".txt") and filename in do_list:
            ankiTH(os.path.splitext(filename),
                   gen_sound=True, exactly_mode=False)

    # ankiTH('N3_full_jp', gen_sound=True, exactly_mode=False)
    # ankiTH('N3_100_jp', gen_sound=False, exactly_mode=False)
    # ankiTH('vocab_jp', gen_sound=True, exactly_mode=False)
    # ankiTH('vocab_en', gen_sound=True, exactly_mode=False)

def django_request(input_text, gen_sound=False, exactly_mode=False, lang_select="jp"):
    
    #########################################################################################################
    
    loading_page_html = open("card_generator/templates/card_generator/loading_page.html", "r")
    loading_page_html_list = loading_page_html.read().splitlines()
    for line in loading_page_html_list:
        yield line
    loading_page_html.close()
    
    time_capture = time.time()
    acc_avg_time = 2 # avg time about 2 sec
    
    ######################################################################################################### 
    
    parent_path = os.path.dirname(os.path.dirname(input_text))
    input_text_file_name = os.path.basename(input_text)
    input_text_file_name = os.path.splitext(input_text_file_name)[0]

    vocab_lst = read_txt(input_text)
    output = open(parent_path + "/output/" + input_text_file_name +'_output.txt', "w", encoding="utf8")
    fail_output = open(parent_path + "/output/" + input_text_file_name +'_fail_output.txt', "w", encoding="utf8")

    for vocab_cnt, vocab in enumerate(vocab_lst):
        if 'jp' in lang_select:
            meaning_lst = search_vocab_jp(vocab, exactly_mode)
            if exactly_mode is False:
                meaning_lst_exact = search_vocab_jp(vocab, True)
                if meaning_lst is not None and meaning_lst_exact is not None:
                    meaning_lst = meaning_lst_exact + meaning_lst
                    meaning_lst = remove_repeated_element(meaning_lst)
            furigana_offset = "</br>"
        elif 'en' in lang_select:
            meaning_lst = search_vocab_en(vocab, exactly_mode)
            furigana_offset = ""
        else:
            break
        if meaning_lst is not None:
            # print(search_vocab_en(vocab))
            meaning_text, furigana = text_convert(meaning_lst, vocab)
            if gen_sound is True:
                sound_number = input_text_file_name + '_' + str(vocab_cnt)
                sound_call_name = '[sound:#' + sound_number + '.mp3]'
                text2sound(vocab, sound_number, parent_path, lang_select)
            else:
                sound_call_name = ''
            vocab = '<span style="color:rgb(233, 253, 226); font-size:50px">' \
                    + "<ruby>" + vocab + "<rt>" + furigana_offset \
                    + "</rt></ruby>" + '</span>'
            if furigana == '':
                furigana = vocab
            output.write(vocab + '@' + meaning_text + sound_call_name
                         + '@' + furigana + '\n')
        else:
            fail_output.write(vocab + '\n')
        progress(vocab_cnt+1, len(vocab_lst))
        
        #############################################
        
        # yield "<div>%s</div>\n" % str(vocab)+"\n"
        # yield " " * 1024
         
        percent_int = int((vocab_cnt+1)/(len(vocab_lst))*100)
        yield '<script>document.getElementById("progress_bar").style.width = "'+ str(percent_int) +'%";</script>'
        # yield '<script>document.getElementById("message").textContent = "'+ str(vocab_cnt%4*".") + str((4-vocab_cnt%4)*" ") +'";</script>'
        
        time_per_word = (time.time() - time_capture)
        time_capture = time.time()
        acc_avg_time = (time_per_word + acc_avg_time)/2
        remain_time = str(int((len(vocab_lst)-(vocab_cnt+1))*acc_avg_time))  
        yield '<script>document.getElementById("progress_text").textContent = "Progress: '+ str(vocab_cnt+1) + "/" + str(len(vocab_lst))
        yield '   Remaining Time: ' +  remain_time  + 'sec' +'";</script>'
        time.sleep(1) # hold 100 percent progress
        #############################################
    
    output.close()
     
    ######################################################################
    gen_apkg(parent_path + "/output/" + input_text_file_name +'_output.txt')
    yield "<script>window.location.href = '';</script>"
    # unique_folder = os.path.basename(parent_path)
    # yield "<script>window.location.search = 'loading_end_folder="+unique_folder+"';</script>"    
    ######################################################################

if __name__ == '__main__':
    gen_apkg()
    # main()
