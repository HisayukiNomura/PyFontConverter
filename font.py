# -*- coding: utf-8 -*-
#
# MIT License
# Copyright (c) 2025 Hisayuki Nomura
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import codecs
import argparse
import struct
from pathlib import Path
import sys
import os
import locale


def GetMessage(isJapanese,msgKey):
    messages = {
    "en" : {
"general" : 
"""Convert Bitmap data file from TrueType(.TTF) file.

This program is a tool for generating bitmap font data from TrueType (.ttf) font files, including Japanese characters.
It can output the data in various formats such as C language header files, binary, Python, and FONTX2.""",
"epilog" :
"""note:
When converting to small-sized images, carefully choose the font file. 
Fonts commonly used in GUI-based operating systems (such as MS-Mincho) may not convert well into clean small images.If you need to convert to a small size, it is recommended to use fonts specifically designed for small sizes, such as those with embedded bitmaps, for better results.Specify a source font file with the extension .ttf for conversion.

Here is the information about free fonts suitable for small sizes, including those available for commercial use:
- Information on Free Fonts: [http://jikasei.me/font/jf-dotfont/]
- Direct Download Link: [https://ftp.iij.ad.jp/pub/osdn.jp/users/8/8541/jfdotfont-20150527.7z]""",
"font_path": "Path to the TrueType font file (.ttf) to be converted.",
"--name" : "Specify the name of the structure to be generated in the C language header file.\nIf not specified, it will be automatically generated based on the file name or other arguments.",
"--size" : "The size of the output bitmap. \n Multibyte characters (aka. 全角) are converted into squares with equal width and height. \nSingle-byte characters (aka. 半角) are drawn with a width that is half of the size specified here. \nIf not specified, the default size is 12.",
"--xoffset" : "Specify the number of pixels to shift characters horizontally or vertically.\nWhen TrueType fonts are rendered, adjacent characters may appear too close together, making them difficult to read.\r\nTo avoid this, characters usually have extra padding on all sides—top, bottom, left, and right.\r\nDuring data conversion, this padding may cause characters to exceed the specified size (set with the -s option) or result in unnatural spacing between characters.\nUse this offset to minimize padding or position it as needed, improving control over the output.\nIf unspecified, the default value is 0.",
"--yoffset" : "Reffer to -xo option.\n If not specified, the default value is -1.\n",
"--codeset" : "Code Sets to Include in the Data\n" \
                "- ALL: Includes JIS Level 1, Level 2 characters, various symbols, Kana, and all other supported characters.\n" \
                "- LEVEL1: Includes JIS Level 1 characters, various symbols, Kana, and all other supported characters.\n" \
                "- SCHOOL: Includes educational Kanji (learned by the end of 6th grade in elementary school), Hiragana, Katakana, and various symbols.\n" \
                "- CUSTOM: Specify the characters used in a text file with the '-cf' argument.\n" \
                "- TEST: A smaller set of characters intended for debugging purposes. Used during testing and contains fewer characters.\n" \
                "If not specified, the default value is ALL. ",
"--charfile" : "Specify a text file containing the list of characters to include in the output. \nEach character in the file will be used for font data generation. \nThis option is required when using the CUSTOM code set (-cs CUSTOM).",
"--output" : "Specifies the name of the output file.\nDepending on the output type, half-width and full-width characters may be generated as separate files\nIf not specified, the file name will be automatically generated based on the source file name, font size, and code set.",
"--mapping" : "Mapping Specific Character Groups to Alternative Glyphs.\n" \
                "- KANA: Remap single-byte Kana code\n" \
                "\tOn many Japanese retro-computers, the single-byte codes 0xA1-0xDF(a range where international characters are defined in ISO8859)\n" \
                "\tare typically assigned to half-width Kana characters.\n" \
                "\tWhen this option is selected, the glyphs in the range 0xA1-0xDF are mapped to the glyphs for half-width characters in UTF-8 (range 0xFF61–0xFF9F).\n" \
                "- NONE: No mapping conversion is performed.\n" \
                "\tFor example, the single-byte codes 0xA1–0xDF will result in undefined glyphs following the ISO8859 standard, leading to unexpected character shapes.\n" \
                "\tif not specified, the default value is KANA.",

"--endmark" :"Specify the Type of End Mark to Add at the End of the Data.\n"
            "Defines the type of end mark to append at the end of the data. A special line indicating the termination will be added to the end of the data.\n" \
            "This option is only applicable when `-t` or `--outtype` is specified for a particular language, such as C or Python.\n" \
            "For example, in C, the termination marker may be structured as an array or macro definition, while in Python, \n" \
            "it could be represented as a specific byte sequence or dictionary entry.\n" \
            "- ALLZERO: Appends a termination marker where all values for UTF8, SJIS, and JIS are set to zero.\n" \
            "- ALLMAX: Appends a termination marker where all values for UTF8, SJIS, and JIS are set to MAX VALUE.\n" \
            "- NONE: No termination mark will be used.\n" \
            "If not specified, the default value is ALLZERO.\n",
"--outtype" : "Specifies the format of the output font data.\n" \
            "CData: Outputs as a C language struct and bitmap array (header file).\n" \
            "PBinary: Outputs as binary files (for code and bitmap). \n" \
            "Python: Outputs as a Python file containing font data.\n" \
            "FONTX2: Outputs in FONTX2 format (alf-width and full-width characters are output as separate files." \
            "If not specified, the default is CData.", 
"--filereplace" : "Replace inappropriate characters in output file names (such as spaces and mathematical symbols) with underscores.",
"--bdf-split" : "If set with -t BDF, outputs half-width and full-width characters as separate BDF files.",
"--verbose" : "Enable verbose output mode.\n",
"--image" : "To assist with debugging, the screen displays the characters being converted during execution. This is useful when adjusting xoffset and yoffset\n",
"--encoding" : "Encoding to use for the output file. " ,
"err_codeblock" : "Error: Block number overflow. In FONTX, consecutive character codes are managed as blocks in a table and maximum block number is 256.\n" 
                    "This character set required {} of blocks and unable to represent in FONTX2 format." 
                    "Change the code set specified with -cs or output in a format other than FONTX2." ,
"err_codefileReqired" : "Error: -cf option is required when -cs CUSTOM is specified." ,
"err_codefilenotexist" : "Error: The specified character file {} does not exist. Please check the path and file name." ,
"err_invalidcodepoint" : "Error: Invalid Unicode code-point {}.",
"err_decordingerror":  "Error: Decorging error for {} : {}",
"err_fontfilenotexist" : "Error: The specified font file {} does not exist. Please check the path and file name.",
"err_fontfileinvalid" : "Error: Failed to load the specified font file {}. Exception: {}",
"err_logicerror" : "Error: Logic error. This should not happen.  Please report this issue to the developer. Line:{} - Msg:{}",
"err_notsupportedencoding" : "Error: The specified encoding {} is not supported.",
"err_cannotuseenc" : "Error: The specified encoding {} cannot use in {}.",
"err_bdfsplitonlybdf": "Error: The --bdf-split option can only be used with the BDF output type (-t BDF).",


"log_gencodetbl" : "Generating code table for {} characters....",
"log_removingcodetbl" : "Removing non-Kyouiku-kanji characters....",
"log_removeunused" : "Removing unused characters....",
"log_readingcodefile" : "Reading code file {}....",
"log_outputcontains" : "Output contains following characters\n{}",
"log_sorting" : "Sorting code list by {} code....",
"log_genbitmap" : "Generating Bitmap data...",
"log_rendering" : "render_glyph_to_bitmap: Rendering glyphs {} (Unicode: {})",
"log_success" : "Success: Output file {} was created.",
"log_done" : "done.",
"log_creatingimg" : "Creating {}x{} image and drawing object.",
"log_drawing2mem" : "Drawing character to offscreen image.",
"log_ctrlchar" : "Unprintable half-size character.",
"log_halfsizechar" : "Half-size character.",
"log_fullsizechar" : "Full-size character.",
"log_remapping" : "re-mapping for Hankaku-Kana character {}({}) -> {}({}) , draw and  crop to half-size",
"log_cropping" : "Cropping half-size Kana character to half size",
"log_dispimage" : "Displaying the image. Please close the window before pressing [ENTER]...",
"log_donewithsize" : "done. Image size: {}",
"log_getcodetbl" : "Get Code table for {}-{}",
"log_analyzingcode" : "Analyzing Code as a single-byte code. {} is ",
"log_ishankakukana" : "half-size kana character {}.",
"log_isascii" : "ascii character {} \"{}\".",
"log_isnonprintableascii" : "non-printable ascii character {}.",
"log_codedisp" : "JIS: {}, Shift-JIS: {}, UTF-8: {}",
"log_analyzingmulticode" : "Analyzing Code as a multi-byte code. {}  ",
"log_skippingcode" : "Skipping code {}. No UTF-8 assigned for this code.",
"log_convdatabitmap" : "convToDataAndBitmap:: count:{} , Size=({},{}), Offset=({},{})",
"log_converting" : "Converting UTF-8:{}, SJIS:{}, JIS:{}, Character:\"{}\",Offset:{}",
"log_doneconvert" : "done. code list count = {} , bitmap list count = {}",
"log_genoutput" : "Generating output file {}",
},
    "ja" : {
"general" : 
"""TrueType(.TTF)フォントファイルからビットマップデータファイルを変換します。

このプログラムは、TrueTypeフォント（.ttf）ファイルから日本語を含む各種文字のビットマップデータを生成し、C言語ヘッダファイルやバイナリ、Python、FONTX2形式など複数の形式で出力するツールです。""",
"epilog" :
"""注意：
小型の画像に変換する場合は、フォントファイルを慎重に選択してください。
GUIベースのオペレーティングシステム（MS-Minchoなど）で一般的に使用されるフォントは、クリーンな小型画像に変換するのに適していない場合があります。小型サイズに変換する必要がある場合は、ビットマップが埋め込まれた小型サイズ用に設計されたフォントを使用することをお勧めします。変換には、拡張子が.ttfのソースフォントファイルを指定してください。
以下は、商用利用可能な小型サイズに適した無料フォントに関する情報です。
- 無料フォントの情報: [http://jikasei.me/font/jf-dotfont/]
- 直接ダウンロードリンク: [https://ftp.iij.ad.jp/pub/osdn.jp/users/8/8541/jfdotfont-20150527.7z]""",
"font_path": "変換するTrueTypeフォントファイル(.ttf)のパスを指定します。",
"--name" : "C言語ヘッダファイルで生成される構造体の名前を指定します。\r\n指定しない場合は、ファイル名や他の引数に基づいて自動的に生成されます。",
"--size" : "出力されるビットマップのサイズを指定します。\r\nマルチバイト文字（全角）は、指定されたサイズの正方形に変換されます。\r\nシングルバイト文字（半角）は、指定されたサイズの半分の幅で描画されます。\r\n指定しない場合、デフォルトサイズは12です。",
"--xoffset" : "文字を水平方向または垂直方向にシフトするピクセル数を指定します。\r\nTrueTypeフォントが描画されると、隣接する文字が近すぎて読みづらくなることがあります。\r\nこれを避けるために、通常、文字は上下左右に余分なパディングをもっています。\r\nデータ変換中、このパディングが原因で指定されたサイズ（-sオプションで設定）を超えたり、不自然な文字間の空白が生じる可能性があります。\r\nこのオフセットを使用して、パディングを最小限に抑えるか、必要な場所に配置し、出力の制御を改善します。\r\n指定しない場合、デフォルト値は0です。",
"--yoffset" : "xoオプションを参照してください。\n指定しない場合、デフォルト値は-1です。\n",
"--codeset" : "データに含める文字セットを指定します。\n" \
                "- ALL: JISレベル1、レベル2の文字、各種記号、カタカナ、ひらがななど、サポートされているすべての文字を含みます。\n" \
                "- LEVEL1: JISレベル1の文字、各種記号、カタカナ、ひらがななど、サポートされているすべての文字を含みます。\n" \
                "- SCHOOL: 小学校6年生までに学習する教育漢字、ひらがな、カタカナ、各種記号を含みます。\n" \
                "- CUSTOM: '-cf'引数で指定されたテキストファイルに使用されている文字を指定します。\n" \
                "- TEST: デバッグ目的で使用される小さな文字セット。テスト用に使用され、文字数が少ないです。ソースコードを変更してください\n" \
                "指定しない場合、デフォルト値はALLです。",
"--charfile" : "出力に含める文字のリストを含むテキストファイルを指定します。\n各文字は、フォントデータ生成に使用されます。\nCUSTOMコードセット（-cs CUSTOM）を使用する場合、このオプションは必須です。",
"--output" : "出力ファイルの名前を指定します。\n指定しない場合、ソースファイル名、フォントサイズ、コードセットに基づいて自動的に生成されます。出力タイプによっては半角文字と全角文字が別々のファイルとして出力されることもあります。",
"--mapping" : "特定の文字グループを代替グリフにマッピングします。\n" \
                "- KANA: シングルバイトのカナコードをマッピングします。\n" \
                "\t多くの日本のレトロコンピュータでは、シングルバイトコード0xA1-0xDF（ISO8859で国際文字が定義されている範囲）は、通常、半角カナ文字に割り当てられています。\n" \
                "\tこのオプションを選択すると、範囲0xA1-0xDFのグリフがUTF-8の半角文字（範囲0xFF61–0xFF9F）のグリフにマッピングされます。\n" \
                "- NONE: マッピング変換は行われません。\n" \
                "\t例えば、シングルバイトコード0xA1–0xDFはISO8859標準に従って未定義のグリフとなり、予期しない文字形状になります。\n" \
                "\t指定しない場合、デフォルト値はKANAです。",
"--endmark" :"データの末尾に追加する終了マークのタイプを指定します。\n" \
            "このオプションは、特定の言語（CやPythonなど）で`-t`または`--outtype`が指定された場合にのみ適用されます。\n" \
            "GetMessage例えば、Cでは終了マーカーは配列やマクロ定義として構造化され、Pythonでは特定のバイトシーケンスや辞書エントリとして表現されることがあります。\n" \
            "- ALLZERO: UTF8、SJIS、JISのすべての値がゼロに設定された終了マーカーを追加します。\n" \
            "- ALLMAX: UTF8、SJIS、JISのすべての値が最大値に設定された終了マーカーを追加します。\n" \
            "- NONE: 終了マークは使用されません。\n" \
            "指定しない場合、デフォルト値はALLZEROです。\n",

"--outtype" : "出力フォントデータの形式を指定します。\n" \
            "CData: C言語の構造体とビットマップ配列として出力（ヘッダファイル）。\n" \
            "PBinary: バイナリファイルとして出力（コードとビットマップ用）。\n" \
            "Python: フォントデータを含むPythonファイルとして出力。\n" \
            "FONTX2: FONTX2形式で出力（半角文字と全角文字は別々のファイルとして出力）。\n" \
            "指定しない場合、デフォルトはCDataです。",
"--filereplace" : "出力ファイル名の不適切な文字（スペースや数学記号など）をアンダースコアに置き換えます。",
"--bdf-split" : "BDF形式で出力する場合、半角文字と全角文字を別々のBDFファイルとして出力します。",
"--verbose" : "出力の詳細を表示します。\n" ,
"--image": " デバッグのため、実行中に変換している文字の画面を表示させます。xoffsetやyoffsetの調整を行う際に便利です。\n" ,
"--encoding" : "使用されるエンコーディングを指定します。 " ,
"err_codeblock" : "エラー: ブロック番号のオーバーフローです。FONTXでは、連続する文字コードはテーブル内のブロックとして管理され、最大ブロック数は256です。\n" \
                "この文字セットでは{}のブロックが必要で、FONTX2形式で表現できません。\n" \
                "コードセットを変更するか、FONTX2以外の形式で出力してください。",
"err_codefileReqired" : "エラー: -cs CUSTOMを指定した場合、-cfオプションが必要です。",
"err_codefilenotexist" : "エラー: 指定された文字ファイル {} が存在しません。パスとファイル名を確認してください。",
"err_invalidcodepoint" : "エラー: Unicode {} のコードポイントが不正です",
"err_decordingerror":  "エラー: 文字 {} のデコードに失敗しました: {}",
"err_fontfilenotexist" : "エラー: 指定されたフォントファイル {} が存在しません。パスとファイル名を確認してください。",
"err_fontfileinvalid" : "エラー: 指定されたフォントファイル {} の読み込みに失敗しました。例外：{}",
"err_logicerror" : "エラー: ロジックエラーです。これは発生しないはずです。開発者にこの問題を報告してください。行:{} - メッセージ:{}",
"err_notsupportedencoding" : "エラー: 指定されたエンコーディング {} はサポートされていません。",
"err_cannotuseenc" : "エラー: 指定されたエンコーディング {} は {} では使用できません。",
"err_bdfsplitonlybdf": "エラー: --bdf-splitオプションはBDF出力タイプ（-t BDF）でのみ使用できます。",

"log_gencodetbl" : "{}文字のコードテーブルを生成しています....",
"log_removingcodetbl" : "教育漢字以外の文字を削除しています....",
"log_readingcodefile" : "文字ファイル {} を読み込んでいます....",
"log_outputcontains" : "出力ファイルは次の文字を含んでいます{}",
"log_sorting" : "{}コードでコードリストをソートしています....",
"log_genbitmap" : "ビットマップデータを生成しています...",
"log_rendering" : "render_glyph_to_bitmap: グリフ {} (Unicode: {}) をレンダリングしています",
"log_success" : "成功しました。出力ファイル {} が作成されました",
"log_done": "完了しました。",
"log_creatingimg" : "{}x{}の画像と描画オブジェクトを作成しています。",
"log_drawing2mem" : "オフスクリーン画像に文字を描画しています。",
"log_ctrlchar" : "印刷不能な制御文字です",
"log_halfsizechar" : "半角文字です。",
"log_fullsizechar" : "全角文字です。",
"log_remapping" : "半角カナ文字 {}({}) を {}({}) に再マッピングし、半分のサイズで描画しています",
"log_cropping" : "半角カナ文字のサイズを半分にしています",
"log_dispimage" : "画像を表示しています。ウィンドウを閉じてから[ENTER]を押してください...",
"log_donewithsize" : "完了しました。画像サイズ: {}",
"log_getcodetbl" : "{}-{}のコードテーブルを取得しています",
"log_analyzingcode" : "シングルバイトコードとして解析中・・・コード {} は",
"log_isHankakuKana" : "半角カナ文字の{}です",
"log_isascii" : "ASCII文字 {} \"{}\" です。",
"log_isnonprintableascii" : "印刷できないASCII文字 {} です。",
"log_codedisp" : "JIS: {}, Shift-JIS: {}, UTF-8: {}",
"log_analyzingmulticode" : "マルチバイトコードとして解析中・・・コード {} です",
"log_skippingcode" : "コード {} をスキップします。このコードにはUTF-8が割り当てられていません。",
"log_convdatabitmap" : "convToDataAndBitmap:: 数:{} , サイズ=({},{}), オフセット=({},{})",
"log_converting" : "変換中: UTF-8:{}, SJIS:{}, JIS:{}, 文字:\"{}\", オフセット:{}",
"log_doneconvert" : "完了しました。コードリストの数 = {} , ビットマップリストの数 = {}",
"log_genoutput" : "出力ファイル {} を生成しています",
},

    }

    if isJapanese:
        return messages["ja"].get(msgKey, f"Message not found.({msgKey})")
    else:
        return messages["en"].get(msgKey, f"Message not found.({msgKey})")




