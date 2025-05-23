# TTFファイルから、ビットマップ形式のフォントファイルを作成するためのユーティリティ。

現在のところ、C言語、Pythonのソースコード、バイナリの出力が可能。
そのうち、FONTXとかに出せるようにしたい。

## PyFontConverterの使い方

1. [PyFontConverterのGitHub](https://github.com/HisayukiNomura/PyFontConverter) から `font.py` をダウンロードします。
2. コマンドラインで以下のように実行します。

```
python font.py [オプション] フォントファイル(ttf)
```

## 主なコマンドラインオプション

| オプション | 説明 |
|------------|------|
| font_path  | 変換元のTrueTypeフォントファイル（.ttf）を指定（必須） |
| -n, --name | 出力データや構造体の名前を指定（省略時は自動生成） |
| -s, --size | 出力ビットマップのサイズ（省略時は12） |
| -xo, --xoffset | 文字の横方向オフセット（省略時は0） |
| -yo, --yoffset | 文字の縦方向オフセット（省略時は-1） |
| -cs, --codeset | 収録文字セット（ALL, LEVEL1, SCHOOL, CUSTOM, TEST） |
| -cf, --charfile | CUSTOM指定時に使用する文字リストファイル |
| -o, --output | 出力ファイル名（省略時は自動生成） |
| -m, --mapping | 特定文字グループのマッピング（KANA, NONE） |
| -em, --endmark | データ終端マークの種類（ALLZERO, ALLMAX, NONE） |
| -t, --outtype | 出力フォーマット（CData, PBinary, Python） |
| -fr, --filereplace | ファイル名の不適切文字をアンダースコアに置換 |
| -v, --verbose | 詳細出力 |
| -i, --image | フォント画像を表示 |

#### 例

```
python font.py JF-Dot-Shinonome12.ttf -s 12 -cs SCHOOL -o MyFont.h
```

### 注意事項

- 小さいサイズのビットマップを作成する場合は、ドットフォントなど小サイズ向けのフォントを推奨します。
- Windows標準のMS明朝などは小サイズ変換に向きません。
- 無料で商用利用可能な小サイズ向けフォント例：[http://jikasei.me/font/jf-dotfont/](http://jikasei.me/font/jf-dotfont/)  
  [直接ダウンロード](https://ftp.iij.ad.jp/pub/osdn.jp/users/8/8541/jfdotfont-20150527.7z)

### 出力ファイルについて

- デフォルトではC++ヘッダファイル（.h）として出力されます。
- バイナリ形式やPython形式での出力も可能です（-tオプション）。
- 生成されたヘッダファイルはKNJGfx9341プロジェクトのフォントデータとして利用できます。

---