import json
import requests
from bs4 import BeautifulSoup as bs
import chinese_converter
import pinyin
from datetime import datetime

# PHRASE="開天闢地"
# PHRASE="你爭我奪"
# PHRASE="爾虞我詐"
# PHRASE="亂七八糟"
# PHRASE="法輪常轉"
# PHRASE="人浮於事"

PHRASE = "無能為力"
contentType = ("def", "example", "quote", "synonyms", "antonyms")


def saveDict2JSON(dict, outFileName="dict.json"):
    with open("outFileName", "w") as outfile:
        json.dump(dict, outfile, indent=4)


def saveDict2txt(dict, outFileName="dict.txt"):
    with open(outFileName, "w") as outfile:
        json.dump(dict, outfile, indent=4)


def convertDict2JSON(dictObject) -> json:
    jsonobj = json.dumps(dictObject, indent=4)
    print(type(jsonobj))
    return jsonobj


def convertJSON2Dict(JSONobject) -> dict:
    dictObject = json.loads(JSONobject)
    print(type(dictObject))
    return dictObject


def convertTxt2Dict(txtObject="dict.txt"):
    str = ""
    with open(txtObject) as file:
        for line in file:
            str += line
    dictObject = eval(str)
    return dictObject


def generateText(text, times) -> str:
    result = ""
    for i in range(times):
        result += text
    return result


def updateResult(paragraphs, detailSpans: str, resultDict: dict) -> None:
    allSpans = paragraphs.find_all("span", detailSpans)
    if allSpans != []:
        for s in allSpans:
            content = s.text
            # print(content)
            resultDict[detailSpans] = content


def getSpellingContent(phrase=PHRASE) -> dict:
    """Result['pinyin']=pinyin
        Result['zhuyin']=zhuyin

    Args:
        spellingType (int, optional): 1: pinyin, 2: zhuyin. Defaults to 1.
        phrase (_type_, optional): phrase to get spelling. Defaults to PHRASE.
    """

    spellingContent = {}
    spellingContent["traChinese"] = phrase
    spellingContent["simChinese"] = chinese_converter.to_simplified(phrase)
    spellingContent["pinyin"] = ""
    spellingContent["zhuyin"] = ""
    link = f"https://www.zdic.net/hans/{phrase}"
    spellingContent["zdicLink"] = link
    web = requests.get(link)
    data = web.content
    soup = bs(data, features="html.parser")
    spellingTag = soup.find_all("span", "dicpy")
    # print(len(definitionTag))
    contentOrder = 1
    for spelling in spellingTag:
        if contentOrder == 1:
            spellingContent["pinyin"] = spelling.text
            contentOrder += 1
        elif contentOrder == 2:
            spellingContent["zhuyin"] = spelling.text
            break

    if spellingContent["pinyin"] == "":
        spellingContent["pinyin"] = pinyin.get(phrase, delimiter=" ")
    return spellingContent


def getChineseDetails(phrase=PHRASE) -> dict:
    result = {}
    finalResult = {}
    link = f"https://www.moedict.tw/{phrase}"
    web = requests.get(link)
    data = web.content
    soup = bs(data, features="html.parser")
    definitionTag = soup.find_all("p", "definition")
    # print(len(definitionTag))
    contentOrder = 1
    for definition in definitionTag:
        for i in range(len(contentType)):
            updateResult(definition, contentType[i], result)
        finalResult[contentOrder] = result
        result = {}
        contentOrder += 1
    # print(finalResult)

    return finalResult


# print(getChineseDetails("開天闢地"))


def getEnglishContent(phrase=PHRASE) -> str:
    link = f"https://www.moedict.tw/{phrase}"
    web = requests.get(link)
    data = web.content
    soup = bs(data, features="html.parser")
    definitionTag = soup.find_all("span", "fw_def")
    order = 1
    englishDetailString = ""
    for i in definitionTag:
        if order == 1:
            englishDetailString += f"---(E){i.text}"
            break
    # englishDetailString+="\n"
    return englishDetailString


