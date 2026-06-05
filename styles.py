"""
styles.py  ─  다크/라이트 테마 CSS 인젝션 모듈
"""

import streamlit as st


# ── 테마 색상 토큰 ─────────────────────────────────────────────────────────────
DARK = {
    "bg_main":        "#0f0f13",
    "bg_sidebar":     "#16161f",
    "bg_card":        "#1a1a26",
    "bg_input":       "#1a1a26",
    "bg_hover":       "#1e1e2e",
    "border":         "#2e2e42",
    "border_sub":     "#2a2a38",
    "text_primary":   "#ffffff",
    "text_body":      "#e0e0e0",
    "text_muted":     "#aaaaaa",
    "text_dim":       "#666666",
    "accent":         "#ff6b9d",
    "accent2":        "#c44dff",
    "accent_alpha":   "#ff6b9d22",
    "accent2_alpha":  "#c44dff44",
    "cal_selected_bg":"#ff6b9d",
    "cal_today_bg":   "#2a1a2e",
    "cal_today_border":"#c44dff",
    "btn_bg":         "#1e1e2e",
    "btn_hover_bg":   "#ff6b9d22",
    "highlight_bg":   "#1c1428",
    "next_plan_bg":   "#0d1a28",
    "next_plan_border":"#1a4060",
    "next_plan_color": "#88ddff",
    "search_badge_bg": "#2a1a3a",
    "settings_bg":    "#1a1a26",
    "mode_inactive":  "#2a2a3a",
    "mode_inactive_txt":"#888888",
    "scrollbar_thumb":"#2a2a3a",
}

LIGHT = {
    "bg_main":        "#f5f0f8",
    "bg_sidebar":     "#ede8f5",
    "bg_card":        "#ffffff",
    "bg_input":       "#ffffff",
    "bg_hover":       "#f0ebfa",
    "border":         "#d8cce8",
    "border_sub":     "#e0d8f0",
    "text_primary":   "#1a1020",
    "text_body":      "#2c2040",
    "text_muted":     "#6b5e80",
    "text_dim":       "#9988aa",
    "accent":         "#d63384",
    "accent2":        "#8b2be2",
    "accent_alpha":   "#d6338422",
    "accent2_alpha":  "#8b2be244",
    "cal_selected_bg":"#d63384",
    "cal_today_bg":   "#f3e8ff",
    "cal_today_border":"#8b2be2",
    "btn_bg":         "#f0ebfa",
    "btn_hover_bg":   "#d6338422",
    "highlight_bg":   "#fdf4ff",
    "next_plan_bg":   "#eff8ff",
    "next_plan_border":"#bfdbfe",
    "next_plan_color": "#1d4ed8",
    "search_badge_bg": "#f3e8ff",
    "settings_bg":    "#ede8f5",
    "mode_inactive":  "#e8e0f0",
    "mode_inactive_txt":"#6b5e80",
    "scrollbar_thumb":"#d8cce8",
}


