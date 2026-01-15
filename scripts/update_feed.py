import feedparser
import json
import os
from datetime import datetime
import pytz

# 这里配置你的 RSS 源地址
# 你需要把之前 JS 里用的 RSS 地址填到这里对应的位置
RSS_SOURCES = {
    "policy": [
        "https://feedx.net/rss/caixin/finance.xml", # 示例，请替换为你原来的政策法规 RSS
    ],
    "mergers": [
        "https://rsshub.app/36kr/newsflashes", # 示例，请替换为你原来的收并购 RSS
    ],
    "companies": {
        "huace": "https://rsshub.app/xueqiu/user/8566580983", # 华测检测 (示例)
        "guangdian": "https://rsshub.app/xueqiu/user/12345678", # 广电计量 (请替换)
        "sushi": "https://rsshub.app/xueqiu/user/12345678", # 苏试试验 (请替换)
        "anche": "https://rsshub.app/xueqiu/user/12345678"  # 安车检测 (请替换)
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
