# pixiv-rank

## 说明

本项目引入了AI对原代码进行了重构（翻译成人话就是代码基本上都是AI重新写的我试了下能跑通就传上来了），提高了代码的可读性（也许吧），并对原代码进行了精简（这个确实是）。

## 安装第三方依赖

```bash
pip install -r requirements.txt
```

## 获取REFRESH_TOKEN

[@ZipFile Pixiv OAuth Flow](https://gist.github.com/ZipFile/c9ebedb224406f4f11845ab700124362) 或 [OAuth with Selenium/ChromeDriver](https://gist.github.com/upbit/6edda27cb1644e94183291109b8a5fde)

## 修改REFRESH_TOKEN

```bash
vim rank.py

REFRESH_TOKEN = "YOUR TOKEN"
```

## 运行

```bash
python3 rank.py
```

## 致谢

Pixiv API: [PixivPy](https://github.com/upbit/pixivpy)
AI: [Google AI Studio](https://aistudio.google.com)
