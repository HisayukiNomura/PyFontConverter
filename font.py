
from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import codecs

## フォントをビットマップにレンダリングする関数
def render_glyph_to_bitmap(font, char, font_size=64,X_offset = 0,Y_offset=-1):
    # FontToolsでフォントファイルを解析
    #ttfont = TTFont(font_path)
    #print(f"Font Family: {ttfont['name'].getDebugName(1)}")  # フォントファミリー名を取得

    # Pillowでフォントを読み込み
    #font = ImageFont.truetype(font_path, font_size)
    
    # ビットマップ画像を作成
    image_size = (font_size , font_size )  # 画像サイズを指定
    image = Image.new("L", image_size, color=255)  # グレースケール画像（白背景）
    draw = ImageDraw.Draw(image)
    draw.text((X_offset, Y_offset), char, font=font, fill=1)  # 文字を黒で描画

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
    
    ArraySizeX,ArraySizeY  = binary_bitmap.shape
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
        #print()
    #print()

    """
    for row in bitArray:
        for value in row:
            print(bin(value)[2:].zfill(8), end="")
        print() 
    print()
    """
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
# 戻り値は、utf-8,sjis,jis,文字,ｗ,ｈ、オフセット。 W,H,オフセットは後から決定する
def getCodeTbl(codeRange): 
    CodeList = []
    for code in codeRange:
        codeJIS , codeSJIS , codeUTF8 = jis_to_encodings(code)
        if codeJIS == 0 or codeSJIS == 0 or codeUTF8 == 0:
            #print(f"JISコード: {hex(code)}をスキップ")
            continue
        #print(f"JISコード: {hex(codeJIS)}, Shift-JIS: {hex(codeSJIS)}, UTF-8: {hex(codeUTF8)} ")

        utf8_bytes = codeUTF8.to_bytes(3, byteorder='big')
        unicode_char = utf8_bytes.decode('utf-8')
        #print(f"JISコード: {hex(codeJIS)}, Shift-JIS: {hex(codeSJIS)}, UTF-8: {hex(codeUTF8)} : 文字：{unicode_char}")
        
        CodeList.append([codeUTF8,codeSJIS,codeJIS,unicode_char,0,0,0])
    return CodeList

# コードの一覧からビットマップ配列を作り、コード一覧にはビットマップのオフセット位置を追加する関数
def convToDataAndBitmap(codeList,fntSize,xOffset = 0,yOffset=-1): 
    byteOffset = 0
    for code in codeList:
        code[6] = byteOffset
        print(hex(code[0]),hex(code[1]),hex(code[2]),code[3],code[6])
        bitmap_image = render_glyph_to_bitmap(font, code[3], fntSize,xOffset,yOffset)
        code[4] = bitmap_image.size[0]  # 幅を取得
        code[5] = bitmap_image.size[1]  # 高さを取得
        bmpData = display_bitmap_data(bitmap_image)
        bmpList.append(bmpData)
        byteOffset += bmpData.size
    return (codeList,bmpList)

def printBitArray(bitArray):
    for row in bitArray:
        for value in row:
            print(bin(value)[2:].zfill(8), end="")
        print() 
    print()

"""
struct KanjiData {
    uint32_t Unidoe;
    uint16_t SJIS;
    uint16_t JIS;
    uint8_t width;
    uint8_t height;
    uint16_t offsetBMP;
};
static const KanjiData fontNameData[] = { {unicode,sjis,jis,12,12,0x0001}, ,,,}

static const uint8_t fontNameBitmap[] = {....}
という感じにして生きた。

問題は、offsetBMP。レンダリングするまでサイズは正確にはわからない。
リストの各要素はタプルになっているので、サイズの追加が面倒
　⇒　別のリストを用意するか？　タプルを書き換えるか？そもそもタプルを止めて、リストのリストにするか？
"""

if __name__ == "__main__":
    font_path = "E:\Programing\VSCode\Font\JF-Dot-Shinonome12.ttf"  # フォントファイルのパス
    #char = "野"  # レンダリングする文字
    font_size = 12  # フォントサイズを指定
    
    # Pillowでフォントを読み込み
    font =  ImageFont.truetype(font_path, font_size)

    JISL1 = range(0x3021,0x4f53)
    JISL2 = range(0x5021,0x7426)
    JISKIGOU = range(0x2121,0x2F7E)
    
    test = range(0x3021,0x3023)    

    
    codeList = []