#二段階入れ子の要素数
def total_size(obj):
    count = 0
    
    for item in obj:
        count +=  item.size  # 各要素のサイズを加算
    return count


#与えられたUnicodeコードポイントをUTF-8文字にデコードする関数
def decode_utf8(codeUTF8):
   

    # 必要なバイト数を計算
    # 1バイト: 0x00-0x7F, 2バイト: 0x80-0x7FF, 3バイト: 0x800-0xFFFF, etc.
    if codeUTF8 <= 0xFF:
        byte_length = 1
    elif codeUTF8 <= 0xFFFF:
        byte_length = 2
    elif codeUTF8 <= 0xFFFFFF:
        byte_length = 3
    elif codeUTF8 <= 0xFFFFFFFF:
        byte_length = 4
    else:
        raise ValueError(GetMessage(isJapanese,"err_invalidcodepoint").format(hex(codeUTF8)))

    # バイト列を生成
    utf8_bytes = codeUTF8.to_bytes(byte_length, byteorder='big')

    # UTF-8としてデコード
    try:
        unicode_char = utf8_bytes.decode('utf-8')
    except UnicodeDecodeError as e:
        raise ValueError(GetMessage(isJapanese,"err_decordingerror").format(hex(codeUTF8),e))

    return unicode_char

## フォントをビットマップにレンダリングする関数
def render_glyph_to_bitmap(font, char_unicode , char, font_XSize=64,font_YSize=64,X_offset = 0,Y_offset=-1):
    if isVerbose:
        print("\t\t" + GetMessage(isJapanese,"log_rendering").format(char ,hex(char_unicode) ))
    global isImage

    # ビットマップ画像を作成
    if isVerbose:
        print("\t\t\t" + GetMessage(isJapanese,"log_creatingimg").format(font_XSize,font_YSize))

    image_size = (font_XSize , font_YSize )  # 画像サイズを指定
    image = Image.new("L", image_size, color=255)  # グレースケール画像（白背景）
    draw = ImageDraw.Draw(image)
    
    #半角文字の場合には、半分のサイズにする
    if isVerbose:
        print("\t\t\t" + GetMessage(isJapanese,"log_drawing2mem"))
    if (len(char) == 4) :           # 印刷不能の１バイト文字。何もせず、イメージのサイズを半分にする。（半角なので）
        if isVerbose:
            print("\t\t\t\t"+ GetMessage(isJapanese,"log_ctrlchar"))
        image = image.crop((0,0,font_XSize/2,font_YSize))
    elif char_unicode <= 0xFF :        # 半角文字の場合
        if isVerbose:
            print("\t\t\t\t" + GetMessage(isJapanese,"log_halfsizechar"))
        if mapping == "KANA" and char_unicode >= 0xA1 and char_unicode <= 0xDF : # カナ文字にマッピングする場合、半角文字のカナ文字は、半角カナ文字にマッピングを変える
            charwk = chr(char_unicode - 0xa1 + 0xFF61)  # 半角カナに変換
            if isVerbose:
                print("\t\t\t\t" + GetMessage(isJapanese,"log_remapping").format(chr(char_unicode), hex(char_unicode), charwk , hex(ord(charwk))))
            draw.text((X_offset, Y_offset), charwk, font=font, fill=1)  # 文字を黒で描画
            image = image.crop((0,0,font_XSize/2,font_YSize))
        else:           # 半角文字の場合                                            # 何もしない場合、ASCIIの拡張コードのママとする
            if isVerbose:
                print("\t\t\t\t" + GetMessage(isJapanese,"log_cropping"))
            draw.text((X_offset, Y_offset), char, font=font, fill=1)  # 文字を黒で描画
            image = image.crop((0,0,font_XSize/2,font_YSize))
    else:                           # 全角文字の場合
        if isVerbose:
            print("\t\t\t\t" + GetMessage(isJapanese,"log_fullsizechar"))
        draw.text((X_offset, Y_offset), char, font=font, fill=1)  # 文字を黒で描画
    
    if isImage:
        image.show()
        print(GetMessage(isJapanese,"log_dispimage"))
        input()  
    if isVerbose:
        print("\t\t" + GetMessage(isJapanese,"log_donewithsize").format(image.size))
    return image

