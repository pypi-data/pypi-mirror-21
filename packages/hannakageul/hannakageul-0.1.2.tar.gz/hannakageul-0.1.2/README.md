# Hannakageul

Hangeul - Kana encoding converter

## Features

* Web browser-like character encoding switch.
* Restore broken character. something like '궇궋궎궑궓' for 'あいうえお'

## Requirements

* Python 3

## Supported Encoding

* UTF-8
* EUC-CN
* EUC-JP
* EUC-KR(CP949)
* Shift-JIS
* JIS

## Usage

### EUC-CN to EUC-KR

<pre><code>
>>> hannakageul.convert.euccn.euckr('猫叉Master')
>>> '챔꿩Master'
</code></pre>


### Shift-JIS to EUC-KR

<pre><code>
>>> hannakageul.convert.sjis.euckr('佐竹美奈子')
>>> '뜴�|뷏볖럔'
</code></pre>


### EUC-KR to Shift-JIS

<pre><code>
>>> hannakageul.convert.euckr.sjis('뱦뺴Project')
>>> '東方Project'
</code></pre>

### UTF-8 to EUC-KR

<pre><code>
>>> hannakageul.convert.utf8.euckr('한나카글')
>>> '�븳�굹移닿��'
</code></pre>
