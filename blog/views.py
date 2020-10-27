from django.shortcuts import render,redirect,get_object_or_404
from django.core.files.storage import FileSystemStorage
from keras.models import load_model
from PIL import Image
import numpy as np
import sqlite3

from .models import Selection
from .forms import ClothForm
from .models import Cloth
from .models import Recommend
# render는 데이터 값을 반아온뒤 html로 데이터를 보내기 위한 함수

# Create your views here.

#결과 값을 render 함수를 통해 요청을 index.html 문서로 리턴
def index(request):
    return render(request, 'index.html')



def upload(request):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name,uploaded_file)
        context['url'] = fs.url(name)
    return render(request,'upload.html',context)




def upload_cloth(request):
    if request.method == 'POST':
        form = ClothForm(request.POST, request.FILES)
        request.session["closet_file"] = str(request.FILES['closet'])

        print("세션 성공", request.session["closet_file"])
        if form.is_valid():
            form.save()
            category = AI_check(request.session["closet_file"])
            request.session["category"] = category
            print("AI Check result :", category)
            return render(request,'save_cloth.html')
    else:
        form = ClothForm()
        return render(request, 'upload_cloth.html',{
            'form' : form
        })

def save_cloth(request):
    if request.method == 'POST':
        conn = sqlite3.connect("C:/Django/pjt/myfashion/db.sqlite3")
        c = conn.cursor()

        print( request.POST["category"] )
        label, num = category_to_label_and_num(request.POST["category"])
        category = "'"+request.POST["category"]+"','"+label+"','"+num+"'"
        path = "'"+"clothes/closets/"+request.session["closet_file"]+"'"
        update = "UPDATE blog_cloth SET (Category, label, category_num) = (" + category + ") WHERE closet = "+path
        print(update)
        c.execute(update)
        conn.commit()

        return redirect('cloth_list')
    else:
        form = ClothForm()
    return render(request, 'save_cloth.html', {
        'form': form
    })

def AI_check(file):
    X =[]
    categories = ['long_blouse_check', 'long blouse_none', 'long blouse_pattern', 'long dress_long sleeves',
                  'long dress_short sleeves', 'long pants_jean', 'long pants_cotton', 'long shirt_check',
                  'long shirt_none', 'long shirt_pattern', 'long skirt_A', 'long skirt_asymmetric',
                  'long skirt_H', 'long sleeve_none', 'long sleeve_print', 'long sleeve_stripe',
                  'mini dress_long sleeves', 'mini dress_short sleeves', 'short blouse_check', 'short blouse_none',
                  'short blouse_pattern', 'short pants_jean', 'short pants_cotton', 'short shirt_check',
                  'short shirt_none', 'short shirt_pattern', 'short skirt_A', 'short skirt_asymmetric',
                  'short skirt_H', 'short sleeve_none', 'short sleeve_print', 'short sleeve_stripe',
                  'sleeveless_none', 'sleeveless_print', 'sleeveless_stripe']


    model = load_model('C:/Django/pjt/myfashion/blog/fashion_best_model.h5')

    img_path = ["C:/Django/pjt/myfashion/media/clothes/base.png",
                "C:/Django/pjt/myfashion/media/clothes/closets/" + str(file)]
    print(str(file))

    for fname in img_path:
        img = Image.open(fname)
        img = img.convert("RGB")
        img = img.resize((64, 64))
        in_data = np.asarray(img)
        in_data = in_data.astype("float") / 256
        X.append(in_data)

    X = np.array(X)
    pre = model.predict(X)

    for i, p in enumerate(pre):
        y = p.argmax()
        category = categories[y]
    return category

def category_to_label_and_num(category):

    categories = ['long shirt_none', 'long shirt_check', 'long shirt_pattern', 'short shirt_none', 'short shirt_check', 'short shirt_pattern',
                  'long blouse_none', 'long_blouse_check', 'long blouse_pattern', 'short blouse_none', 'short blouse_check', 'short blouse_pattern',
                  'long sleeve_none', 'long sleeve_stripe', 'long sleeve_print', 'short sleeve_none', 'short sleeve_stripe', 'short sleeve_print',
                  'sleeveless_none', 'sleeveless_stripe', 'sleeveless_print', 'long pants_jean', 'long pants_cotton',
                  'short pants_jean', 'short pants_cotton', 'long skirt_H', 'long skirt_A', 'long skirt_asymmetric',
                  'short skirt_H', 'short skirt_A', 'short skirt_asymmetric','long dress_long sleeves', 'long dress_short sleeves',
                  'short dress_long sleeves', 'short dress_short sleeves']
    i=0
    for cate in categories:
        i = i+1
        if category == cate:
            num = str(i)
            break

    for cate in categories[0:21]:
        if category == cate:
            label = "T"
            return label, num

    for cate in categories[21:31]:
        if category == cate:
            label = "B"
            return label, num

    for cate in categories[31:]:
        if category == cate:
            label = "D"
            return label, num

def cloth_list(request):
    clothes = Cloth.objects.all()
    ##############
    qs2 = Selection.objects.get(v_id=1)
    qs2.v_id = 1
    qs2.v_up = 0
    qs2.v_down = 0

    qs2.save()
    ###########
    return render(request,'cloth_list.html',{
        'clothes' : clothes,
    })



def result(request,cloth_id ):
    choices = get_object_or_404(Cloth, pk = cloth_id )
    if choices.label == 'T':
        qs3 = Selection.objects.get(v_id=1)
        qs3.v_id=1
        qs3.v_up=choices.category_num
        qs3.v_up_img=choices.closet.url
        qs3.save()

    if choices.label == 'B':
        qs3 = Selection.objects.get(v_id=1)
        qs3.v_id=1
        qs3.v_down=choices.category_num
        qs3.v_down_img = choices.closet.url
        qs3.save()

    rT = Cloth.objects.filter(label='B')
    rB = Cloth.objects.filter(label='T')



    return render(request,'result.html',{
        'choices' : choices,
        'rT': rT,
        'rB': rB
    })


def Rec(request):
    rec = Recommend.objects.all()
    rec_row = len(rec)

    print("***************",rec_row)
    qs = Selection.objects.get(v_id=1)
    if qs.v_up !=0 :
        codi = Recommend.objects.filter(label_T= qs.v_up).values()& Recommend.objects.filter(label_B= request.POST["category_num"]).values()

    if qs.v_down !=0 :
        codi = Recommend.objects.filter(label_T=request.POST["category_num"]).values() & Recommend.objects.filter(label_B= qs.v_down).values()

    return render(request,'test.html',{
        'codi' : codi,
    })


def cloth_list1(request):
    clothes = Cloth.objects.filter(label='T')
    ##############
    qs2 = Selection.objects.get(v_id=1)
    qs2.v_id = 1
    qs2.v_up = 0
    qs2.v_down = 0

    qs2.save()
    ###########
    return render(request,'cloth_list.html',{
        'clothes' : clothes,
    })

def cloth_list2(request):
    clothes = Cloth.objects.filter(label='B')
    ##############
    qs2 = Selection.objects.get(v_id=1)
    qs2.v_id = 1
    qs2.v_up = 0
    qs2.v_down = 0

    qs2.save()
    ###########
    return render(request,'cloth_list.html',{
        'clothes' : clothes,
    })

def cloth_list3(request):
    clothes = Cloth.objects.filter(label='D')
    ##############
    qs2 = Selection.objects.get(v_id=1)
    qs2.v_id = 1
    qs2.v_up = 0
    qs2.v_down = 0

    qs2.save()
    ###########
    return render(request,'cloth_list.html',{
        'clothes' : clothes,
    })