# Audio spectrum Movie Maker

- 静止画のサムネイル画像に音声データの波形をのせた動画を出力するpythonスクリプト


## Usage

### 準備

- [Zip Download](https://github.com/dieu-detruit/werther-audio-spectrum-python/archive/refs/heads/master.zip)からダウンロードし、好きな場所に解凍します
- 解凍したら、ターミナルを開いて解凍した場所へ移動します
- 例(デスクトップに解凍した場合)
```
cd ~/Desktop/werther-audio-spectrum-python
```

- 続いて、セットアップを行います(はじめの1回だけでよいです)
```
./setup.sh
```

### 動画の書き出し

- werther-audio-spectrum-pythonフォルダの中に、サムネ画像と音声データを入れます
- 例
```
werther-audio-spectrum-python/
　├ thumb/
　│　└ 17710512.png
　└ wav/
　 　└ 17710512.wav
```

- 入れたら、ターミナルで書き出しを行います
- 例 (日付は適宜変更してください)
```
./pipeline.sh 17710512
```