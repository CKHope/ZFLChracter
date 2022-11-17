import pandas as pd
import jieba  # Importjieba Chinese word segmentation package
import numpy as np

# list of fileName
fileNameArray = [
    "zfl",
    "zflC1",
    "zflC2",
    "zflC3",
    "zflC4",
    "zflC5",
    "zflC6",
    "zflC7",
    "zflC8",
    "zflC9",
]
fileName = fileNameArray[0]
radicalFileName = "radical"

# setup file links
baseInputLink = f"./zfl/wordCountInput/{fileName}.txt"
baseOutputLinkExcel = f"zfl/wordCountOutput/{fileName}.xlsx"
baseOutputLinkCSV = f"zfl/wordCountOutput/{fileName}.csv"
radicalLinkCSV = f"zfl/wordCountInput/{radicalFileName}.csv"


def addPercentileColumn(df):
    df["percentile"] = np.flip(np.arange(1, len(df) + 1) / len(df) * 100)
    return df


def createWordListFromText(textLink):

    txt = open(textLink, "r", encoding="utf-8").read()  # Read data
    words = jieba.lcut(txt)  # Participle
    counts = {}  # Word Frequency Statistics
    for word in words:
        if len(word) == 1:
            continue
        else:
            counts[word] = counts.get(word, 0) + 1
    items = list(counts.items())  # The results show that
    items.sort(key=lambda x: x[1], reverse=True)
    # print("This list consist {} item".format(len(items)))
    dfWords = pd.DataFrame(items)
    dfWords.columns = ["traditionalChinese", "times"]
    dfWords.to_excel(baseOutputLinkExcel)
    # dfWords.iloc[:100]
    addPercentileColumn(dfWords)
    # print(dfWords[:5])
    return dfWords


def createCharacterListFromText(textLink):

    txt = open(textLink, "r", encoding="utf-8").read()  # Read data
    words = jieba.lcut(txt)  # Participle

    all_requent = {}
    all_character = {}

    for word in words:
        for word_lv2 in word:
            if word_lv2 in all_character:
                all_character[word_lv2] += 1
            else:
                all_character[word_lv2] = 1

    # print(all_character)
    knownWords = pd.DataFrame.from_dict(all_character, orient="index")

    knownWords = knownWords.reset_index()
    knownWords.rename(columns={"index": "word"}, inplace=True)

    # print(knownWords.sort_values(by=[0],ascending=False).head(300))
    knownWords = knownWords.sort_values(by=[0], ascending=False)
    # knownWords.iloc[:100]
    knownWords.columns = ["word", "times"]
    # print(knownWords[:3])
    return knownWords


# createWordListFromText(baseInputLink)
# createCharacterListFromText(baseInputLink)


def convertTxt2Dict(txtObject="dict.txt"):
    str = ""
    dict = {}
    with open(txtObject) as file:
        i = 1
        for line in file:
            str += line
            dict[f"{i}"] = str
            # print(str)
            str = ""
            i += 1
    # dictObject = eval(str)
    return dict


def getColorBasedOnPercentile(
    floatNum, Percentile1=80, Percentile2=64, Percentile3=51
) -> hex:
    colorDict = {
        Percentile1: "#f3e000",
        Percentile2: "#e1c5ae",
        Percentile3: "#309b8b",
    }
    if floatNum >= Percentile1:
        return [colorDict[Percentile1], 1]
    elif floatNum >= Percentile2:
        return [colorDict[Percentile2], 2]
    else:
        return [colorDict[Percentile3], 3]


def sliceRadicalListFromDf(df, sliceLen):
    # Create list of radlist that have less than 100 character or more than 100 character for 1 radical
    temp = df.groupby(["radical"]).size().sort_values(ascending=False)
    print(type(temp))
    dfTemp = pd.DataFrame(data=temp)
    dfTemp.columns = ["times"]
    # print(dfTemp[:20])
    tempTimesSum = 0
    RAD_LIST = []
    tempRadList = []
    for i in dfTemp.iterrows():
        rad = i[0]
        tempTimes = i[1]["times"]
        if tempTimes >= sliceLen:
            RAD_LIST.append(rad)
        if tempTimes < sliceLen:
            tempTimesSum += tempTimes
            if tempTimesSum < sliceLen:
                tempRadList.append(rad)
            else:
                RAD_LIST.append(tempRadList)
                tempRadList = []
                tempRadList.append(rad)
                tempTimesSum = 0
                tempTimesSum += tempTimes
        # print(i[0])
    listOfRadList = []
    for i in RAD_LIST:
        listOfRadList.append("".join(i))
        # print(i)
    print(listOfRadList[:-3])
    return listOfRadList


from cjkradlib import RadicalFinder


def getRadical(chineseCharacter):
    finder = RadicalFinder(lang="zh")  # default is 'zh'
    result = finder.search("麻")
    print(result.compositions)  # ['广', '林']
    print(result.supercompositions)  # ['摩', '魔', '磨', '嘛', '麽', '靡', '糜', '麾']
    print(result.variants)  # ['菻']
