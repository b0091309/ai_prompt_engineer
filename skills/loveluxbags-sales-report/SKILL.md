---
name: loveluxbags-sales-report
description: 將 LoveLuxBags 銷售報表 Excel 檔案轉換為 Google Slides 簡報。當使用者需要整理月度銷售數據、分析銷售表現或製作銷售報告簡報時使用此 skill。觸發情境包括：「整理這個月的銷售報表」、「幫我做銷售簡報」、「分析銷售數據」等請求。
---

# LoveLuxBags 銷售報表轉 Google Slides

將 LoveLuxBags 的銷售報表 Excel 檔案解析並整理成專業的 Google Slides 簡報。

## 支援模式

### 模式一：單月報告
- 輸入：1 個 Excel 檔案
- 輸出：7 頁單月銷售報告

### 模式二：多月份比較報告
- 輸入：多個 Excel 檔案（不同月份）
- 輸出：8 頁多月份比較報告，包含月度趨勢和成長分析

## 資料來源格式

銷售報表 Excel 檔案的主要數據來自 **Order Details** 分頁：

### Order Details 欄位說明
| 欄位 | 說明 |
|------|------|
| Order No. | 訂單編號 |
| Order Date | 訂單日期 (格式: YYYYMMDD) |
| Account | 客戶帳號 |
| Item Name | 商品名稱 |
| Price | 銷售價格 |
| Cost | 成本 |
| Profit | 利潤 |
| Quantity | 數量 |
| Discount | 折扣 |
| Payment Method | 付款方式 |
| Recipient | 收件人 |
| Address | 地址 |
| Session | 直播場次 |
| Source of order | 訂單來源 (FB, TikTok, LINE 等) |

## Excel 解析方法

### 單一檔案解析

```python
import pandas as pd
import os
import re

def parse_single_file(file_path):
    """解析單一 Excel 檔案"""
    df = pd.read_excel(file_path, sheet_name='Order Details')

    # 從檔名提取月份
    filename = os.path.basename(file_path)
    date_match = re.search(r'(\d{4})-(\d{2})-\d{2}', filename)
    if date_match:
        year = date_match.group(1)
        month = date_match.group(2)
    else:
        year, month = "2025", "01"

    # 計算匯總數據
    summary = {
        'total_orders': len(df),
        'total_quantity': df['Quantity'].sum(),
        'total_price': df['Price'].sum(),
        'total_cost': df['Cost'].sum(),
        'total_profit': df['Profit'].sum(),
        'profit_rate': (df['Profit'].sum() / df['Price'].sum() * 100) if df['Price'].sum() > 0 else 0
    }

    # 商品銷售統計
    item_stats = df.groupby('Item Name').agg({
        'Quantity': 'sum',
        'Price': 'sum',
        'Profit': 'sum'
    }).reset_index()
    item_stats['Profit_Rate'] = (item_stats['Profit'] / item_stats['Price'] * 100).fillna(0)

    # 付款方式統計
    payment_stats = df.groupby('Payment Method').agg({
        'Order No.': 'count',
        'Price': 'sum'
    }).reset_index()
    payment_stats.columns = ['Payment Method', 'Order Count', 'Amount']

    # 訂單來源統計
    source_stats = df.groupby('Source of order').agg({
        'Order No.': 'count',
        'Price': 'sum'
    }).reset_index()
    source_stats.columns = ['Source', 'Order Count', 'Amount']

    # Session 統計
    session_stats = df.groupby('Session').agg({
        'Order No.': 'count',
        'Price': 'sum',
        'Profit': 'sum'
    }).reset_index()
    session_stats.columns = ['Session', 'Order Count', 'Amount', 'Profit']
    session_stats = session_stats.dropna(subset=['Session'])

    return {
        'year': year,
        'month': month,
        'month_name': f"{year} 年 {int(month)} 月",
        'orders_data': df,
        'summary': summary,
        'item_stats': item_stats,
        'payment_stats': payment_stats,
        'source_stats': source_stats,
        'session_stats': session_stats
    }
```

### 多檔案解析

```python
def parse_multiple_files(file_paths):
    """解析多個 Excel 檔案（多月份）"""
    monthly_data = []
    all_orders = []

    for f in file_paths:
        parsed = parse_single_file(f)
        monthly_data.append(parsed)
        parsed['orders_data']['Month'] = parsed['month_name']
        all_orders.append(parsed['orders_data'])

    # 按月份排序
    monthly_data.sort(key=lambda x: (x['year'], x['month']))

    # 合併所有訂單
    combined_df = pd.concat(all_orders, ignore_index=True)

    # 商品統計（合併所有月份）
    item_stats = combined_df.groupby('Item Name').agg({
        'Quantity': 'sum',
        'Price': 'sum',
        'Profit': 'sum'
    }).reset_index()
    item_stats['Profit_Rate'] = (item_stats['Profit'] / item_stats['Price'] * 100).fillna(0)

    # 付款方式統計
    payment_stats = combined_df.groupby('Payment Method').agg({
        'Order No.': 'count',
        'Price': 'sum'
    }).reset_index()
    payment_stats.columns = ['Payment Method', 'Order Count', 'Amount']

    # 訂單來源統計
    source_stats = combined_df.groupby('Source of order').agg({
        'Order No.': 'count',
        'Price': 'sum'
    }).reset_index()
    source_stats.columns = ['Source', 'Order Count', 'Amount']

    return {
        'monthly_data': monthly_data,
        'combined_df': combined_df,
        'item_stats': item_stats,
        'payment_stats': payment_stats,
        'source_stats': source_stats,
    }
```

## 簡報結構

### 單月報告 (7頁)

