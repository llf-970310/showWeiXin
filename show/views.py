from django.shortcuts import render,redirect
from django.http import response,HttpResponse
from show.models import *
from xlrd import xldate_as_tuple
import datetime,time
from django.core.paginator import *
from django.db.models import *
import numpy as np
# import matplotlib.pyplot as lhwd
import matplotlib.pyplot
from matplotlib.ticker import MultipleLocator
import matplotlib

# Create your views here.
STATIC_NUM = 0

def page_pre_solve(request):
    return render(request,'pre_solve.html')

def finish(request):
    return render(request,'finish.html')

def pre_solve(request):
    import xlrd
    import jieba
    import jieba.analyse
    from PIL import Image
    from wordcloud import WordCloud
    import numpy as np
    import matplotlib.pyplot as lhwd

    # jieba.analyse.set_stop_words("/Users/lhwd/Desktop/project/weixin/main/jieba/extra_dict/self_stop_words.txt")

    def open_xls(rfile="catch.xlsx"):
        try:
            data = xlrd.open_workbook(rfile)
            # wf.write("open successfully !"+'\n')
            print("open successfully !")
            return data
        except:
            # wf.write("open error !")
            print("open error!")

    def excel_msg_byindex1():
        data = open_xls()
        table = data.sheets()[0]
        gongzhong = []
        for rownum in range(1, table.nrows):
            row = table.row_values(rownum)
            if row:
                for i in range(table.ncols):
                    if i == 0:
                        gongzhong.append(row[i])

        newgongzhong = []
        for i in gongzhong:
            if not i in newgongzhong:
                newgongzhong.append(i)

        for i in newgongzhong:
            if (i):
                Dept.objects.create(dept=i)

    def excel_msg_byindex2():
        data = open_xls()
        table = data.sheets()[0]
        gongzhong = []
        yuedu = {}
        dianzan = {}
        count = 1
        for rownum in range(1, table.nrows):
            row = table.row_values(rownum)
            if row:
                try:
                    Passage.objects.create(title=row[2],dianzan=row[5],yuedu=row[4],text=row[6])
                    passagedept = Passage.objects.get(id = count)
                    passagedept.department_id = Dept.objects.get(dept=row[0]).id
                    passagedept.save()
                    try:
                        a = xldate_as_tuple(row[3], 0)
                        y, m, d = a[0:3]
                        if row:
                            #Datetest.objects.create(date=datetime.datetime(y, m, d))
                            passage = Passage.objects.get(id=count)
                            passage.publish_time = datetime.datetime(y, m, d)
                            passage.save()
                    except:
                        ttt = 0



                    for i in range(table.ncols):
                        if i == 0:
                            gongzhong.append(row[i])

                        if i == 4:
                            ftext = open(
                                "./data/text_yueduanddianzan/" + str(count) + ".txt", "w")
                            ftext.write(str(row[4]) + ' ' + str(row[5]))
                            yuedu[count] = row[4]
                            dianzan[count] = row[5]
                            ftext.close()

                        if i == 6:
                            wf.write(str(row[i]) + '\n')
                            ftext = open("./data/all_text/" + str(count) + ".txt", "w")
                            ftext.write(str(row[i]))
                            ftext.close()
                    count += 1
                except:
                    ttt = 0

        # newgongzhong = list(set(gongzhong))
        # for i in newgongzhong:
        #     fgongzhong.write(i + '\n')
        #print(yuedu)
        #print(dianzan)
        print(count)
        newgongzhong = []
        for i in gongzhong:
            if not i in newgongzhong:
                newgongzhong.append(i)
                fgongzhong.write(i + '\n')
        wf.close()
        global STATIC_NUM
        STATIC_NUM = count

    def posseg_textrank():
        r = open("./data/analyse_text_excel.txt", "r").read()
        textrankword = []
        for x, w in jieba.analyse.textrank(r, topK=50, withWeight=True):
            textrankword.append((x, w))
            f2.write(str(x) + '   ' + str(w) + '\n')
            try:
                Keyword.objects.create(word=x,freq=w)
            except:
                ttt = 0

        # ------------------------------将关键词的关联文件取出并存放在txt文件中------------------------------#
        #print(textrankword)
        for i in textrankword:
            #print(i)
            tt = []
            for j in range(1, STATIC_NUM):
                filett = open("./data/all_text/" + str(j) + ".txt", "r")
                text = filett.read()
                # print (text)
                if i[0] in text:
                    try:
                        a = Keyword.objects.get(word=i[0])
                        b = Passage.objects.get(id = j )
                        b.aboutwords.add(a)
                    except:
                        ttt = 0
                    tt.append(j)
            fkey = open("./data/textrankkey_to_text/" + str(i[0]) + ".txt", "w")
            fkey.write(str(tt))
            fkey.close()

        # a = Author.objects.get(id=1)
        # b = Book.objects.get(id=50)
        # b.authors.add(a)
        # ------使用wordcloud云图库对所提取出的关键词进行云图的绘制，记住需要提供可以汉化的ttf，否则显示不了汉字，非常蛋疼！！！------#
        phone_mask = np.array(Image.open("background.jpg", "r"))
        lhwd11 = WordCloud(
            font_path="/Library/Frameworks/Python.framework/Versions/3.5/lib/python3.5/site-packages/matplotlib/mpl-data/fonts/ttf/Yahei.ttf",
            background_color="black", mask=phone_mask).fit_words(textrankword[:50])
        lhwd.axis("off")
        # lhwd.show()
        lhwd11.to_file("./data/textrank_wordcloud.jpg")  # 保存生成的云图

    def main():
        excel_msg_byindex1()
        excel_msg_byindex2()
        wf.close()
        posseg_textrank()  # 通过textrank算法进行相应的关键词分词，同时显示关键词的词频

    wf = open("./data/analyse_text_excel.txt", "w")
    f = open("./data/analyse_result_tfidf.txt", "w")
    f1 = open("./data/analyse_result_freq.txt", "w")
    f2 = open("./data/analyse_result_textrank.txt", "w")
    fgongzhong = open("./data/gongzhong/gongzhong.txt", "w")
    main()
    f.close()
    f1.close()
    f2.close()

    """
        tf－idf算法    http://baike.baidu.com/link?url=XNoEF6_j7kL1AX1Mwy5m7BP4e4wKrWiHSNJ5hjeGOELl3KMxxlPZuC_qXfRrBPczn8yvN6zQjXeVZCI3yUjQP_
    """
    return redirect('finish')

