#!/usr/bin/env python
# -*- coding:utf-8 -*-
import tornado.ioloop
import tornado.web
import json
from pypinyin import pinyin, lazy_pinyin, Style
from name_set import get_source


def check_pinyin(name, constrain):
    for i in lazy_pinyin(name):
        if i in constrain:
            return True
    return False


def check_init(name, constrain):
    for i in pinyin(name, style=Style.FIRST_LETTER):
        if i in constrain:
            return True
    return False


def check_character(name, constrain):
    for i in name:
        if i in constrain:
            return True
    return False

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, World")


# 访问: http://localhost:8888/story/sishen232
# 显示:U get story id is sishen232
class StoryHandler(tornado.web.RequestHandler):
    def get(self, story_id):

        self.write("U get story id is " + story_id)

# 取名
class GenNameHandler(tornado.web.RequestHandler):
    def get(self):
        reqParams = self.get_arguments("json")
        print("reqParams:", reqParams)
        params = reqParams[0]
        paramsObj = json.loads(params)

        gender = paramsObj["gender"]
        lastName = paramsObj["lastName"]
        source = paramsObj["source"]
        name_ch_count = paramsObj["name_ch_count"]
        duplicate = paramsObj["replicate"]

        success_code="000"
        status = "success"
        success_msg="成功"

        result = {
            "nameList": [
                {"name": "晨霞", "sentence": "晨霞出沒弄丹闕，春雨依微自甘泉。"},
                {"name": "春雨", "sentence": "春雨依微春尚早，長安貴遊愛芳草。"}
            ],
            "retCode": success_code,
            "retMsg": success_msg,
            "status": status
                  }

        # 长辈姓名--删掉所有读音相同的字--例：加入“伟”，则结果中不会出现任何读音为we的字（为伟位微卫...）
        banned_list = lazy_pinyin("可悦思平笑华世永念沁建宏中人春山雨国清溪瑞峰")
        # 名字开头字母--删掉所有以此字母开头的字--例：加入“w”，则结果中不会出现任何拼音以w开头的字（卫瓦望卧...）
        bad_init = list("eqrsxy")
        # 不想要的名字--删掉所有相同的字--例：加入“贵”，则结果中不会出现“贵”字
        bad_words = list("富贵民国军卫义二三四"
                         "介少大毛伟帅攻立生田"
                         "水火金木土才花凤龙春"
                         "艳芳淑杰俊志强昌银婷"
                         "丽芬发梅蛋铁铜娜宝春"
                         "夏秋冬武力天地圣神佛"
                         "老乾坤云")
        # 笔画数--名字的笔画总数的范围--例：王伟，名字笔画总数为6（不计姓氏）
        stroke_number = [0, 200]

        # 字数--名字的字数--例：王伟，字数为1
        character_number = 2

        # 姓--不会影响名字的生成，仅仅影响输出
        last_name = "张"

        # 允许叠字--例：欢欢，西西
        replicate = False
        # replicate = True
        # 选择词库
        # 0: "默认", 1: "诗经", 2: "楚辞", 3: "论语",
        # 4: "周易", 5: "唐诗", 6: "宋诗", 7: "宋词"
        # 8: 自定义
        name_source = 1

        # 是否筛选名字--仅输出默认库中存在的名字
        name_validate = True

        # 是否筛选性别--仅输出与默认库中对应名字性别相同的名字--仅当开启名字筛选时有效
        filter_gender = True

        # 性别--男/女--仅当开启名字筛选时有效
        gender = "女"

        names = list()
        with open("names.txt", "w+", encoding='utf-8') as f:
            for i in get_source(name_source, name_validate, character_number):
                if i.stroke_number < stroke_number[0] or stroke_number[1] < i.stroke_number:
                    continue
                if i.count != character_number:
                    continue
                if name_validate and filter_gender and (i.gender != gender or i.gender == "双"):
                    continue
                if check_init(i.first_name, bad_init):
                    continue
                if check_pinyin(i.first_name, banned_list):
                    continue
                if check_character(i.first_name, bad_words):
                    continue
                if not replicate and i.first_name[0] == i.first_name[1]:
                    continue
                names.append(i)
            print(">>正在输出结果...")
            names.sort()
            for i in names:
                result["nameList"].append(i)
                f.write(last_name + str(i) + "\n")
            print(">>输出完毕，请查看目录中的\"names.txt\"文件")

        print("response content : ", result)
        self.write(json.dumps(result))

class AddHandler(tornado.web.RequestHandler):
    # 这里可以用get的form信息,也可以直接用curl来post json数据

    def post(self):
        raw_data = self.request.body
        print("raw:", raw_data)
        res = json.loads(raw_data)
        s = res["num1"] + res["num2"]
        self.write(json.dumps({"sum":s}))


application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/story/(sishen[0-9]+)", StoryHandler), # 正则url映射,方便get
    (r"/add", AddHandler),
    (r"/api/gen-name-by-condition", GenNameHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()