#!/usr/bin/env python
# coding=utf-8

import os
import Tkinter as tk
import ttk as ttk
from tkFileDialog import *
import tkMessageBox
from Tkconstants import *
import json


class MyTools(tk.Tk):
    mInputText = None
    mResultText = None
    mLogText = None
    BG_COLOR = 'lightblue'

    BASE64_TABLE = [
        # 0 -> 15
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
        # 16 -> 31
        'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f',
        # 32 -> 47
        'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n','o', 'p', 'q', 'r', 's', 't', 'u', 'v',
        # 48 -> 63, =号是64
        'w', 'x', 'y', 'z', '0', '1', '2', '3','4', '5', '6', '7', '8', '9', '+', '/', '='
    ]

    def __init__(self):
        tk.Tk.__init__(self)  # python 2.7
        self.initTools()

    def initTools(self):
        self.initView()

    def initView(self):
        self.title("python工具合集")
        self.geometry("1000x760")
        # self.config(bg="blue")
        # self["bg"] = "blue" #"pink"

        # 构建layout布局
        topBar = tk.Frame(self, height=60, bg=self.BG_COLOR)
        topBar.pack(side=TOP, fill=X)
        self.initTopBar(topBar)

        leftFrame = tk.Frame(self, width=430, bg=self.BG_COLOR)
        leftFrame.pack(side=LEFT, fill=Y)
        self.initLeftFrame(leftFrame)

        midFrame = tk.Frame(self, width=140, bg=self.BG_COLOR)
        midFrame.pack(side=LEFT, fill=Y)
        self.initMiddleFrame(midFrame)

        rightFrame = tk.Frame(self, width=430, bg=self.BG_COLOR)
        rightFrame.pack(expand=True, fill=Y)
        self.initRightFrame(rightFrame)

    def initTopBar(self, parent):
        label = tk.Label(parent, text="请输入数据", bg=self.BG_COLOR, padx=30, pady=10, font=('Arial', 16, "bold"))
        label.pack(side=LEFT, anchor=CENTER)
        btn = ttk.Button(parent, text="清空输入", command=lambda: self.clearText(self.mInputText))
        btn.pack(side=LEFT, anchor=CENTER)

        resultLabel = tk.Label(parent, text="输出结果", bg=self.BG_COLOR, font=('Arial', 16, "bold"))
        resultLabel.place(x=600, y=10)

        resultBtn = ttk.Button(parent, text="清空结果", command=lambda: self.clearText(self.mResultText))
        resultBtn.place(x=700, y=10)

    def initLeftFrame(self, parent):
        self.mLogText = tk.Text(parent, width=60, height=12)
        self.mLogText.pack(side='bottom', anchor=W, padx=5, pady=5)

        infoFrame = tk.Frame(parent, height=60, bg=self.BG_COLOR)
        infoFrame.pack(side='bottom', fill='x')

        # 自动缩放
        self.mInputText = tk.Text(parent, width=60)
        self.mInputText.pack(expand=True, fill=BOTH, padx=5, pady=5)

        strLine = "-----------------------------------------------------------------"
        label = tk.Label(infoFrame, text=strLine, bg=self.BG_COLOR, pady=2)
        label.pack(side=TOP, anchor=W)
        label = tk.Label(infoFrame, text="日志", bg=self.BG_COLOR, padx=30, pady=8, font=('Arial', 16, "bold"))
        label.pack(side=LEFT, anchor=CENTER)
        btn = ttk.Button(infoFrame, text="清空日志", command=lambda: self.clearText(self.mLogText))
        btn.pack(side=LEFT, anchor=CENTER)

    def initMiddleFrame(self, parent):
        copyBtn = ttk.Button(parent, text="<<<文本", width=8, command=self.onCopyResult)
        copyBtn.pack(side=TOP, padx=5, pady=10)

        jsonParseBtn = ttk.Button(parent, text="Json格式化", width=8, command=self.onJsonFormat)
        jsonParseBtn.pack(side=TOP, padx=5, pady=10)

        jsonCompressBtn = ttk.Button(parent, text="Json压缩  ", width=8, command=self.onJsonCompress)
        jsonCompressBtn.pack(side=TOP, padx=5, pady=10)

        b64EncodeBtn = ttk.Button(parent, text="Base64编码", width=8, command=self.onBase64Encode)
        b64EncodeBtn.pack(side=TOP, padx=5, pady=10)

        b64DecodeBtn = ttk.Button(parent, text="Base64解码", width=8, command=self.onBase64Decode)
        b64DecodeBtn.pack(side=TOP, padx=5, pady=10)

        charToUtf8Btn = ttk.Button(parent, text="中文转UTF8", width=8, command=self.onCharToUtf8)
        charToUtf8Btn.pack(side=TOP, padx=5, pady=10)

        utf8ToCharBtn = ttk.Button(parent, text="UTF8转中文", width=8, command=self.onUtf8ToChar)
        utf8ToCharBtn.pack(side=TOP, padx=5, pady=10)

    def initRightFrame(self, parent):
        self.mResultText = tk.Text(parent)
        self.mResultText.pack(expand=True, fill=BOTH, padx=5, pady=5)

    def clearText(self, text):
        if self and text:
            text.delete(1.0, END)

    def getInput(self):
        if self.mInputText:
            strInput = self.mInputText.get(1.0, END)
            if strInput and len(strInput):
                if strInput[len(strInput)-1] == '\n':
                    strInput = strInput[0: len(strInput)-1]
                    return strInput
        return ""

    # 测试例子：
    def testJson(self):
        # strInput = '{"a":1,"b":"2","3":"c","4":["k","k1"], "info":{"name":"宝塔","test":["python","java"]}}'
        # strInput = '{"total":300,"url":"http:wap.abc.com","bizs":{"biz":[{"id":555555,"name":"兰州烧饼","add":"北京市海定区中关村"},{"id":666666,"name":"兰州拉面","add":"北京市海定区中关村"},{"id":888888,"name":"肯德基","add":"北京市海定区中关村"}]}}'
        # strInput = '{"0":[{"name":"品牌","value":"1,2,3,4"},{"a":1,"b":"2","3":"c","4":["k","k1"], "info":{"name":"宝塔","test":["python","java"]}}],"1":[{"name":"材质","value":""},{"name":"风格","value":""}],"2":[{"name":"类型","value":"运动,休闲,登山"}],"3":[{"name":"适用季节","value":"春,夏,秋,冬"}],"4":[{"name":"生产日期","value":""},{"name":"结束日期","value":""}]}'
        strInput = '{"0":[{"name":"品牌","value":"1,2,3,4"},{"a":1,"b":"2","3":"c","4":["k","k1"], "info":{"name":"宝塔","beijing":{"total":300,"url":"http:wap.abc.com","bizs":{"biz":[{"id":555555,"name":"兰州烧饼","add":"北京市海定区中关村"},{"id":666666,"name":"兰州拉面","add":"北京市海定区中关村"},{"id":888888,"name":"肯德基","add":"北京市海定区中关村"}]}},"test":["python","java"]}}],"1":[{"name":"材质","value":""},{"name":"风格","value":""}],"2":[{"name":"类型","value":"运动,休闲,登山"}],"3":[{"name":"适用季节","value":"春,夏,秋,冬"}],"4":[{"name":"生产日期","value":""},{"name":"结束日期","value":""}]}'
        return strInput

    # 复制结果到输出区
    def onCopyResult(self):
        strResult = ""
        if self.mResultText:
            strResult = self.mResultText.get(1.0, END)
            self.mResultText.delete(1.0, END)

        if len(strResult) > 0:
            if strResult[len(strResult)-1] == '\n':
                strResult = strResult[0: len(strResult)-1]

            if self.mInputText:
                self.mInputText.delete(1.0, END)
                self.mInputText.insert(1.0, strResult)

    # 解析JSON
    def onJsonFormat(self):
        strInput = self.getInput()
        strInput = strInput.replace(" ", "")

        if self.mResultText:
            self.mResultText.delete(1.0, END)

        jsData = None
        try:
            jsData = json.JSONDecoder().decode(strInput)
        except ValueError as e:
            info = "不能解析Json. %s\n" % e
            print(info)
            if self.mLogText:
                self.mLogText.insert(END, info)

        if jsData:
            level = 0
            out = self.parseOneJson(jsData, level, False)
            if self.mResultText:
                self.mResultText.insert(1.0, out)

    # 解析Json, 递归操作
    def parseOneJson(self, jsData, level, firstNoSpace):
        outStr = ""
        strSpace = "    "
        jsType = type(jsData)
        loop = 0

        # 最多支持50层递归，避免死循环
        if level >= 50:
            return outStr
        # print("parseOneJson: jsData=", jsData)
        # print("parseOneJson: jsType=", jsType)

        # 对字典的处理
        if jsType == dict:
            # 添加 {
            outStr = firstNoSpace and "{\n" or (strSpace * level + "{\n")

            # 对key值进行排序
            allKeys = jsData.keys()
            allKeys.sort()
            total = len(allKeys)

            for key in allKeys:
                item = jsData[key]
                # print("dict key=", key)
                # print("dict value=", item)

                if type(item) == dict or type(item) == list:
                    # 先写入key值
                    newLevel = level + 1
                    strKey = "\"%s\"" % key
                    outStr += strSpace * (level + 1) + ("%s : " % strKey)

                    # 子类型是字典或数组，递归解析
                    outStr += self.parseOneJson(item, newLevel, True)
                else:
                    # 添加元素，字符类型需要添加冒号，其它不需要, 格式: "key": value
                    strKey = "\"%s\"" % key
                    strItem = ""
                    if type(item) == unicode or type(item) == str:
                        strItem = "\"%s\"" % item
                    else:
                        strItem = "%s" % item
                    outStr += strSpace * (level + 1) + ("%s : %s" % (strKey, strItem))
                pass

                # 最后一个不写入逗号
                loop += 1
                if loop <= total - 1:
                    outStr += ",\n"
                else:
                    outStr += "\n"
            # 写入 }
            outStr += strSpace * level + "}"
        elif jsType == list:
            # 对数组的处理
            outStr = firstNoSpace and "[\n" or (strSpace * level + "[\n")
            total = len(jsData)

            for item in jsData:
                # print("list item=", item)
                if type(item) == dict or type(item) == list:
                    newLevel = level + 1
                    outStr += self.parseOneJson(item, newLevel, False)
                else:
                    # 添加元素，字符类型需要添加冒号，其它不需要
                    strItem = ""
                    if type(item) == unicode or type(item) == str:
                        strItem = "\"%s\"" % item
                    else:
                        strItem = "%s" % item
                    outStr += strSpace * (level + 1) + ("%s" % strItem)

                loop += 1
                if loop <= total - 1:
                    outStr += ",\n"
                else:
                    outStr += "\n"
            outStr += strSpace * level + "]"
        # print("outStr=", outStr)
        return outStr

    def onJsonCompress(self):
        print("onJsonCompress")
        strInput = self.getInput()
        strInput = strInput.replace(" ", "")
        strInput = strInput.replace("\n", "")

        self.mResultText.delete(1.0, END)
        self.mResultText.insert(1.0, strInput)


    def onBase64Encode(self):
        strInput = self.getInput()
        length = len(strInput)
        if length > 0:
            # Base64编码
            ret = self.base64EncodeString(strInput)

            self.mResultText.delete(1.0, END)
            self.mResultText.insert(1.0, ret)

    # 解码
    def onBase64Decode(self):
        print("onBase64Decode()")
        strInput = self.getInput()
        length = len(strInput)
        if length > 0:
            # Base64编码
            ret = self.base64DecodeString(strInput)

            self.mResultText.delete(1.0, END)
            self.mResultText.insert(1.0, ret)

    def onCharToUtf8(self):
        print("onCharToUtf8()")
        strInput = self.getInput()
        if len(strInput) > 0:
            bytesList = self.Utf16ToUtf8BytesList(strInput)
            print("onCharToUtf8: bytesList: ", bytesList)

            ret = self.formatUtf8BytesList(bytesList)
            self.mResultText.delete(1.0, END)
            self.mResultText.insert(1.0, ret)
        pass

    def onUtf8ToChar(self):
        strInput = self.getInput()
        length = len(strInput)
        if length > 0:
            byteList = self.parseCharList(strInput)
            ret = self.Utf8BytesListToUtf16(byteList)
            self.mResultText.delete(1.0, END)
            self.mResultText.insert(1.0, ret)


    def base64EncodeString(self, strData):
        ret = ""
        if strData is None or len(strData) == 0:
            return ret

        # 字符先转为utf8的字节数组
        bytesList = self.Utf16ToUtf8BytesList(strData)

        # 对字节数组编码
        ret = self.base64EncodeBytesList(bytesList)
        return ret

    # 对字节数组进行base64编码
    def base64EncodeBytesList(self, bytesList):
        ret = ""
        if bytesList is None or len(bytesList) == 0:
            return ret

        length = len(bytesList)
        i = 0
        chList = []
        while i < length:
            v1 = bytesList[i]
            i += 1
            # 取高6位，向左移2位
            code1 = (v1 & 0xFF) >> 2
            chList.append(self.BASE64_TABLE[code1])
            # 长度不满3个，补2个=
            if i == length:
                # 取低2位, 左移4位，形成6位的值
                code2 = (v1 & 0x03) << 4
                chList.append(self.BASE64_TABLE[code2])
                chList.append("==")
                break

            v2 = bytesList[i]
            i += 1
            if i == length:
                code2 = ((v1 & 0x03) << 4) | ((v2 >> 4) & 0x0F)
                code3 = (v2 & 0x0F) << 2
                chList.append(self.BASE64_TABLE[code2])
                chList.append(self.BASE64_TABLE[code3])
                chList.append("=")
                break

            v3 = bytesList[i]
            i += 1
            code2 = ((v1 & 0x03) << 4) | ((v2 >> 4) & 0x0F)
            code3 = (v2 & 0x0F) << 2 | ((v3 >> 6) & 0x03)
            code4 = v3 & 0x3F
            chList.append(self.BASE64_TABLE[code2])
            chList.append(self.BASE64_TABLE[code3])
            chList.append(self.BASE64_TABLE[code4])

        # 组合输出字符
        for ch in chList:
            ret += ch
        return ret

    def base64DecodeString(self, strData):
        # 把输入的base64字符解码为Utf8字节流数组
        byteList, info = self.base64DecodeToUtf8BytesList(strData)
        print("base64DecodeString: byteList=", byteList)

        if info and len(info) > 0:
            self.mLogText.insert(END, info)

        # 由于文本框基本都是使用UTF16格式，所以需要Utf8字节流数组转Utf16字符
        ret = self.Utf8BytesListToUtf16(byteList)
        return ret

        # return self.base64DecodeToUtf8String(strData)

    # base64字符解码为Utf8字符
    def base64DecodeToUtf8String(self, strData):
        ret = ""
        if strData is None or len(strData) == 0:
            return ret, ""

        byteList = []
        length = len(strData)
        if length % 4 != 0:
            print("base64DecodeToUtf8String: not 4 double")
            info = "Base64字符长度不是4的倍数\n"
            return ret, info

        i = 0
        while i < length:
            value1, value2, value3, value4 = 0, 0, 0, 0
            try:
                value1 = self.BASE64_TABLE.index(strData[i])
                i += 1
                value2 = self.BASE64_TABLE.index(strData[i])
                i += 1
                value3 = self.BASE64_TABLE.index(strData[i])
                i += 1
                value4 = self.BASE64_TABLE.index(strData[i])
                i += 1
            except ValueError as e:
                info = "不能解析Base64. %s\n" % e
                print(info)
                return "", info

            v1 = (value1 << 2) | (value2 >> 4)
            v2 = ((value2 & 0x0F) << 4) | (value3 >> 2)
            v3 = ((value3 & 0x03) << 6) | value4

            # 添加第1个数据
            byteList.append(chr(v1))
            # 是=号不添加
            if value3 != 64:
                byteList.append(chr(v2))
            if value4 != 64:
                byteList.append(chr(v3))
        for ch in byteList:
            ret += ch
        return ret, ""

    # base64字符解码为Utf8字节流数组
    def base64DecodeToUtf8BytesList(self, strData):
        byteList = []
        if strData is None or len(strData) == 0:
            return byteList, ""

        length = len(strData)
        if length % 4 != 0:
            print("base64DecodeToUtf8BytesList: not 4 double")
            info = "Base64字符长度不是4的倍数\n"
            return byteList, info

        i = 0
        while i < length:
            value1, value2, value3, value4 = 0, 0, 0, 0
            try:
                value1 = self.BASE64_TABLE.index(strData[i])
                i += 1
                value2 = self.BASE64_TABLE.index(strData[i])
                i += 1
                value3 = self.BASE64_TABLE.index(strData[i])
                i += 1
                value4 = self.BASE64_TABLE.index(strData[i])
                i += 1
            except ValueError as e:
                info = "不能解析Base64. %s\n" % e
                print(info)
                return [], info

            # value1-value4 是在 0--0b00111111的范围
            # 第一个数据，取value1的全部数据，左移2位占新数据的前6位，value2取前2位，右移4位占低2位
            v1 = (value1 << 2) | (value2 >> 4)
            # 第2个数据，取value2的低4位，左移4位占前4位，value3取前4位，，右移2位占低4位
            v2 = ((value2 & 0x0F) << 4) | (value3 >> 2)
            # 第3个数据，取第3个数据低两位, 左移6位占前2位，与第4个数据合并
            v3 = ((value3 & 0x03) << 6) | (value4 & 0x3F)

            # 添加第1个数据
            byteList.append(v1)
            # 是=号不添加
            if value3 != 64:
                byteList.append(v2)
            if value4 != 64:
                byteList.append(v3)
        return byteList, ""

    # Utf16转化为Utf8的字符，返回String类型
    def Utf16ToUtf8String(self, strData):
        ret = ""
        if strData is None or len(strData) == 0:
            return ret

        chList = []
        for item in strData:
            # 转为整型数值
            value = ord(item)
            if 0x0000 < value <= 0x007F:
                # 单字节 U0000 – U007F: 0xxxxxxx
                chList.append(chr(value))
            elif 0x0080 <= value <= 0x7FF:
                # 双字节110xxxxx
                # U0080–U07FF: 110xxxxx 10xxxxxx
                b1 = 0xC0 | ((value >> 6) & 0x1F)
                b2 = 0x80 | (value & 0x3F)
                chList.append(chr(b1))
                chList.append(chr(b2))
            elif 0x800 <= value <= 0xFFFF:
                # 三字节  1110xxxx
                # U0800–UFFFF  1110xxxx 10xxxxxx 10xxxxxx
                b1 = 0xE0 | ((value >> 12) & 0x0F)
                b2 = 0x80 | ((value >> 6) & 0x3F)
                b3 = 0x80 | (value & 0x3F)

                chList.append(chr(b1))
                chList.append(chr(b2))
                chList.append(chr(b3))
        # 组合输出字符
        for ch in chList:
            ret += ch
        return ret

    # 转换为utf8字节流, 返回字节数组
    def Utf16ToUtf8BytesList(self, strData):
        bytesList = []
        if strData is None or len(strData) == 0:
            return bytesList
        for item in strData:
            # 转为整型数值
            value = ord(item)
            if 0x0000 < value <= 0x007F:
                # 单字节 U0000 – U007F: 0xxxxxxx
                bytesList.append(value)
            elif 0x0080 <= value <= 0x7FF:
                # 双字节110xxxxx
                # U0080–U07FF: 110xxxxx 10xxxxxx
                b1 = 0xC0 | ((value >> 6) & 0x1F)
                b2 = 0x80 | (value & 0x3F)
                bytesList.append(b1)
                bytesList.append(b2)
            elif 0x800 <= value <= 0xFFFF:
                # 三字节  1110xxxx
                # U0800–UFFFF  1110xxxx 10xxxxxx 10xxxxxx
                b1 = 0xE0 | ((value >> 12) & 0x0F)
                b2 = 0x80 | ((value >> 6) & 0x3F)
                b3 = 0x80 | (value & 0x3F)
                bytesList.append(b1)
                bytesList.append(b2)
                bytesList.append(b3)
        return bytesList

    def Utf8ToUtf16String(self, strData):
        ret = ""
        if strData is None or len(strData) == 0:
            return ret
        chList = []
        total = len(strData)
        for i in range(total):
            item = strData[i]
            # 转为整型数值
            value = ord(item)

            if (value >> 7) & 0xFF == 0x00:
                # 单字节 0xxxxxxx
                chList.append(chr(value))
            elif (value >> 5) & 0xFF == 0x06:
                # 双字节
                # 110xxxxx 10xxxxxx
                i += 1
                val2 = ord(strData[i])
                u16 = ((value & 0x1F) << 6) | (val2 & 0x3F)
                chList.append(chr(u16))
            elif (value >> 4) & 0xFF == 0x0E:
                # 三字节 1110xxxx 10xxxxxx 10xxxxxx
                i += 1
                val2 = ord(strData[i])
                i += 1
                val3 = ord(strData[i])
                u16 = ((value & 0x0F) << 12) | ((val2 & 0x3F) << 6) | (val3 & 0x3F)
                chList.append(chr(u16))
        # 组合输出字符
        for ch in chList:
            ret += ch
        return ret

    # utf8字节数组转为utf16字符
    def Utf8BytesListToUtf16(self, bytesList):
        ret = ""
        if bytesList is None or len(bytesList) == 0:
            return ret

        chList = []
        total = len(bytesList)
        for i in range(total):
            value = bytesList[i]
            print("Utf8BytesListToUtf16: value=", value)

            if (value >> 7) & 0xFF == 0x00:
                # 单字节 0xxxxxxx
                print("one value=", value)
                chList.append(unichr(value))
            elif (value >> 5) & 0xFF == 0x06:
                # 双字节 110xxxxx 10xxxxxx
                i += 1
                val2 = bytesList[i]
                u16 = ((value & 0x1F) << 6) | (val2 & 0x3F)
                print("double value=", u16)
                chList.append(unichr(u16))
            elif (value >> 4) & 0xFF == 0x0E:
                # 三字节 1110xxxx 10xxxxxx 10xxxxxx
                i += 1
                val2 = bytesList[i]
                i += 1
                val3 = bytesList[i]
                u16 = ((value & 0x0F) << 12) | ((val2 & 0x3F) << 6) | (val3 & 0x3F)
                print("three value=", u16)
                chList.append(unichr(u16))
        # 组合输出字符
        for ch in chList:
            ret += ch
        return ret

    # utf8字节数组转为utf16字符
    def formatUtf8BytesList(self, bytesList):
        ret = ""
        if bytesList is None or len(bytesList) == 0:
            return ret

        chList = []
        total = len(bytesList)
        for i in range(total):
            value = bytesList[i]
            # print("Utf8BytesListToUtf16: value=", value)

            if (value >> 7) & 0xFF == 0x00:
                # 单字节 0xxxxxxx
                print("one value=", value)
                chList.append("\u%02x" % value)
            elif (value >> 5) & 0xFF == 0x06:
                # 双字节 110xxxxx 10xxxxxx
                i += 1
                val2 = bytesList[i]
                chList.append("\u%02x%02x" % (value, val2))
            elif (value >> 4) & 0xFF == 0x0E:
                # 三字节 1110xxxx 10xxxxxx 10xxxxxx
                i += 1
                val2 = bytesList[i]
                i += 1
                val3 = bytesList[i]
                chList.append("\u%02x%02x%02x" % (value, val2, val3))
        # 组合输出字符
        for ch in chList:
            ret += ch
        return ret

    def getCharByteValue(self, value):
        num = 0
        if 0x30 <= value <= 0x39:     # 0-9
            num = value - 0x30
        elif 0x41 <= value <= 0x46:   # A-F
            num = value - 0x41 + 10
        elif 0x61 <= value <= 0x66:   # a-f
            num = value - 0x61 + 10
        return num

    # 解析unicode字符串，格式如： \u36\u3a54\u5bcf89
    def parseCharList(self, strData):
        ret = ""
        if strData is None or len(strData) == 0:
            return ret

        chList = strData.split("\u")
        # print("chList=", chList)
        byteList = []
        for item in chList:
            if item and len(item) > 0:
                length = len(item)
                # 不是2的倍数位，需要在前面补0
                if length % 2 != 0:
                    item = "0" + item
                # 取两位作为一个字节，从高位开始取
                for i in range(length/2):
                    ch = item[(i*2): (i+1)*2]
                    hg = ord(ch[0])
                    low = ord(ch[1])
                    hgValue = self.getCharByteValue(hg)
                    lowValue = self.getCharByteValue(low)
                    num = (hgValue << 4) + lowValue
                    byteList.append(num)
        # print("byteList=", byteList)
        return byteList


if __name__ == "__main__":
    app = MyTools()
    app.mainloop()
