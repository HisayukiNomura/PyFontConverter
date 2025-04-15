
from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import codecs
import argparse
from pathlib import Path
import sys


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
        raise ValueError(f"Invalid Unicode code point: {hex(codeUTF8)}")

    # バイト列を生成
    utf8_bytes = codeUTF8.to_bytes(byte_length, byteorder='big')

    # UTF-8としてデコード
    try:
        unicode_char = utf8_bytes.decode('utf-8')
    except UnicodeDecodeError as e:
        raise ValueError(f"Decoding error for {hex(codeUTF8)}: {e}")

    return unicode_char

## フォントをビットマップにレンダリングする関数
def render_glyph_to_bitmap(font, char_unicode , char, font_XSize=64,font_YSize=64,X_offset = 0,Y_offset=-1):
    if isVerbose:
        print(f"\t\trender_glyph_to_bitmap:Rendering glyph: {char} (Unicode: {hex(char_unicode)})")
    global isImage

    # ビットマップ画像を作成
    if isVerbose:
        print(f"\t\t\tCreating {font_XSize},{font_YSize} image and drawing object.")

    image_size = (font_XSize , font_YSize )  # 画像サイズを指定
    image = Image.new("L", image_size, color=255)  # グレースケール画像（白背景）
    draw = ImageDraw.Draw(image)
    
    #半角文字の場合には、半分のサイズにする
    if isVerbose:
        print(f"\t\t\tdrawing character to offscreen image.")
    if (len(char) == 4) :           # 印刷不能の１バイト文字。何もせず、イメージのサイズを半分にする。（半角なので）
        if isVerbose:
            print(f"\t\t\t\tUnprintable half-size character.")
        image = image.crop((0,0,font_XSize/2,font_YSize))
    elif char_unicode <= 0xFF :        # 半角文字の場合
        if isVerbose:
            print(f"\t\t\t\tHalf size character...",end="")
        if mapping == "KANA" and char_unicode >= 0xA1 and char_unicode <= 0xDF : # カナ文字にマッピングする場合、半角文字のカナ文字は、半角カナ文字にマッピングを変える
            charwk = chr(char_unicode - 0xa1 + 0xFF61)  # 半角カナに変換
            if isVerbose:
                print(f"re-mapping for Hankaku-Kana character {chr(char_unicode)}({hex(char_unicode)}) -> {charwk}({hex(ord(charwk))}) , draw and  crop to half-size")
            draw.text((X_offset, Y_offset), charwk, font=font, fill=1)  # 文字を黒で描画
            image = image.crop((0,0,font_XSize/2,font_YSize))
        else:           # 半角文字の場合                                            # 何もしない場合、ASCIIの拡張コードのママとする
            if isVerbose:
                print(f"draw and crop to half-size")
            draw.text((X_offset, Y_offset), char, font=font, fill=1)  # 文字を黒で描画
            image = image.crop((0,0,font_XSize/2,font_YSize))
    else:                           # 全角文字の場合
        if isVerbose:
            print(f"\t\t\t\tFull size character.")
        draw.text((X_offset, Y_offset), char, font=font, fill=1)  # 文字を黒で描画
    
    if isImage:
        image.show()
        print("Displaying the image. Please close the window before pressing [ENTER]...")
        input()  
    if isVerbose:
        print(f"\t\tdone. Image size: {image.size}")
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
        print(f"\tGet Code table for {hex(codeRange.start)}-{hex(codeRange.stop)}")  

    CodeList = []
    for code in codeRange:
        if (code >= 0x00 and  code <= 0xFF):
            if (isVerbose):
                print(f"\t\tAnalyzing Code: {hex(code)} as single-byte code....",end="")
            if mapping == "KANA" and code >= 0xA1 and code <= 0xDF :  # カナ文字にマッピングする場合、半角カナ文字は、全角カナ文字にマッピングを変える
                if (isVerbose):
                    print(f"{hex(code)} is Hankaku-Kana charactor")
                char = chr(code - 0xa1 + 0xFF61)
                codeList.append([code,code,code,char,0,0,0])
            else:                                                   # 半角文字、カナ文字マッピングを行わない場合                                           
                char = chr(code)
                if char.isprintable():                     # 印刷できる文字の場合
                    if (isVerbose):
                        print(f"{hex(code)} \"{code}\" is ASCII charactor" )
                else:
                    if (isVerbose):
                        print(f"{hex(code)} is non-printable ASCII charactor" )
                    char = "0x" + hex(code)[2:].zfill(2)            # 印刷できない文字は、コードをそのまま表示する
                codeList.append([code,code,code,char,0,0,0])
            if (isVerbose):
                print(f"\t\t\tJIS-Code: {hex(code)}, Shift-JIS: {hex(code)}, UTF-8: {hex(code)} ")

        else:
            if (isVerbose):
                print(f"\t\tAnalyzing Code: {hex(code)} as multi-byte code")
            codeJIS , codeSJIS , codeUTF8 = jis_to_encodings(code)
            if codeJIS == 0 or codeSJIS == 0 or codeUTF8 == 0:
                if (isVerbose):
                    print(f"\t\t\tSkipping Code: {hex(code)} because no UTF-8 charctor assigned for this code")
                continue
            unicode_char = decode_utf8(codeUTF8)  # JISコードをUnicode文字に変換
            CodeList.append([codeUTF8,codeSJIS,codeJIS,unicode_char,0,0,0])

            if (isVerbose):
                print(f"\t\t\tJIS-Code: {hex(codeJIS)}, Shift-JIS: {hex(codeSJIS)}, UTF-8: {hex(codeUTF8)} ")

    return CodeList