## 画像データを、ビットマップ配列にする
def display_bitmap_data(image):
    # 画像データをNumPy配列に変換
    bitmap_data = np.array(image)
    #print("ビットマップデータ:")
    #print(bitmap_data)  # 数値データをコンソールに表示

    # ビットマップとして0と1のデータに変換
    binary_bitmap = (bitmap_data < 128).astype(int)  # しきい値128で白黒に変換
    #print("バイナリ形式のビットマップデータ:")
    #print(binary_bitmap)  # コンソールに0と1のデータ
    
    ArraySizeY,ArraySizeX  = binary_bitmap.shape
    ArraySizeX = round(ArraySizeX/8)
    if (ArraySizeX == 0) :
        ArraySizeX = 1
    
    bitArray = np.zeros((ArraySizeY, ArraySizeX), dtype=np.uint8)  # ビット配列を初期化


    for i , row in enumerate(binary_bitmap) :
        padding_length = padding_length = (8 - len(row) % 8) % 8
        #print (f"{padding_length}")
        padded_row = np.pad(row,  ( 0,padding_length), constant_values= 0 ) 
        #print(f"{padded_row}")
        byte_array = np.packbits(padded_row)  # ビットをバイトに変換
        #print("value=",end=":")
        for value in byte_array :
            #print(bin(value)[2:].zfill(8),end="")  # バイナリ形式で表示
            bitArray[i] = byte_array

    return bitArray




