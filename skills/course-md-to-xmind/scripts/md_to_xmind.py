#!/usr/bin/env python3
"""
將課程 Markdown 檔案轉換為 XMind 心智圖

XMind 格式說明：
- XMind 8 使用 .xmind 格式（實際上是一個 zip 檔案）
- 內含 content.xml（心智圖結構）和 meta.xml（元數據）
"""

import re
import zipfile
import os
import sys
from datetime import datetime
from xml.etree import ElementTree as ET
from xml.dom import minidom


def parse_markdown(md_content):
    """
    解析 Markdown 內容，提取標題層級和內容
    
    返回格式：
    {
        'title': '課程名稱',
        'chapters': [
            {
                'title': '章節標題',
                'level': 2,
                'content': '章節內容',
                'subsections': [...]
            }
        ]
    }
    """
    lines = md_content.split('\n')
    
    # 提取主標題（第一個 # 標題）
    main_title = None
    for line in lines:
        if line.startswith('# '):
            main_title = line[2:].strip()
            break
    
    if not main_title:
        main_title = "課程心智圖"
    
    # 解析所有標題
    structure = {'title': main_title, 'chapters': []}
    current_chapter = None
    current_section = None
    current_content = []
    
    for line in lines:
        # 檢查是否為標題
        heading_match = re.match(r'^(#{1,6})\s+(.+)$', line)
        
        if heading_match:
            level = len(heading_match.group(1))
            title = heading_match.group(2).strip()
            
            # 儲存之前的內容
            if current_section:
                current_section['content'] = '\n'.join(current_content).strip()
                current_content = []
            elif current_chapter and level == 2:
                current_chapter['content'] = '\n'.join(current_content).strip()
                current_content = []
            
            if level == 1:
                # 主標題已經處理過
                continue
            elif level == 2:
                # 新章節
                current_chapter = {
                    'title': title,
                    'level': level,
                    'content': '',
                    'subsections': []
                }
                structure['chapters'].append(current_chapter)
                current_section = None
            elif level >= 3 and current_chapter:
                # 子章節
                current_section = {
                    'title': title,
                    'level': level,
                    'content': '',
                    'subsections': []
                }
                current_chapter['subsections'].append(current_section)
        else:
            # 非標題行，加入內容
            if line.strip():
                current_content.append(line)
    
    # 儲存最後的內容
    if current_section:
        current_section['content'] = '\n'.join(current_content).strip()
    elif current_chapter:
        current_chapter['content'] = '\n'.join(current_content).strip()
    
    return structure


def create_topic_element(topic_id, title, content=''):
    """創建一個 XMind topic 元素"""
    topic = ET.Element('topic', {
        'id': topic_id,
        'timestamp': str(int(datetime.now().timestamp() * 1000))
    })
    
    # 標題
    title_elem = ET.SubElement(topic, 'title')
    title_elem.text = title
    
    # 如果有內容，加入備註
    if content:
        notes = ET.SubElement(topic, 'notes')
        plain = ET.SubElement(notes, 'plain')
        plain.text = content
    
    children = ET.SubElement(topic, 'children')
    topics = ET.SubElement(children, 'topics', {'type': 'attached'})
    
    return topic, topics


def build_xmind_tree(structure):
    """根據解析的結構建立 XMind XML 樹"""
    # 建立根元素
    xmap_content = ET.Element('xmap-content', {
        'xmlns': 'urn:xmind:xmap:xmlns:content:2.0',
        'xmlns:fo': 'http://www.w3.org/1999/XSL/Format',
        'xmlns:svg': 'http://www.w3.org/2000/svg',
        'xmlns:xhtml': 'http://www.w3.org/1999/xhtml',
        'xmlns:xlink': 'http://www.w3.org/1999/xlink',
        'version': '2.0'
    })
    
    sheet = ET.SubElement(xmap_content, 'sheet', {
        'id': 'sheet1',
        'timestamp': str(int(datetime.now().timestamp() * 1000))
    })
    
    # 中心主題
    root_topic, root_topics = create_topic_element('root', structure['title'])
    sheet.append(root_topic)
    
    topic_id_counter = 1
    
    # 添加章節
    for chapter in structure['chapters']:
        chapter_id = f'topic{topic_id_counter}'
        topic_id_counter += 1
        
        chapter_topic, chapter_topics = create_topic_element(
            chapter_id, 
            chapter['title'],
            chapter['content']
        )
        root_topics.append(chapter_topic)
        
        # 添加子章節
        for subsection in chapter['subsections']:
            subsection_id = f'topic{topic_id_counter}'
            topic_id_counter += 1
            
            subsection_topic, subsection_topics = create_topic_element(
                subsection_id,
                subsection['title'],
                subsection['content']
            )
            chapter_topics.append(subsection_topic)
            
            # 添加更深層的子章節（如果有的話）
            for subsubsection in subsection.get('subsections', []):
                subsubsection_id = f'topic{topic_id_counter}'
                topic_id_counter += 1
                
                subsubsection_topic, _ = create_topic_element(
                    subsubsection_id,
                    subsubsection['title'],
                    subsubsection['content']
                )
                subsection_topics.append(subsubsection_topic)
    
    return xmap_content


