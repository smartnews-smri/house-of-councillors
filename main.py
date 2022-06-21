# coding: utf-8

from bs4 import BeautifulSoup
import requests
import csv
import time
import datetime
import json
import glob
import os



#-------------------------------------------------------------
# Get constants
#-------------------------------------------------------------

def get_content_folder():
  dir_data = "./data/"
  return dir_data


def get_latest_kaiji():
  r = requests.get("https://www.sangiin.go.jp/japanese/kon_kokkaijyoho/index.html")
  html = BeautifulSoup(r.content, "html.parser")
  ul = html.find("ul", class_="exp_disnone_list_n")
  href = ul.find("li").find("a").attrs["href"]

  href = href.replace("../joho1/kousei/koho/", "")
  href = href.replace("/keika.htm", "")

  return href



#-------------------------------------------------------------
# Versatile functions
#-------------------------------------------------------------

# Get Kaiji URL
def get_kaiji_url(kaiji):
  prefix = "https://www.sangiin.go.jp/japanese/joho1/kousei/gian/"
  suffix = "/gian.htm"
  return prefix + kaiji + suffix



# Get CSV file content as array
# Return False if the file does NOT exist
def get_csv(url):
  try:
    with open(url) as csvfile:
      read = csv.reader(csvfile, delimiter = ',')
      rows = list(read)
      return rows
  except FileNotFoundError:
    return False


# Save CSV or JSON file
def save_file(url, values):
  ext = url.split(".")[-1]

  if ext == "csv":
    with open(url, 'w', newline = '') as f:
      writer = csv.writer(f)
      writer.writerows(values)

  if ext == "json":
    with open(url, 'w') as f:
      json.dump(values, f, ensure_ascii = False)


# Convert 和暦 to 西暦
def convert_to_wcalendar(string):
  string = convert_to_half(string)

  if "年" in string and "月" in string and "日" in string:
    string = string.replace("昭和", "1925／")
    string = string.replace("平成", "1988／")
    string = string.replace("令和", "2018／")
    string = string.replace("元年", "1／")
    string = string.replace("年", "／")
    string = string.replace("月", "／")
    string = string.replace("日", "")

    strs = string.split("／")

    y = str(int(strs[0]) + int(strs[1]))
    m = ("0" + strs[2])[-2:]
    d = ("0" + strs[3])[-2:]
    string = y + "-" + m + "-" + d

  return string



# Convert full-width number and alphabet into half-width
def convert_to_half(string):
  string = string.strip()

  full = "０１２３４５６７８９ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ"
  half = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

  for i in range(len(full)):
    string = string.replace(full[i], half[i])

  return string





#-------------------------------------------------------------
# Update gian
#-------------------------------------------------------------

