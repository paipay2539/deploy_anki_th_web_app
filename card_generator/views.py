from typing import Tuple
from django.shortcuts import render

# Create your views here.

#from .models import Post


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

    file_path = os.path.realpath('../reference')
    print(file_path)

    
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
            if request.POST['button_jp_th_status'] == "ON":
                lang = "jp"
            else:
                lang = "en"
            input_text_post = request.POST['input_text']  
            input_text_temp = open('../reference/data/input/text_temp.txt', "w", encoding="utf8")
            input_text_temp.write(input_text_post) 
            input_text_temp.close()
            ankiTH.ankiTH("../reference/data/input/text_temp", gen_sound=False, exactly_mode=False, lang_select=lang)
            output = open('../reference/data/output/text_temp_output.txt', "r", encoding="utf8")
            output_text = output.read().strip('\n')
            output_dict = {"input_text_post": input_text_post, "output_text": output_text}
            output.close()
            return render(request, "card_generator/try_it.html", output_dict)

        if 'download_text' in request.POST:
            output_path = '../reference/data/output/text_temp_output.txt'
            output = open(output_path, "r", encoding="utf8")
            response = HttpResponse(output.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(output_path)
            output.close()
            return response

        if 'download_mp3' in request.POST:
            dir_name = '../reference/data/output/sound/'
            output_filename = '../reference/data/output/sound_zip_upload'
            ankiTH.ankiTH("../reference/data/input/text_temp", gen_sound=True, exactly_mode=False, lang_select="jp")
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


            
    return render(request, "card_generator/try_it.html")

def shared_deck_page(request):
    # return HttpResponse("w")
    return render(request, "card_generator/shared_deck.html")

def generate_output(request):
    print("pressed")
    return HttpResponse("w")
    return render(request, "card_generator/try_it.html", {"output_text":"hello"})