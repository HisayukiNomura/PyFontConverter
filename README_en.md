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