def inject_custom_css(theme: str = "dark"):
    t = DARK if theme == "dark" else LIGHT

    st.markdown(
        f"""
        <style>
        /* ── Google Fonts ──────────────────────────────────────────────── */
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;600;700&family=Noto+Serif+KR:wght@300;400;600&display=swap');

        /* ── CSS 변수 ──────────────────────────────────────────────────── */
        :root {{
            --bg-main:          {t["bg_main"]};
            --bg-sidebar:       {t["bg_sidebar"]};
            --bg-card:          {t["bg_card"]};
            --bg-input:         {t["bg_input"]};
            --bg-hover:         {t["bg_hover"]};
            --border:           {t["border"]};
            --border-sub:       {t["border_sub"]};
            --text-primary:     {t["text_primary"]};
            --text-body:        {t["text_body"]};
            --text-muted:       {t["text_muted"]};
            --text-dim:         {t["text_dim"]};
            --accent:           {t["accent"]};
            --accent2:          {t["accent2"]};
            --accent-alpha:     {t["accent_alpha"]};
            --accent2-alpha:    {t["accent2_alpha"]};
        }}

        /* ── 전체 배경 ─────────────────────────────────────────────────── */
        html, body, [class*="css"], .stApp {{
            background-color: var(--bg-main) !important;
            color: var(--text-body) !important;
            font-family: 'Noto Sans KR', sans-serif !important;
        }}

        /* ── 사이드바 ──────────────────────────────────────────────────── */
        [data-testid="stSidebar"] {{
            background-color: var(--bg-sidebar) !important;
            border-right: 1px solid var(--border-sub) !important;
        }}
        [data-testid="stSidebar"] > div:first-child {{
            padding-top: 1rem !important;
            display: flex !important;
            flex-direction: column !important;
            height: 100vh !important;
        }}

        /* ── 메인 콘텐츠 여백 ──────────────────────────────────────────── */
        .main .block-container {{
            padding: 2rem 2.5rem 3rem 2.5rem !important;
            max-width: 860px;
        }}

        /* ── 사이드바 타이틀 ───────────────────────────────────────────── */
        .sidebar-title {{
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 1.1rem;
            font-weight: 700;
            color: var(--text-primary);
            padding: 0.3rem 0.5rem 0.9rem 0.5rem;
            letter-spacing: -0.3px;
        }}
        .sidebar-logo {{ font-size: 1.3rem; }}

        /* ── 구분선 ────────────────────────────────────────────────────── */
        .sidebar-divider {{
            height: 1px;
            background: linear-gradient(90deg, transparent, var(--border-sub), transparent);
            margin: 0.6rem 0;
        }}

        /* ── 상단 버튼 (일기 / 공유) ───────────────────────────────────── */
        [data-testid="stSidebar"] .stButton button {{
            background-color: {t["btn_bg"]} !important;
            color: var(--text-muted) !important;
            border: 1px solid var(--border) !important;
            border-radius: 8px !important;
            font-size: 0.8rem !important;
            font-weight: 500 !important;
            padding: 0.4rem 0.3rem !important;
            transition: all 0.2s ease !important;
            width: 100% !important;
        }}
        [data-testid="stSidebar"] .stButton button:hover {{
            background-color: {t["btn_hover_bg"]} !important;
            border-color: var(--accent) !important;
            color: var(--accent) !important;
            transform: translateY(-1px) !important;
        }}

        /* ── 달력 헤더 텍스트 ──────────────────────────────────────────── */
        .cal-header {{
            text-align: center;
            font-size: 0.88rem;
            font-weight: 600;
            color: var(--text-primary);
            padding: 0.2rem 0;
        }}

        /* ── 달력 요일 이름 ─────────────────────────────────────────────── */
        .cal-dayname {{
            text-align: center;
            font-size: 0.65rem;
            font-weight: 600;
            padding: 0.1rem 0 0.2rem 0;
        }}

        /* ── 달력 날짜 셀 컨테이너 ─────────────────────────────────────── */
        .cal-cell {{
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 1px;
            padding: 1px 0;
        }}

        /* ── 달력 날짜 버튼 — 원형 ─────────────────────────────────────── */
        [data-testid="stSidebar"] [data-testid^="stBaseButton"] button {{
            background: transparent !important;
            border: 1px solid transparent !important;
            color: var(--text-body) !important;
            font-size: 0.72rem !important;
            font-weight: 400 !important;
            padding: 0 !important;
            border-radius: 50% !important;
            width: 26px !important;
            min-width: 26px !important;
            max-width: 26px !important;
            height: 26px !important;
            min-height: 26px !important;
            line-height: 26px !important;
            margin: 0 auto !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            white-space: nowrap !important;
            overflow: hidden !important;
            text-overflow: clip !important;
        }}
        [data-testid="stSidebar"] [data-testid^="stBaseButton"] button:hover {{
            background-color: {t["btn_hover_bg"]} !important;
            border-color: var(--accent) !important;
            color: var(--accent) !important;
        }}

        /* ── 달력 날짜 아래 점 ─────────────────────────────────────────── */
        .entry-dot {{
            width: 5px;
            height: 5px;
            border-radius: 50%;
            background-color: var(--accent);
            margin: 0 auto;
        }}
        .entry-dot-empty {{
            width: 5px;
            height: 5px;
            margin: 0 auto;
        }}

        /* ── 달력 빈 셀 ────────────────────────────────────────────────── */
        .cal-empty {{ height: 32px; }}

        /* ── 목차 아이템 ───────────────────────────────────────────────── */
        .toc-item {{
            font-size: 0.75rem;
            color: var(--accent);
            padding: 0.18rem 0.5rem;
            border-left: 2px solid var(--accent2-alpha);
            margin: 0.15rem 0;
        }}

        /* ── 검색창 ────────────────────────────────────────────────────── */
        [data-testid="stSidebar"] .stTextInput input {{
            background-color: {t["bg_input"]} !important;
            border: 1px solid var(--border) !important;
            border-radius: 8px !important;
            color: var(--text-body) !important;
            font-size: 0.8rem !important;
        }}
        [data-testid="stSidebar"] .stTextInput input:focus {{
            border-color: var(--accent) !important;
            box-shadow: 0 0 0 2px var(--accent-alpha) !important;
        }}

        /* ── 사이드바 하단 설정 패널 ────────────────────────────────────── */
        .settings-panel {{
            background: {t["settings_bg"]};
            border-top: 1px solid var(--border-sub);
            padding: 0.7rem 0.5rem 0.5rem 0.5rem;
            margin-top: auto;
        }}
        .settings-title {{
            font-size: 0.72rem;
            color: var(--text-dim);
            font-weight: 600;
            letter-spacing: 0.05em;
            text-transform: uppercase;
            margin-bottom: 0.4rem;
        }}

        /* ── 메인 화면 모드 탭 ─────────────────────────────────────────── */
        .mode-tabs {{
            display: flex;
            gap: 8px;
            margin-bottom: 1.2rem;
        }}
        .mode-tab {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 0.4rem 1.1rem;
            border-radius: 20px;
            font-size: 0.82rem;
            font-weight: 600;
            cursor: default;
            border: 1.5px solid transparent;
            transition: all 0.2s;
        }}
        .mode-tab-active {{
            background: linear-gradient(135deg, var(--accent), var(--accent2));
            color: #ffffff;
            border-color: transparent;
            box-shadow: 0 2px 12px var(--accent-alpha);
        }}
        .mode-tab-inactive {{
            background: {t["mode_inactive"]};
            color: {t["mode_inactive_txt"]};
            border-color: var(--border);
        }}

        /* ── 페이지 헤더 ───────────────────────────────────────────────── */
        .page-header {{ margin-bottom: 0.3rem; }}
        .page-title {{
            display: flex;
            align-items: center;
            gap: 12px;
            font-size: 1.4rem;
            font-weight: 700;
            color: var(--text-primary);
            font-family: 'Noto Serif KR', serif;
        }}
        .page-icon {{ font-size: 1.4rem; }}
        .page-subtitle {{
            font-size: 0.8rem;
            color: var(--text-muted);
            margin-top: 0.25rem;
            padding-left: 2.6rem;
        }}
        .page-divider {{
            height: 1px;
            background: linear-gradient(90deg, var(--accent), var(--accent2-alpha), transparent);
            margin: 0.9rem 0 1.4rem 0;
            opacity: 0.6;
        }}

        /* ── 일기/공유 카드 (뷰 모드) ──────────────────────────────────── */
        .entry-card {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 1.8rem 2rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 24px rgba(0,0,0,0.15);
        }}
        .entry-meta {{
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 0.8rem;
        }}
        .entry-mood, .entry-rating {{ font-size: 1.05rem; }}
        .entry-place {{
            font-size: 0.78rem;
            color: var(--text-muted);
            background: {t["mode_inactive"]};
            padding: 0.2rem 0.7rem;
            border-radius: 20px;
        }}
        .entry-title {{
            font-size: 1.25rem;
            font-weight: 600;
            color: var(--text-primary);
            font-family: 'Noto Serif KR', serif;
            margin: 0.5rem 0 1rem 0;
            line-height: 1.4;
        }}
        .entry-content {{
            font-size: 0.9rem;
            color: var(--text-body);
            line-height: 1.9;
            white-space: pre-wrap;
            word-break: keep-all;
        }}
        .entry-photos {{
            font-size: 0.78rem;
            color: var(--text-muted);
            margin-top: 1rem;
            padding-top: 0.8rem;
            border-top: 1px solid var(--border-sub);
        }}

        /* ── 하이라이트 박스 ────────────────────────────────────────────── */
        .highlight-box {{
            background: {t["highlight_bg"]};
            border: 1px solid var(--accent2-alpha);
            border-left: 3px solid var(--accent2);
            border-radius: 8px;
            padding: 0.8rem 1.2rem;
            margin: 1rem 0;
        }}
        .highlight-label {{
            font-size: 0.73rem;
            color: var(--accent2);
            font-weight: 600;
            display: block;
            margin-bottom: 0.3rem;
        }}
        .highlight-text {{
            font-size: 0.9rem;
            color: var(--text-body);
        }}

        /* ── 다음 계획 박스 ─────────────────────────────────────────────── */
        .next-plan-box {{
            font-size: 0.83rem;
            color: {t["next_plan_color"]};
            background: {t["next_plan_bg"]};
            border: 1px solid {t["next_plan_border"]};
            border-radius: 8px;
            padding: 0.6rem 1rem;
            margin-top: 1rem;
        }}

        /* ── 입력 폼 카드 ───────────────────────────────────────────────── */
        .form-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-sub);
            border-radius: 16px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
        }}

        /* ── 메인 영역 입력 위젯 ────────────────────────────────────────── */
        .stTextInput input,
        .stTextArea textarea {{
            background-color: var(--bg-input) !important;
            border: 1px solid var(--border) !important;
            border-radius: 8px !important;
            color: var(--text-body) !important;
            font-family: 'Noto Sans KR', sans-serif !important;
        }}
        .stTextInput input:focus,
        .stTextArea textarea:focus {{
            border-color: var(--accent) !important;
            box-shadow: 0 0 0 2px var(--accent-alpha) !important;
        }}
        .stTextInput label, .stTextArea label,
        .stSelectbox label, .stSlider label {{
            color: var(--text-muted) !important;
            font-size: 0.8rem !important;
        }}

        /* ── 셀렉트박스 ─────────────────────────────────────────────────── */
        [data-testid="stSelectbox"] > div > div {{
            background-color: var(--bg-input) !important;
            border: 1px solid var(--border) !important;
            border-radius: 8px !important;
            color: var(--text-body) !important;
        }}

        /* ── 슬라이더 ───────────────────────────────────────────────────── */
        .stSlider > div > div > div {{ background-color: var(--accent) !important; }}

        /* ── 메인 영역 버튼 ─────────────────────────────────────────────── */
        .main .stButton button {{
            background: linear-gradient(135deg, var(--accent), var(--accent2)) !important;
            color: white !important;
            border: none !important;
            border-radius: 10px !important;
            font-weight: 600 !important;
            font-size: 0.86rem !important;
            transition: all 0.2s ease !important;
            box-shadow: 0 2px 12px var(--accent-alpha) !important;
        }}
        .main .stButton button:hover {{
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px var(--accent-alpha) !important;
            filter: brightness(1.08) !important;
        }}

        /* ── 빈 상태 ────────────────────────────────────────────────────── */
        .empty-state {{
            text-align: center;
            padding: 3.5rem 2rem;
            color: var(--text-dim);
        }}
        .empty-icon {{ font-size: 2.8rem; margin-bottom: 1rem; }}
        .empty-text {{
            font-size: 1rem;
            color: var(--text-muted);
            margin-bottom: 0.4rem;
            font-weight: 500;
        }}
        .empty-sub {{
            font-size: 0.8rem;
            color: var(--text-dim);
            margin-bottom: 1.5rem;
        }}

        /* ── 검색 결과 카드 ─────────────────────────────────────────────── */
        .search-result-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-sub);
            border-radius: 12px;
            padding: 1.1rem 1.4rem;
            margin-bottom: 0.5rem;
            transition: border-color 0.2s;
        }}
        .search-result-card:hover {{ border-color: var(--accent-alpha); }}
        .search-result-meta {{
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 0.45rem;
        }}
        .search-type-badge {{
            font-size: 0.7rem;
            background: {t["search_badge_bg"]};
            color: var(--accent2);
            padding: 0.15rem 0.6rem;
            border-radius: 20px;
            border: 1px solid var(--accent2-alpha);
        }}
        .search-date {{ font-size: 0.73rem; color: var(--text-dim); }}
        .search-result-title {{
            font-size: 0.97rem;
            font-weight: 600;
            color: var(--text-primary);
            margin-bottom: 0.35rem;
        }}
        .search-result-preview {{
            font-size: 0.8rem;
            color: var(--text-muted);
            line-height: 1.55;
        }}

        /* ── success 메시지 ──────────────────────────────────────────────── */
        .stSuccess {{
            background-color: {'#0a2a1a' if theme=='dark' else '#f0fdf4'} !important;
            border: 1px solid {'#1a6a3a' if theme=='dark' else '#86efac'} !important;
            color: {'#66ddaa' if theme=='dark' else '#15803d'} !important;
            border-radius: 8px !important;
        }}

        /* ── 스크롤바 ───────────────────────────────────────────────────── */
        ::-webkit-scrollbar {{ width: 4px; height: 4px; }}
        ::-webkit-scrollbar-track {{ background: var(--bg-main); }}
        ::-webkit-scrollbar-thumb {{
            background: {t["scrollbar_thumb"]};
            border-radius: 3px;
        }}
        ::-webkit-scrollbar-thumb:hover {{ background: var(--accent); opacity:0.5; }}

        /* ── 모바일 반응형 ──────────────────────────────────────────────── */
        @media (max-width: 768px) {{
            .main .block-container {{ padding: 1rem !important; }}
            .page-title {{ font-size: 1.1rem !important; }}
            .entry-card {{ padding: 1.1rem !important; }}
        }}

        /* ── Streamlit 기본 요소 숨기기 ─────────────────────────────────── */
        #MainMenu {{ visibility: hidden; }}
        footer {{ visibility: hidden; }}
        header {{ visibility: hidden; }}
        </style>
        """,
        unsafe_allow_html=True,
    )
