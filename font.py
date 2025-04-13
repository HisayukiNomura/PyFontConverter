
from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import codecs
import argparse
from pathlib import Path


## フォントをビットマップにレンダリングする関数
def render_glyph_to_bitmap(font, char, font_size=64,X_offset = 0,Y_offset=-1):
    global isImage
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
    if isImage:
        image.show()
        print("Displaying the image. Please close the window before pressing [ENTER]...")
        input()  
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




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert Bitmap font from TrueType(.TTF) file.",
                                        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    epilog='''
    Additional helpful information can be added here.
    '''
    )
    parser.add_argument("font_path", type=str,help="Path to the turetype font file")
    parser.add_argument("-n", "--name", type=str, default="", help="Name of generated structure instance")
    parser.add_argument("-s", "--size", type=int, default=12, help="Font size")
    parser.add_argument("-xo", "--xoffset", type=int, default=0, help="X offset")
    parser.add_argument("-yo", "--yoffset", type=int, default=-1, help="Y offset")
    parser.add_argument("-cs", "--codeset", choices=["ALL","LEVEL1","JYOUYOU","KYOUIKU","TEST"], default="ALL", help="Code set to use.")
    parser.add_argument("-o", "--output", type=str, default="XXX.XXX", help="Output file name")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("-i", "--image", action="store_true", help="Display truetype font image")
    args = parser.parse_args()
    font_path = args.font_path
    font_size = args.size
    x_offset = args.xoffset
    y_offset = args.yoffset
    code_set = args.codeset
    output_file = args.output
    isVerbose = args.verbose
    isImage = args.image




    #入力ファイルが　”test" なら、テスト用のデータを読み込む
    if (font_path == "test"):
        font_path = "E:\Programing\VSCode\Font\JF-Dot-Shinonome12.ttf"

    #出力ファイルが指定されなかったら、フォントファイル名に基づいて、.hファイルを作成する
    if (output_file == "XXX.XXX"):
        output_file = font_path.split(".")[0]+ "_" + str(font_size).zfill(2)  + "_" + code_set +".h"

    if (args.name == ""):
        namebase = Path(font_path).name.split(".")[0]
        # 置換対象の文字リスト
        invalid_chars = {"+", "-", "*" ,"/", " ", " ", "(", ")", "[", "]", "{", "}", ":", ";", ",", ".", "<", ">", "?", "!", "@", "#", "$", "%", "^", "&", "~", "`"}
        # 置換後の文字列を作成
        cleaned_name = "".join(char for char in namebase if char not in invalid_chars)



        structure_name =  cleaned_name+ "_" + str(font_size).zfill(2)  + "_" + code_set
        bitmapdata_name = cleaned_name+ "_" + str(font_size).zfill(2)  + "_" + code_set + "_bitmap"
    else:
        structure_name = args.name
        bitmapdata_name =  args.name+"_bitmap"

    #font_path = "E:\Programing\VSCode\Font\JF-Dot-Shinonome12.ttf"  # フォントファイルのパス
    #char = "野"  # レンダリングする文字
    #font_size = 12  # フォントサイズを指定
    
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
    


    codeList , bmpList = convToDataAndBitmap(codeList,font_size,x_offset,y_offset)

    """
    for code in codeList:
        print(hex(code[0]),hex(code[1]),hex(code[2]),code[3],code[4],code[5],code[6])
        ArraySizeX = round(code[4]/8) * code[5]
        printBitArray(bmpList[code[6]])
    """
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("// This file is auto generated by font.py\n")
        f.write("// Do not edit this file directly.\n")
        f.write("// Font: " + Path(font_path).name + "\n")
        f.write("// Font Size: " + str(font_size) + "\n")
        f.write("// Code Set: " + code_set + "\n")
        

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
            print(strOutput,end="");
            print()

        strOutput = ""
        strOutput += f"static const KanjiData {structure_name}[] = {{\n"
        for i, code in enumerate(codeList):
            strWkLine = ""
            strWkLine = f"\t{{ 0x{hex(code[0])[2:].zfill(8)} , {hex(code[1])} , {hex(code[2])} , {code[4]} ,{code[5]} , 0x{hex(code[6])[2:].zfill(8)} }}}}"
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
        print()

        print(f"Output file: {output_file} created.")