# コードの一覧からビットマップ配列を作り、コード一覧にはビットマップのオフセット位置を追加する関数
def convToDataAndBitmap(codeList,fontXSize,fontYSize,xOffset = 0,yOffset=-1): 
    if (isVerbose):
        print(f"\tconvToDataAndBitmap:: count:{len(codeList)} , Size=({fontXSize},{fontYSize}), Offset=({xOffset},{yOffset})")

    byteOffset = 0
    for code in codeList:
        code[6] = byteOffset
        if isVerbose:
            print(f"\t\tConverting UTF-8:{hex(code[0])}, SJIS:{hex(code[1])}, JIS:{hex(code[2])}, Character:\"{code[3]}\",Offset:{code[6]})")
        bitmap_image = render_glyph_to_bitmap(font,code[0], code[3], fontXSize, fontYSize ,xOffset,yOffset)
        code[4] = bitmap_image.size[0]  # 幅を取得
        code[5] = bitmap_image.size[1]  # 高さを取得
        bmpData = display_bitmap_data(bitmap_image)
        bmpList.append(bmpData)
        byteOffset += bmpData.size
    if isVerbose:
        print(f"\tdone. code list count = {len(codeList)} , bitmap list count = {len(bmpList)}")
    return (codeList,bmpList)

def printBitArray(bitArray):
    for row in bitArray:
        for value in row:
            print(bin(value)[2:].zfill(8), end="")
        print() 
    print()




