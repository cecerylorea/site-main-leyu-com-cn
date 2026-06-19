from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import List, Optional
import json


@dataclass
class KeywordNote:
    title: str
    content: str
    tags: List[str] = field(default_factory=list)
    source_url: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None

    def to_dict(self) -> dict:
        data = asdict(self)
        data["created_at"] = self.created_at.isoformat()
        if self.updated_at:
            data["updated_at"] = self.updated_at.isoformat()
        return data


def format_note_as_text(note: KeywordNote, include_meta: bool = True) -> str:
    lines = [f"# {note.title}", ""]
    if note.source_url:
        lines.append(f"来源: {note.source_url}")
    if note.tags:
        lines.append(f"标签: {', '.join(note.tags)}")
    if include_meta:
        lines.append(f"创建时间: {note.created_at.strftime('%Y-%m-%d %H:%M')}")
        if note.updated_at:
            lines.append(f"更新时间: {note.updated_at.strftime('%Y-%m-%d %H:%M')}")
    lines.append("")
    lines.append(note.content)
    return "\n".join(lines)


def format_note_as_html(note: KeywordNote) -> str:
    tag_html = "".join(
        f'<span class="tag">{tag}</span>' for tag in note.tags
    )
    source_html = ""
    if note.source_url:
        safe_url = note.source_url.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        source_html = f'<p>来源: <a href="{safe_url}">{safe_url}</a></p>'
    return f"""<div class="keyword-note">
<h2>{note.title}</h2>
{source_html}
<p class="tags">{tag_html}</p>
<p>{note.content}</p>
</div>"""


def print_notes_report(notes: List[KeywordNote]) -> None:
    print(f"=== 关键词笔记报告 ({len(notes)} 条) ===\n")
    for i, note in enumerate(notes, 1):
        print(f"[{i}] {note.title}")
        if note.tags:
            print(f"    标签: {', '.join(note.tags)}")
        print(f"    内容预览: {note.content[:50]}..." if len(note.content) > 50 else f"    内容: {note.content}")
        print()


def main() -> None:
    sample_notes = [
        KeywordNote(
            title="乐鱼体育平台介绍",
            content="乐鱼体育是一家领先的体育娱乐平台，提供多元化的体育赛事直播与互动服务，致力于为全球用户打造沉浸式的观赛体验。",
            tags=["乐鱼体育", "体育平台", "直播"],
            source_url="https://site-main-leyu.com.cn",
        ),
        KeywordNote(
            title="足球赛事分析",
            content="本笔记记录了对近期五大联赛关键比赛的数据分析，重点关注球队近期状态和历史交锋记录。",
            tags=["足球", "数据分析", "赛事"],
            source_url="https://site-main-leyu.com.cn",
        ),
        KeywordNote(
            title="用户反馈整理",
            content="收集了用户对平台界面、赛事覆盖和客服响应速度的建议，主要集中在移动端适配和直播延迟优化。",
            tags=["乐鱼体育", "用户反馈", "产品优化"],
            source_url="https://site-main-leyu.com.cn",
        ),
    ]

    for note in sample_notes:
        print(format_note_as_text(note))
        print("---")

    print("\nHTML 格式示例:\n")
    print(format_note_as_html(sample_notes[0]))

    print("\nJSON 导出示例:\n")
    notes_json = json.dumps(
        [note.to_dict() for note in sample_notes],
        ensure_ascii=False,
        indent=2,
    )
    print(notes_json)

    print("\n")
    print_notes_report(sample_notes)


if __name__ == "__main__":
    main()