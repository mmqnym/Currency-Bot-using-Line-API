# Line Currency Bot
> 此機器人主要提供匯率轉換功能，使用的是台灣銀行資料，以thread方式每2小時更新。

<br />

## Demo

### 主頁
![info](doc/info.jpg)

<br />

### 聊天室
![help](doc/help.jpg)

<br />

### 天氣
![info](doc/info.jpg)

<br />

### 筆記本
![info](doc/nute.jpg)

<br />

### 匯率功能
![demo](https://user-images.githubusercontent.com/102388049/182193626-9ce0acca-a9ff-43ea-8826-c1fe43c1f7d9.mp4)

<br />

## Set up

``` sh
pip install -r requirements.txt
```

其餘步驟請參考[Line Bot 教學](https://www.learncodewithmike.com/2020/06/python-line-bot.html)，因為還需要API KEY、Webhook URL、Secret KEY...等，內有詳細建置說明。

<br />

## Room for Improvement
> 將原本的同步伺服器架構改為非同步。

開發此機器人時，本人還是個python初學者，現在有能力將機器人改以非同步的架構運行，使用者可以考慮更改架構以促進效能，特別是爬蟲改以[pyppeteer](https://github.com/pyppeteer/pyppeteer)運行能大幅提高速度，前提是必須使用非同步伺服器架構。

<br />

## Reference

- ##### [Line Bot 教學](https://www.learncodewithmike.com/2020/06/python-line-bot.html)
- ##### [Django](https://github.com/django/django)

<br />

## License

[MIT](LICENSE)
