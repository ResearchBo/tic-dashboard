import feedparser
import json
import os
from datetime import datetime
import time

# 辅助函数：生成 Google News 搜索链接（限定最近 3 个月，中文结果）
def make_url(keyword):
    base = "https://news.google.com/rss/search"
    # q=关键词 when:90d (最近90天)
    # hl=zh-CN (语言)
    query = f"{keyword} when:90d"
    return f"{base}?hl=zh-CN&gl=CN&ceid=CN:zh-Hans&q={query}"

RSS_SOURCES = {
    # 1. 政策与法规 (增加到 100 条)
    "policy": make_url("检验检测 政策"),

    # 2. 行业与收并购 (增加到 100 条)
    "mergers": make_url("检验检测 收并购"),

    # 3. 海外上市公司 (新增板块)
    "companies_overseas": {
        "SGS": make_url("SGS 检测"),
        "必维国际 (BV)": make_url("必维集团"), # Bureau Veritas
        "欧陆科技 (Eurofins)": make_url("欧陆检测"),
        "天祥集团 (Intertek)": make_url("Intertek 天祥"),
    },

    # 4. 国内上市公司 (扩充至 ~20 家)
    "companies_domestic": {
        "华测检测": make_url("华测检测"),
        "广电计量": make_url("广电计量"),
        "苏试试验": make_url("苏试试验"),
        "安车检测": make_url("安车检测"),
        "谱尼测试": make_url("谱尼测试"),
        "信测标准": make_url("信测标准"),
        "国检集团": make_url("国检集团"),
        "钢研纳克": make_url("钢研纳克"),
        "实朴检测": make_url("实朴检测"),
        "电科院": make_url("苏州电科院"),
        "中国汽研": make_url("中国汽研"),
        "垒知集团": make_url("垒知集团"),
        "建科股份": make_url("建科股份"),
        "迪安诊断": make_url("迪安诊断"), # 医学检测巨头
        "金域医学": make_url("金域医学"), # 医学检测巨头
        "凯普生物": make_url("凯普生物"),
        "达安基因": make_url("达安基因"),
        "优利德": make_url("优利德"), # 测量仪器
        "东方中科": make_url("东方中科"),
        "西测测试": make_url("西测测试"),
    }
}

def parse_date(entry):
    # 尝试解析 RSS 的时间，用于后续排序
    # Google News 通常返回 published_parsed (struct_time)
    if hasattr(entry, 'published_parsed') and entry.published_parsed:
        return entry.published_parsed
    return time.localtime(0) # 如果没有时间，放到最后

def fetch_feed(url, limit=100):
    """
    抓取 RSS 并按时间倒序排列
    limit: 默认 100 条
    """
    try:
        print(f"正在抓取: {url} ...")
        feed = feedparser.parse(url)
        entries = []
        
        # 提取数据
        for entry in feed.entries:
            entries.append({
                "title": entry.title,
                "link": entry.link,
                "published": entry.get("published", "未知时间"),
                "published_parsed": parse_date(entry), # 临时字段，用于排序
                "summary": entry.get("summary", "")
            })
        
        # 按时间倒序排序 (最新的在最前)
        entries.sort(key=lambda x: x['published_parsed'], reverse=True)
        
        # 删除临时排序字段，只保留前 limit 条
        for e in entries:
            del e['published_parsed']
            
        return entries[:limit]
        
    except Exception as e:
        print(f"抓取失败 {url}: {e}")
        return []

def main():
    final_data = {
        "update_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "policy": [],
        "mergers": [],
        "companies_overseas": {},
        "companies_domestic": {}
    }

    # 1. 抓取政策
    final_data["policy"] = fetch_feed(RSS_SOURCES["policy"], limit=100)

    # 2. 抓取收并购
    final_data["mergers"] = fetch_feed(RSS_SOURCES["mergers"], limit=100)

    # 3. 抓取海外公司
    for name, url in RSS_SOURCES["companies_overseas"].items():
        # 公司新闻不需要 100 条那么多，保持 10 条精华即可，避免页面太长
        final_data["companies_overseas"][name] = fetch_feed(url, limit=10)

    # 4. 抓取国内公司
    for name, url in RSS_SOURCES["companies_domestic"].items():
        final_data["companies_domestic"][name] = fetch_feed(url, limit=10)

    # 保存
    with open('news_data.json', 'w', encoding='utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, indent=2)
    
    print(f"更新完成！国内公司: {len(final_data['companies_domestic'])}, 海外公司: {len(final_data['companies_overseas'])}")

if __name__ == "__main__":
    main()