def update_gian(kaiji):

  def clean_value(val):
    substitutions = ["　　", "　", "\xa0"]
    for sub in substitutions:
      if val == sub:
        val = ""
    return val


  def parse_main_list(kaiji):

    def get_td_value(tds, i, ttype):
      ret = ""

      if (len(tds) >= i + 1):
        if (ttype == "text"):
          ret = tds[i].text
        if (ttype == "href"):
          if (tds[i].find("a") != None):
            ret = tds[i].find("a")["href"]
            ret = ret.replace("./", "https://www.sangiin.go.jp/japanese/joho1/kousei/gian/" + kaiji + "/")

      # Convert to half-width characters
      ret = convert_to_half(ret)

      # Clean if the value consists of only spaces
      ret = clean_value(ret)

      return ret


    result = [[
      "審議回次",
      "種類",
      "提出回次",
      "提出番号",
      "件名",
      "議案URL",
      "議案要旨",
      "提出法律案",
      "議案審議情報一覧 - 提出日",
      "議案審議情報一覧 - 衆議院から受領／提出日",
      "議案審議情報一覧 - 衆議院へ送付／提出日",
      "議案審議情報一覧 - 先議区分",
      "議案審議情報一覧 - 継続区分",
      "参議院委員会等経過情報 - 本付託日",
      "参議院委員会等経過情報 - 付託委員会等",
      "参議院委員会等経過情報 - 議決日",
      "参議院委員会等経過情報 - 議決・継続結果",
      "参議院本会議経過情報 - 議決日",
      "参議院本会議経過情報 - 議決",
      "参議院本会議経過情報 - 採決態様",
      "参議院本会議経過情報 - 採決方法",
      "参議院本会議経過情報 - 投票結果",
      "衆議院委員会等経過情報 - 本付託日",
      "衆議院委員会等経過情報 - 付託委員会等",
      "衆議院委員会等経過情報 - 議決日",
      "衆議院委員会等経過情報 - 議決・継続結果",
      "衆議院本会議経過情報 - 議決日",
      "衆議院本会議経過情報 - 議決",
      "衆議院本会議経過情報 - 採決態様",
      "衆議院本会議経過情報 - 採決方法",
      "その他の情報 - 公布年月日",
      "その他の情報 - 法律番号",
      "成立法律",
    ]]

    r = requests.get(get_kaiji_url(kaiji))
    html = BeautifulSoup(r.content, "html.parser")
    tables = html.find_all('table')

    for table in tables:
      if "class" in table.attrs:
        if "list_c" in table["class"]:
          summary = table["summary"].replace("一覧", "")

          trs = table.find_all('tr')

          for tr in trs:
            tds = tr.find_all('td')

            if len(tds) >= 1:
              row = [""] * 33
              row[0] = int(kaiji)                         # 審議回次
              row[1] = convert_to_half(summary)           # 種類
              row[2] = int(get_td_value(tds, 0, "text"))  # 提出回次
              row[3] = int(get_td_value(tds, 1, "text"))  # 提出番号
              row[4] = get_td_value(tds, 2, "text")       # 件名
              row[5] = get_td_value(tds, 2, "href")       # 議案URL
              row[6] = get_td_value(tds, 3, "href")       # 議案要旨
              row[7] = get_td_value(tds, 4, "href")       # 提出法律案

              result.append(row)

    return result


  def parse_keika(kaiji, result):

    def parse_keika_individual(row):

      time.sleep(1)
      url = row[5]
      r = requests.get(url)
      html = BeautifulSoup(r.content, "html.parser")

      tables = html.find_all("table")

      for table in tables:
        summary = table["summary"]
        summary = summary.replace("", "")
        trs = table.find_all("tr")

        for i, tr in enumerate(trs):
          th = ""
          td = ""

          if tr.find("th"):
            th = tr.find("th").text

          if tr.find("td"):
            td = tr.find("td").text

          header = summary + " - " + th

          #print(header + " - " + str(i))

          if header in result[0]:
            index = result[0].index(header)
            value = clean_value(td)

            if index in [8,9,10,13,15,17,22,24,26,30]:
              value = convert_to_wcalendar(value)

            row[index] = value

            if header == "参議院本会議経過情報 - 採決方法":
              if "（" in td:
                idx = td.find("（")
                row[20] = td[:idx]

              if tr.find("td").find("a"):
                row[21] = "https://www.sangiin.go.jp" + tr.find("td").find("a")["href"]

          # 成立法律のPDFファイル
          if header == "議案等のファイル情報 - " and i == 1:
            links = tr.find("td").find_all("a")
            if len(links) == 2:
              href = links[1]["href"].replace("../", "https://www.sangiin.go.jp/japanese/joho1/kousei/gian/" + kaiji + "/")
              row[32] = href



    for row in result:
      if (row[5][0:8] == "https://"):
        parse_keika_individual(row)

    return result


  def update_gian_file(kaiji, result):

    # Get existing kaiji CSV
    gian_raw = get_csv(DIR_DATA + "gian.csv")

    # Delete existing kaiji row
    gian_new = []
    for kaiji_row in gian_raw:
      if kaiji_row[0] != kaiji:
        gian_new.append(kaiji_row)

    # Get index of kaiji
    index = len(gian_new)
    for i, kaiji_row in enumerate(gian_new):
      if i == 0:
        continue
      if int(kaiji_row[0]) > int(kaiji):
        index = i
        break

    # Insert into gian
    for row in result[1:]:
      gian_new.insert(index, row)
      index += 1

    save_file(DIR_DATA + "gian.csv", gian_new)
    save_file(DIR_DATA + "gian.json", gian_new)

    # Save sample (for web viewer)
    gian_sample = gian_new[-500:]
    gian_sample.reverse()
    gian_sample.insert(0, gian_new[0])
    save_file(DIR_DATA + "gian_sample.json", gian_sample)



  result = parse_main_list(kaiji)
  result = parse_keika(kaiji, result)
  update_gian_file(kaiji, result)