#    codeList += getCodeTbl(JISL1)
#    codeList += getCodeTbl(JISL2)
#   codeList += getCodeTbl(JISKIGOU)
    codeList += getCodeTbl(test)
    codeList.sort(key=lambda x: x[0])



    bmpList = []
    print(len(codeList))
    


    codeList , bmpList = convToDataAndBitmap(codeList,font_size,0,-1)

    """
    for code in codeList:
        print(hex(code[0]),hex(code[1]),hex(code[2]),code[3],code[4],code[5],code[6])
        ArraySizeX = round(code[4]/8) * code[5]
        printBitArray(bmpList[code[6]])
    """
    
    #まず、ビットマップ情報の表示
    print ("struct KanjiData {")
    print ("\tuint32_t Unidoe;")
    print ("\tuint16_t SJIS;")
    print ("\tuint16_t JIS;")
    print ("\tuint8_t width;")
    print ("\tuint8_t height;")
    print ("\tuint32_t offsetBMP;")
    print ("};")
    print()
    print ("static const KanjiData fontNameData[] = {")

    for i, code in enumerate(codeList):
        strWkLine = ""
        strWkLine = f"\t{{ 0x{hex(code[0])[2:].zfill(8)} , {hex(code[1])} , {hex(code[2])} , {code[4]} ,{code[5]} , 0x{hex(code[6])[2:].zfill(8)} }}}}"
        if i < len(codeList) - 1:
            strWkLine += ","
        else:
            strWkLine += " "
        strWkLine += f"\t// {code[3]}\r\n"
        print(strWkLine,end="")
    print("};")
    print()

    # 次に対応するビットマップデータを表示
    offset = 0
    print("static const uint8_t fontNameBitmap[] = {")
    for charNo , row in enumerate(bmpList):
        oneBlock = ""
        oneBlock += f"// UNICODE:0x{hex(codeList[charNo][0])[2:].zfill(8)} -  Offset:0x{hex(codeList[charNo][6])[2:].zfill(8)}   -- CHAR:\"{codeList[charNo][3]}\" \r\n"
        for value in row:
            bitsInfo = ""
            for x , xdata in enumerate(value) :
                bitsInfo += bin(xdata)[2:].zfill(8)
                oneBlock += f"0x{hex(xdata)[2:].zfill(2)}"

                #print(f"0x{hex(xdata)[2:].zfill(2)}",end = "")
                if x < len(value) - 1:
                    oneBlock += ","
                else:
                    oneBlock += ","
                    oneBlock += f"\t\t// {bitsInfo} \r\n"
                    #print(f"\t\t// {bitsInfo}")
        oneBlock += "\r\n"
        print (oneBlock,end="")
        #print("")
    print ("};")    
    print()

"""
truct KanjiData {
    uint32_t Unidoe;
    uint16_t SJIS;
    uint16_t JIS;
    uint8_t width;
    uint8_t height;
    uint16_t offsetBMP;
};
static const KanjiData fontNameData[] = { {unicode,sjis,jis,12,12,0x0001}, ,,,}

static const uint8_t fontNameBitmap[] = {....}
という感じにして生きた。            
"""
"""
    for code in codeJISL1:
        codeJIS , codeSJIS , codeUTF8 = jis_to_encodings(code)
        if codeJIS == 0 or codeSJIS == 0 or codeUTF8 == 0:
            print(f"JISコード: {hex(code)}をスキップ")
            continue
        #print(f"JISコード: {hex(codeJIS)}, Shift-JIS: {hex(codeSJIS)}, UTF-8: {hex(codeUTF8)} ")

        utf8_bytes = codeUTF8.to_bytes(3, byteorder='big')
        unicode_char = utf8_bytes.decode('utf-8')
        print(f"JISコード: {hex(codeJIS)}, Shift-JIS: {hex(codeSJIS)}, UTF-8: {hex(codeUTF8)} : 文字：{unicode_char}")
        CodeList.append(codeUTF8,codeSJIS,codeJIS,unicode_char)

        # char = unicode_char  # レンダリングする文字
        #
        #bitmap_image = render_glyph_to_bitmap(font, char, font_size)
        #display_bitmap_data(bitmap_image)


    bitmap_image = render_glyph_to_bitmap(font, char, font_size)
    # bitmap_image.show()  # ビットマップ画像を表示
    display_bitmap_data(bitmap_image)
"""

"""
import codecs

jis_code = 0x3022  # JISコード
try:
    # 2バイトのJISコードをバイト列に変換
    jis_bytes = jis_code.to_bytes(2, byteorder='big')
    hex_representation = jis_bytes.hex()
    print(f"JISコードのバイト列: {hex_representation}")
    
    
    # JISコードをデコードしてUnicode文字に変換
    unicode_char = codecs.decode(jis_bytes, 'iso2022_jp')
    print(f"対応する文字: {unicode_char}")

    # Unicode文字をUTF-8バイト列にエンコード
    utf8_bytes = unicode_char.encode('utf-8')
    hex_representation = utf8_bytes.hex()
    print(f"UTF-8バイト列: {hex_representation}")

except Exception as e:
    print(f"エラー: {e}")
"""


"""
import freetype
import numpy as np
import matplotlib.pyplot as plt

def render_glyph_from_ttc(ttc_path, font_index, char, font_size=64):
    # フォントコレクションから特定のフォントを選択
    face = freetype.Face(ttc_path, font_index)
    face.set_char_size(font_size * 64)

    # 指定した文字をロード
    face.load_char(char)
    bitmap = face.glyph.bitmap

    # ビットマップデータを取得
    rows, width = max(bitmap.rows, 1), max(bitmap.width, 1)  # 幅と高さが0にならないように最低値を1に設定
    bitmap_data = np.zeros((rows, width), dtype=np.uint8)

    if bitmap.buffer:
        for row in range(bitmap.rows):
            bitmap_data[row, :bitmap.width] = bitmap.buffer[row * bitmap.width: (row + 1) * bitmap.width]

    return bitmap_data

def display_bitmap(bitmap):
    plt.imshow(bitmap, cmap="gray", interpolation="nearest")
    plt.axis("off")
    plt.show()

if __name__ == "__main__":
    ttc_path = "E:\Programing\VSCode\Font\JF-Dot-Shinonome12.ttf"  # TTCファイルのパス
    font_index = 0  # 使用したいフォントのインデックス（0から始まる）
    char = "あ"  # レンダリングする文字
    font_size = 12  # フォントサイズ

    bitmap = render_glyph_from_ttc(ttc_path, font_index, char, font_size)
    display_bitmap(bitmap)

"""