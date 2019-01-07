# mon2_kadai
MIMOシミュレータプログラム
## 実行
```
python MimoSimulator.py
```
## 実験設定・オプション
推定方式、送信アンテナ数、受信アンテナ数、イテレーション数、シンボルビット数を設定可能です。
デフォルト値はそれぞれ、zf, 4, 4, 50000, 256です。
`-h`or`--help`を参考に設定して下さい。
### 例)MMSEで推定・受信アンテナ数=8
```
python MimoSimulator.py -m mmse -o 8
```
