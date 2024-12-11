# TrainGTFSGenerator

列車時刻表、列車路線情報、駅情報の3つからGTFSデータを生成するためのスクリプトです。<br>
列車時刻表、列車路線情報、駅情報の3つは[**Mini Tokyo 3D**](https://github.com/nagix/mini-tokyo-3d)のリポジトリ内のデータを使用しています。<br>
Mini Tokyo 3Dの一部のJSONデータにバグが存在するため、自分のリポジトリに[フォーク](https://github.com/fksms/mini-tokyo-3d)し修正したものをSubmoduleとして取り込んでいます。<br>
<br>

## GTFS出力対応オペレーター
自分が利用したい22のオペレーターをピックアップしています。<br>
アップストリームには下記以外のデータも存在するので、下記以外のGTFSを出力したい場合は`src/main.py`を修正して実行してください。<br>

- 京王電鉄
- 相模鉄道（相鉄）
- 東日本旅客鉄道（JR東日本）
- 東武鉄道
- 横浜市交通局
- 東京都交通局
- 東京臨海高速鉄道
- 多摩都市モノレール
- 東京メトロ
- 首都圏新都市鉄道（つくばエクスプレス）
- 北総鉄道
- 京急電鉄
- 京成電鉄
- 横浜高速鉄道（みなとみらい線）
- 小田急電鉄
- 西武鉄道
- 新京成電鉄
- 埼玉高速鉄道
- 東京モノレール
- 東急電鉄
- 東葉高速鉄道
- ゆりかもめ
<br>
<br>

## 生成済みGTFSのダウンロード

生成済みGTFSは[Release](https://github.com/fksms/TrainGTFSGenerator/releases)からダウンロード可能です。<br>
新規にReleaseを発行する場合は[Actions](https://github.com/fksms/TrainGTFSGenerator/actions)から手動でワークフローを実行する。<br>
<br>

## スクリプトの利用方法

MacOSで実行する前提の手順です。<br>
スクリプト実行後は`dist`フォルダにオペレーター毎のGTFSデータが生成されます。<br>
<br>

### 事前準備

pipxのインストール
```sh
brew install pipx
```

Poetryのインストール
```sh
pipx install poetry
```

Poetryのパッケージインストール先をプロジェクトのルートフォルダに変更
```sh
poetry config virtualenvs.in-project true
```
<br>

### スクリプトの実行

このリポジトリをクローン<br>
（Submoduleを追加しているので`--recursive --shallow-submodules`を指定）
```sh
git clone --recursive --shallow-submodules https://github.com/fksms/TrainGTFSGenerator.git
```

ディレクトリを移動
```sh
cd TrainGTFSGenerator
```

必要なパッケージをインストール
```sh
poetry install
```

実行
```sh
poetry run python src/main.py
```
<br>

## ライセンス

The MIT License (MIT)<br>
Copyright (c) 2024 Shogo Fukushima