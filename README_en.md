# Utility for Creating Bitmap Font Files from TTF Files

Currently, output is possible in C language, Python source code, binary, FontX, and BDF formats.


## Preparation
Install the required packages:

```
pip install -r requirements.txt
```

## How to Use PyFontConverter

1. Download `font.py` from [PyFontConverter GitHub](https://github.com/HisayukiNomura/PyFontConverter).
2. Run the following command in the terminal:

```
python font.py [options] fontfile(ttf)
```


### Main Options and Default Values

| Option | Description | Default Value |
|--------|-------------|--------------|
| `-h, --help` | Show help message and exit. | - |
| `-n, --name NAME` | Specify the name of the struct generated in the C header file.<br>If not specified, it will be auto-generated based on the file name or other arguments. | Auto-generated |
| `-s, --size SIZE` | Specify the font size.<br>Full-width characters are converted to squares of the specified size.<br>Half-width characters are drawn at half the specified width. | `12` |
| `-xo, --xoffset XOFFSET` | Specify the horizontal shift amount (in pixels) for characters.<br>When rendering TrueType fonts, adjacent characters may be too close and hard to read.<br>This offset can be used to adjust extra padding between characters. | `0` |
| `-yo, --yoffset YOFFSET` | Specify the vertical shift amount (in pixels) for characters.<br>Useful for adjusting spacing, similar to `-xo`. | `-1` |
| `-cs, --codeset {ALL,LEVEL1,SCHOOL,CUSTOM,TEST}` | Specify the character set to include in the data.<br>**ALL:** Includes JIS Level 1 & 2 Kanji, symbols, Katakana, and Hiragana.<br>**LEVEL1:** Includes JIS Level 1 Kanji, symbols, Katakana, and Hiragana.<br>**SCHOOL:** Includes Kanji learned in elementary school, Hiragana, Katakana, and symbols.<br>**CUSTOM:** Use the character set specified with `-cf`.<br>**TEST:** Small set for debugging. | `ALL` |
| `-cf, --charfile CHARFILE` | Specify a text file containing the list of characters to include in the output.<br>Required when using `-cs CUSTOM`. | - |
| `-o, --output OUTPUT` | Specify the name of the output file.<br>If not specified, it will be auto-generated based on the source file name, font size, and code set.<br>Depending on the output type, half-width and full-width characters may be output as separate files. | Auto-generated |
| `-m, --mapping {KANA,NONE}` | Map specific character groups to alternative glyphs.<br>**KANA:** Maps single-byte Kana codes to half-width Kana (UTF-8 `0xFF61–0xFF9F`).<br>**NONE:** No mapping (ISO8859 compliant). | `KANA` |
| `-em, --endmark {ALLZERO,ALLMAX,NONE}` | Specify the type of end mark to add at the end of the data.<br>This option is only valid when `-t` or `--outtype` is specified for a particular language (C or Python).<br>**ALLZERO:** Adds a termination marker with all UTF8, SJIS, and JIS values set to `0`.<br>**ALLMAX:** Adds a termination marker with all values set to `MAX`.<br>**NONE:** No end mark. | `ALLZERO` |
| `-t, --outtype {CData,PBinary,Python,FONTX2,BDF}` | Specify the output font data format.<br>**CData:** C struct and bitmap array (header file).<br>**PBinary:** Binary files (for code and bitmap).<br>**Python:** Output as a Python file containing font data.<br>**FONTX2:** Output in FONTX2 format (half-width and full-width as separate files).<br>**BDF:** Output in BDF format. | `CData` |
| `-bs , --bdf-split {Default,True,False}` | When outputting BDF files, output full-width and half-width characters as separate files.<br>If output type is not BDF, specifying True will cause an error.<br>**Default:** True for BDF files, otherwise follows output type.<br>**True:** Output full-width and half-width characters as separate BDF files.<br>**False:** Output a single file with both types mixed. | `Default` |
| `-en , --encoding {UTF8,SJIS,JIS}` | Specify the encoding for the output file. For BDF files, this sets the encoding for each character; for C or Python, it determines the sort order.<br/>The default value depends on the `-t` option. For C header and Python, it's UTF8; for FONTX, it's SJIS; for BDF, it's JIS. | Follows `-t` |
| `-fr, --filereplace` | Replace unsuitable characters (spaces, symbols, etc.) in output file names with `_`. | - |
| `-v, --verbose` | Show detailed debug information. | - |
| `-i, --image` | For debugging, display the character being converted during execution.<br>Useful when adjusting `xoffset` or `yoffset`. | - |


### About Help

If you start with --help, usage will be displayed without doing anything.

The help is displayed in Japanese or English depending on your system locale, but you can change it by setting the LANG environment variable to "ja_JP", "en_US", etc.

#### Example

```
python font.py JF-Dot-Shinonome12.ttf -s 12 -cs SCHOOL -o MyFont.h
```
This converts the TrueType font JF-Dot-Shinonome12.ttf to 12x12 dots, and outputs it as a C header file named MyFont.h containing only educational Kanji.

```
python font.py FONTDATA/ipam.ttf -s 24 -cs ALL -t FONTX2 -o IPAMincho
```
This converts FONTDATA/ipam.ttf to 24x24 dots, and outputs IPAMincho_zen.fnt (full-width) and IPAMincho_han.fnt (half-width). Full-width includes JIS Level 1 & 2, symbols, Kana, and others (Greek, Cyrillic, etc.).


### Notes

- For small bitmap sizes, it is recommended to use dot fonts or fonts designed for small sizes.
- Standard Windows fonts like MS Mincho are not suitable for small sizes.
- Example of a free, commercially usable small-size font: [http://jikasei.me/font/jf-dotfont/](http://jikasei.me/font/jf-dotfont/)  
  [Direct download](https://ftp.iij.ad.jp/pub/osdn.jp/users/8/8541/jfdotfont-20150527.7z)

### About Output Files

- By default, output is as a C++ header file (.h).
- Output in binary or Python format is also possible (see the -t option).
- The generated header file can be used as font data for the KNJGfx9341 project.


## How to Use the C Header File Format

The C header file output consists of two main parts: a Kanji code table and a bitmap pattern array.

### Kanji Code Table

The Kanji code table is an array of structs, each containing the character code, size, and a pointer (offset) to the bitmap pattern. The array is sorted by the code specified with the -en option (default: UTF-8), so you can use binary search to quickly find the pattern for a given character code.

Example struct:

```c
struct KanjiData {
    uint32_t Unicode;
    uint16_t SJIS;
    uint16_t JIS;
    uint8_t width;
    uint8_t height;
    uint32_t offsetBMP;
};

static const KanjiData JFDotShinonome12_12x12_ALL[] = {
    {0x00000000 , 0x0000 , 0x0000 ,  6 ,12 , 0x00000000}, // "0x00"
    {0x00000001 , 0x0001 , 0x0001 ,  6 ,12 , 0x0000000c}, // "0x01"
    {0x00000002 , 0x0002 , 0x0002 ,  6 ,12 , 0x00000018}, // "0x02"
    ...
    {0x00e88c85 , 0x8a9d , 0x337d , 12 ,12 , 0x0001d508}, // "茅"
    ...
};
```

### Bitmap Pattern

The bitmap pattern is a large array of bytes, each representing the shape of a character. For example:

```c
static const uint8_t JFDotShinonome12_12x12_ALL_bitmap[] = {
// UNICODE:0x00000000 -  Offset:0x00000000   -- CHAR:"0x00" 
    0x00, 0x00, 0x00, ...
// UNICODE:0x00e88c85 -  Offset:0x0001d508   -- CHAR:"茅" 
    0x11, 0x00, 0xff, 0xe0, 0x11, 0x00, 0x7f, 0x80, 0x11, 0x00, 0x0a, 0x00, 0xff, 0xe0, 0x0c, 0x40, 0x14, 0x80, 0x24, 0x00, 0xc4, 0x00, 0x0c, 0x00,
    ...
};
```

### How to Find a Character Pattern

The bitmap pattern array does not contain character code information. To get the pattern for a character, use the offset from the Kanji code table. For example, to display the character "茅" (Unicode 0x00e88c85), search the Kanji code table for this code using binary search. The entry `{0x00e88c85 , 0x8a9d , 0x337d , 12 ,12 , 0x0001d508}` gives the offset `0x0001d508`, so the pattern is at `JFDotShinonome12_12x12_ALL_bitmap[0x0001d508]`.

Even with 6,879 characters, you can find the pattern in at most 13 comparisons using binary search.

#### Example: Binary Search Code

Here is an example (adapted from KanjiHelper.cpp for the KNJGfx9341 project):

```c
struct KanjiData {
    uint32_t Unicode;
    uint16_t SJIS;
    uint16_t JIS;
    uint8_t width;
    uint8_t height;
    uint32_t offsetBMP;
};

const KanjiData* FindKanji(uint32_t unicode) {
    size_t left = 0;
    size_t right = DataSize - 1;
    const KanjiData* pKanjiData = JFDotShinonome12_12x12_ALL;
    while (left <= right) {
        size_t middle = left + (right - left) / 2;
        if (pKanjiData[middle].Unicode == unicode) {
            return &pKanjiData[middle];
        } else if (pKanjiData[middle].Unicode < unicode) {
            left = middle + 1;
        } else {
            right = middle - 1;
        }
    }
    return NULL;
}
```

### How to Use with Python Data

The Python data format is fundamentally similar to the C header format. The code table is packed using struct as IHHBBI, and the bitmap pattern is stored separately.

Example:

```python
import struct

code = b"".join(struct.pack("<IHHBBI", *data) for data in [
    (0x00000000, 0x0000, 0x0000, 12, 24, 0x00000000),  # "0x00"
    # ...
    (0x00e79bb4, 0x92bc, 0x443e, 24, 24, 0x00047b20),  # "直"
    (0x00e79bb8, 0x918a, 0x416a, 24, 24, 0x00047b68),  # "相"
    (0x00e79bbb, 0xe1bb, 0x623d, 24, 24, 0x00047bb0),  # "盻"
])

bitmap = bytes([
    0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, # ...
    # ...
])
```

To search the code table using binary search:

```python
import struct
import ipag_24x24_ALL  # Example: import the generated font data

def binary_search(target_key, record_size):
    left = 0
    right = len(ipag_24x24_ALL.code) // record_size - 1
    while left <= right:
        mid = (left + right) // 2
        start = mid * record_size
        record = struct.unpack("<IHHBBI", ipag_24x24_ALL.code[start:start+record_size])
        if record[0] == target_key:
            return record
        elif record[0] < target_key:
            left = mid + 1
        else:
            right = mid - 1
    return None

record_size = struct.calcsize("<IHHBBI")
key = 0x00e79bb4  # Unicode for '直'
record = binary_search(key, record_size)
print(record if record else "Record not found")
```

If you have enough memory, you can create a dictionary for easier access:

```python
record_size = struct.calcsize("<IHHBBI")
records_dict = {
    struct.unpack("<IHHBBI", code[i:i+record_size])[0]: struct.unpack("<IHHBBI", code[i:i+record_size])
    for i in range(0, len(code), record_size)
}
record = records_dict.get(key, "Record not found")
```

**Note:**
Originally, this Python program was designed for MicroPython on Raspberry Pi Pico to display Kanji on a screen. However, even with educational Kanji at 16x16 dots, memory was insufficient. The data must be loaded into memory to use it, and while the program memory is 1MB, RAM is only 256KB, making practical use difficult on microcontrollers.


## License

This project is licensed under the MIT License.

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

**Note:**
Font files generated in the FONTDATA directory are subject to the license and rights of the original font used for conversion.


---