#-------------------------------------------------------------
# Update giin
#-------------------------------------------------------------

def update_giin(kaiji):

  def clean_name(val):
    val = val.replace("\u3000", "　")
    while "　　" in val:
      val = val.replace("　　", "　")
    return val


  def get_main_list(kaiji):
    r = requests.get("https://www.sangiin.go.jp/japanese/joho1/kousei/giin/" + kaiji + "/giin.htm")
    html = BeautifulSoup(r.content, "html.parser")

    table = html.find_all("table")[1]
    trs = table.find_all("tr")

    result = [[
      "議員氏名",
      "通称名使用議員の本名",
      "議員個人の紹介ページ",
      "読み方",
      "会派",
      "選挙区",
      "任期満了",
      "写真URL",
      "当選年",
      "当選回数",
      "役職等",
      "役職等の時点",
      "経歴",
      "経歴の時点"
    ]]

    for tr in trs:
      tds = tr.find_all("td")

      if len(tds) >= 1:

        # 議員氏名
        name1 = tds[0].text
        name2 = ""

        if "[" in name1:
          name2 = name1.split("[")[1].replace("]", "")
          name1 = name1.split("[")[0]

        name1 = clean_name(name1)
        name2 = clean_name(name2)

        # プロフィールURL
        profile = tds[0].find("a")["href"]
        profile = profile.replace("../", "https://www.sangiin.go.jp/japanese/joho1/kousei/giin/")

        row = [""] * 14

        row[0] = name1
        row[1] = name2
        row[2] = profile
        row[3] = clean_name(tds[1].text)
        row[4] = tds[2].text
        row[5] = tds[3].text
        row[6] = convert_to_wcalendar(tds[4].text)

        result.append(row)

    return result


  def get_giin_detail(row):

    def convert_years(years):
      years = years.replace("年", "")
      years = years.replace("元", "1")
      years = years.replace("昭和", "1925／")
      years = years.replace("平成", "1988／")
      years = years.replace("令和", "2018／")

      ys = years.split("、")
      gs = []
      add = 0

      for y in ys:
        ds = y.split("／")
        g = add + int(ds[0])

        if len(ds) == 2:
          add = int(ds[0])
          g = add + int(ds[1])

        gs.append(str(g))

      return "、".join(gs)


    time.sleep(1)
    r = requests.get(row[2])
    html = BeautifulSoup(r.content, "html.parser")

    # photo_src：写真URL
    photo_div = html.find('div', id="profile-photo")
    photo_src = photo_div.find("img")["src"]
    photo_src = photo_src.replace("../", "https://www.sangiin.go.jp/japanese/joho1/kousei/giin/")

    # years：当選年
    elected = html.find_all("dl", class_="profile-detail")[1].find("dd").text
    years = convert_years(elected.split("／")[1])

    # elected：当選回数
    elected = elected.split("／")[2]
    elected = elected.replace("当選", "")
    elected = elected.replace("回", "")
    elected = elected.replace(" ", "")

    # roles：役職等
    # roles_date：役職等の時点
    roles_str = html.find_all("dl", class_="profile-detail")[2].find("dd").text
    roles = roles_str.splitlines()
    roles_date = roles[0].replace("現在", "")
    roles = "、".join(roles[1:])

    # career：経歴
    career = html.find("p", class_="profile2").text
    career = career.strip("　")

    # career_date：経歴の時点
    career_date = ""
    career_date_p = html.find_all("p", class_="mt10")

    if len(career_date_p) >= 1:
      career_date = career_date_p[0].text.replace("（", "")
      career_date = career_date.replace("現在）", "")

    row[7] = photo_src
    row[8] = years
    row[9] = elected
    row[10] = roles
    row[11] = convert_to_wcalendar(roles_date)
    row[12] = convert_to_half(career)
    row[13] = convert_to_wcalendar(career_date)

  result = get_main_list(kaiji)

  for row in result[1:]:
    get_giin_detail(row)

  #get_giin_detail(result[2])
  #print(result[2])

  save_file(DIR_DATA + "giin.csv", result)
  save_file(DIR_DATA + "giin.json", result)