def getVietnameseContent(phrase) -> str:
    content = ""
    link = f"https://api.hanzii.net/api/search/vi/{phrase}"
    web = requests.get(link)
    tempstring = web.content.decode("utf-8")
    jsonvalue = json.loads(tempstring)

    try:
        vietnamesesMeaning = jsonvalue["result"][0]["content"][0]["means"]
        content += "---(V)"
        orderNumber = 1
        for i in vietnamesesMeaning:
            toadd = i["mean"]
            content += f"{orderNumber}. {toadd}"
            content += "\n"
            orderNumber += 1
    except:
        print(f"no Vietnamese content got for {phrase}")

    return content


def printChineseDetails(phrase=PHRASE) -> str:
    chineseDetailString = ""
    b = getChineseDetails(phrase)
    # print(b)
    itemOder = 1
    for key, value in b.items():
        # print(f"{key}")
        for k, v in value.items():
            # print(k[0])
            if k[0] == "d":
                chineseDetailString += f"({itemOder})."
                content = f"{v}"
                chineseDetailString += content + "\n"
            elif k[0] == "e":
                content = f"{v}"
                chineseDetailString += content + "\n"
            elif k[0] == "q":
                content = f"{v}"
                chineseDetailString += content + "\n"
            else:
                chineseDetailString += f"({itemOder})"
                content = f"--|{k[0]}|{v}"
                chineseDetailString += content
        itemOder += 1
    return chineseDetailString


def getPhraseContent(phrase=PHRASE) -> dict:
    """get phrase content include: traditional Chinese, simplified Chinese, pinyin, zhuzin,
    Chinese meaning, English meaning, Vietnamese meaning, link zdic, moedict.

    Args:
        phrase (str, optional): phrase to get content. Defaults to PHRASE.

    Returns:
        dict: dictionary
    """
    print(f"Working on {phrase}")
    today = str(datetime.now().strftime("%d.%m.%y"))
    content = {}
    chineseContent = printChineseDetails(phrase)
    spellingContent = getSpellingContent(phrase)
    englishContent = getEnglishContent(phrase)
    vietnameseContent = getVietnameseContent(phrase)
    content["traChinese"] = spellingContent["traChinese"]
    content["simChinese"] = spellingContent["simChinese"]
    content["pinyin"] = spellingContent["pinyin"]
    content["zhuyin"] = spellingContent["zhuyin"]
    content["zdicLink"] = spellingContent["zdicLink"]
    content["moedictLink"] = f"https://www.moedict.tw/{phrase}"
    content["chineseDetails"] = chineseContent
    content["englishDetails"] = englishContent
    content["vietnameseDetails"] = vietnameseContent
    content["updateDate"] = today
    content["scrapStatus"] = 0
    # print(content)
    return content


def scrapContent2Txt(
    fileName="chengyu.txt", dictTxtFileName="dict.txt", forceScrap=0
) -> None:
    chengyu = {}
    if forceScrap == 1:
        with open(fileName) as file:
            i = 1
            for line in file:
                traChineseText = str.strip(line[:])
                if traChineseText != "":
                    print(f"Processing {i}: {traChineseText}")
                    content = getPhraseContent(traChineseText)
                chengyu[traChineseText] = content
                i += 1
    else:
        dictObject = convertTxt2Dict()
        with open(fileName) as file:
            i = 1
            for line in file:
                traChineseText = str.strip(line[:])
                if traChineseText != "":
                    print(f"Processing {i}: {traChineseText}")
                    dictObjectFind = dictObject.get(traChineseText)
                    if dictObjectFind:
                        content = dictObjectFind
                    else:
                        content = getPhraseContent(traChineseText)
                chengyu[traChineseText] = content
                i += 1

    saveDict2txt(chengyu)


# scrapContent2Txt()


def getPhraseOfflineContent(phrase=PHRASE) -> str:
    dictObject = convertTxt2Dict()
    result = dictObject.get(phrase)
    print("Start")
    print(result)
    print("Done")
    return result


# getPhraseOfflineContent("廣義的")

# a = getPhraseContent("廣義的")
# print(a)


def checkExist(phrase=PHRASE):
    tempDict = getChineseDetails(phrase)
    print(phrase)
    if tempDict == {}:
        return 0