def show_keywords(request):
    keywords = Keyword.objects.all()
    for keyword in keywords:
        keyword.releate = keyword.passage_set.all().count()
        keyword.save()
    #Keyword.objects.values('word').annotate(Count('passage')).order_by('id')
    paginator = Paginator(keywords, 18)
    page = request.GET.get('page')
    try:
        keywords = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        keywords = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        keywords = paginator.page(paginator.num_pages)
    page = True
    return render(request,'main.html',locals())

def show_keyword_passage(request,page1):
    keyword = Keyword.objects.get(id=page1)
    passages = keyword.passage_set.all().order_by('-dianzan')
    paginator = Paginator(passages, 100)
    page = request.GET.get('page')
    try:
        passages = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        passages = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        passages = paginator.page(paginator.num_pages)
    page = True
    return render(request,'keyword_passage.html',locals())

def passage_detail(request,page):
    passage = Passage.objects.get(id = page)
    return render(request,'passage_detail.html',locals())

def passage_all_analyse(request):
    passages03 = Passage.objects.filter(publish_time__year='2016',publish_time__month='03')
    passages031 = passages03.filter(publish_time__day='2')
    passages04 = Passage.objects.filter(publish_time__year='2016', publish_time__month='04')
    passages05 = Passage.objects.filter(publish_time__year='2016', publish_time__month='05')
    passages06 = Passage.objects.filter(publish_time__year='2016', publish_time__month='06')
    passagesall = Passage.objects.filter(publish_time__year='2016')
    passagesum = Passage.objects.all()
    dept = Dept.objects.all()
    sumdianzan = 0
    sumyuedu = 0
    for passage in passagesum:
        sumdianzan += passage.dianzan
        sumyuedu += passage.yuedu
    passageshot = Passage.objects.all().order_by('-dianzan')[:10]
    passagesyuedu = Passage.objects.all().order_by('-yuedu')[:10]
    return render(request,'all_analyse.html',locals())

