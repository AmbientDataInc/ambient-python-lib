# ambient-python-lib AmbientのPythonモジュール

## Ambient
[Ambient](https://ambidata.io)はIoTクラウドサービスで、センサーデーターを受信し、蓄積し、可視化(グラフ化)します。

![Ambient structure](https://ambidata.io/wp/wp-content/uploads/2016/09/AmbientStructure.jpg)

Ambientにユーザー登録(無料)し、マイコンからデーターを送ると、こんな感じでグラフ表示させることができます。

![Ambient chart](https://ambidata.io/wp/wp-content/uploads/2016/09/fig3-1024x651.jpg)

ambient-python-libはAmbientのPythonライブラリーです。
Ambientにデーターを送信する機能と、Ambientに蓄積されたデーターを読み込む機能があります。

## モジュールのインストール

```sh
$ sudo pip install git+https://github.com/TakehikoShimojima/ambient-python-lib.git
```

## モジュールのimport

```python
import ambient
```
## Ambientへのデーター送信

最初にチャネルIdとライトキーを指定してAmbientのインスタンスを作り、send()メソッドでデーターを送信します。データーは次のような辞書形式で渡します。キーは'd1'から'd8'までのいずれかを指定します。

```python
am = ambient.Ambient(チャネルId, ライトキー[, リードキー[, ユーザーキー]])
r = am.send({'d1': 数値, 'd2': 数値})
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
d = am.read(n=件数[, skip=スキップ件数])
```

#### パラメーター

* n: 読み込むデーター件数を指定します。最新のn件のデーターが読み込まれます。
* skip: スキップ件数。最新からスキップ件のデーターを読み飛ばし、その先n件のデーターが読み込まれます。

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
d = am.read(date='YYYY-mm-dd')
```

#### パラメーター

* date='YYYY-mm-dd': 指定した日付のデーターを読み込みます。

#### 戻り値

件数を指定した場合と同じ辞書形式の配列が返されます。

### 期間を指定してデーターを読み込む

```python
d = am.read(start='YYYY-mm-dd HH:MM:SS', end='YYYY-mm-dd HH:MM:SS')
```

#### パラメーター

* start='YYYY-mm-dd HH:MM:SS':
* end='YYYY-mm-dd HH:MM:SS':
　startからendまでの期間のデーターを読み込みます。

#### 戻り値

件数を指定した場合と同じ辞書形式の配列が返されます。

## Example

examplesディレクトリーの下に例を置きました。

### hdc1000_example

hdc1000というセンサーで5分ごとに温度、湿度を測定し、Ambientに送信してグラフ化する例です。
