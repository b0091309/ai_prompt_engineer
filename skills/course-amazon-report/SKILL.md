---
name: course-amazon-report
description: 將課程資訊轉換為 Amazon 風格的6頁 PDF 報告。當使用者需要將課程大綱、課程內容或教學資料整理成專業的6頁簡報報告時使用此 skill。適用於任何需要製作課程介紹、課程提案或教學簡報的場景。
---

# 課程 Amazon 報告生成器

將課程資訊轉換為 Amazon 風格的6頁 PDF 報告，適合用於課程介紹和講述。

## 報告結構

Amazon 風格報告固定為6頁，每頁都有明確的目的和內容要求：

### 第1頁：為什麼要學（Why Learn）
**目的**：建立學習動機和緊迫感
**內容要求**：
- 標題：清晰點出課程主題
- 當前痛點：描述不學習此課程會面臨的問題或挑戰
- 市場趨勢：說明為何現在學習此主題特別重要
- 機會成本：不學習的代價
- 視覺元素：使用粗體強調關鍵痛點

### 第2頁：學了之後能解決什麼問題（What Problems Solved）
**目的**：展示課程的實際價值
**內容要求**：
- 3-5個具體的問題解決方案
- 每個解決方案包含：
  - 問題描述
  - 解決方式
  - 預期成果
- 使用編號列表呈現
- 強調可量化的成果（如果適用）

### 第3-6頁：課程內容（Course Content）
**目的**：展示課程架構和學習路徑
**內容靈活性**：第3-6頁的內容根據課程特性自由安排，可包含：
- 課程大綱與章節結構
- 核心概念和技能
- 學習成果與能力培養
- 實作項目或案例研究
- 課程特色與差異化優勢
- 適合對象與先備知識
- 學習時程與里程碑

**設計原則**：
- 每頁聚焦一個主題
- 使用清晰的標題
- 適當使用列表、表格或圖表
- 保持視覺一致性

## PDF 生成指南

### 使用 reportlab 創建專業 PDF

```python
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

# 註冊中文字體（使用系統內建字體）
pdfmetrics.registerFont(TTFont('NotoSans', '/System/Library/Fonts/Supplemental/Arial Unicode.ttf'))

# 創建文檔
doc = SimpleDocTemplate(
    "course_report.pdf",
    pagesize=letter,
    rightMargin=72,
    leftMargin=72,
    topMargin=72,
    bottomMargin=72
)

# 設定樣式（支援中文）
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(
    name='ChineseTitle',
    parent=styles['Heading1'],
    fontName='NotoSans',
    fontSize=24,
    textColor=colors.HexColor('#232F3E'),  # Amazon 深藍色
    spaceAfter=12,
    alignment=TA_CENTER
))

styles.add(ParagraphStyle(
    name='ChineseHeading',
    parent=styles['Heading2'],
    fontName='NotoSans',
    fontSize=16,
    textColor=colors.HexColor('#232F3E'),
    spaceAfter=10,
    spaceBefore=12
))

styles.add(ParagraphStyle(
    name='ChineseBody',
    parent=styles['Normal'],
    fontName='NotoSans',
    fontSize=11,
    leading=16,
    textColor=colors.HexColor('#000000'),
    alignment=TA_JUSTIFY
))

styles.add(ParagraphStyle(
    name='ChineseBullet',
    parent=styles['Normal'],
    fontName='NotoSans',
    fontSize=11,
    leading=16,
    leftIndent=20,
    bulletIndent=10
))
```

### 頁面編排技巧

**第1頁範例**：
```python
story = []

# 標題
title = Paragraph("為什麼要學習 [課程名稱]", styles['ChineseTitle'])
story.append(title)
story.append(Spacer(1, 0.3*inch))

# 痛點部分
heading = Paragraph("當前挑戰", styles['ChineseHeading'])
story.append(heading)

pain_points = [
    "痛點1的描述...",
    "痛點2的描述...",
    "痛點3的描述..."
]

for point in pain_points:
    p = Paragraph(f"• {point}", styles['ChineseBullet'])
    story.append(p)
    story.append(Spacer(1, 0.1*inch))

story.append(PageBreak())
```

**第2頁範例**：
```python
# 第2頁：解決方案
title2 = Paragraph("學了之後能解決什麼問題", styles['ChineseTitle'])
story.append(title2)
story.append(Spacer(1, 0.3*inch))

solutions = [
    {
        "problem": "問題1描述",
        "solution": "解決方式",
        "outcome": "預期成果"
    },
    # ... 更多解決方案
]

for i, sol in enumerate(solutions, 1):
    heading = Paragraph(f"{i}. {sol['problem']}", styles['ChineseHeading'])
    story.append(heading)
    
    body = Paragraph(f"<b>解決方式：</b>{sol['solution']}", styles['ChineseBody'])
    story.append(body)
    story.append(Spacer(1, 0.1*inch))
    
    outcome = Paragraph(f"<b>預期成果：</b>{sol['outcome']}", styles['ChineseBody'])
    story.append(outcome)
    story.append(Spacer(1, 0.2*inch))

story.append(PageBreak())
```

### 視覺元素

**使用表格**：
```python
data = [
    ['章節', '主題', '時長'],
    ['第一章', '基礎概念', '2小時'],
    ['第二章', '進階技巧', '3小時'],
]

table = Table(data, colWidths=[1.5*inch, 3*inch, 1.5*inch])
table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#FF9900')),  # Amazon 橘色
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, 0), 'NotoSans'),
    ('FONTSIZE', (0, 0), (-1, 0), 12),
    ('FONTNAME', (0, 1), (-1, -1), 'NotoSans'),
    ('FONTSIZE', (0, 1), (-1, -1), 10),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('GRID', (0, 0), (-1, -1), 1, colors.grey),
]))
story.append(table)
```

**Amazon 品牌色彩**：
- 主色：`#232F3E`（深藍）
- 強調色：`#FF9900`（橘色）
- 輔助色：`#146EB4`（亮藍）

### 最終生成

```python
# 建立 PDF
doc.build(story)
```

## 工作流程

1. **接收課程資訊**：從使用者提供的課程大綱、文件或描述中提取資訊
2. **結構化內容**：
   - 分析課程資訊
   - 提取關鍵學習動機（第1頁）
   - 識別問題解決方案（第2頁）
   - 組織課程內容（第3-6頁）
3. **生成 PDF**：
   - 使用 reportlab 創建6頁文檔
   - 應用 Amazon 風格設計
   - 確保中文字體正確顯示
4. **輸出檔案**：將完成的 PDF 存檔到 `/mnt/user-data/outputs/`

## 品質檢查

生成報告前確認：
- ✓ 第1頁清楚說明「為什麼要學」
- ✓ 第2頁列出具體的「問題解決方案」
- ✓ 總共6頁（不多不少）
- ✓ 每頁都有清晰的標題
- ✓ 中文字體正確顯示
- ✓ 視覺元素使用 Amazon 品牌色
- ✓ 內容編排專業、易讀
