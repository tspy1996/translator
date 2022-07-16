Steps Record

#### 下載python，套件
```
sudo apt update

sudo apt install python3-pip

sudo apt-get install git -y

cd execute
```
* argo
```
git clone https://github.com/argosopentech/argos-translate.git
cd argos-translate
pip install -e .
```
* openCC, streamlit
```
pip install opencc-python-reimplemented
pip install streamlit==1.10.0
```
* solve "bash: streamlit: command not found"
WARNING: The script _ is installed in '/home/cleotsai/.local/bin' which is not on PATH.
    ```
    export PATH="/usr/local/bin:$PATH"
    source ~/.bash_profile
    ```

#### Install all language packages
1.
```bash
argospm update
```
2. 
```bash
for i in $(argospm search | sed 's/:.*$//g'); do argospm install $i ; done
```

#### Run streamlit.py
```
cd execute
streamlit run Translator.py
```

#### 測試文本
```
# en -> zh
I am R.O.C. national and represent our country to have a meeting with Scottish Council for Development and Industry. Both of us are willing to sign a treaty about following the rule of regional economic integration organization.
# terms: 中華民國國民 蘇格蘭工業發展協進會 簽署條約 區域經濟整合組織

# ja -> zh 1
1995年に放送を開始した「映像の世紀」の新シリーズ。チョウの羽ばたきのような、一人一人のささやかな営みが、いかに連鎖し、世界を動かしていくのか？　世界各国から収集した貴重なアーカイブス映像をもとに、人類の歴史に秘められた壮大なバタフライエフェクトの世界をお届けする。

    # google translate
    1995年開始播出的新系列“電影世紀”。 每個人的小活動，如蝴蝶的拍動，如何連鎖和移動世界？ 基於從世界各地收集的珍貴檔案視頻，我們將傳遞隱藏在人類歷史中的壯麗蝴蝶效應世界。
    # argo time=3.6
    1995年開始廣播的一批新世紀。 你如何連接和移防，調動，運動世界? 基於所有遠彈，請回答(通信電語)的寶貴檔案 世界,投放，交貨，運送，釋放，傳達，交付，發射人類歷史上所隱藏但暗淡的影響的世界。
----
# ja -> zh 2
安倍元総理大臣が奈良市で演説中に銃で撃たれ死亡した事件で、逮捕された容疑者は「火薬はネットで購入した」と供述していることが分かりました。事件で使用した手製の銃についても、インターネット上の動画を参考に製造したという趣旨の供述をしているということで警察は詳しいいきさつを調べています。
安倍元総理大臣は今月8日、奈良市の大和西大寺駅近くで演説中に銃で撃たれて死亡し、警察は奈良市に住む無職の山上徹也容疑者（41）を逮捕して殺人の疑いで捜査しています。
    
    # google translate
    前首相安倍晉三在奈良市發表演講時被槍殺，被捕嫌疑人稱自己“在網上購買了火藥”。 警方正在調查案件中使用的手工槍的細節，稱它是參考網上的視頻製作的。
    本月8日，前首相安倍晉三在奈良市大和西大寺站附近發表演講時被槍擊身亡，警方逮捕了居住在奈良市並涉嫌謀殺的失業人員山神哲也（41歲）。正在調查。

    # agro time:4.85
    在旗套，事件，實例，彈殼，大箱年裏,總理 在納拉市的演說中,一名涉嫌人說,“毒品是網上購買的”。 火砲，加農砲審查了該案件使用的手槍的詳細想法,以及網上製作錄像的目的。 本月8日,總理 在納拉市的山多託·尼希達伊吉站附近,可能死亡。 內務巡視，整理內務，整頓，內務值勤人員，警察逮捕Tetsuya Yamagami(41),他是Nara市的一個沒有理由,並受到謀殺的調查。

--
# ru to zh
Сам Яшин находится в спецприемнике в районе Мневники. Политика задержали в ночь на 28 июня в парке у Новодевичьего монастыря. Сотрудники МВД указали в рапорте, что депутат «хватал их за форму, оскорблял, грязно ругался и толкал, всячески провоцируя драку». Поводом для задержания депутата стала некая «ориентировка по уголовному делу», однако ее к делу не приобщили.

# argo
Yashin本人是Divnik面積，區域，空軍器材區，範圍號特殊接受者。 6月28日夜間,在諾沃傑·莫蒂拉斯舉行了政治儀式。 內務部官員在停機坪，汽車場，停放，停置，集中停放年指出,報告，報到，告發，爆聲人讚揚他們穿制服,侮辱他們,通過副職把他們趕出所有,戰鬥的理由是有些拘留的刑事指導,但她沒有受到審判。

# google
Yashin本人在Mnevniki地區的一個特殊拘留中心。 這位政治家於 6 月 28 日晚在新聖女修道院附近的公園被拘留。 內政部工作人員在報告中表示，該副手“抓著他們的製服、侮辱他們、髒話、推搡，千方百計挑起鬥毆”。 副手被拘留的原因是某種“刑事案件取向”，但與案件無關。

```