import codecs
# JISコードをShift-JISとUTF-8に変換する関数
def jis_to_encodings(jis_code):
    """
    JISコードをShift-JISとUTF-8に変換してタプルで返す
    """
    try:
        # JISコードをバイト列に変換
        jis_bytes = jis_code.to_bytes(2, byteorder='big')
        jis_bytes = b'\x1b$B' + jis_bytes

        # JISコードをUnicodeにデコード（iso2022_jp）
        unicode_char = codecs.decode(jis_bytes, 'iso2022_jp')
        
        # Unicode文字をShift-JISとUTF-8にエンコード
        shift_jis_bytes = unicode_char.encode('shift_jis')
        sjis_code = int.from_bytes(shift_jis_bytes, byteorder='big')
        utf8_bytes = unicode_char.encode('utf-8')
        utf8_code = int.from_bytes(utf8_bytes, byteorder='big')

        # 文字列形式の返却
        return (jis_code, sjis_code, utf8_code)
    except Exception as e:
        return 0,0,0

# JISコードの範囲を指定して、Shift-JISとUTF-8に変換する関数
# 0x00～0xFFの場合は、JIS、SJIS、UTF-8は同じ値になる
# 戻り値は、utf-8,sjis,jis,文字,ｗ,ｈ、オフセット。 W,H,オフセットは後から決定する
def getCodeTbl(codeRange): 
    if (isVerbose):
        print("\t"+GetMessage(isJapanese,"log_getcodetbl").format(hex(codeRange.start),hex(codeRange.stop)))  
    CodeList = []
    for code in codeRange:
        
        if (code >= 0x00 and  code <= 0xFF):
            if (isVerbose):
                print(f"\t\t" + GetMessage(isJapanese,"log_analyzingcode").format(hex(code)),end="")
            if mapping == "KANA" and code >= 0xA1 and code <= 0xDF :  # カナ文字にマッピングする場合、半角カナ文字は、全角カナ文字にマッピングを変える
                if (isVerbose):
                    print(GetMessage(isJapanese,"log_ishankakukana").format(hex(code)))
                char = chr(code - 0xa1 + 0xFF61)
                codeList.append([code,code,code,char,0,0,0])
            else:                                                   # 半角文字、カナ文字マッピングを行わない場合                                           
                char = chr(code)
                if char.isprintable():                     # 印刷できる文字の場合
                    if (isVerbose):
                        print(GetMessage(isJapanese,"log_isascii").format(hex(code),code))
                else:
                    if (isVerbose):
                        print(GetMessage(isJapanese,"log_isnonprintableascii").format(hex(code)))
                    char = "0x" + hex(code)[2:].zfill(2)            # 印刷できない文字は、コードをそのまま表示する
                codeList.append([code,code,code,char,0,0,0])
            if (isVerbose):
                print("\t\t\t" + GetMessage(isJapanese,"log_codedisp").format(hex(code),hex(code),hex(code)))

        else:
            if (isVerbose):
                print("\t\t" + GetMessage(isJapanese,"log_analyzingmulticode" ).format(hex(code)))
            codeJIS , codeSJIS , codeUTF8 = jis_to_encodings(code)
            if codeJIS == 0 or codeSJIS == 0 or codeUTF8 == 0:
                if (isVerbose):
                    print(f"\t\t\t" + GetMessage(isJapanese,"log_skippingcode").format(hex(code)))
                continue
            unicode_char = decode_utf8(codeUTF8)  # JISコードをUnicode文字に変換
            CodeList.append([codeUTF8,codeSJIS,codeJIS,unicode_char,0,0,0])

            if (isVerbose):
                print("\t\t\t" + GetMessage(isJapanese,"log_codedisp").format(hex(codeJIS),hex(codeSJIS),hex(codeUTF8)))

    return CodeList

# コードの一覧からビットマップ配列を作り、コード一覧にはビットマップのオフセット位置を追加する関数
def convToDataAndBitmap(codeList,fontXSize,fontYSize,xOffset = 0,yOffset=-1): 
    if (isVerbose):
        print(f"\t" + GetMessage(isJapanese,"log_convdatabitmap").format(len(codeList),fontXSize,fontYSize,xOffset,yOffset))

    byteOffset = 0
    for code in codeList:
        code[6] = byteOffset
        if isVerbose:
            print(f"\t\t" + GetMessage(isJapanese,"log_converting").format(hex(code[0]),hex(code[1]),hex(code[2]),code[3],code[6]))
        bitmap_image = render_glyph_to_bitmap(font,code[0], code[3], fontXSize, fontYSize ,xOffset,yOffset)
        code[4] = bitmap_image.size[0]  # 幅を取得
        code[5] = bitmap_image.size[1]  # 高さを取得
        bmpData = display_bitmap_data(bitmap_image)
        bmpList.append(bmpData)
        byteOffset += bmpData.size
    if isVerbose:
        print(f"\t" + GetMessage(isJapanese,"log_doneconvert").format(len(codeList),len(bmpList)))
    return (codeList,bmpList)

def printBitArray(bitArray):
    for row in bitArray:
        for value in row:
            print(bin(value)[2:].zfill(8), end="")
        print() 
    print()




# C言語のヘッダファイルに出力する関数
def Output2CLang(OutFileName, codeList , bitmapList) :

    strOutput = ""
    if isVerbose:
        print(GetMessage(isJapanese,"log_genoutput").format(OutFileName))

    with open(OutFileName, "w", encoding="utf-8") as f:
        cmd_line = " ".join(sys.argv)  # 引数をスペース区切りの文字列として取得
        cmd_line = os.path.basename(cmd_line)
        strOutput = ""
        strOutput +="// This file is auto generated by font.py\n"
        strOutput +="// "+cmd_line+"\n"
        strOutput +="// Do not edit this file directly.\n"
        strOutput +="// Font: " + Path(font_path).name + "\n"
        strOutput +="// Font Size: " + str(font_XSize)+"x"+str(font_YSize)  + "\n"
        strOutput +="// Code Set: " + code_set + "\n"
        strOutput +="// Character count: " + str(len(codeList)) + "\n"
        strOutput +=f"// data size:{total_size(bitmapList):} bytes\n"
        strOutput +=f"// \n"

        f.write(strOutput)
        if isVerbose:
            print(strOutput,end="")
            print()


        #まず、ビットマップ情報の表示
        strOutput = ""
        strOutput += "/*\n"
        strOutput += "struct KanjiData {\n"
        strOutput += "\tuint32_t Unicode;\n"
        strOutput += "\tuint16_t SJIS;\n"
        strOutput += "\tuint16_t JIS;\n"  
        strOutput += "\tuint8_t width;\n"
        strOutput += "\tuint8_t height;\n"
        strOutput += "\tuint32_t offsetBMP;\n"
        strOutput += "};\n"
        strOutput += "*/\n"

        f.write(strOutput)
        if isVerbose:
            print(strOutput,end="")
            print()

        if (isEndMark == "ALLZERO"):
            codeList.append([0,0,0,"",0,0,0])
        elif (isEndMark == "ALLMAX"):
            codeList.append([0xFFFFFFFF,0xFFFF,0xFFFF,"",0,0,0])

        strOutput = ""
        strOutput += f"static const KanjiData {structure_name}[] = {{\n"
        for i, code in enumerate(codeList):
            strWkLine = ""
            strWkLine = "\t{" + f"0x{hex(code[0])[2:].zfill(8)} , 0x{hex(code[1])[2:].zfill(4)} , 0x{hex(code[2])[2:].zfill(4)} , {code[4]:>2} ,{code[5]:>2} , 0x{hex(code[6])[2:].zfill(8)}" + "}"
            if i < len(codeList) - 1:
                strWkLine += ","
            else:
                strWkLine += " "
            # 最後に、どの文字コードなのかを示すため、コメントを付ける。ただ、バックスラッシュ記号が // の中にあると、
            # 継続行として扱われてしまい、次の行がコメントになってしまうので、表示文字はダブルクォートで囲む。
            # この動作って、C++の仕様？と思って調べたら、仕様だった。
            # なので、
            #   char *fn;    //　読み込み元 C:\hoge\
            #   fn = "moge.txt";
            # というプログラムは、誤動作する。
            #   char *fn;    //　読み込み元 "C:\hoge\"
            # だと、行末がバックスラッシュにならないので問題ない。
            # //を継続行にしたい奴っているの？？？もはや仕様のバグ・・・
            strWkLine += f"\t// \"{code[3]}\"\n"
            strOutput += strWkLine
        strOutput += "};\n"

        f.write(strOutput)
        if isVerbose:
            print (strOutput,end="")

        # 次に対応するビットマップデータを表示
        offset = 0
        strOutput = f"static const uint8_t {bitmapdata_name}[] = {{\n"
        f.write(strOutput)
        if isVerbose:
            print (strOutput,end="")


        for charNo , row in enumerate(bitmapList):
            oneBlock = ""
            oneBlock += f"// UNICODE:0x{hex(codeList[charNo][0])[2:].zfill(8)} -  Offset:0x{hex(codeList[charNo][6])[2:].zfill(8)}   -- CHAR:\"{codeList[charNo][3]}\" \n"
            for value in row:
                bitsInfo = ""
                for x , xdata in enumerate(value) :
                    bitsInfo += bin(xdata)[2:].zfill(8)
                    oneBlock += f"\t0x{hex(xdata)[2:].zfill(2)}"

                    #print(f"0x{hex(xdata)[2:].zfill(2)}",end = "")
                    if x < len(value) - 1:
                        oneBlock += ","
                    else:
                        oneBlock += ","
                        oneBlock += f"\t\t// {bitsInfo} \n"
                        #print(f"\t\t// {bitsInfo}")
            oneBlock += "\n"
            f.write(oneBlock)
            if isVerbose:
                print (oneBlock,end="")
        f.write("};\n")
        if isVerbose:
            print ("};")
    if isVerbose:
        print(GetMessage(isJapanese,"log_done"))