def passage_part_analyse(request):
    # depts = Dept.objects.all()
    # for dept in depts:
    ptext =Dept.objects.values('dept').annotate(Count('passage')).order_by('-passage__count')[:20]
    pyuedu = Passage.objects.values('department__dept').annotate(Sum('yuedu')).order_by('-yuedu__sum')[:20]
    pdianzan = Passage.objects.values('department__dept').annotate(Sum('dianzan')).order_by('-dianzan__sum')[:20]
    keywords1 = Keyword.objects.filter(word='1')
    #keywords2 = Keyword.objects.filter(word='2')
    passages2 = Passage.objects.values('aboutwords__word').annotate()
    return render(request,'part_analyse.html',locals())

def tophot(request):
    monthhot3 = Passage.objects.filter(publish_time__month='3').order_by('-passagehot')[:50]
    monthhot4 = Passage.objects.filter(publish_time__month='4').order_by('-passagehot')[:50]
    monthhot5 = Passage.objects.filter(publish_time__month='5').order_by('-passagehot')[:50]
    monthhot6 = Passage.objects.filter(publish_time__month='6').order_by('-passagehot')[:50]
    monthhotall = Passage.objects.all().order_by('-yuedu')[:50]
    # passages = Passage.objects.all()
    # for passage in passages:
    #     passage.departmentname = Dept.objects.get(id = passage.department_id).dept
    #     passage.save()
    # passages = Passage.objects.all()
    # for passage in passages:
    #     passage.passagehot = passage.dianzan * 10 + passage.yuedu
    #     passage.save()
    return render(request,'tophot.html',locals())

# def passage_tendency(request):
#     passages3 = Passage.objects.filter(publish_time__month='3')
#     passages4 = Passage.objects.filter(publish_time__month='4')
#     passages5 = Passage.objects.filter(publish_time__month='5')
#     passages6 = Passage.objects.filter(publish_time__month='6')
#
#     return render(request,'passage_tendency.html',locals())

