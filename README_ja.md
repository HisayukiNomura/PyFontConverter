# TTFファイルから、ビットマップ形式のフォントファイルを作成するためのユーティリティ。

現在のところ、C言語、Pythonのソースコード、バイナリ、FontX、BDFの出力が可能です。


## 準備
必要なパッケージをインストールします。

```
pip install -r requirements.txt
```

## PyFontConverterの使い方

1. [PyFontConverterのGitHub](https://github.com/HisayukiNomura/PyFontConverter) から `font.py` をダウンロードします。
2. コマンドラインで以下のように実行します。

```
python font.py [オプション] フォントファイル(ttf)
```


### 主なオプションとデフォルト値

| オプション | 説明 | デフォルト値 |
|------------|------|-------------|
| `-h, --help` | ヘルプメッセージを表示して終了します。 | - |
| `-n, --name NAME` | C 言語ヘッダファイルで生成される構造体の名前を指定します。<br>指定しない場合は、ファイル名や他の引数に基づいて自動生成されます。 | 自動生成 |
| `-s, --size SIZE` | フォントサイズを指定します。<br>全角文字は指定したサイズの正方形に変換されます。<br>半角文字は、指定したサイズの半分の幅で描画されます。 | `12` |
| `-xo, --xoffset XOFFSET` | 文字の水平方向シフト量（ピクセル単位）を指定します。<br>TrueTypeフォントが描画されると、隣接する文字が近すぎて読みづらくなることがあります。<br>このオフセットを使用することで、文字間の余分なパディングを調整できます。 | `0` |
| `-yo, --yoffset YOFFSET` | 文字の垂直方向シフト量（ピクセル単位）を指定します。<br>`-xo` オプションと同様に、文字間の調整に役立ちます。 | `-1` |
| `-cs, --codeset {ALL,LEVEL1,SCHOOL,CUSTOM,TEST}` | データに含める文字セットを指定します。<br>**ALL:** JIS レベル1・2の漢字、記号、カタカナ、ひらがなを含みます。<br>**LEVEL1:** JIS レベル1の漢字、記号、カタカナ、ひらがなを含みます。<br>**SCHOOL:** 小学校で学習する漢字、ひらがな、カタカナ、記号を含みます。<br>**CUSTOM:** `-cf` で指定した文字セットを使用します。<br>**TEST:** デバッグ用の小さな文字セット。 | `ALL` |
| `-cf, --charfile CHARFILE` | 出力に含める文字リストを格納したテキストファイルを指定します。<br>`-cs CUSTOM` を使用する場合、このオプションは必須です。 | - |
| `-o, --output OUTPUT` | 出力ファイルの名前を指定します。<br>指定しない場合は、ソースファイル名、フォントサイズ、コードセットに基づいて自動生成されます。<br>出力タイプによっては、半角文字と全角文字が別々のファイルとして出力されることがあります。 | 自動生成 |
| `-m, --mapping {KANA,NONE}` | 特定の文字グループを代替グリフにマッピングします。<br>**KANA:** シングルバイトのカナコードを、半角カナ（UTF-8 の `0xFF61–0xFF9F`）にマッピングします。<br>**NONE:** マッピングなし（ISO8859準拠）。 | `KANA` |
| `-em, --endmark {ALLZERO,ALLMAX,NONE}` | データの末尾に追加する終了マークのタイプを指定します。<br>このオプションは **特定の言語 (C や Python) で `-t` または `--outtype` が指定された場合のみ有効** です。<br>**ALLZERO:** UTF8、SJIS、JIS の値をすべて `0` に設定した終了マーカーを追加。<br>**ALLMAX:** UTF8、SJIS、JIS の値を `MAX` に設定した終了マーカーを追加。<br>**NONE:** 終了マークなし。 | `ALLZERO` |
| `-t, --outtype {CData,PBinary,Python,FONTX2,BDF}` | 出力フォントデータの形式を指定します。<br>**CData:** C 言語の構造体とビットマップ配列（ヘッダファイル）。<br>**PBinary:** バイナリファイル（コードとビットマップ用）。<br>**Python:** フォントデータを含む Python ファイルとして出力。<br>**FONTX2:** FONTX2 形式で出力（半角・全角を別々のファイルとして出力）。<br> **BDF:** BDF 形式で出力| `CData` |
| `-bs , --bdf-split {Default,True,False} `|BDFファイル出力時に、全角文字と半角文字を別々のファイルに出力します。<br>出力タイプがBDF以外の場合、Trueを指定するとエラーになります。<br>**Default** BDFファイルの場合True、それ以外の場合は出力タイプに従います。<br>**True** BDFファイルの全角と半角文字を別のファイルとして出力します。<br>**False** 全角と半角が混在した、１つのファイルを出力します|`Default`|
| `-en , --encoding {UTF8,SJIS,JIS}` |　出力されるファイルのエンコーディングを指定します。BDFファイルでは各文字のエンコード指定、C言語やPythonなどでは並び替え順に使われる文字コードです。<br/>デフォルト値は-tの指定により異なります。CヘッダやPythonの場合はUTF8、FONTXの場合はSJIS、BDFの場合はJISコードです。|-t　に従う|
| `-fr, --filereplace` | 出力ファイル名に適さない文字（空白や記号など）を `_` に置き換えます。 | - |
| `-v, --verbose` | 詳細なデバッグ情報を表示します。 | - |
| `-i, --image` | デバッグのため、実行中に変換している文字の画面を表示します。<br>`xoffset` や `yoffset` の調整を行う際に便利です。 | - |




### ヘルプについて

--helpを付けて起動すると、何もせずに使い方が表示されます。

使い方はシステムロケールにより日本語、もしくは英語で表示されますが、環境変数 LANGの値を"ja_JP"、"en_US"などに指定することで変更できます。

#### 例

```
python font.py JF-Dot-Shinonome12.ttf -s 12 -cs SCHOOL -o MyFont.h
```
　JF-Dot-Shinonome12.ttf　というTrueTypeフォントを、12x12ドットに変換します。教育漢字だけを含んだC言語のヘッダファイルとして、MyFont.hという名前で出力します。

```
python font.py FONTDATA/ipam.ttf -s 24 -cs ALL -t FONTX2 -o IPAMincho   
```
カレントディレクトリ/FONTDATA/ipam.ttfファイルを、24x24ドットのIPAMincho_zen.fnt（全角文字）と、12x24ドットのIPAMincho_han.fnt（半角文字）に変換します。全角文字は、JIS第一水準、第二水準と記号、かなカナ、その他（ギリシャ文字やキリル文字）を含みます。




### 注意事項

- 小さいサイズのビットマップを作成する場合は、ドットフォントなど小サイズ向けのフォントを推奨します。
- Windows標準のMS明朝などは小サイズ変換に向きません。
- 無料で商用利用可能な小サイズ向けフォント例：[http://jikasei.me/font/jf-dotfont/](http://jikasei.me/font/jf-dotfont/)  
  [直接ダウンロード](https://ftp.iij.ad.jp/pub/osdn.jp/users/8/8541/jfdotfont-20150527.7z)

### 出力ファイルについて

- デフォルトではC++ヘッダファイル（.h）として出力されます。
- バイナリ形式やPython形式での出力も可能です（-tオプション）。
- 生成されたヘッダファイルはKNJGfx9341プロジェクトのフォントデータとして利用できます。


## ライセンスについて

このプロジェクトはMITライセンスのもとで公開されています。

```
MIT License

Copyright (c) 2025 Hisayuki Nomura

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```


※注意：FONTDATAディレクトリに存在する変換後のフォントファイルの権利は、変換元になったフォントの権利に従います。



---