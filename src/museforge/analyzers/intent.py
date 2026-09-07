"""Intent analysis — turn a natural-language request into a structured Intent.

Works with a configured LLM, or falls back to deterministic keyword heuristics so the core
path runs with no API key.
"""

from __future__ import annotations

from museforge.knowledge.models import Intent
from museforge.providers.llm import LLMProvider

# Keyword → (use_case, category) mappings. Order matters: first match wins.
_USE_CASE_RULES: list[tuple[tuple[str, ...], str, str]] = [
    (("招聘", "recruit", "hiring", "job"), "recruitment marketing", "social media poster"),
    (("小红书", "xiaohongshu", "rednote", "red note"), "social media marketing", "social media poster"),
    (("银行卡", "信用卡", "fintech", "金融", "bank card", "credit card"), "fintech marketing", "product advertisement"),
    (("产品", "product", "电商", "e-commerce", "ecommerce", "商品"), "product marketing", "product advertisement"),
    (("海报", "poster", "flyer"), "marketing", "poster"),
    (("信息图", "infographic", "图表", "数据"), "education", "infographic"),
    (("漫画", "comic", "storyboard", "多格", "分镜"), "storytelling", "comic"),
    (("人物", "肖像", "portrait", "写真", "摄影", "photography"), "photography", "photography"),
    (("hero", "landing", "saas", "app", "应用", "软件"), "product marketing", "product hero"),
    (("封面", "cover", "thumbnail", "缩略图"), "social media marketing", "social media poster"),
]

_PLATFORM_RULES: list[tuple[tuple[str, ...], str]] = [
    (("小红书", "xiaohongshu", "rednote", "red note"), "Xiaohongshu"),
    (("instagram", "ins"), "Instagram"),
    (("twitter", "x.com", "推特"), "Twitter/X"),
    (("youtube", "油管"), "YouTube"),
    (("linkedin", "领英"), "LinkedIn"),
]

_ASPECT_RULES: list[tuple[tuple[str, ...], str]] = [
    (("3:4", "3：4", "竖版", "portrait"), "3:4"),
    (("4:3", "4：3", "横版", "landscape"), "4:3"),
    (("1:1", "1：1", "方形", "square"), "1:1"),
    (("16:9", "16：9", "宽屏", "widescreen"), "16:9"),
    (("9:16", "9：16", "story", "竖屏"), "9:16"),
]

_STYLE_RULES: list[tuple[tuple[str, ...], str]] = [
    (("极简", "minimal", "minimalist", "简洁"), "editorial minimalism"),
    (("编辑", "editorial", "杂志", "magazine"), "editorial minimalism"),
    (("奢华", "luxury", "高端", "premium", "高级"), "luxury commercial"),
    (("写实", "realistic", "photoreal", "真实"), "cinematic realism"),
    (("扁平", "flat", "矢量", "vector"), "flat vector"),
    (("3d", "三维", "立体", "render"), "3D commercial"),
    (("日系", "japanese", "和风"), "Japanese magazine editorial"),
    (("复古", "retro", "vintage"), "retro print"),
    (("瑞士", "swiss", "网格"), "Swiss editorial"),
    (("中文", "chinese", "国风", "中式"), "modern Chinese editorial"),
]

_DENSITY_RULES: list[tuple[tuple[str, ...], str]] = [
    (("极简", "minimal", "留白", "简洁", "干净"), "low"),
    (("丰富", "detail", "复杂", "密集", "信息量大"), "high"),
]

_PATTERN_RULES: list[tuple[tuple[str, ...], str]] = [
    (("海报", "poster", "封面", "cover", "文字", "text"), "Editorial Text-first Poster"),
    (("产品", "product", "hero", "商品", "电商"), "Breakout Product Hero"),
    (("信息图", "infographic", "图表"), "Magazine Infographic"),
    (("漫画", "comic", "多格", "storyboard"), "Multi-panel Comic"),
    (("人物", "portrait", "肖像", "写真"), "Cinematic Character Portrait"),
    (("对比", "before", "after", "前后"), "Split-screen Comparison"),
]


class IntentAnalyzer:
    """Analyze a user request into a structured Intent."""

    def __init__(self, llm: LLMProvider | None = None) -> None:
        self.llm = llm

    def understand_request(self, request: str) -> Intent:
        if self.llm is not None:
            try:
                return self._llm_analyze(request)
            except Exception:  # noqa: BLE001 - fall back to heuristics on any LLM failure
                pass
        return self._heuristic_analyze(request)

    # -- heuristic fallback ---------------------------------------------

    def _heuristic_analyze(self, request: str) -> Intent:
        low = request.lower()
        use_case, category = self._first_match(_USE_CASE_RULES, low, ("general", "general"))
        platform = self._first_match(_PLATFORM_RULES, low, ("",))[0]
        aspect_ratio = self._first_match(_ASPECT_RULES, low, ("",))[0]
        style = self._first_match(_STYLE_RULES, low, ("",))[0]
        visual_density = self._first_match(_DENSITY_RULES, low, ("medium",))[0]
        likely_pattern = self._first_match(_PATTERN_RULES, low, ("",))[0]
        priority = "text readability" if category in {"poster", "social media poster", "infographic"} else ""
        return Intent(
            use_case=use_case,
            category=category,
            platform=platform,
            aspect_ratio=aspect_ratio,
            priority=priority,
            style=style,
            visual_density=visual_density,
            likely_pattern=likely_pattern,
            keywords=self._keywords(request),
            language="zh" if self._is_chinese(request) else "en",
            raw_request=request,
        )

    @staticmethod
    def _first_match(
        rules: list[tuple[tuple[str, ...], str, str]] | list[tuple[tuple[str, ...], str]],
        text: str,
        default: tuple[str, ...],
    ) -> tuple[str, ...]:
        for keywords, *rest in rules:
            if any(k in text for k in keywords):
                return tuple(rest)
        return default

    @staticmethod
    def _is_chinese(text: str) -> bool:
        return any("一" <= ch <= "鿿" for ch in text)

    @staticmethod
    def _keywords(request: str) -> list[str]:
        from museforge.normalizers.text import tokenize

        return tokenize(request)

    # -- LLM path -------------------------------------------------------

    def _llm_analyze(self, request: str) -> Intent:
        assert self.llm is not None
        system = (
            "You analyze an image-generation request. Respond with ONLY a JSON object with "
            "keys: use_case, category, platform, aspect_ratio, priority, style, visual_density, "
            "likely_pattern. Use empty strings when unknown."
        )
        raw = self.llm.complete(request, system=system)
        import json

        data = json.loads(raw)
        return Intent(
            raw_request=request,
            use_case=str(data.get("use_case", "")),
            category=str(data.get("category", "")),
            platform=str(data.get("platform", "")),
            aspect_ratio=str(data.get("aspect_ratio", "")),
            priority=str(data.get("priority", "")),
            style=str(data.get("style", "")),
            visual_density=str(data.get("visual_density", "")),
            likely_pattern=str(data.get("likely_pattern", "")),
        )
