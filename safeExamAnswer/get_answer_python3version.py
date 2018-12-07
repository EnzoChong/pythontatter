# -*- coding:utf8 -*_

import sys
import json 
import urllib
import urllib.request
from bs4 import BeautifulSoup

question_list = []
exam_post_data = {
        "runpage": 2,
        "page": 1,
        "direction": '',
        "tijiao": 0,
        "postflag": 1,
        "autosubmit": 0
}
exam_url = "http://222.197.182.137/redir.php?catalog_id=6&cmd=dati"
exam_head = {
        "Host":"222.197.182.137",
        "Connection": "keep-alive",
        "Cache-Control": "max-age=0",
        "Origin": "http://222.197.182.137",
        "Upgrade-Insecure-Requests": 1,
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Mobile Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Referer": "http://222.197.182.137/redir.php?catalog_id=6&cmd=dati",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Cookie": ""
}

def get_question():
    for page in range(0, 5):
        exam_post_data['runpage'] = page + 1
        req = urllib.request.Request(url=exam_url, data=urllib.parse.urlencode(exam_post_data).encode(encoding='UTF8'), headers=exam_head)
        res = urllib.request.urlopen(req)
        bsObj = BeautifulSoup(res.read(), "html.parser")
        qlist = bsObj.findAll('div', {'class':'shiti'})
        for q in qlist:
            question_list.append(q.text.encode("utf8"))

answer_url = "https://www.asklib.com/s/"
answer_head = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Mobile Safari/537.36",
}
answer_list = []

def get_query_ans(words):
        query = urllib.parse.quote(words)
        req = urllib.request.Request(url=answer_url + query, headers=answer_head)
        res = urllib.request.urlopen(req)
        bsObj = BeautifulSoup(res.read(), "html.parser")
        qlist = bsObj.findAll('a', {'class':'list-a'})
        if len(qlist) == 0:
                return {}
        
        ans_url = "https://www.asklib.com" + qlist[0]['href']
        req2 = urllib.request.Request(url=ans_url, headers=answer_head)
        res = urllib.request.urlopen(req2)
        bsObj = BeautifulSoup(res.read(), "html.parser")
        desc_list = bsObj.findAll('div', {'class': 'check_title'})
        if len(desc_list) == 0:
                return {}
        ans_list = bsObj.findAll('div', {'class':'answer_all'})
        if len(ans_list) == 0:
                return {}
        return {"desc": desc_list[0].text.strip(), "answer": ans_list[0].text.strip().replace('\n', '')}

def get_answers():
    index = 1
    for que in question_list:   
        # 这里的que是byte类型字符
        node = get_query_ans(que)
        if len(node) == 0:
            node = {"index": index, "desc": "没找到答案", "answer": ""}
        else:
            node["index"] = index
        print ("第" + str(node['index']) + "题:" + node["desc"])
        print (node["answer"])
        print ("")
        index += 1

if __name__ == "__main__":
        if len(sys.argv) < 2:
                print ("未输入cookie")
                exit()
        exam_head["Cookie"] = sys.argv[1]
        get_question()
        get_answers()