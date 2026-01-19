---
name: live-sales-inventory-excel-to-pdf
description: 將直播庫存 Excel 檔案轉換為直播用的 PDF 檔案，只保留 Item、Ref Qty.、Sale Price、Keyword 四個欄位。當使用者說「請幫我把直播excel 轉成直播用的pdf」或類似請求時使用此 skill。觸發情境包括：「轉成直播用的pdf」、「直播excel轉pdf」、「庫存報表轉pdf」等請求。
---

# 直播庫存 Excel 轉 PDF

將直播的庫存報表 Excel 檔案轉換為簡潔的 PDF，只保留直播需要的四個欄位。

## 輸入格式

Excel 檔案名稱格式：`Inventory Report YYYY-MM-DD.xlsx`

### 欄位結構（header 在第 3 行，即 header=2）

| 欄位 | 說明 |
|------|------|
| Item | 商品名稱 |
| Ref Qty. | 庫存數量 |
| Sale Price | 售價 |
| Keyword | 關鍵字編號 |

## 輸出格式

- 格式：PDF
- 欄位：Item, Ref Qty., Sale Price, Keyword
- 行高：30
- 樣式：藍色標題列、交替行背景色
- 輸出位置：`/mnt/user-data/outputs/`
- 檔名：與原始 Excel 相同，副檔名改為 .pdf

## 完整 Python 程式碼

```python
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
import os

def convert_inventory_to_pdf(excel_path):
    """將庫存 Excel 轉換為直播用 PDF"""

    # 讀取 Excel，header 在第 3 行
    df = pd.read_excel(excel_path, header=2)

    # 選取需要的欄位
    selected_columns = ['Item', 'Ref Qty.', 'Sale Price', 'Keyword']
    df_selected = df[selected_columns].copy()

    # 清理資料，移除空行
    df_selected = df_selected.dropna(subset=['Item'])

    # 設定輸出路徑
    filename = os.path.basename(excel_path)
    base_name = os.path.splitext(filename)[0]
    output_path = f'/mnt/user-data/outputs/{base_name}.pdf'

    # 建立 PDF
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=30,
        leftMargin=30,
        topMargin=30,
        bottomMargin=30
    )

    elements = []

    # 標題
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=20,
        alignment=1  # 置中
    )

    title = Paragraph(base_name, title_style)
    elements.append(title)
    elements.append(Spacer(1, 12))

    # 準備表格資料
    table_data = [selected_columns]  # 標題行
    for _, row in df_selected.iterrows():
        table_data.append([
            str(row['Item']) if pd.notna(row['Item']) else '',
            str(int(row['Ref Qty.'])) if pd.notna(row['Ref Qty.']) else '',
            str(int(row['Sale Price'])) if pd.notna(row['Sale Price']) else '',
            str(row['Keyword']) if pd.notna(row['Keyword']) else ''
        ])

    # 建立表格，行高設為 30
    col_widths = [250, 60, 70, 60]
    row_heights = [30] * len(table_data)
    table = Table(table_data, colWidths=col_widths, rowHeights=row_heights)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4472C4')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('ALIGN', (1, 0), (3, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#E8F0FE')]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))

    elements.append(table)

    # 建立 PDF
    doc.build(elements)

    print(f"PDF 已成功建立：{output_path}")
    print(f"共 {len(df_selected)} 筆資料")

    return output_path
```

## 執行步驟

1. 確認 Excel 檔案在 `/mnt/user-data/uploads/` 目錄
2. 安裝依賴套件：`pip install pandas openpyxl reportlab --break-system-packages`
3. 執行轉換函數：`convert_inventory_to_pdf(excel_path)`
4. PDF 會儲存在 `/mnt/user-data/outputs/` 目錄

## 注意事項

1. Excel 檔案的欄位標題在第 3 行（header=2）
2. 會自動過濾掉 Item 欄位為空的行
3. 數值欄位（Ref Qty.、Sale Price）會轉為整數顯示
4. 輸出檔案統一存放在 outputs 目錄，方便使用者下載