#バイナリデータに変換する
#
def Output2Binary(OutFileName, codeList , bitmapList) :
    #　まず、struct KanjiData をそのままバイナリデータにしていく。
    with open(OutFileName+"_code.bin", "wb") as f:
        if isVerbose:
            print(GetMessage(isJapanese,"log_genoutput").format(OutFileName+"_code.bin"))
        for code in codeList:
            # 各データをバイナリ形式に変換して書き込む。IHHBBIとして、32bit/16/16/8/8/32 を指定する。
            binary_data = struct.pack(">IHHBBI", code[0], code[1],code[2], code[4],code[5],code[6])
            f.write(binary_data)
    #　次に、ビットマップデータをバイナリ形式に変換して書き込む。            
    with open(OutFileName+"_bitmap.bin", "wb") as f:
        if isVerbose:
            print(GetMessage(isJapanese,"log_genoutput").format(OutFileName+"_bitmap.bin"))       
        for charNo , row in enumerate(bitmapList):
            oneBlock = ""
            oneBlock += f"// UNICODE:0x{hex(codeList[charNo][0])[2:].zfill(8)} -  Offset:0x{hex(codeList[charNo][6])[2:].zfill(8)}   -- CHAR:\"{codeList[charNo][3]}\" \n"
            for value in row:
                for x , xdata in enumerate(value) :
                    f.write(xdata)
    if isVerbose:
        print(GetMessage(isJapanese,"log_done"))

# Pythonのバイナリデータに変換する
def Output2Python(OutFileName, codeList , bitmapList) :

    strOutput = ""
    if isVerbose:
        print(GetMessage(isJapanese,"log_genoutput").format(OutFileName))
    cmd_line = " ".join(sys.argv)  # 引数をスペース区切りの文字列として取得
    cmd_line = os.path.basename(cmd_line)


    with open(OutFileName, "w", encoding="utf-8") as f:
        strOutput = ""
        strOutput +="# This file is auto generated by font.py\n"
        strOutput +="# "+cmd_line+"\n"
        strOutput +="# Do not edit this file directly.\n"
        strOutput +="# Font: " + Path(font_path).name + "\n"
        strOutput +="# Font Size: " + str(font_XSize)+"x"+str(font_YSize)  + "\n"
        strOutput +="# Code Set: " + code_set + "\n"
        strOutput +="# Character count: " + str(len(codeList)) + "\n"
        strOutput +=f"# data size:{total_size(bitmapList):} bytes\n"
        strOutput +=f"# \n"
        strOutput += "import struct\n"
        strOutput +=f"\n"



        f.write(strOutput)
        if isVerbose:
            print(strOutput,end="")
            print()

        if isVerbose:
            print(strOutput,end="")
            print()
        if (isEndMark == "ALLZERO"):
            codeList.append([0,0,0,"",0,0,0])
        elif (isEndMark == "ALLMAX"):
            codeList.append([0xFFFFFFFF,0xFFFF,0xFFFF,"",0,0,0])
        strOutput = ""
        strOutput += f"code = b\"\".join(struct.pack(\"<IHHBBI\", *data) for data in [\n"
#        strOutput += f"{structure_name} = b\"\".join(struct.pack(\"<IHHBBI\", *data) for data in [\n"
        for i, code in enumerate(codeList):
            strWkLine = "("
            strWkLine += f"0x{hex(code[0])[2:].zfill(8)}" + ", "
            strWkLine += f"0x{hex(code[1])[2:].zfill(4)}" + ", "
            strWkLine += f"0x{hex(code[2])[2:].zfill(4)}" + ", "
            strWkLine += f"{code[4]:>2}" + ", "
            strWkLine += f"{code[5]:>2}" + ", "
            strWkLine += f"0x{hex(code[6])[2:].zfill(8)}" 
            strWkLine += "),"
            strWkLine += f"\t# \"{code[3]}\"\n"
            strOutput += strWkLine
        strOutput += "])\n"
        f.write(strOutput)
        if isVerbose:
            print(strOutput,end="")
            print()

        strOutput = ""
        #strOutput += f"{structure_name}_BMP = bytes(["
        strOutput += f"bitmap = bytes(["
        f.write(strOutput+"\n")
        if isVerbose:
            print(strOutput)

        # 次に対応するビットマップデータを表示
        # 各サブリストを処理
        for sublist in bitmapList:
            strOutput = ""
            for subsublist in sublist:
                for byte in subsublist:
                    strOutput += f"0x{byte:02X},"
            f.write(strOutput+"\n")  # 変数を出力
            if isVerbose:
                print(strOutput)
        strOutput = "])\n"
        f.write(strOutput)
        if isVerbose:
            print(strOutput)
    if isVerbose:
        print(GetMessage(isJapanese,"log_done"))



#bdfファイルに出力する

 

