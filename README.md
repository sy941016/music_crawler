# music_crawler

基于 [Scrapy](https://scrapy.org/) 框架构建的咪咕音乐歌曲信息爬虫，用于抓取指定歌手的歌曲名称与风格/流派数据，结果以 JSON 格式持久化输出。

---

## 功能特性

- 自动遍历咪咕音乐搜索结果的所有分页
- 提取每首歌曲的名称（`name`）与风格/流派（`genre`）
- 搜索关键词可通过命令行参数灵活指定
- 结果自动写入 `output/<spider_name>.json`
- 启用 AutoThrottle 自动限速，避免对目标服务器造成过大压力

---

## 项目结构

```
music_crawler/
├── music_pachong/
│   ├── items/
│   │   └── SongType.py       # Item 数据模型（SongItem）
│   ├── spiders/
│   │   └── music.py          # 核心爬虫（MiguMusicSpider）
│   ├── pipelines.py          # JSON 文件输出 Pipeline
│   ├── middlewares.py        # 中间件（预留）
│   └── settings.py           # 项目配置
├── begin.py                  # 快捷启动脚本
└── scrapy.cfg
```

---

## 环境依赖

- Python >= 3.9
- Scrapy >= 2.11

安装依赖：

```bash
pip install scrapy
```

---

## 快速开始

### 方式一：命令行

```bash
# 爬取默认关键词（周杰伦）
scrapy crawl music

# 指定其他歌手
scrapy crawl music -a query=林俊杰
```

### 方式二：Python 脚本

```bash
python begin.py
```

---

## 输出格式

爬取完成后，结果保存至 `output/music.json`，格式示例：

```json
[
{"name": "稻香", "genre": ["华语流行"]},
{"name": "青花瓷", "genre": ["中国风"]}
]
```

---

## 配置说明

核心配置项位于 [`music_pachong/settings.py`](music_pachong/settings.py)：

| 配置项 | 默认值 | 说明 |
|---|---|---|
| `CONCURRENT_REQUESTS` | 8 | 最大并发请求数 |
| `DOWNLOAD_DELAY` | 1 | 请求间隔（秒） |
| `AUTOTHROTTLE_ENABLED` | True | 自动限速开关 |
| `COOKIES_ENABLED` | False | 是否启用 Cookie |

---

## 注意事项

- 本项目仅供学习与技术研究，请勿用于商业用途。
- 爬取前请确认目标网站的服务条款，遵守相关法律法规。
- 网站页面结构变更后，XPath 选择器可能需要同步更新。