#-------------------------------------------------------------
# Update kaiha
#-------------------------------------------------------------

def update_kaiha(kaiji):

  def get_main_list(kaiji):

    def split_val(val):
      val = val.replace(")", "")
      svals = val.split("(")
      ivals = [int(svals[0]), int(svals[1])]
      return ivals

    result = [[
      "会派名と略称の時点",
      "会派名",
      "略称",
      "議員数の時点",
      "議員数",
      "議員数／女性",
      "任期1／任期満了",
      "任期1／比例",
      "任期1／比例／女性",
      "任期1／選挙区",
      "任期1／選挙区／女性",
      "任期1／合計",
      "任期1／合計／女性",
      "任期2／任期満了",
      "任期2／比例",
      "任期2／比例／女性",
      "任期2／選挙区",
      "任期2／選挙区／女性",
      "任期2／合計",
      "任期2／合計／女性"
    ]]

    # 会派名と略称
    time.sleep(1)
    r = requests.get("https://www.sangiin.go.jp/japanese/joho1/kousei/giin/kaiha/kaiha" + kaiji + ".htm")
    html = BeautifulSoup(r.content, "html.parser")

    # 会派名と略称の時点
    ta_r = html.find("p", class_="ta_r").text
    ta_r = ta_r.replace("現在", "")
    ta_r = ta_r.strip()

    table = html.find("table")
    trs = table.find_all("tr")

    for tr in trs[1:]:
      tds = tr.find_all("td")

      row = [""] * 20

      row[0] = convert_to_wcalendar(ta_r)
      row[1] = tds[0].text
      row[2] = tds[1].text

      result.append(row)


    # 議員数
    time.sleep(1)
    r = requests.get("https://www.sangiin.go.jp/japanese/joho1/kousei/giin/" + kaiji + "/giinsu.htm")
    html = BeautifulSoup(r.content, "html.parser")
    table = html.find("table")
    trs = table.find_all("tr")

    term1 = trs[0].find_all("th")[1].text.strip().replace("任期満了", "")
    term2 = trs[0].find_all("th")[2].text.strip().replace("任期満了", "")

    # 議員数の時点
    ta_r = html.find("p", class_="ta_r").text
    ta_r = ta_r.replace("現在", "")
    ta_r = ta_r.strip()

    for i, tr in enumerate(trs[2:-3]):
      tds = tr.find_all("td")

      result[i + 1][3]  = convert_to_wcalendar(ta_r)
      result[i + 1][4]  = split_val(tds[0].text)[0]
      result[i + 1][5]  = split_val(tds[0].text)[1]
      result[i + 1][6]  = convert_to_wcalendar(term1)
      result[i + 1][7]  = split_val(tds[1].text)[0]
      result[i + 1][8]  = split_val(tds[1].text)[1]
      result[i + 1][9]  = split_val(tds[2].text)[0]
      result[i + 1][10] = split_val(tds[2].text)[1]
      result[i + 1][11] = split_val(tds[3].text)[0]
      result[i + 1][12] = split_val(tds[3].text)[1]
      result[i + 1][13] = convert_to_wcalendar(term2)
      result[i + 1][14] = split_val(tds[4].text)[0]
      result[i + 1][15] = split_val(tds[4].text)[1]
      result[i + 1][16] = split_val(tds[5].text)[0]
      result[i + 1][17] = split_val(tds[5].text)[1]
      result[i + 1][18] = split_val(tds[6].text)[0]
      result[i + 1][19] = split_val(tds[6].text)[1]


    return result


  result = get_main_list(kaiji)

  save_file(DIR_DATA + "kaiha.csv", result)
  save_file(DIR_DATA + "kaiha.json", result)