def Output2FONTX2(OutFileName, codeList, bitmapList,out_encoding):
    """
    FONTX2形式で全角用・半角用を別々のファイルに出力する（文字コードはShiftJIS、エンディアン逆）
    ヘッダは全角で17バイト（+コードブロック数+テーブル）、半角で16バイト
    コードリスト・ビットマップリストはSJIS順に並び替えて出力
    """

    zen_file = OutFileName + "_zen.fnt"
    han_file = OutFileName + "_han.fnt"

    # コードブロックテーブルを作成（全角用のみ）
    def make_code_blocks(codeList,out_encoding):
        blocks = []
        prev = None
        start = None
        if (out_encoding == "UTF8"):
            raise SystemExit(GetMessage(isJapanese,"err_cannotuseenc").format(out_encoding,"FONTX2"))
        elif (out_encoding == "SJIS"):
            cidx = 1   
        elif (out_encoding == "JIS"):
            cidx = 2
        else:
            raise SystemExit(GetMessage(isJapanese,"err_notsupportedencoding").format(out_encoding))

        for code in sorted([c[cidx] for c in codeList if c[cidx] > 0xFF]):
            if start is None:
                start = code
                prev = code
            elif prev != None and code == prev + 1:
                prev = code
            elif prev == None :
                SystemError(GetMessage(isJapanese,"err_logicerror").format(sys._getframe().f_lineno, "make_code_blocks: prev is None but start is not None"))
            else:
                blocks.append((start, prev))
                start = code
                prev = code
        if start is not None:
            blocks.append((start, prev))
        return blocks

    def make_header_zen(font_name, width, height, nb):
        header = bytearray(18 + nb * 4)
        header[0:6] = b'FONTX2'
        name_bytes = Path(font_name).stem.encode('ascii', errors='replace')[:8]
        header[6:6+len(name_bytes)] = name_bytes
        header[14] = width
        header[15] = height
        header[16] = 1  # 1:シフトJIS
        header[17] = nb  # コードブロック数
        # コードブロックテーブルは18バイト目以降
        return header

    def make_header_han(font_name, width, height):
        header = bytearray(17)
        header[0:6] = b'FONTX2'
        name_bytes = Path(font_name).stem.encode('ascii', errors='replace')[:8]
        header[6:6+len(name_bytes)] = name_bytes
        header[14] = width
        header[15] = height
        # 16バイト目: 0=ANK(半角), 1=全角
        header[16] = 0
        return header

    # SJIS順に並び替え
    sjis_sorted = sorted(enumerate(codeList), key=lambda x: x[1][1])
    sorted_codeList = [x[1] for x in sjis_sorted]
    sorted_bitmapList = [bitmapList[x[0]] for x in sjis_sorted]

    # 半角用ファイル出力（ShiftJISコードを使う、エンディアン逆、ヘッダ17バイト）
    if isVerbose:
        print(GetMessage(isJapanese,"log_genoutput").format(han_file))
    with open(han_file, "wb") as f_han:
        f_han.write(make_header_han(font_path, font_XSize // 2, font_YSize))
        for idx, code in enumerate(sorted_codeList):
            sjis_val = code[1]
            width = code[4]
            bmp = sorted_bitmapList[idx]
            if sjis_val <= 0xFF:
                # f_han.write(bytes([0x00, sjis_val & 0xFF]))  # FONTX2仕様では不要なので削除
                bytes_per_row = max(1, (width + 7) // 8)
                for row in bmp:
                    f_han.write(bytes(row[:bytes_per_row]))
    if isVerbose:
        print(GetMessage(isJapanese,"log_done"))

    # 全角用ファイル出力（ShiftJISコードを使う、エンディアン逆、ヘッダ18+4*NBバイト）
    code_blocks = make_code_blocks(sorted_codeList,out_encoding)
    nb = len(code_blocks)
    if (nb >=256) : 
        raise SystemExit(GetMessage(isJapanese,"err_codeblock").format(nb))

    header = make_header_zen(font_path, font_XSize, font_YSize, nb)
    # コードブロックテーブルを格納
    for i, (start, end) in enumerate(code_blocks):
        base = 18 + i*4
        header[base + 0] = start & 0xFF
        header[base + 1] = (start >> 8) & 0xFF
        header[base + 2] = end & 0xFF
        header[base + 3] = (end >> 8) & 0xFF

    if isVerbose:
       print(GetMessage(isJapanese,"log_genoutput").format(han_file))

    with open(zen_file, "wb") as f_zen:
        f_zen.write(header)
        for idx, code in enumerate(sorted_codeList):
            sjis_val = code[1]
            width = code[4]
            if sjis_val > 0xFF:
                bmp = sorted_bitmapList[idx]
                # f_zen.write(bytes([0x01, sjis_val & 0xFF, (sjis_val >> 8) & 0xFF]))  # FONTX2仕様上不要なので削除
                bytes_per_row = max(1, (width + 7) // 8)
                for row in bmp:
                    f_zen.write(bytes(row[:bytes_per_row]))
    if isVerbose:
        print(GetMessage(isJapanese,"log_done"))



"""
    BDF形式でビットマップフォントを出力する関数。
    OutFileName: 出力ファイル名（.bdf推奨）
    codeList: [[utf8, sjis, jis, char, width, height, offset], ...]
    bitmapList: 各文字のビットマップデータ
    font_name: フォント名
    font_XSize, font_YSize: フォントサイズ

    """
def Output2BDF(OutFileName, codeList, bitmapList, font_name, font_XSize, font_YSize, bdf_split,out_encoding):
    import datetime
    from pathlib import Path
    def bdf_header(font_name, font_XSize, font_YSize, count):
        now = datetime.datetime.now()
        header = f"""STARTFONT 2.1
FONT {font_name}
SIZE {font_YSize} 75 75
FONTBOUNDINGBOX {font_XSize} {font_YSize} 0 0
STARTPROPERTIES 2
FONT_ASCENT {font_YSize}
FONT_DESCENT 0
ENDPROPERTIES
CHARS {count}
"""
        return header
    def bdf_char_entry(code, bitmap, font_XSize, font_YSize,out_encoding):
        width = code[4]
        height = code[5]
        bbx = f"BBX {width} {height} 0 0"
        swidth = f"SWIDTH {int((960 * 16)/width)} 0"
        dwidth = f"DWIDTH {width} 0"

        if out_encoding == "UTF8":
            encoding = code[0] 
            lines = [f"STARTCHAR UTF8:{encoding:04X}", f"ENCODING {encoding}",swidth , dwidth, bbx, f"BITMAP"]
        elif out_encoding == "SJIS":
            encoding = code[1] 
            lines = [f"STARTCHAR SJIS:{encoding:04X}", f"ENCODING {encoding}",swidth , dwidth, bbx, f"BITMAP"]
        elif out_encoding == "JIS":
            encoding = code[2] 
            lines = [f"STARTCHAR JIS:{encoding:04X}", f"ENCODING {encoding}",swidth , dwidth, bbx, f"BITMAP"]
        else:
            raise ValueError(GetMessage(isJapanese,"err_notsupportedencoding").format(out_encoding))
        

        for row in bitmap:
            hexstr = ''.join(f"{b:02X}" for b in row[:(width+7)//8])
            lines.append(hexstr)
        lines.append("ENDCHAR")
        return '\n'.join(lines)
    

    if not bdf_split:
        with open(OutFileName, "w", encoding="utf-8") as f:
            f.write(bdf_header(font_name, font_XSize, font_YSize, len(codeList)))
            for code, bitmap in zip(codeList, bitmapList):
                f.write(bdf_char_entry(code, bitmap, font_XSize, font_YSize,out_encoding))
                f.write("\n")
            f.write("ENDFONT\n")
    else:
        # 半角
        han_codes = [(c, b) for c, b in zip(codeList, bitmapList) if c[1] <= 0xFF]
        zen_codes = [(c, b) for c, b in zip(codeList, bitmapList) if c[1] > 0xFF]
        han_file = OutFileName.replace('.bdf', '_han.bdf')
        zen_file = OutFileName.replace('.bdf', '_zen.bdf')
        # 半角
        with open(han_file, "w", encoding="utf-8") as f:
            f.write(bdf_header(font_name+"_HAN", font_XSize//2, font_YSize, len(han_codes)))
            for code, bitmap in han_codes:
                f.write(bdf_char_entry(code, bitmap, font_XSize//2, font_YSize,out_encoding))
                f.write("\n")
            f.write("ENDFONT\n")
        # 全角
        with open(zen_file, "w", encoding="utf-8") as f:
            f.write(bdf_header(font_name+"_ZEN", font_XSize, font_YSize, len(zen_codes)))
            for code, bitmap in zen_codes:
                f.write(bdf_char_entry(code, bitmap, font_XSize, font_YSize,out_encoding))
                f.write("\n")
            f.write("ENDFONT\n")
        if isVerbose:
            print(GetMessage(isJapanese,"log_done"))


if __name__ == "__main__":

    # locale.getlocale()[0] が None の場合を考慮して安全に判定
    loc = locale.getlocale()[0]
    if loc is not None and (('JP' in loc) or ('Japanese' in loc)):
        isJapanese = True
    else:
        isJapanese = False

    # 環境変数LANGが存在していたらisJapaneseを上書き
    lang_env = os.environ.get('LANG')
    if lang_env:
        if 'ja' in lang_env.lower() or 'jp' in lang_env.lower():
            isJapanese = True
        else:
            isJapanese = False

    #教育漢字の一覧
    KyouikuKanji = "一右雨円王音下火花貝学気九休玉金空月犬見五口校左三山子四糸字耳七車手十出女小上森人水正生青夕石赤千川先早草足村大男竹中虫町天田土二日入年白八百文木本名目立力林六\
引羽雲園遠何科夏家歌画回会海絵外角楽活間丸岩顔汽記帰弓牛魚京強教近兄形計元言原戸古午後語工公広交光考行高黄合谷国黒今才細作算止市矢姉思紙寺自時室社弱首秋週春書少場色食心新親図数西声星晴切雪船線前組走多太体台地池知茶昼長鳥朝直通弟店点電刀冬当東答頭同道読内南肉馬売買麦半番父風分聞米歩母方北毎妹万明鳴毛門夜野友用曜来里理話\
悪安暗医委意育員院飲運泳駅央横屋温化荷界開階寒感漢館岸起期客究急級宮球去橋業曲局銀区苦具君係軽血決研県庫湖向幸港号根祭皿仕死使始指歯詩次事持式実写者主守取酒受州拾終習集住重宿所暑助昭消商章勝乗植申身神真深進世整昔全相送想息速族他打対待代第題炭短談着注柱丁帳調追定庭笛鉄転都度投豆島湯登等動童農波配倍箱畑発反坂板皮悲美鼻筆氷表秒病品負部服福物平返勉放味命面問役薬由油有遊予羊洋葉陽様落流旅両緑礼列練路和\
愛案以衣位囲胃印英栄塩億加果貨課芽改械害街各覚完官管関観願希季紀喜旗器機議求泣救給挙漁共協鏡競極訓軍郡径型景芸欠結建健験固功好候航康告差菜最材昨札刷殺察参産散残士氏史司試児治辞失借種周祝順初松笑唱焼象照賞臣信成省清静席積折節説浅戦選然争倉巣束側続卒孫帯隊達単置仲貯兆腸低底停的典伝徒努灯堂働特得毒熱念敗梅博飯飛費必票標不夫付府副粉兵別辺変便包法望牧末満未脈民無約勇要養浴利陸良料量輪類令冷例歴連老労録\
圧移因永営衛易益液演応往桜恩可仮価河過賀快解格確額刊幹慣眼基寄規技義逆久旧居許境均禁句群経潔件券険検限現減故個護効厚耕鉱構興講混査再災妻採際在財罪雑酸賛支志枝師資飼示似識質舎謝授修述術準序招承証条状常情織職制性政勢精製税責績接設舌絶銭祖素総造像増則測属率損退貸態団断築張提程適敵統銅導徳独任燃能破犯判版比肥非備俵評貧布婦富武復複仏編弁保墓報豊防貿暴務夢迷綿輸余預容略留領\
異遺域宇映延沿我灰拡革閣割株干巻看簡危机揮貴疑吸供胸郷勤筋系敬警劇激穴絹権憲源厳己呼誤后孝皇紅降鋼刻穀骨困砂座済裁策冊蚕至私姿視詞誌磁射捨尺若樹収宗就衆従縦縮熟純処署諸除将傷障城蒸針仁垂推寸盛聖誠宣専泉洗染善奏窓創装層操蔵臓存尊宅担探誕段暖値宙忠著庁頂潮賃痛展討党糖届難乳認納脳派拝背肺俳班晩否批秘腹奮並陛閉片補暮宝訪亡忘棒枚幕密盟模訳郵優幼欲翌乱卵覧裏律臨朗論\
、。，．・：；？！゛゜´｀¨＾￣＿ヽヾゝゞ〃仝々〆〇ー―‐／＼～∥｜…‥‘’“”（）〔〕［］｛｝〈〉《》「」『』【】＋－±×÷＝≠＜＞≦≧∞∴♂♀°′″℃￥＄￠￡％＃＆＊＠§☆★○●◎◇\
◆□■△▲▽▼※〒→←↑↓〓∈∋⊆⊇⊂⊃∪∩∧∨￢⇒⇔∀∃∠⊥⌒∂∇≡≒≪≫√∽∝∵∫∬Å‰♯♭♪†‡¶◯\
０１２３４５６７８９ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ\
ぁあぃいぅうぇえぉおかがきぎくぐけげこごさざしじすずせぜそぞただちぢっつづてでとどなにぬねのはばぱひびぴふぶぷへべぺほぼぽまみむめもゃやゅゆょよらりるれろゎわゐゑをん\
ァアィイゥウェエォオカガキギクグケゲコゴサザシジスズセゼソゾタダチヂッツヅテデトドナニヌネノハバパヒビピフブプヘベペホボポマミムメモャヤュユョヨラリルレロヮワヰヱヲンヴヵヶ"







    parser = argparse.ArgumentParser(description=GetMessage(isJapanese,"general"),formatter_class=argparse.RawTextHelpFormatter,epilog=GetMessage(isJapanese,"epilog"))
    # コマンドライン引数の解析
    parser.add_argument("font_path", type=str,help=GetMessage(isJapanese,"font_path"))
    parser.add_argument("-n", "--name", type=str, default="", help=GetMessage(isJapanese,"--name"))
    parser.add_argument("-s", "--size", type=int, default=12, help=GetMessage(isJapanese,"--siuze"))
    parser.add_argument("-xo", "--xoffset", type=int, default=0, help=GetMessage(isJapanese,"--xoffset"))
    parser.add_argument("-yo", "--yoffset", type=int, default=-1, help=GetMessage(isJapanese,"--yoffset"))
    parser.add_argument("-cs", "--codeset", choices=["ALL","LEVEL1","SCHOOL","CUSTOM","TEST"], default="ALL", help=GetMessage(isJapanese,"--codeset"))
    parser.add_argument("-cf", "--charfile", type=str, default="",help=GetMessage(isJapanese,"--charfile"))
    parser.add_argument("-o", "--output", type=str, default="XXX.XXX", help=GetMessage(isJapanese,"--output"))
    parser.add_argument("-m", "--mapping", choices=["KANA","NONE"], default="KANA", help=GetMessage(isJapanese,"--mapping"))
    parser.add_argument("-em","--endmark" , choices=["ALLZERO","ALLMAX","NONE"], default="ALLZERO", help=GetMessage(isJapanese,"--endmark"))

    parser.add_argument("-t","--outtype" , choices=["CData","PBinary","Python", "FONTX2","BDF"], default="CData", help=GetMessage(isJapanese,"--outtype"))
    parser.add_argument("-bs", "--bdf-split", choices=["Default" , "True","False"], default="Default" , help=GetMessage(isJapanese,"--bdf-split"))
    parser.add_argument("-en" , "--encoding", choices=["DEFAULT" , "UTF8","SJIS","JIS"], default="DEFAULT", help=GetMessage(isJapanese,"--encoding"))
    parser.add_argument("-fr", "--filereplace", action="store_true", help=GetMessage(isJapanese,"--oufilereplacettype"))
    parser.add_argument("-v", "--verbose", action="store_true", help=GetMessage(isJapanese,"--verbose"))
    parser.add_argument("-i", "--image", action="store_true", help=GetMessage(isJapanese,"--image"))
    args = parser.parse_args()
    font_path = args.font_path
    font_XSize = args.size
    font_YSize = args.size
    x_offset = args.xoffset
    y_offset = args.yoffset
    code_set = args.codeset
    mapping = args.mapping
    output_file = args.output
    isVerbose = args.verbose
    isImage = args.image
    isEndMark = args.endmark
    outFormat = args.outtype
    isReplace = args.filereplace
    charfile = args.charfile
    bdf_split = args.bdf_split
    out_encoding = args.encoding

    #bdf_splitがデフォルトの場合は、BDF形式のときだけTrueにする
    if (bdf_split.lower() == "default"):
        if (outFormat == "BDF"):
            bdf_split = True
        else:
            bdf_split = False
    else:
        bdf_split = (bdf_split.lower() == "true")

    #エンコーディングのデフォルト値を、出力タイプにより決定する
    if (out_encoding == "DEFAULT"):
        if (outFormat == "CData") or (outFormat == "PBinary") or (outFormat == "Python"):
            out_encoding = "UTF8"
        elif (outFormat == "FONTX2"):
            out_encoding = "SJIS"
        elif (outFormat == "BDF"):
            out_encoding = "JIS"
    

    #入力ファイルが　”test" なら、テスト用のデータを読み込む
    if (font_path == "test"):
        font_path = "E:\\Programing\\VSCode\\Font\\JF-Dot-Shinonome12.ttf"
    
    if (code_set == "CUSTOM"):
        if charfile == "":
            raise SystemExit(GetMessage(isJapanese,"err_codefileReqired"))
        if os.path.exists(charfile) == False:
            raise SystemExit(GetMessage(isJapanese,"err_codefilenotexist").format(charfile))

    #出力ファイルが指定されなかったら、フォントファイル名に基づいて、.hファイルを作成する
    if (output_file == "XXX.XXX"):
        if (outFormat == "CData"):
            output_file = Path(font_path).name.split(".")[0] + "_" + str(font_XSize).zfill(2) + "x"+str(font_YSize).zfill(2)  + "_" + code_set +".h"
        elif (outFormat == "PBinary"):
            output_file = Path(font_path).name.split(".")[0] + "_" + str(font_XSize).zfill(2) + "x"+str(font_YSize).zfill(2)  + "_" + code_set
        elif (outFormat == "Python"):
            output_file = Path(font_path).name.split(".")[0] + "_" + str(font_XSize).zfill(2) + "x"+str(font_YSize).zfill(2)  + "_" + code_set +".py"
        elif (outFormat == "FONTX2"):
            output_file = Path(font_path).name.split(".")[0] + "_" + str(font_XSize).zfill(2) + "x"+str(font_YSize).zfill(2)  + "_" + code_set +".fnt"
        elif (outFormat == "BDF"):
            output_file = Path(font_path).name.split(".")[0] + "_" + str(font_XSize).zfill(2) + "x"+str(font_YSize).zfill(2)  + "_" + code_set +".bdf"

    #全角半角分離(-bsオプション）は、BDF形式のときしか指定できない
    if (bdf_split and outFormat != "BDF"):
        raise SystemExit(GetMessage(isJapanese,"err_bdfsplitonlybdf"))

    #出力ファイル名に不適切な文字が含まれている場合、アンダースコアに置換する
    if (isReplace):
        # 置換対象の文字リスト
        invalid_chars = {"-"," ","+", "-", "*" ,"/", " ", " ", "(", ")", "[", "]", "{", "}", ":", ";", ",",  "<", ">", "?", "!", "@", "#", "$", "%", "^", "&", "~", "`"}
        # 置換後の文字列を作成
        cleaned_name = "".join("_" if char in invalid_chars else char for char in output_file)
        output_file = cleaned_name


    if (args.name == ""):
        namebase = Path(font_path).name.split(".")[0]
        # 置換対象の文字リスト
        invalid_chars = {"+", "-", "*" ,"/", " ", " ", "(", ")", "[", "]", "{", "}", ":", ";", ",", ".", "<", ">", "?", "!", "@", "#", "$", "%", "^", "&", "~", "`"}
        # 置換後の文字列を作成
        cleaned_name = "".join(char for char in namebase if char not in invalid_chars)



        structure_name =  cleaned_name+ "_" + str(font_XSize).zfill(2) + "x"+str(font_YSize).zfill(2)  + "_" + code_set
        bitmapdata_name = cleaned_name+ "_" + str(font_XSize).zfill(2) + "x"+str(font_YSize).zfill(2)  + "_" + code_set + "_bitmap"
    else:
        structure_name = args.name
        bitmapdata_name =  args.name+"_bitmap"

   
    # Pillowでフォントデータを読み込み。
    if not os.path.exists(font_path) :
        raise SystemExit(GetMessage(isJapanese,"err_fontfilenotexist").format(font_path))
    try:
        font =  ImageFont.truetype(font_path, font_XSize)
    except Exception as e:
        raise SystemExit(GetMessage(isJapanese,"err_fontfileinvalid").format(font_path, e))
    

    #フォントの範囲を定義しておく

    ASCII = range(0x0000,0x0100)
    JISL1 = range(0x3021,0x4f54)
    JISL2 = range(0x5021,0x7427)
    JISKIGOU = range(0x2121,0x2F7E)
    
    # デバッグ用の特別なフォント範囲
    test1 = range(0x00A1,0xAF) 
    test2 = range(0x443E,0x4450)

    #指定されたフォントセットに基づいて、文字コードを変換してUTF-8/SJIS/JISコードのリスト配列にしておく
    codeList = []                           # コードのリスト。
    if (code_set == "ALL"):
        if isVerbose :
            print(GetMessage(isJapanese,"log_gencodetbl").format("ASCII/JISL1/JISL2/JISKIGOU"))
        codeList += getCodeTbl(ASCII)
        codeList += getCodeTbl(JISL1)
        codeList += getCodeTbl(JISL2)
        codeList += getCodeTbl(JISKIGOU)   
   
    elif (code_set == "LEVEL1"):
        if isVerbose :
            print(GetMessage(isJapanese,"log_gencodetbl").format("ASCII/JISL1/JISKIGOU"))
        codeList += getCodeTbl(ASCII)
        codeList += getCodeTbl(JISL1)
        codeList += getCodeTbl(JISKIGOU)
    elif (code_set == "SCHOOL"):
        #教育漢字の場合、少し複雑。とりあえずJISL1のテーブルを作って、そこから該当しないものを削除していくことにする。
        if isVerbose :
            print(GetMessage(isJapanese,"log_gencodetbl").format("ASCII/教育漢字/JISKIGOU"))
        codeList += getCodeTbl(ASCII)
        codeList += getCodeTbl(JISL1)
        codeList += getCodeTbl(JISKIGOU)
        if isVerbose :
            print(GetMessage(isJapanese,"log_removingcodetbl"))

        for d in codeList :
            if d[0] <= 0xFF:            #１バイト文字は含める
                continue
            if d[3] not in KyouikuKanji:    #教育漢字に含まれないものは削除する
                codeList.remove(d)
    elif (code_set == "CUSTOM"):
        # 教育漢字と同じ方法で、ALLのセットから使用しないものを削除していく。効率は大変悪くなるが仕方ない。
        if isVerbose :
            print(GetMessage(isJapanese,"log_readingcodefile").format(charfile))
        with open(charfile, "r", encoding="utf-8") as file:
            content = file.read().replace("\n", "")  # 改行を削除
        if isVerbose :
            print(GetMessage(isJapanese,"log_outputcontains").format(content))
        if isVerbose :
            print(GetMessage(isJapanese,"log_gencodetbl").format("ASCII/JISL1/JISL2/JISKIGOU"))
        codeList += getCodeTbl(ASCII)
        codeList += getCodeTbl(JISL1)
        codeList += getCodeTbl(JISKIGOU)

        if isVerbose :
            print(GetMessage(isJapanese,"log_removeunused"))
        for d in codeList :
            if d[0] <= 0xFF:            #１バイト文字は含める
                continue
            if d[3] not in content:    #教育漢字に含まれないものは削除する
                codeList.remove(d)
    elif (code_set == "CUSTOM2"):
        # 教育漢字と同じ方法で、ALLのセットから使用しないものを削除していく。CUSTOMと違い、１バイト文字も削除対象にする。
        # 本来の利用目的は１バイト文字は２５６個あるという前提で作られている（キーでの検索ではなく直接計算でビットマップ画像を求めるため）ので、これは主にデバッグ用になる
        if isVerbose :
            print(GetMessage(isJapanese,"log_readingcodefile").format(charfile))
        with open(charfile, "r", encoding="utf-8") as file:
            content = file.read().replace("\n", "")  # 改行を削除
        if isVerbose :
            print(GetMessage(isJapanese,"log_outputcontains").format(content))
            print(f"{content}")
        if isVerbose :
            print(GetMessage(isJapanese,"log_gencodetbl").format("ASCII/JISL1/JISL2/JISKIGOU"))
        codeList += getCodeTbl(ASCII)
        codeList += getCodeTbl(JISL1)
        codeList += getCodeTbl(JISKIGOU)

        if isVerbose :
            print(GetMessage(isJapanese,"log_removeunused"))
        for d in codeList :
            if d[3] not in content:    #教育漢字に含まれないものは削除する
                codeList.remove(d)

    elif (code_set == "TEST"):
        if isVerbose :
            print(GetMessage(isJapanese,"log_gencodetbl").format("TEST"))
        codeList += getCodeTbl(test1)
        codeList += getCodeTbl(test2)
    if isVerbose:
        print(GetMessage(isJapanese,"log_done"))


    # コードセットを、指定されたエンコーディングでソートする。こうしないと、後から検索するときにバイナリサーチで検索ができないため

    if isVerbose:
        print(GetMessage(isJapanese,"log_sorting").format(out_encoding))
    if (out_encoding == "UTF8") :
        codeList.sort(key=lambda x: x[0])
    elif (out_encoding == "SJIS") :
        codeList.sort(key=lambda x: x[1])
    elif (out_encoding == "JIS") :
        codeList.sort(key=lambda x: x[2])
    else:
        raise SystemExit(GetMessage(isJapanese,"err_notsupportedencoding").format(out_encoding))
    
    if isVerbose:
        print(GetMessage(isJapanese,"log_done"))

    #　コードセットテーブルを、ビットマップデータに変換する。同時に、コードセットテーブル内のXサイズ、Yサイズ、ビットマップデータを更新する
    if isVerbose:
        print(GetMessage(isJapanese,"log_genbitmap"))
    bmpList = []
    codeList , bmpList = convToDataAndBitmap(codeList,  font_XSize,font_YSize,x_offset,y_offset)
    if isVerbose:
        print(GetMessage(isJapanese,"log_done"))

    if outFormat == "CData" :
        Output2CLang(output_file,codeList,bmpList)
    elif outFormat == "PBinary" :
        Output2Binary(output_file,codeList,bmpList)
    elif outFormat == "Python" :
        Output2Python(output_file,codeList,bmpList)
    elif outFormat == "FONTX2":
        Output2FONTX2(output_file, codeList, bmpList,out_encoding)
    elif outFormat == "BDF":
        Output2BDF(output_file, codeList, bmpList, Path(font_path).name, font_XSize, font_YSize, bdf_split , out_encoding)

    print(GetMessage(isJapanese,"log_success").format(output_file))

