# WSJ -> .puz
I wanted to collaborate with other people on the [Wall Street Journal's Friday Crossword Contests](https://blogs.wsj.com/puzzle/category/crossword-contest/).

[Down For Across](https://downforacross.com) is a wonderful website which allows people to work on crosswords together in real time! It also has a wonderful feature which allows people to upload .puz files.

So, my challenge was: how can I make a .puz file out of this week's Crossword Contest? I could do it by hand... or I could make my computer do it for me. The latter sounded infinitely superior.

There's a program called [Across Lite](https://www.litsoft.com/across/alite/download/), which can make .puz files. You can import a .txt file, formatted according to the [Across Lite Text Format](https://www.litsoft.com/across/docs/AcrossTextFormat.pdf), and then save it as a proper .puz file!

This script is not intended to work for other websites, and it doesn't output a .puz file directly (instead, it outputs a .txt, which has to be imported into Across Lite and subsequently saved). I'm hoping it will be useful anyway.

Usage is as follows:
```
python3 /path/to/wsj_to_puz.py https://link-to-WSJ
```

# DFC -> GSheet
All right, so you've just filled out the entirety of your crossword. BUT HOW DO YOU EXTRACT???

I like using Google Sheets to solve puzzles, and I've been copying over the WSJ crosswords  after solving them. I've spent time learning how to deal with crossword websites already. At this point, I might as well make a script to help transcribe crosswords on Down For Across.

Providing a link to a Down For Across puzzle and running the script copies a tab-separated (copy-pasteable!) version of the crossword to your clipboard. Black squares and unfilled squares are designated by characters of your choosing. Conditional formatting will be your friend.

Usage is as follows:
```
python3 /path/to/dfc_to_wsj.py https://link-to-downforacross
```