def prettify_xml(elem):
    """格式化 XML 輸出"""
    rough_string = ET.tostring(elem, encoding='utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent='  ', encoding='utf-8')


def create_meta_xml():
    """創建 meta.xml 檔案"""
    meta = ET.Element('meta', {
        'xmlns': 'urn:xmind:xmap:xmlns:meta:2.0',
        'version': '2.0'
    })
    
    # 添加創建者資訊
    ET.SubElement(meta, 'Author').text = 'Claude'
    ET.SubElement(meta, 'Create').text = datetime.now().isoformat()
    
    return prettify_xml(meta)


def create_manifest_xml():
    """創建 manifest.xml 檔案"""
    manifest = ET.Element('manifest', {
        'xmlns': 'urn:xmind:xmap:xmlns:manifest:1.0'
    })
    
    # 添加檔案條目
    ET.SubElement(manifest, 'file-entry', {
        'full-path': 'content.xml',
        'media-type': 'text/xml'
    })
    
    ET.SubElement(manifest, 'file-entry', {
        'full-path': 'META-INF/',
        'media-type': ''
    })
    
    ET.SubElement(manifest, 'file-entry', {
        'full-path': 'META-INF/manifest.xml',
        'media-type': 'text/xml'
    })
    
    ET.SubElement(manifest, 'file-entry', {
        'full-path': 'meta.xml',
        'media-type': 'text/xml'
    })
    
    return prettify_xml(manifest)


def md_to_xmind(md_file_path, output_path=None):
    """
    將 Markdown 檔案轉換為 XMind 格式
    
    Args:
        md_file_path: Markdown 檔案路徑
        output_path: 輸出的 .xmind 檔案路徑（可選）
    
    Returns:
        輸出檔案的路徑
    """
    # 讀取 Markdown 檔案
    with open(md_file_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # 解析 Markdown
    structure = parse_markdown(md_content)
    
    # 建立 XMind XML 樹
    xmap_content = build_xmind_tree(structure)
    
    # 決定輸出路徑
    if output_path is None:
        base_name = os.path.splitext(os.path.basename(md_file_path))[0]
        output_path = f"{base_name}.xmind"
    
    # 確保輸出路徑以 .xmind 結尾
    if not output_path.endswith('.xmind'):
        output_path += '.xmind'
    
    # 創建 XMind 檔案（實際上是 zip 檔案）
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as xmind_zip:
        # 添加 content.xml
        content_xml = prettify_xml(xmap_content)
        xmind_zip.writestr('content.xml', content_xml)
        
        # 添加 meta.xml
        meta_xml = create_meta_xml()
        xmind_zip.writestr('meta.xml', meta_xml)
        
        # 添加 manifest.xml
        manifest_xml = create_manifest_xml()
        xmind_zip.writestr('META-INF/manifest.xml', manifest_xml)
    
    return output_path


def main():
    """命令列介面"""
    if len(sys.argv) < 2:
        print("使用方式: python md_to_xmind.py <markdown_file> [output_file]")
        print("範例: python md_to_xmind.py course.md course.xmind")
        sys.exit(1)
    
    md_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not os.path.exists(md_file):
        print(f"錯誤: 找不到檔案 {md_file}")
        sys.exit(1)
    
    try:
        result = md_to_xmind(md_file, output_file)
        print(f"✅ 成功生成 XMind 檔案: {result}")
    except Exception as e:
        print(f"❌ 錯誤: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
