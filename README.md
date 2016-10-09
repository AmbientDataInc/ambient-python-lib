# ambient-python-lib AmbientのPythonモジュール

## Ambient
[Ambient](https://ambidata.io)はIoTクラウドサービスで、センサーデーターを受信し、蓄積し、可視化(グラフ化)します。

![Ambient structure](https://ambidata.io/wp/wp-content/uploads/2016/09/AmbientStructure.jpg)

Ambientにユーザー登録(無料)し、マイコンからデーターを送ると、こんな感じでグラフ表示させることができます。

![Ambient chart](https://ambidata.io/wp/wp-content/uploads/2016/09/fig3-1024x651.jpg)

ambient-python-libはAmbientにデーターを送信するPythonモジュールです。

## モジュールのインストール

```sh
$ sudo pip install git+https://github.com/TakehikoShimojima/ambient-python-lib.git
```

## モジュールのimport

```python
import ambient
```
## Ambientへの接続

```python
ambi = ambient.Ambient(チャネルId, ライトキー[, リードキー[, ユーザーキー]])
```
Ambientにデーターを送信するときは、チャネルIdとライトキーを指定してAmbientに接続します。

## Ambientへのデーター送信

```python
r = ambi.send({"d1": 2.0, "d2": 3.1, "d3": 4.5})
```

* パラメーター
  上記のような辞書形式でデーターを渡してください。キーは"d1"から"d8"までのいずれかを指定してください。
