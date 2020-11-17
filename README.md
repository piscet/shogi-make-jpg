# れあｄめ
Python で盤面を一気に生成したいなーって思いつきからこのリポジトリを作りました。
以下のことができるようになるのが目標です宜しくお願いします。

* sfen -> jpg : **対応した！！！**
* kifファイル -> gif or jpg
* ライブラリ化

またディスコードで譜面作成などやりたいなぁ...

## How To Use
### sfen を画像化する
現在使い方としては src ファイルを直接利用するか main.py を使って sfen を指定するかの二択になっています。

```bash
$ python main.py 'sfen lnsgkgsnl/1r5b1/ppppppppp/9/9/9/PPPPPPPPP/1B5R1/LNSGKGSNL b - 1'
```

のように main.py の後に sfen を指定することでできるようになっています。まあとりあえずこんなくらい。
