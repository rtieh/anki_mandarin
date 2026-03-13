#this is an algorithm into which scrapes  “教育部國語辭典簡片本" (an online Chinese dictionary) 
#for the zhuyin, top definition, and example sentence usage of a given vocabulary word 
#and formats it into Anki flaschards (cloze and basic)
#please note: this code was made with the help of ChatGPT-5
import requests
import random
import time
import urllib3
from bs4 import BeautifulSoup

session = requests.Session()

headers = {
"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
"Accept-Language": "zh-TW,zh;q=0.9,en;q=0.8",
"Connection": "keep-alive"
}

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#scraping function
def scrape(word):

    search_url = "https://dict.concised.moe.edu.tw/search.jsp"

    params = {
        "md": "1",
        "word": word
    }

    r = session.get(search_url, params=params, headers=headers, verify=False)
    soup = BeautifulSoup(r.text, "html.parser")

    link = soup.find("a", href=lambda x: x and "dictView.jsp" in x)

    if not link:
        return "No entry found"

    entry_url = "https://dict.concised.moe.edu.tw/" + link["href"]

    r2 = session.get(entry_url, headers=headers, verify=False)
    soup2 = BeautifulSoup(r2.text, "html.parser")

    meta = soup2.find("meta", {"name": "Description"})

    if meta:
        return meta["content"]

    return "No definition found"

#organizing and storing scraped data into zhuyin, top defintion, and example sentence
def organize_word(word):

    content = scrape(word)

    if content == "No entry found" or content == "No definition found":
        return {"zhuyin": "", "definition": "", "example": ""}

    try:
        parts = content.split(",", 2)

        zhuyin = parts[1].split("注音:")[1].replace("　", " ").strip()

        defs = parts[2].split("釋義:")[1]

        top_def = defs.split("2.")[0]

        definition = top_def.split("[例]")[0].replace("1.", "").strip()

        example = top_def.split("[例]")[1].strip()

        return {
            "zhuyin": zhuyin,
            "definition": definition,
            "example": example
        }

    except:
        return {"zhuyin": "", "definition": "", "example": ""}
    
#format into cloze anki cards
def format_cloze(word_data_dict):

    for word, data in word_data_dict.items():

        zhuyin = data["zhuyin"]
        definition = data["definition"]
        example = data["example"]

        card = f"{{{{c1::{word}}}}} {definition};【{zhuyin}】{example}"

        print(card)

#format into basic anki cards
def format_basic(word_data_dict):

    for word, data in word_data_dict.items():

        zhuyin = data["zhuyin"]
        definition = data["definition"]
        example = data["example"]

        card = f"{word}【{zhuyin}】例{example}; {definition}"

        print(card)

#add your wordlist here
words = ['俯臥', '引體', '建模', '反鳥託邦', '羞愧', '內鬼', '浴室', '寫愛無緣', '謠言', '辛虧', '探望', '揮舞', '歡呼', '謙虛', '致意', '壓倦', '單調', '承讓', '富裕', '聳肩', '不以為然', '羞愧', '怠惰', '令人髮指', '糾正', '雞皮疙瘩', '留意', '得意', '自大', '隱晦', '走神', '佔有', '後頸', '愉悅', '含糊', '探究', '肩胛骨', '羞恥', '塌下', '僻字', '磨蹭', '咕噥', '摩娑', '珊瑚', '尖', '評估', '攤派', '繁殖', '抹面', '缺陷', '溫馨', '胡話', '心坎', '洋人', '點燃', '正經', '關節炎', '缺乏', '蒼蠅', '準確', '富裕', '島嶼', '註冊', '專利', '倒是', '意味', '歌唱', '重蹈覆轍', '王八蛋', '洗漱', '榴蓮', '念想', '健忘', '迷戀', '堵住', '罪過', '褪色', '情愫', '知己', '瓢潑', '房檐', '身影', '慶幸', '水道', '抑制', '隨波逐流', '放蕩', '慈祥', '背影', '便利店', '傻瓜', '璀璨']
organized = {}

for w in words:
    print("Searching:", w)
    organized[w] = organize_word(w)
    time.sleep(random.uniform(3,7))

format_cloze(organized)
format_basic(organized)