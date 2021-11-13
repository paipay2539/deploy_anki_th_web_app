from typing import Tuple
from django.shortcuts import render

# Create your views here.

#from .models import Post

input_text_post = 0
output_exist = 0

import sys 
sys.path.append('./reference')
import ankiTH

from django.shortcuts import redirect

from django.http import HttpResponse

def home_page(request):
    # return HttpResponse("w")
    return render(request, "card_generator/home.html")

def guide_page(request):
    # return HttpResponse("w")
    return render(request, "card_generator/guide.html")

def try_it_page(request):
    # return HttpResponse("w")
    import os
    import sys 
    import shutil
    import glob

    file_path = os.path.realpath('./reference')
    print(file_path)

    global input_text_post, output_exist
    
    
    

    
    
    output_exist = request.session.get('output_exist')
    if output_exist is None:
        request.session['output_exist'] = 0  
        
    if output_exist == 1:
        request.session['output_exist'] = 0
        output           = open('./reference/data/output/text_temp_output.txt', "r", encoding="utf8")
        fail_output      = open('./reference/data/output/text_temp_fail_output.txt', "r", encoding="utf8")
        output_text      = output.read().strip('\n')
        fail_output_text = fail_output.read().strip('\n')
        output_dict = {"input_text_post": input_text_post, 
                        "output_text": output_text,
                        "fail_output_text": fail_output_text}
        output.close()
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

            from django.http import StreamingHttpResponse
            output_exist = 1
            
            input_text_post = request.POST['input_text']
            lang_status_post       = "jp" if request.POST['button_jp_th_status'] == "ON" else "en"
            sound_status_post      = True if request.POST['sound_status'] == "ON" else False
            exact_find_status_post = True if request.POST['exact_find_status'] == "ON" else False

            input_text_temp = open('./reference/data/input/text_temp.txt', "w", encoding="utf8")
            input_text_temp.write(input_text_post) 
            input_text_temp.close()

            resp = StreamingHttpResponse(ankiTH.django_request(  
                                    input_text   = "./reference/data/input/text_temp.txt", 
                                    gen_sound    = sound_status_post, 
                                    exactly_mode = exact_find_status_post, 
                                    lang_select  = lang_status_post))
            return resp

        if 'download_text' in request.POST:
            output_path = './reference/data/output/text_temp_output.txt'
            output = open(output_path, "r", encoding="utf8")
            response = HttpResponse(output.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(output_path)
            output.close()
            return response

        if 'download_mp3' in request.POST:
            dir_name = './reference/data/output/sound/'
            output_filename = './reference/data/output/sound_zip_upload'
            ankiTH.ankiTH("./reference/data/input/text_temp", gen_sound=True, exactly_mode=False, lang_select="jp")
            shutil.make_archive(output_filename, 'zip', dir_name)

            shutil.rmtree(dir_name)
            os.mkdir(dir_name)

            output_path = output_filename + ".zip"
            output = open(output_path, "rb")
            response = HttpResponse(output, content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(output_path) 
            output.close()
            return response
            # 'attachment; filename=' มันจะโหลดไฟล์เลย
            # 'inline; filename=' มันจะพยายามเปิดบน browser ก่อนเช่นพวก pdf
            # ถ้าไฟล์เปิดบน browser ไม่ได้ มันจะโหลดเองทั้ง attachment และ inline

        if 'download_apkg' in request.POST:
            output_path = "./reference/data/output/output.apkg"
            output = open(output_path, "rb")
            response = HttpResponse(output, content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(output_path) 
            output.close()
            return response
            
    return render(request, "card_generator/try_it.html")

def shared_deck_page(request):
    # return HttpResponse("w")
    return render(request, "card_generator/shared_deck.html")

def generate_output(request):
    print("pressed")
    return HttpResponse("w")
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