import feedparser
import json
import os
from datetime import datetime
import pytz

# 这里配置你的 RSS 源地址
# 基于你 index.html 中的关键词生成的 Google News 搜索链接
RSS_SOURCES = {
    "policy": [
        # 关键词：检验检测 政策
        "https://news.google.com/rss/search?hl=zh-CN&gl=CN&ceid=CN:zh-Hans&q=%E6%A3%80%E9%AA%8C%E6%A3%80%E6%B5%8B+%E6%94%BF%E7%AD%96"
    ],
    "mergers": [
        # 关键词：检验检测 收并购
        "https://news.google.com/rss/search?hl=zh-CN&gl=CN&ceid=CN:zh-Hans&q=%E6%A3%80%E9%AA%8C%E6%A3%80%E6%B5%8B+%E6%94%B6%E5%B9%B6%E8%B4%AD"
    ],
    "companies": {
        # 关键词：华测检测
        "huace": "https://news.google.com/rss/search?hl=zh-CN&gl=CN&ceid=CN:zh-Hans&q=%E5%8D%8E%E6%B5%8B%E6%A3%80%E6%B5%8B",
        # 关键词：广电计量
        "guangdian": "https://news.google.com/rss/search?hl=zh-CN&gl=CN&ceid=CN:zh-Hans&q=%E5%B9%BF%E7%94%B5%E8%AE%A1%E9%87%8F",
        # 关键词：苏试试验
        "sushi": "https://news.google.com/rss/search?hl=zh-CN&gl=CN&ceid=CN:zh-Hans&q=%E8%8B%8F%E8%AF%95%E8%AF%95%E9%AA%8C",
        # 关键词：安车检测
        "anche": "https://news.google.com/rss/search?hl=zh-CN&gl=CN&ceid=CN:zh-Hans&q=%E5%AE%89%E8%BD%A6%E6%A3%80%E6%B5%8B"
    }
}

def fetch_feed(url):
    try:
        print(f"正在抓取: {url}")
        feed = feedparser.parse(url)
        entries = []
        for entry in feed.entries[:5]: # 每个源只取前5条，防止太多
            entries.append({
                "title": entry.title,
                "link": entry.link,
                "published": entry.get("published", entry.get("updated", "未知时间")),
                "summary": entry.get("summary", "")[:100] + "..." # 只取摘要前100字
            })
        return entries
    except Exception as e:
        print(f"抓取失败 {url}: {e}")
        return []

def main():
    final_data = {
        "update_time": datetime.now(pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S'),
        "policy": [],
        "mergers": [],
        "companies": {}
    }

    # 1. 抓取政策
    for url in RSS_SOURCES["policy"]:
        final_data["policy"].extend(fetch_feed(url))

    # 2. 抓取收并购
    for url in RSS_SOURCES["mergers"]:
        final_data["mergers"].extend(fetch_feed(url))

    # 3. 抓取公司
    for name, url in RSS_SOURCES["companies"].items():
        final_data["companies"][name] = fetch_feed(url)

    # 保存为 json 文件
    # 存放在根目录，方便网页读取
    with open('news_data.json', 'w', encoding='utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, indent=2)
    
    print("数据更新完成！")

if __name__ == "__main__":
    main()