#-------------------------------------------------------------
# Update syuisyo
#-------------------------------------------------------------

def update_syuisyo(kaiji):

  def get_main_list(kaiji):

    def get_url(td):
      href = ""
      if td.find("a"):
        href = td.find("a")["href"]
        href = "https://www.sangiin.go.jp/japanese/joho1/kousei/syuisyo/" + kaiji + "/" + href
      return href

    result = [[
      "提出回次",
      "提出番号",
      "件名",
      "提出者",
      "提出人数",
      "質問本文（html）",
      "答弁本文（html）",
      "質問本文（PDF）",
      "答弁本文（PDF）",
      "明細URL",
      "提出日",
      "転送日",
      "答弁書受領日",
      "備考"
    ]]

    r = requests.get("https://www.sangiin.go.jp/japanese/joho1/kousei/syuisyo/" + kaiji + "/syuisyo.htm")
    html = BeautifulSoup(r.content, "html.parser")

    table = html.find_all("table")[1]
    trs = table.find_all("tr")


    for i in range(0, len(trs), 3):
      tr1 = trs[i]
      tr2 = trs[i + 1]
      tr3 = trs[i + 2]

      row = [""] * 14
      row[0] = kaiji
      row[1] = tr2.find_all("td")[0].text.strip()
      row[2] = convert_to_half(tr1.find("td").text.strip())
      row[3] = tr2.find_all("td")[1].text.strip()
      row[4] = 1
      row[5] = get_url(tr2.find_all("td")[2])
      row[6] = get_url(tr2.find_all("td")[3])
      row[7] = get_url(tr3.find_all("td")[0])
      row[8] = get_url(tr3.find_all("td")[1])
      row[9] = get_url(tr1.find("td"))

      # 提出者名
      # ex. "有田　　芳生君"
      # ex. "北條　　秀一君 外4名"
      if row[3][-1:] == "名":
        sp = row[3].split("君 外")
        row[3] = sp[0]
        row[4] = int(sp[1][:-1]) + 1

      if row[3][-1:] == "君":
        row[3] = row[3][:-1]

      while "　　" in row[3]:
        row[3] = row[3].replace("　　", "　")

      result.append(row)

    return result


  def get_meisai_detail(row):
    time.sleep(1)
    r = requests.get(row[9])
    html = BeautifulSoup(r.content, "html.parser")

    tables = html.find_all("table")

    row[10] = convert_to_wcalendar(tables[1].find("td").text)
    row[11] = convert_to_wcalendar(tables[3].find_all("td")[0].text)
    row[12] = convert_to_wcalendar(tables[3].find_all("td")[1].text)
    row[13] = tables[2].find("td").text.strip()

    return row


  def update_syuisyo_file(kaiji, result):

    # Get existing CSV
    existing_csv = get_csv(DIR_DATA + "syuisyo.csv")

    # Delete existing row
    new_csv = []
    for row in existing_csv:
      if row[0] != kaiji:
        new_csv.append(row)

    # Get index
    index = len(new_csv)
    for i, row in enumerate(new_csv):
      if i == 0:
        continue
      if int(row[0]) > int(kaiji):
        index = i
        break

    # Insert into gian
    for row in result[1:]:
      new_csv.insert(index, row)
      index += 1

    save_file(DIR_DATA + "syuisyo.csv", new_csv)
    save_file(DIR_DATA + "syuisyo.json", new_csv)

    # Save sample (for web viewer)
    csv_sample = new_csv[-500:]
    csv_sample.reverse()
    csv_sample.insert(0, new_csv[0])
    save_file(DIR_DATA + "syuisyo_sample.json", csv_sample)


  result = get_main_list(kaiji)

  for row in result[1:]:
    row = get_meisai_detail(row)

  update_syuisyo_file(kaiji, result)



#-------------------------------------------------------------
# Main
#-------------------------------------------------------------

DIR_DATA = get_content_folder()
kaiji = get_latest_kaiji()
update_gian(kaiji)
update_giin(kaiji)
update_kaiha(kaiji)
update_syuisyo(kaiji)
