# AmbientのPython/MicroPythonモジュール

## Ambient
[Ambient](https://ambidata.io)はIoTデーター可視化サービスで、センサーデーターを受信し、蓄積し、可視化(グラフ化)します。

![Ambient structure](https://ambidata.io/wp/wp-content/uploads/2016/09/AmbientStructure.jpg)

Ambientにユーザー登録(無料)し、マイコンからデーターを送ると、こんな感じでグラフ表示させることができます。

![Ambient chart](https://ambidata.io/wp/wp-content/uploads/2016/09/fig3-1024x651.jpg)

ambient-python-libはAmbientのPython/MicroPythonライブラリーです。
Ambientにデーターを送信する機能と、Ambientに蓄積されたデーターを読み込む機能があります。
MicroPythonでも動作します。

## モジュールのインストール

```sh
$ sudo pip install git+https://github.com/AmbientDataInc/ambient-python-lib.git
```

## モジュールのimport

```python
import ambient
```
## Ambientへのデーター送信

最初にチャネルIdとライトキーを指定してAmbientのインスタンスを作り、send()メソッドでデーターを送信します。データーは次のような辞書形式で渡します。キーは'd1'から'd8'までのいずれかを指定します。

```python
am = ambient.Ambient(チャネルId, ライトキー[, リードキー[, ユーザーキー]])
r = am.send({'d1': 数値, 'd2': 数値}[, timeout = timeout])
```

#### パラメーター
  上記のような辞書形式でデーターを渡してください。キーは"d1"から"d8"までのいずれかを指定してください。

この形式でデーターを送信した場合、Ambientはデーターを受信した時刻を合わせて記録します。 次のようにデーターを測定した時刻を指定することもできます。

```python
r = am.send({'created': 'YYYY-MM-DD HH:mm:ss.sss', 'd1': 1.1, 'd2': 2.2})
```

また、次のように複数のデーターを一括で送信することもできます。

```python
data = [
    {'created': '2017-02-18 12:00:00', 'd1': 1.1, 'd2': 2.1},
    {'created': '2017-02-18 12:01:00', 'd1': 1.5, 'd2': 3.8},
    {'created': '2017-02-18 12:02:00', 'd1': 1.0, 'd2': 0.8}
]
r = am.send(data)
```

timeout にはサーバー接続のタイムアウト値を指定します。省略時は5.0秒です。

#### 戻り値

Pythonの[Requests](http://requests-docs-ja.readthedocs.io/en/latest/)の戻り値と同じものが返ります。特に

```python
r.status_code
```

に、サーバーにデーターを送信したときの結果(ステータスコード)がセットされます。送信に成功していれば200がセットされます。

## Ambientからのデーター読み込み

データー送信と同様に最初にチャネルIdとライトキー、リードキーを指定してインスタンスを作ります。
読み込みしかしない場合、ライトキーは''を指定しても大丈夫です。

```python
am = ambient.Ambient(チャネルId, ライトキー[, リードキー[, ユーザーキー]])
```

データーの読み込みにはデーター件数を指定する方法、日付を指定する方法、期間を指定する方法があります。

### 件数を指定してデーターを読み込む

```python
d = am.read(n=件数[, skip=スキップ件数[, timeout = timeout]])
```

#### パラメーター

* n: 読み込むデーター件数を指定します。最新のn件のデーターが読み込まれます。
* skip: スキップ件数。最新からスキップ件のデーターを読み飛ばし、その先n件のデーターが読み込まれます。
* timeout: サーバー接続のタイムアウト値（秒）。省略時は5.0秒。

#### 戻り値

* 次のような辞書形式(JSON形式)の配列が返されます。

```python
[
    {'created': '2017-02-25T15:01:48.000Z', 'd1': 数値, 'd2': 数値, 'd3': 数値},
    {'created': '2017-02-25T15:06:47.000Z', 'd1': 数値, 'd2': 数値, 'd3': 数値},
    ...
]
```

データーの生成時刻'created'は協定世界時(UTC)で表示されます。データーは生成時刻の昇順(古いものから新しいものへ)で並びます。

### 日付を指定してデーターを読み込む

```python
d = am.read(date='YYYY-mm-dd'[, timeout = timeout])
```

#### パラメーター

* date='YYYY-mm-dd': 指定した日付のデーターを読み込みます。
* timeout: サーバー接続のタイムアウト値（秒）。省略時は5.0秒。

#### 戻り値

件数を指定した場合と同じ辞書形式の配列が返されます。

### 期間を指定してデーターを読み込む

```python
d = am.read(start='YYYY-mm-dd HH:MM:SS', end='YYYY-mm-dd HH:MM:SS'[, timeout = timeout])
```

#### パラメーター

* start='YYYY-mm-dd HH:MM:SS':
* end='YYYY-mm-dd HH:MM:SS':
　startからendまでの期間のデーターを読み込みます。
* timeout: サーバー接続のタイムアウト値（秒）。省略時は5.0秒。

#### 戻り値

件数を指定した場合と同じ辞書形式の配列が返されます。

## チャネル情報の取得

データー名やチャネルの位置情報など、Ambientで指定したチャネル情報を取得します。

```python
prop = am.getprop([, timeout = timeout])
```

#### パラメーター

* timeout: サーバー接続のタイムアウト値（秒）。省略時は5.0秒。

#### 戻り値

チャネル情報が辞書形式で返されます。d1からd8までのデーターに設定した名前は

```python
prop['d1']['name']
```

で参照できます。

## MicroPythonでの使い方

「ambient.py」を開発環境にダウンロードし、
さらにmpfshellなどのツールを使ってマイコンのローカルファイルシステムにコピーしてください。
mpfshellについては「[ESP-WROOM-02でMicroPython (Mac) shellの導入](http://qiita.com/taka-murakami/items/25bec288d4aa1bc6f63f)」をご覧ください。
これでMicroPythonのインタープリターやプログラムから「import ambient」できるようになります。

## 事例

examplesディレクトリーの下に例を置きました。

### hdc1000

Raspberry PiのPythonでhdc1000というセンサーで5分ごとに温度、湿度を測定し、Ambientに送信してグラフ化する例です。
詳しくは「[Raspberry Pi3で温度湿度を測定し、Ambientで可視化する](https://ambidata.io/examples/python/)」をご覧ください。

### uenv

ESP8266のMicroPythonで温度、湿度、照度、振動を測定し、Ambientで記録する例です。
詳しくは「[MicroPython (ESP8266)で温度、湿度、照度、振動を測定し、Ambientで記録、可視化する](https://ambidata.io/samples/vibration/vibration-2/)」をご覧ください。

### M5_BME280

M5Stackに温湿度・気圧センサーBME280をつなぎ、温度、湿度、気圧を測定して、Ambientに送信する例です。
詳しくは「[M5Stack(Micropython編)](https://ambidata.io/samples/m5stack/m5stack-micropython/)」をご覧ください。

### M5_BME680

M5Stackに温湿度・気圧・空気品質センサーBME680をつなぎ、温度、湿度、気圧を測定して、Ambientに送信する例です。
詳しくは「[M5Stack(Micropython編)](https://ambidata.io/samples/m5stack/m5stack-micropython/)」をご覧ください。
