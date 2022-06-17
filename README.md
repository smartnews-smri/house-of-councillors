# 参議院 会派・議員・議案・質問主意書データ
- 参議院の会派、議員、議案、質問主意書をデータベース化しました。
- 商用・非商用を問わず、自由にデータのダウンロードや検索が可能です。

## 概要

- [参議院のウェブサイト](https://www.sangiin.go.jp/)では会派（政党）、議員、議案、質問主意書といったさまざまな情報が公開されていますが、検索や集計を行うには各ページに分かれたデータを整理する必要があります。
- そこでスマートニュース メディア研究所では、参議院ウェブサイトをクローリングして各データを整理し、CSVやJSONなど機械判読可能なデータで公開するとともに、[閲覧用のページ](https://smartnews-smri.github.io/house-of-councillors/)を作成して自由に検索・集計できるようにしました。

![image_1200_630](https://user-images.githubusercontent.com/12462251/174038900-59da3b9b-829c-4c7f-8dcb-ab18fa6cd0fb.png)

## 公開データの見方

- [/data](https://github.com/smartnews-smri/house-of-councillors/tree/main/data)にデータファイルを公開しています。
  - すべてのデータはCSVとJSONの両方で公開しています。
  - 原則としてデータの表記等は元データに準じますが、以下の変更を加えています。
    - 和暦を西暦に変換し表記をYYYY-MM-DDに統一（例：「令和4年1月28日」→「2022-01-28」）
    - 全角の英数字を半角に統一（例：「ＮＨＫ決算」→「NHK決算」）
    - 氏名などに使われるスペースの重複を圧縮（例：「山東　　昭子」→「山東　昭子」）

### 各データの内容
- [kaiha.csv](https://github.com/smartnews-smri/house-of-councillors/blob/main/data/kaiha.csv) / [kaiha.json](https://github.com/smartnews-smri/house-of-councillors/blob/main/data/kaiha.json)
  - 会派（政党）の名称・略称と、会派別の議員数を掲載するファイルです。
- [giin.csv](https://github.com/smartnews-smri/house-of-councillors/blob/main/data/giin.csv) / [giin.json](https://github.com/smartnews-smri/house-of-councillors/blob/main/data/giin.json)
  - 各議員の氏名や当選年、経歴を掲載するファイルです。
- [gian.csv](https://github.com/smartnews-smri/house-of-councillors/blob/main/data/gian.csv) / [gian.json](https://github.com/smartnews-smri/house-of-councillors/blob/main/data/gian.json)
  - 第153回国会（臨時会、2001年）以降の議案を掲載するファイルです。
- [syuisyo.csv](https://github.com/smartnews-smri/house-of-councillors/blob/main/data/syuisyo.csv) / [syuisyo.json](https://github.com/smartnews-smri/house-of-councillors/blob/main/data/syuisyo.json)
  - 第1回国会（特別会、1947年）以降の質問主意書を掲載するファイルです。


## 閲覧用ページについて
- 本プロジェクトのデータを閲覧・検索できるページを公開しています。
- https://smartnews-smri.github.io/house-of-councillors/
- 検索で絞り込んだデータだけダウンロードすることも可能です。
- なお議案と質問主意書データは量が多いため、閲覧用ページにおいて全件の掲載はしていません。


## 二次利用とライセンスについて
- すべてのデータとソースコードは自由に閲覧・ダウンロードが可能です。
- GitHubプロジェクトのライセンスはMITライセンスとしており、商用・非商用を問わずご自由にお使いいただけます。
- ソースコード等を引用する際の著作権表記は『スマートニュース メディア研究所「参議院 会派・議員・議案・質問主意書データ」』としてください。
- なお、本プロジェクトの利用によって生じたいかなる損害についても、開発者およびスマートニュース株式会社は一切責任を負いません。

