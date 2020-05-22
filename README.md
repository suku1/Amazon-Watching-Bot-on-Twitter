# Amazon-Watching-Bot-on-Twitter
OculusRiftS入荷情報bot
https://twitter.com/oculusrifts_bot  
の中身です.  
試してはいませんが, URLとか価格とか書き換えると他の商品にも使えると思います. 

**価格取得時にエラーが出てしまう場合, UAを書き換えることで解消する可能性があります.**  
**任意のブラウザでAmazonにアクセスし正常につながることを確認した後, bot.pyのUAをそのブラウザのものに書き換えてみてください.**  

## Requires  
**使用モジュール**  
 - Requests
```bash
$ pip install requests
```
 - BeautifulSoup4
```bash
$ pip install bs4
```
 - lxml
```bash
$ pip install lxml
```
 - requests_oauthlib
```bash
$ pip install requests_oauthlib
```

## Usage  
APIkey.jsonにTwitterAPIのkeyを設定すれば動きます.  
```bash
$ python bot.py
```

## Licence

MIT

## Author

[sksim](https://github.com/suku1)
