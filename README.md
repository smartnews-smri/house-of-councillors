# 国会議案データベース：参議院
- 参議院の公式ウェブサイトから議案、議員、会派、質問主意書をデータベース化しました。
- 商用・非商用を問わず、自由にデータのダウンロードや検索が可能です。

## 概要

- [参議院のウェブサイト](https://www.sangiin.go.jp/)では議案、議員、会派（政党）、質問主意書といったさまざまな情報が公開されていますが、検索や集計を行うには各ページに分かれたデータを整理する必要があります。
- そこでスマートニュース メディア研究所では、参議院ウェブサイトをクローリングして各データを整理し、CSVやJSONなど機械判読可能なデータで公開するとともに、[閲覧用のページ](https://smartnews-smri.github.io/house-of-councillors/)を作成して自由に検索・集計できるようにしました。

![image_1200_630](https://user-images.githubusercontent.com/12462251/176725779-0d52a061-6568-4472-a558-3bc54bdf70df.png)

## 公開データの見方

- [/data/](https://github.com/smartnews-smri/house-of-councillors/tree/main/data)にデータファイルを公開しています。
  - すべてのデータはCSVとJSONの形式で公開しています（内容は同じです）。
  - 原則としてデータの表記等は元データに準じますが、検索や再利用のため以下の変更を加えています。
    - 和暦を西暦に変換し表記をYYYY-MM-DDに統一（例：「令和4年1月28日」→「2022-01-28」）
    - 全角の英数字を半角に統一（例：「ＮＨＫ決算」→「NHK決算」）
    - 氏名などに使われるスペースの重複を圧縮（例：「山東　　昭子」→「山東　昭子」）

### 各データの内容
- [gian.csv](https://github.com/smartnews-smri/house-of-councillors/blob/main/data/gian.csv) / [gian.json](https://github.com/smartnews-smri/house-of-councillors/blob/main/data/gian.json)
  - 提出された議案の付託委員会、採決結果などを掲載。データは第153回国会（臨時会、2001年）以降。
- [giin.csv](https://github.com/smartnews-smri/house-of-councillors/blob/main/data/giin.csv) / [giin.json](https://github.com/smartnews-smri/house-of-councillors/blob/main/data/giin.json)
  - 各議員の氏名や当選年、経歴を掲載。
- [kaiha.csv](https://github.com/smartnews-smri/house-of-councillors/blob/main/data/kaiha.csv) / [kaiha.json](https://github.com/smartnews-smri/house-of-councillors/blob/main/data/kaiha.json)
  - 会派（政党）の名称・略称と、会派別の議員数を掲載。
- [syuisyo.csv](https://github.com/smartnews-smri/house-of-councillors/blob/main/data/syuisyo.csv) / [syuisyo.json](https://github.com/smartnews-smri/house-of-councillors/blob/main/data/syuisyo.json)
  - 提出された質問主意書の提出者、提出日などを掲載。データは第1回国会（特別会、1947年）以降。


## 閲覧用ページについて
- 本プロジェクトのデータを閲覧・検索できるページを公開しています。
- https://smartnews-smri.github.io/house-of-councillors/
- 検索で絞り込んだデータのみダウンロードすることも可能です。
- なお議案と質問主意書データは量が多いため、閲覧用ページにおいて全件の掲載はしていません。


## 二次利用とライセンスについて
- すべてのデータとソースコードは自由に閲覧・ダウンロードが可能です。
- GitHubプロジェクトのライセンスはMITライセンスとしており、商用・非商用を問わずご自由にお使いいただけます。
- ソースコード等を引用する際の著作権表記は「スマートニュース メディア研究所」または「SmartNews Media Research Institute」としてください。
- なお、本プロジェクトの利用によって生じたいかなる損害についても、スマートニュース株式会社は一切責任を負いません。