def huitu(request):
    matplotlib.use('Agg')
    # x = np.arange(250, 20250, 500)
    # y = np.arange(0, 20000, 500)
    # xmajorLocator = MultipleLocator(1000);
    # ymajorLocator = MultipleLocator(1000);
    # lhwd.plot(x, y, 'r--', linewidth=2)
    # lhwd.xlim(-2000, 20000)
    # lhwd.ylim(-0.1, 0.30)
    lhwd1 = matplotlib.pyplot
    lhwd2 = matplotlib.pyplot
    lhwd3 = matplotlib.pyplot
    lhwd4 = matplotlib.pyplot
    def month3():
        for i in range(1,32):
            y1.append(passages3.filter(publish_time__day= i ).count())
        xmajorLocator = MultipleLocator(1);
        ymajorLocator = MultipleLocator(10);
        lhwd1.plot(x1, y1, 'r', linewidth=1)
        lhwd1.xlim(0, 31)
        lhwd1.ylim(0, 100)
        lhwd1.rc('font', size=8)  # 设置全局字体大小
        for i in range(0,31):  #设置坐标值
            lhwd1.text(x1[i],y1[i],y1[i])

        lhwd1.grid()  #开启网格线
        ax = lhwd1.gca()
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.xaxis.set_ticks_position('bottom')
        ax.spines['bottom'].set_position(('data', 0))
        ax.yaxis.set_ticks_position('left')
        ax.spines['left'].set_position(('data', 0))
        ax.xaxis.set_major_locator(xmajorLocator)
        ax.yaxis.set_major_locator(ymajorLocator)
        fig = lhwd1.gcf()
        fig.savefig('static/march.png',dpi=200)
        lhwd1.close()

    def month4():
        for i in range(1, 31):
            y2.append(passages4.filter(publish_time__day=i).count())
        xmajorLocator = MultipleLocator(1);
        ymajorLocator = MultipleLocator(10);
        lhwd2.plot(x2, y2, 'r', linewidth=1)
        lhwd2.xlim(0, 30)
        lhwd2.ylim(0, 100)
        lhwd2.rc('font', size=8)  # 设置全局字体大小
        for i in range(0, 30):  # 设置坐标值
            lhwd2.text(x2[i], y2[i], y2[i])

        lhwd2.grid()  # 开启网格线
        ax = lhwd2.gca()
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.xaxis.set_ticks_position('bottom')
        ax.spines['bottom'].set_position(('data', 0))
        ax.yaxis.set_ticks_position('left')
        ax.spines['left'].set_position(('data', 0))
        ax.xaxis.set_major_locator(xmajorLocator)
        ax.yaxis.set_major_locator(ymajorLocator)
        fig = lhwd2.gcf()
        fig.savefig('static/april.png', dpi=200)
        lhwd2.close()

    def month5():
        for i in range(1, 32):
            y3.append(passages5.filter(publish_time__day=i).count())
        xmajorLocator = MultipleLocator(1);
        ymajorLocator = MultipleLocator(10);
        lhwd3.plot(x3, y3, 'r', linewidth=1)
        lhwd3.xlim(0, 31)
        lhwd3.ylim(0, 100)
        lhwd3.rc('font', size=8)  # 设置全局字体大小
        for i in range(0, 31):  # 设置坐标值
            lhwd3.text(x3[i], y3[i], y3[i])

        lhwd3.grid()  # 开启网格线
        ax = lhwd3.gca()
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.xaxis.set_ticks_position('bottom')
        ax.spines['bottom'].set_position(('data', 0))
        ax.yaxis.set_ticks_position('left')
        ax.spines['left'].set_position(('data', 0))
        ax.xaxis.set_major_locator(xmajorLocator)
        ax.yaxis.set_major_locator(ymajorLocator)
        fig = lhwd3.gcf()
        fig.savefig('static/may.png', dpi=200)
        lhwd3.close()

    def month6():
        for i in range(1, 31):
            y4.append(passages6.filter(publish_time__day=i).count())
        xmajorLocator = MultipleLocator(1);
        ymajorLocator = MultipleLocator(10);
        lhwd4.plot(x4, y4, 'r', linewidth=1)
        lhwd4.xlim(0, 30)
        lhwd4.ylim(0, 100)
        lhwd4.rc('font', size=8)  # 设置全局字体大小
        for i in range(0, 30):  # 设置坐标值
            lhwd4.text(x4[i], y4[i], y4[i])

        lhwd4.grid()  # 开启网格线
        ax = lhwd4.gca()
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.xaxis.set_ticks_position('bottom')
        ax.spines['bottom'].set_position(('data', 0))
        ax.yaxis.set_ticks_position('left')
        ax.spines['left'].set_position(('data', 0))
        ax.xaxis.set_major_locator(xmajorLocator)
        ax.yaxis.set_major_locator(ymajorLocator)
        fig = lhwd4.gcf()
        fig.savefig('static/june.png', dpi=200)
        lhwd4.close()
    passages3 = Passage.objects.filter(publish_time__month='3')
    passages4 = Passage.objects.filter(publish_time__month='4')
    passages5 = Passage.objects.filter(publish_time__month='5')
    passages6 = Passage.objects.filter(publish_time__month='6')

    x1 = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31']
    x2 = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
          '21', '22', '23', '24', '25', '26', '27', '28', '29', '30']
    x3 = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
          '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31']
    x4 = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
          '21', '22', '23', '24', '25', '26', '27', '28', '29', '30']
    y1 = []
    y2 = []
    y3 = []
    y4 = []
    month3()
    month4()
    month5()
    month6()
    return render(request, 'passage_tendency.html', locals())

def releated(request):
    keywords = Keyword.objects.all()
    array = []

    for keyword in keywords:
        array.append(keyword.word)

    # for i in range(0,50):
    #     for j in range(i+1,50):
    #         Relate.objects.create(word1 = array[i],word2 = array[j])

    for i in range(0,50):
        passage1 = Passage.objects.filter(aboutwords__word=array[i])
        for j in range(i+1,50):
            passage2 = Passage.objects.filter(aboutwords__word=array[j])
            for passage in passage1:
                if(passage2.filter(title=passage.title)):
                    relate1 = Relate.objects.get(word1=array[i],word2=array[j])
                    relate1.relation +=1
                    relate1.save()
    print(array)
    return render(request,'related.html',locals())

def related_sort(request):
    related = Keyword.objects.all()
    count = 0
    for relatetest in related:
        word = relatetest.word
        relate = Relate.objects.filter(word1=word).order_by('-relation')[:10]
        #relate = relate.filter(relate.relation>=300)
        for relatetest1 in relate:
            if(relatetest1.relation>=10):
                print(relatetest1.word1 + '  ' + relatetest1.word2 + '  ' + str(relatetest1.relation) )
                count+=1
    print(count)
    return render(request,'main.html',locals())