1. **封面** - 月份標題
2. **銷售總覽** - 6 個 KPI（訂單數、數量、金額、成本、利潤、利潤率）
3. **Top 10 熱銷商品** - 依數量排序
4. **Top 10 營收商品** - 依金額排序
5. **Top 10 獲利商品** - 含利潤率分析
6. **付款方式分析** - 各付款方式佔比
7. **訂單來源與場次分析** - FB/TikTok 來源 + 直播場次表現

### 多月份比較報告 (8頁)

1. **封面** - 日期範圍（如：2025 年 10月 - 12月）
2. **月度銷售總覽** - 4 個合計 KPI + 月度比較表格
3. **月度成長分析** - MoM 成長率（金額、訂單數）
4. **Top 10 熱銷商品** - 合併所有月份，依數量排序
5. **Top 10 營收商品** - 合併所有月份，依金額排序
6. **Top 10 獲利商品** - 合併所有月份，含利潤率
7. **付款方式分析** - 合計
8. **訂單來源分析** - 合計

## PowerPoint 生成

### 使用 python-pptx

```python
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def add_slide_title(slide, title_text):
    """添加投影片標題"""
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(12.333), Inches(0.8))
    title_para = title_box.text_frame.paragraphs[0]
    title_para.text = title_text
    title_para.font.size = Pt(36)
    title_para.font.bold = True

def create_kpi_card(slide, left, top, label, value, width=Inches(4), height=Inches(2)):
    """創建 KPI 卡片"""
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = RGBColor(255, 240, 245)  # 淺粉色背景
    shape.line.color.rgb = RGBColor(255, 182, 193)

    # 標籤
    label_box = slide.shapes.add_textbox(left, top + Inches(0.3), width, Inches(0.4))
    label_para = label_box.text_frame.paragraphs[0]
    label_para.text = label
    label_para.font.size = Pt(14)
    label_para.alignment = PP_ALIGN.CENTER

    # 數值
    value_box = slide.shapes.add_textbox(left, top + Inches(0.8), width, Inches(0.8))
    value_para = value_box.text_frame.paragraphs[0]
    value_para.text = value
    value_para.font.size = Pt(24)
    value_para.font.bold = True
    value_para.alignment = PP_ALIGN.CENTER
```

### 單月報告生成

```python
def create_single_month_presentation(data, output_path):
    """創建單月報告簡報"""
    prs = Presentation()
    prs.slide_width = Inches(13.333)  # 16:9
    prs.slide_height = Inches(7.5)
    slide_layout = prs.slide_layouts[6]  # 空白版面

    # 第1頁：封面
    slide = prs.slides.add_slide(slide_layout)
    # ... 封面內容

    # 第2頁：銷售總覽 (6 個 KPI)
    # 第3頁：Top 10 熱銷商品
    # 第4頁：Top 10 營收商品
    # 第5頁：Top 10 獲利商品
    # 第6頁：付款方式分析
    # 第7頁：訂單來源與場次分析

    prs.save(output_path)
```

### 多月份報告生成

```python
def create_multi_month_presentation(data, output_path):
    """創建多月份比較報告"""
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide_layout = prs.slide_layouts[6]

    monthly_data = data['monthly_data']
    months = [m['month_name'] for m in monthly_data]

    # 第1頁：封面（日期範圍）
    # 第2頁：月度銷售總覽 + 比較表格
    # 第3頁：月度成長分析（MoM）
    # 第4頁：Top 10 熱銷商品（合計）
    # 第5頁：Top 10 營收商品（合計）
    # 第6頁：Top 10 獲利商品（合計）
    # 第7頁：付款方式分析（合計）
    # 第8頁：訂單來源分析（合計）

    prs.save(output_path)
```

## 完整工作流程

```python
def main(file_paths, output_dir=None):
    """主程式：根據檔案數量自動選擇報告類型"""

    if isinstance(file_paths, str):
        file_paths = [file_paths]

    # 確定輸出目錄
    if output_dir is None:
        output_dir = os.path.dirname(file_paths[0])

    if len(file_paths) == 1:
        # 單月報告
        data = parse_single_file(file_paths[0])
        output_filename = f"LoveLuxBags_Sales_Report_{data['year']}{data['month']}.pptx"
        output_path = os.path.join(output_dir, output_filename)
        create_single_month_presentation(data, output_path)
    else:
        # 多月份報告
        data = parse_multiple_files(file_paths)
        months = [m['month'] for m in data['monthly_data']]
        year = data['monthly_data'][0]['year']
        output_filename = f"LoveLuxBags_Sales_Report_{year}_{months[0]}-{months[-1]}.pptx"
        output_path = os.path.join(output_dir, output_filename)
        create_multi_month_presentation(data, output_path)

    print(f"簡報已生成: {output_path}")
    return output_path
```

## 使用方式

### 單月報告
```
使用者提供 1 個 Excel 檔案
→ 解析 Order Details 分頁
→ 生成 7 頁單月報告
```

### 多月份報告
```
使用者提供多個 Excel 檔案（不同月份）
→ 解析所有檔案的 Order Details 分頁
→ 計算月度比較和成長率
→ 生成 8 頁多月份比較報告
```

## 輸出檔案

- 單月：`LoveLuxBags_Sales_Report_YYYYMM.pptx`
- 多月：`LoveLuxBags_Sales_Report_YYYY_MM-MM.pptx`
- 輸出位置：與原始 Excel 檔案相同目錄

## 依賴套件

```bash
pip install pandas openpyxl python-pptx
```

## 注意事項

1. Excel 檔案必須包含 **Order Details** 分頁
2. 多檔案會自動按月份排序
3. 月份從檔名中提取（格式：YYYY-MM-DD）
4. 生成的 .pptx 可直接上傳到 Google Drive，Google Slides 會自動轉換