if __name__ == "__main__":
    
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

    parser = argparse.ArgumentParser(description="""
Convert Bitmap data file from TrueType(.TTF) file.

This program was originally developed to create font data for displaying Japanese characters on small LCDs commonly used in hobby-electronics projects.
As a result, the output file is currently a C++ header file intended for use with a specific program. Direct usage of this header file might be challenging; however, by extracting binary data using an editor or modifying the program, it might be possible to retrieve the data in your desired format.
                                     """,
#                                        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                        formatter_class=argparse.RawTextHelpFormatter,
    epilog='''
note:
When converting to small-sized images, carefully choose the font file. 
Fonts commonly used in GUI-based operating systems (such as MS-Mincho) may not convert well into clean small images.If you need to convert to a small size, it is recommended to use fonts specifically designed for small sizes, such as those with embedded bitmaps, for better results.Specify a source font file with the extension .ttf for conversion.

Here is the information about free fonts suitable for small sizes, including those available for commercial use:
- Information on Free Fonts: [http://jikasei.me/font/jf-dotfont/]
- Direct Download Link: [https://ftp.iij.ad.jp/pub/osdn.jp/users/8/8541/jfdotfont-20150527.7z]
    '''
    )


    # コマンドライン引数の解析
    parser.add_argument("font_path", type=str,help="Specify a source font file with the extension .ttf for conversion.")
    parser.add_argument("-n", "--name", type=str, default="", help="""The name of the data or structure contained in the output file.
If not specified, it will be automatically generated based on the file name or other arguments.
                        """)
    parser.add_argument("-s", "--size", type=int, default=12, help="""The size of the output bitmap. 
Multibyte characters (aka. 全角) are converted into squares with equal width and height. 
Single-byte characters (aka. 半角) are drawn with a width that is half of the size specified here.
If not specified, the default size is 12.
                        """)
    parser.add_argument("-xo", "--xoffset", type=int, default=0, help="""Specifies the number of pixels to shift characters horizontally or vertically.
When TrueType fonts are drawn, adjacent characters can appear too close, making them harder to read.
To avoid this, characters are typically drawn with extra padding on all sides (top, bottom, left, and right).
During data conversion, this padding might cause characters to exceed the specified size 
(set with the -s option) or result in unnecessary blank spaces.
Use this offset to minimize padding or to place it where desired, ensuring better control over the output.
if not specified, the default value is 0.                        
                        """)
    parser.add_argument("-yo", "--yoffset", type=int, default=-1, help="Reffer to -xo option.\n If not specified, the default value is -1.\n")
    parser.add_argument("-cs", "--codeset", choices=["ALL","LEVEL1","SCHOOL","TEST"], default="ALL", help="""Code Sets to Include in the Data\n
- ALL: Includes JIS Level 1, Level 2 characters, various symbols, Kana, and all other supported characters.
- LEVEL1: Includes JIS Level 1 characters, various symbols, Kana, and all other supported characters.
- SCHOOL: Includes educational Kanji (learned by the end of 6th grade in elementary school), Hiragana, Katakana, and various symbols.
- TEST: A smaller set of characters intended for debugging purposes. Used during testing and contains fewer characters.
If not specified, the default value is ALL.                        
                        """)
    parser.add_argument("-o", "--output", type=str, default="XXX.XXX", help="""Specifies the name of the output file.
Since the output file is a C++ header file, it is typically given the extension .h. 
If not specified, the file name will be automatically generated based on the source file name, font size, and code set.
""")
    parser.add_argument("-m", "--mapping", choices=["KANA","NONE"], default="KANA", help="""Mapping Specific Character Groups to Alternative Glyphs.
- KANA: Remap single-byte Kana code
On many Japanese retro-computers, the single-byte codes 0xA1-0xDF (a range where international characters are defined in ISO8859)
are typically assigned to half-width Kana characters.  
When this option is selected, the glyphs in the range 0xA1-0xDF are mapped to the glyphs for half-width characters in 
UTF-8 (range 0xFF61–0xFF9F).  
- NONE: No mapping conversion is performed.
For example, the single-byte codes 0xA1–0xDF will result in undefined glyphs following
the ISO8859 standard, leading to unexpected character shapes.                          
if not specified, the default value is KANA.
""")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("-i", "--image", action="store_true", help="Display truetype font image")
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




    #入力ファイルが　”test" なら、テスト用のデータを読み込む
    if (font_path == "test"):
        font_path = "E:\Programing\VSCode\Font\JF-Dot-Shinonome12.ttf"

    #出力ファイルが指定されなかったら、フォントファイル名に基づいて、.hファイルを作成する
    if (output_file == "XXX.XXX"):
        output_file = Path(font_path).name.split(".")[0] + "_" + str(font_XSize).zfill(2) + "x"+str(font_YSize).zfill(2)  + "_" + code_set +".h"

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
    font =  ImageFont.truetype(font_path, font_XSize)

    #フォントの範囲を定義しておく

    ASCII = range(0x0000,0x0100)
    JISL1 = range(0x3021,0x4f54)
    JISL2 = range(0x5021,0x7427)
    JISKIGOU = range(0x2121,0x2F7E)
    
    # デバッグ用の特別なフォント範囲
    test1 = range(0x00A0,0x00A5) 
    test2 = range(0x212F,0x2130)

    #指定されたフォントセットに基づいて、文字コードを変換してUTF-8/SJIS/JISコードのリスト配列にしておく
    codeList = []                           # コードのリスト。
    if (code_set == "ALL"):
        if isVerbose :
            print(f"Generating Code tables for ASCII/JISL1/JISL2/JISKIGOU....")
        codeList += getCodeTbl(ASCII)
        codeList += getCodeTbl(JISL1)
        codeList += getCodeTbl(JISL2)
        codeList += getCodeTbl(JISKIGOU)   
    elif (code_set == "LEVEL1"):
        if isVerbose :
            print(f"Generating Code tables for ASCII/JISL1/JISKIGOU....")
        codeList += getCodeTbl(ASCII)
        codeList += getCodeTbl(JISL1)
        codeList += getCodeTbl(JISKIGOU)
    elif (code_set == "SCHOOL"):
        #教育漢字の場合、少し複雑。とりあえずJISL1のテーブルを作って、そこから該当しないものを削除していくことにする。
        if isVerbose :
            print(f"Generating Code tables for ASCII/JISL1/JISKIGOU....")
        codeList += getCodeTbl(ASCII)
        codeList += getCodeTbl(JISL1)
        codeList += getCodeTbl(JISKIGOU)
        if isVerbose :
            print(f"Removing non-Kyouiku Kanji characters....")

        for d in codeList :
            if d[0] <= 0xFF:            #１バイト文字は含める
                continue
            if d[3] not in KyouikuKanji:    #教育漢字に含まれないものは削除する
                codeList.remove(d)
    elif (code_set == "TEST"):
        if isVerbose :
            print(f"Generating Code tables for debugging....")
        codeList += getCodeTbl(test1)
        codeList += getCodeTbl(test2)
    if isVerbose:
        print("done.")


    # コードセットを、最初の要素（UTF-8)でソートする。こうしないと、後から検索するときにバイナリサーチで検索ができないため
    if isVerbose:
        print(f"Sorting code list with UTF-8...." )
    codeList.sort(key=lambda x: x[0])
    if isVerbose:
        print("done.")

    #　コードセットテーブルを、ビットマップデータに変換する。同時に、コードセットテーブル内のXサイズ、Yサイズ、ビットマップデータを更新する
    if isVerbose:
        print(f"Generating bitmap data....")
    bmpList = []
    codeList , bmpList = convToDataAndBitmap(codeList,  font_XSize,font_YSize,x_offset,y_offset)
    if isVerbose:
        print("done.")

    if isVerbose:
        print(f"Generating output file: {output_file}....")

    with open(output_file, "w", encoding="utf-8") as f:
        strOutput = ""
        strOutput +="// This file is auto generated by font.py\n"
        strOutput +="// Do not edit this file directly.\n"
        strOutput +="// Font: " + Path(font_path).name + "\n"
        strOutput +="// Font Size: " + str(font_XSize)+"x"+str(font_YSize)  + "\n"
        strOutput +="// Code Set: " + code_set + "\n"
        strOutput +="// Character count: " + str(len(codeList)) + "\n"
        strOutput +=f"// data size:{total_size(bmpList):} bytes\n"
        f.write(strOutput)
        if isVerbose:
            print(strOutput,end="")
            print()


        #まず、ビットマップ情報の表示
        strOutput = ""
        
        strOutput += "struct KanjiData {\n"
        strOutput += "\tuint32_t Unidoe;\n"
        strOutput += "\tuint16_t SJIS;\n"
        strOutput += "\tuint16_t JIS;\n"  
        strOutput += "\tuint8_t width;\n"
        strOutput += "\tuint8_t height;\n"
        strOutput += "\tuint32_t offsetBMP;\n"
        strOutput += "};\n"

        f.write(strOutput)
        if isVerbose:
            print(strOutput,end="")
            print()

        strOutput = ""
        strOutput += f"static const KanjiData {structure_name}[] = {{\n"
        for i, code in enumerate(codeList):
            strWkLine = ""
            strWkLine = f"\t{{ 0x{hex(code[0])[2:].zfill(8)} , 0x{hex(code[1])[2:].zfill(4)} , 0x{hex(code[2])[2:].zfill(4)} , {code[4]:>2} ,{code[5]:>2} , 0x{hex(code[6])[2:].zfill(8)} }}}}"
            if i < len(codeList) - 1:
                strWkLine += ","
            else:
                strWkLine += " "
            strWkLine += f"\t// {code[3]}\n"
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


        for charNo , row in enumerate(bmpList):
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
        print(f"done.")

    print(f"Success.. Output file: {output_file} created.")

