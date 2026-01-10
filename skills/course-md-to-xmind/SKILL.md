---
name: course-md-to-xmind
description: 將課程 Markdown 檔案轉換為 XMind 心智圖格式。當使用者需要將課程大綱、課程內容或教學資料轉換為視覺化的心智圖時使用此 skill。觸發情境包括：「把這個課程 MD 轉成心智圖」、「製作課程的 XMind 檔案」、「將課程大綱轉成 XMind」、「生成課程心智圖」等請求。
---

# Course Markdown to XMind Converter

將課程的 Markdown 檔案轉換為 XMind 心智圖格式，方便視覺化呈現課程結構。

## 核心功能

- 自動解析 Markdown 標題層級（# ## ### 等）
- 將課程名稱設為心智圖中心主題
- 各章節轉換為主要分支
- 子章節自動建立為次級分支
- 保留完整的課程內容在各節點的備註中

## 使用方式

### 基本用法

當使用者提供課程 Markdown 檔案並要求轉換為心智圖時：

1. 確認 Markdown 檔案位置（通常在 `/mnt/user-data/uploads/`）
2. 執行轉換腳本：

```bash
python /mnt/skills/user/course-md-to-xmind/scripts/md_to_xmind.py <markdown_file_path> <output_file_path>
```

3. 將生成的 `.xmind` 檔案移動到 `/mnt/user-data/outputs/` 以便使用者下載

### 範例

```bash
# 轉換課程檔案
python /mnt/skills/user/course-md-to-xmind/scripts/md_to_xmind.py \
  /mnt/user-data/uploads/課程大綱.md \
  /home/claude/課程心智圖.xmind

# 移動到輸出目錄
mv /home/claude/課程心智圖.xmind /mnt/user-data/outputs/
```

## 支援的 Markdown 結構

腳本會自動識別以下結構：

- `#` - 課程主標題（作為中心主題）
- `##` - 章節（第一層分支）
- `###` - 子章節（第二層分支）
- `####` 及更深層級 - 繼續建立次級分支

**重要**：所有非標題內容（段落、列表、程式碼等）會被保留在對應節點的備註欄位中。

## 輸出格式

- 檔案格式：`.xmind`（XMind 8 相容格式）
- 編碼：UTF-8
- 結構：以 ZIP 格式包含 XML 檔案
- 可用軟體：XMind、XMind ZEN、FreeMind 等心智圖軟體

## 工作流程建議

1. **接收檔案**：確認使用者上傳的 MD 檔案
2. **執行轉換**：使用腳本將 MD 轉為 XMind
3. **提供檔案**：將結果移至輸出目錄並使用 `present_files` 工具分享給使用者
4. **簡潔說明**：告知使用者檔案已準備好，可以用 XMind 開啟

## 注意事項

- 腳本會自動處理中文檔名
- 如果沒有指定輸出檔名，會使用輸入檔案的名稱並加上 `.xmind` 副檔名
- 生成的心智圖以課程主標題（第一個 `#` 標題）作為中心主題
- 所有內容細節都會保存在節點的備註中，不會遺失資訊
