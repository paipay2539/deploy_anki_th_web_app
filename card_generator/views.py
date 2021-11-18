from typing import Tuple
from django.shortcuts import render

# Create your views here.

#from .models import Post

import os
import sys 
import shutil
import glob
from datetime import datetime
import time

sys.path.append('./reference')
import ankiTH

from django.shortcuts import redirect
from django.http import HttpResponse
from django.http import StreamingHttpResponse

from .models import Post

def home_page(request):
    # return HttpResponse("w")
    return render(request, "card_generator/home.html")

def guide_page(request):
    # return HttpResponse("w")
    return render(request, "card_generator/guide.html")

def try_it_page(request):
    
    ##################### identity #############################
    
    print(request.POST.get('output_address_post'))

    ip_address = str(request.META.get("REMOTE_ADDR")).replace('.','_')
    print("request.META.get('REMOTE_ADDR')", ip_address)
    identity_folder = './reference/data/' + ip_address + '/'
    
    ip_address_list = request.session.get('ip_address_list')
    if ip_address_list is None:
        request.session['ip_address_list'] = {ip_address:0}
    else:
        if ip_address not in ip_address_list:
            request.session['ip_address_list'][ip_address] = 0
            if os.path.exists(identity_folder):
                print("identity folder found", identity_folder)
                # shutil.rmtree(identity_folder)
                os.mkdir(identity_folder)
                
    ###################################################################

    file_path = os.path.realpath('./reference')
    print(file_path)
        
    output_exist = request.session.get('output_exist')
    if output_exist is None:
        request.session['output_exist'] = 0  
        
    if output_exist == 1:
        request.session['output_exist'] = 0
        input_text_post        = request.session.get('input_text_post')
        lang_status_post       = request.session.get('lang_status_post')
        sound_status_post      = request.session.get('sound_status_post')
        exact_find_status_post = request.session.get('exact_find_status_post')
        
        output           = open('./reference/data/output/text_temp_output.txt', "r", encoding="utf8")
        fail_output      = open('./reference/data/output/text_temp_fail_output.txt', "r", encoding="utf8")
        output_text      = output.read().strip('\n')
        fail_output_text = fail_output.read().strip('\n')
        output_dict = { "input_text_post"   : input_text_post, 
                        "output_text"       : output_text,
                        "fail_output_text"  : fail_output_text,
                        "lang_status"       : lang_status_post,
                        "sound_status"      : sound_status_post,
                        "exact_find_status" : exact_find_status_post,
                        "ip_address"        : ip_address}
        output.close()
        fail_output.close()
        request.session['output_dict'] = output_dict
        return render(request, "card_generator/try_it.html", output_dict)

    
    if request.method == 'GET':
        print("welcome to try_it_page")
    elif request.method == 'POST':
        print("post")
        for key, value in request.POST.items():
            print('Key: %s' % (key) ) 
            print('Value %s' % (value) )

        # ต้องเช็ค input ว่ามีอยู่ใน post จริงมั้ย เพราะต้องเป็น post จากปุ่มอื่น อาจจะไม่มีแล้ว error
        # ถ้าไม่เคยกดปุ่ม หรือไม่ใส่ text จะเป็นแบบนี้
        # request.POST['bautton_jp_th_status'] == "", request.POST['input_text'] == "" 
        # 'input_text' in request.POST ไว้เช็คว่ามี DOM input นี้อยู่รึป่าว

        if 'input_text' in request.POST: # เอาไว้แยกได้ว่า กดปุ่มไหนมา

            lang_status_post       = "jp" if request.POST['button_jp_th_status'] == "ON" else "en"
            sound_status_post      = True if request.POST['sound_status'] == "ON" else False
            exact_find_status_post = True if request.POST['exact_find_status'] == "ON" else False
            input_text_post        = request.POST['input_text']  
            
            request.session['output_exist'] = 1
            request.session['input_text_post'] = input_text_post
            request.session['lang_status_post'] = lang_status_post
            request.session['sound_status_post'] = sound_status_post
            request.session['exact_find_status_post'] = exact_find_status_post

            input_text_temp = open('./reference/data/input/text_temp.txt', "w", encoding="utf8", newline='')
            input_text_temp.write(input_text_post) 
            input_text_temp.close()

            abc = open('./reference/data/input/123.txt', "w")
            abc.close()
            
            sound_path = './reference/data/output/sound/'
            shutil.rmtree(sound_path)
            os.mkdir(sound_path)
            sound_temp_file = open(sound_path+'#text_temp_0.mp3', "w")
            sound_temp_file.close()

            resp = StreamingHttpResponse(ankiTH.django_request(  
                                    input_text   = "./reference/data/input/text_temp.txt", 
                                    gen_sound    = sound_status_post, 
                                    exactly_mode = exact_find_status_post, 
                                    lang_select  = lang_status_post))
            return resp

        if 'download_txt' in request.POST and 'output_address_post' in request.POST:
            output_path = './reference/data/output/text_temp_output.txt'
            output = open(output_path, "r", encoding="utf8")
            response = HttpResponse(output, content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(output_path)
            output.close()
            return response

        if 'download_mp3' in request.POST and 'output_address_post' in request.POST:
            dir_name = './reference/data/output/sound/'
            output_filename = './reference/data/output/sound_zip_upload'
            shutil.make_archive(output_filename, 'zip', dir_name)
            output_path = output_filename + ".zip"
            output = open(output_path, "rb")
            response = HttpResponse(output, content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(output_path) 
            output.close()
            return response
            # 'attachment; filename=' มันจะโหลดไฟล์เลย
            # 'inline; filename=' มันจะพยายามเปิดบน browser ก่อนเช่นพวก pdf
            # ถ้าไฟล์เปิดบน browser ไม่ได้ มันจะโหลดเองทั้ง attachment และ inline

        if 'download_apkg' in request.POST and 'output_address_post' in request.POST:
            output_path = "./reference/data/output/output.apkg"
            output = open(output_path, "rb")
            response = HttpResponse(output, content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(output_path) 
            output.close()
            return response
            
        
        if 'deck_name' in request.POST and 'output_address_post' in request.POST:
            auth_name_get   = request.POST.get("auth_name")
            deck_name_get   = request.POST.get("deck_name")
            comment_get     = request.POST.get("comment")
            
            lang_log_get    = request.POST.get("lang_log")
            sound_log_get   = request.POST.get("sound_log")
            exact_log_get   = request.POST.get("exact_log")
            timestamp_get   = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M')
            
            vocab_list      = request.session.get('output_dict')['output_text'].split("\n")
            output_list = []
            for vocab in vocab_list:
                if "<ruby>" in vocab and "<rt>" in vocab:
                    output_list.append(vocab[vocab.find("<ruby>")+len("<ruby>"):vocab.find("<rt>")])
            
            output_box_get  = ",   ".join(output_list)
            output_num_get  = len(output_list)
            
            output_path     = "./reference/data/output/output.apkg"
            output_apkg     = open(output_path, "rb")
            apkg_file_get   = output_apkg.read()
            output_apkg.close()
            # output_apkg   = open(output_path, "wb")
            # output_apkg.write(output_apkg.read())
            
            id_list = Post.objects.all().values_list('id', flat=True)
            this_id = 1 # ถ้าเราไม่ใส่อันนี้มันจะรันต่อจากตัวมากที่สุด
            while this_id in id_list:
                this_id = this_id + 1
            
            created_post = Post.objects.create( id          = this_id, 
                                                auth_name   = auth_name_get,
                                                deck_name   = deck_name_get,
                                                comment     = comment_get,
                                                output_box  = output_box_get,
                                                output_num  = output_num_get,
                                                apkg_file   = apkg_file_get,
                                                lang_log    = lang_log_get,
                                                sound_log   = sound_log_get,
                                                exact_log   = exact_log_get,
                                                timestamp   = timestamp_get )
            
            
            output_dict  = request.session.get('output_dict')
            return render(request, "card_generator/try_it.html", output_dict)

    return render(request, "card_generator/try_it.html")

def shared_deck_page(request):
    
    all_posts = Post.objects.all() # for i in all_posts จะได้ เหมือน get id
    for id, post in enumerate(all_posts):
        # post.delete()
        if id in ["1000","999"]:
            post.delete()
        pass
    
    args = { 'all_posts':all_posts }
    if "download_this_id" in request.POST:
        
        ip_address = str(request.META.get("REMOTE_ADDR")).replace('.','_')
        
        # single_post = Post.objects.get(id=3) # เวลาใช้ให้ dot ไปเลย เช่น single_post.comment single_post.id
        output_path = './reference/data/output/output_shared_'+ip_address+'.apkg'
        
        request_id = request.POST.get("download_this_id")
        single_post = Post.objects.get(id=request_id)
        
        output_apkg   = open(output_path, "wb") 
        output_apkg.write(single_post.apkg_file)
        output_apkg.close()
        
        output_apkg   = open(output_path, "rb") 
        response = HttpResponse(output_apkg, content_type="application/vnd.ms-excel")
        response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(output_path) 
        output_apkg.close()
        os.remove(output_path)
        
        return response    
    
    return render(request, "card_generator/shared_deck.html", args)

def generate_output(request):
    print("pressed")
    return render(request, "card_generator/try_it.html", {"output_text":"hello"})

'''
from django.views.decorators.http import condition
from django.http import StreamingHttpResponse
import time
@condition(etag_func=None)
def stream_response(request):
    resp = StreamingHttpResponse(stream_response_generator(request))
    return resp

def stream_response_generator(request):
    yield "<html><body>\n"
    for x in range(1,5):
        yield "<div>%s</div>\n" % x
        yield " " * 1024  # Encourage browser to render incrementally
        time.sleep(0.5)
    yield "</body></html>\n"
    yield "<script>window.location.href = 'try_it/output';</script>"
    return render(request, "card_generator/guide.html")
'''