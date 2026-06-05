import streamlit as st
import datetime
import calendar as cal_lib
import importlib
import data_store
importlib.reload(data_store)
from data_store import (
    save_diary_entry,
    load_diary_entries,
    save_shared_entry,
    delete_shared_entry,
    load_shared_entries,
    search_entries,
    get_all_entry_dates,
)

# ── 페이지 기본 설정 ──────────────────────────────────────────────────────────
st.set_page_config(
    page_title="데이트 로그 💕",
    page_icon="💕",
    layout="wide",
    initial_sidebar_state="auto",
)

# ── 세션 상태 초기화 ─────────────────────────────────────────────────────────
if "diaries" not in st.session_state:
    _loaded = load_diary_entries()
    st.session_state.diaries = _loaded if _loaded else {}
    st.session_state._load_debug = f"로드된 일기: {len(st.session_state.diaries)}개 | 파일: {data_store.LOCAL_DATA_FILE}"
if "shared_notes"   not in st.session_state: st.session_state.shared_notes  = load_shared_entries()
if "theme"          not in st.session_state: st.session_state.theme         = "light"
if "mode"           not in st.session_state: st.session_state.mode          = "diary"
if "selected_date"  not in st.session_state: st.session_state.selected_date = datetime.date.today()
if "cal_year"       not in st.session_state: st.session_state.cal_year      = datetime.date.today().year
if "cal_month"      not in st.session_state: st.session_state.cal_month     = datetime.date.today().month
if "search_query"   not in st.session_state: st.session_state.search_query  = ""
if "search_results" not in st.session_state: st.session_state.search_results= []
if "edit_mode"      not in st.session_state: st.session_state.edit_mode     = False


# ═══════════════════════════════════════════════════════════════════════════════
#  CSS 인젝션
# ═══════════════════════════════════════════════════════════════════════════════
def inject_css(theme):
    dk = theme == "dark"
    bg       = "#0f0f13"   if dk else "#f5f0f8"
    sb       = "#16161f"   if dk else "#ede8f5"
    card     = "#1a1a26"   if dk else "#ffffff"
    inp      = "#1a1a26"   if dk else "#ffffff"
    bdr      = "#2e2e42"   if dk else "#d8cce8"
    bdr_s    = "#2a2a38"   if dk else "#e0d8f0"
    tp       = "#ffffff"   if dk else "#1a1020"
    tb       = "#e0e0e0"   if dk else "#2c2040"
    tm       = "#aaaaaa"   if dk else "#6b5e80"
    td       = "#666666"   if dk else "#9988aa"
    ac       = "#ff6b9d"   if dk else "#d63384"
    ac2      = "#c44dff"   if dk else "#8b2be2"
    aca      = "#ff6b9d22" if dk else "#d6338422"
    ac2a     = "#c44dff44" if dk else "#8b2be244"
    bbg      = "#1e1e2e"   if dk else "#f0ebfa"
    bho      = "#ff6b9d22" if dk else "#d6338422"
    hlbg     = "#1c1428"   if dk else "#fdf4ff"
    npbg     = "#0d1a28"   if dk else "#eff8ff"
    npbd     = "#1a4060"   if dk else "#bfdbfe"
    npcl     = "#88ddff"   if dk else "#1d4ed8"
    sbbg     = "#2a1a3a"   if dk else "#f3e8ff"
    setbg    = "#1a1a26"   if dk else "#ede8f5"
    mina     = "#2a2a3a"   if dk else "#e8e0f0"
    minatxt  = "#888888"   if dk else "#6b5e80"
    scth     = "#2a2a3a"   if dk else "#d8cce8"
    succ_bg  = "#0a2a1a"   if dk else "#f0fdf4"
    succ_bd  = "#1a6a3a"   if dk else "#86efac"
    succ_cl  = "#66ddaa"   if dk else "#15803d"
    cal_sun  = "#ff6b6b"   if dk else "#e11d48"
    cal_sat  = "#aaaaaa"   if dk else "#8b8b9a"

    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;600;700&family=Noto+Serif+KR:wght@300;400;600&display=swap');

    html,body,[class*="css"],.stApp{{background:{bg}!important;color:{tb}!important;font-family:'Noto Sans KR',sans-serif!important}}
    [data-testid="stSidebar"]{{background:{sb}!important;border-right:1px solid {bdr_s}!important}}
    [data-testid="stSidebar"]>div:first-child{{padding-top:1rem!important;display:flex!important;flex-direction:column!important;min-height:100vh!important}}
    .main .block-container{{padding:2rem 2.5rem 3rem!important;max-width:860px}}
    .sidebar-title{{display:flex;align-items:center;gap:10px;font-size:1.1rem;font-weight:700;color:{tp};padding:.3rem .5rem .9rem;letter-spacing:-.3px}}
    .sidebar-logo{{font-size:1.3rem}}
    .sidebar-divider{{height:1px;background:linear-gradient(90deg,transparent,{bdr_s},transparent);margin:.6rem 0}}

    div:has(.main-nav-marker) + div button {{
        background: {bbg} !important; color: {tm} !important; border: 1px solid {bdr} !important; border-radius: 8px !important;
        font-size: 0.8rem !important; font-weight: 500 !important; padding: 0.4rem 0.3rem !important; transition: all 0.2s !important; width: 100% !important;
    }}
    div:has(.main-nav-marker) + div button:hover {{
        background: {bho} !important; border-color: {ac} !important; color: {ac} !important; transform: translateY(-1px) !important;
    }}

    div[data-testid="stHorizontalBlock"]:has(.cal-header-row-marker) {{
        align-items: center !important;
    }}
    .cal-header {{
        display: flex; align-items: center; justify-content: center;
        margin: 0; font-size: 1.2rem; font-weight: 700; color: {tp};
    }}
    div[data-testid="stElementContainer"]:has(.nav-btn-marker) + div[data-testid="stElementContainer"] button {{
        height: 34px !important; min-height: 34px !important;
        width: 34px !important; min-width: 34px !important; max-width: 34px !important;
        margin: 0 auto !important; padding: 0 !important;
        display: flex !important; align-items: center !important; justify-content: center !important;
        border-radius: 8px !important; background: {bbg} !important; border: 1px solid {bdr_s} !important; color: {tb} !important;
    }}
    div[data-testid="stElementContainer"]:has(.nav-btn-marker) + div[data-testid="stElementContainer"] button p {{ margin: 0 !important; font-size: 1.2rem !important; line-height: 1 !important; }}
    div[data-testid="stElementContainer"]:has(.nav-btn-marker) + div[data-testid="stElementContainer"] button:hover {{ background: {bho} !important; color: {ac} !important; border-color: {ac} !important; }}

    .cal-dayname {{ text-align: center; font-size: 0.8rem; font-weight: 700; padding: 0.2rem 0; margin-bottom: 0; }}
    div[data-testid="stHorizontalBlock"]:has(.cal-dayname) {{
        margin-bottom: -15px !important;
    }}

    div[data-testid="stHorizontalBlock"]:has(.cal-btn-marker) {{
        margin-bottom: -12px !important;
    }}
    div[data-testid="stElementContainer"]:has(.cal-btn-marker) + div[data-testid="stElementContainer"] button {{
        background: transparent !important; border: 2px solid transparent !important; color: {tb} !important;
        font-size: 0.85rem !important; font-weight: 500 !important; padding: 0 !important;
        border-radius: 50% !important; width: 34px !important; min-width: 34px !important; max-width: 34px !important;
        height: 34px !important; min-height: 34px !important; margin: 0 auto !important;
        display: flex !important; align-items: center !important; justify-content: center !important;
        position: relative !important;
    }}
    div[data-testid="stElementContainer"]:has(.cal-btn-marker) + div[data-testid="stElementContainer"] button div[data-testid="stMarkdownContainer"] {{
        display: flex !important; align-items: center !important; justify-content: center !important;
        width: 100% !important; height: 100% !important; margin: 0 !important; padding: 0 !important;
    }}
    div[data-testid="stElementContainer"]:has(.cal-btn-marker) + div[data-testid="stElementContainer"] button p {{ margin: 0 !important; padding: 0 !important; line-height: 1 !important; }}
    div[data-testid="stElementContainer"]:has(.cal-btn-marker) + div[data-testid="stElementContainer"] button:hover {{ background: {bho} !important; color: {ac} !important; border-color: {ac} !important; }}

    div[data-testid="stElementContainer"]:has(.cal-btn-selected) + div[data-testid="stElementContainer"] button {{
        background: #4facfe !important; color: #ffffff !important; font-weight: 700 !important; border: 2px solid #4facfe !important;
    }}
    div[data-testid="stElementContainer"]:has(.cal-btn-today) + div[data-testid="stElementContainer"] button {{ border-color: #ffffff !important; font-weight: 700 !important; }}
    div[data-testid="stElementContainer"]:has(.cal-btn-selected.cal-btn-today) + div[data-testid="stElementContainer"] button {{
        background: #4facfe !important; border: 2px solid #ffffff !important; color: #ffffff !important;
    }}

    div[data-testid="stElementContainer"]:has(.cal-btn-sun) + div[data-testid="stElementContainer"] button {{ color: {cal_sun} !important; }}
    div[data-testid="stElementContainer"]:has(.cal-btn-sat) + div[data-testid="stElementContainer"] button {{ color: {cal_sat} !important; }}

    div[data-testid="stElementContainer"]:has(.cal-btn-has-entry) + div[data-testid="stElementContainer"] button::after {{
        content: ""; position: absolute; bottom: 4px; left: 50%; transform: translateX(-50%);
        width: 4px; height: 4px; border-radius: 50%; background-color: #ff6b9d;
    }}
    div[data-testid="stElementContainer"]:has(.cal-btn-selected.cal-btn-has-entry) + div[data-testid="stElementContainer"] button::after {{
        background-color: #ffffff;
    }}

    .cal-empty {{ height: 34px; }}

    .toc-item{{font-size:.75rem;color:{ac};padding:.18rem .5rem;border-left:2px solid {ac2a};margin:.15rem 0}}

    [data-testid="stSidebar"] .stTextInput input{{background:{inp}!important;border:1px solid {bdr}!important;border-radius:8px!important;color:{tb}!important;font-size:.8rem!important}}
    [data-testid="stSidebar"] .stTextInput input:focus{{border-color:{ac}!important;box-shadow:0 0 0 2px {aca}!important}}

    .settings-panel{{background:{setbg};border-top:1px solid {bdr_s};padding:.7rem .5rem .8rem;margin-top:auto}}
    .settings-title{{font-size:.72rem;color:{td};font-weight:600;letter-spacing:.05em;text-transform:uppercase;margin-bottom:.4rem}}

    .mode-tabs{{display:flex;gap:8px;margin-bottom:1.2rem}}
    .mode-tab{{display:inline-flex;align-items:center;gap:6px;padding:.4rem 1.1rem;border-radius:20px;font-size:.82rem;font-weight:600;border:1.5px solid transparent}}
    .mode-tab-active{{background:linear-gradient(135deg,{ac},{ac2});color:#fff;box-shadow:0 2px 12px {aca}}}
    .mode-tab-inactive{{background:{mina};color:{minatxt};border-color:{bdr}}}

    .page-header{{margin-bottom:.3rem}}
    .page-title{{display:flex;align-items:center;gap:12px;font-size:1.4rem;font-weight:700;color:{tp};font-family:'Noto Serif KR',serif}}
    .page-icon{{font-size:1.4rem}}
    .page-subtitle{{font-size:.8rem;color:{tm};margin-top:.25rem;padding-left:2.6rem}}
    .page-divider{{height:1px;background:linear-gradient(90deg,{ac},{ac2a},transparent);margin:.9rem 0 1.4rem;opacity:.6}}

    .entry-card{{background:{card};border:1px solid {bdr};border-radius:16px;padding:1.8rem 2rem;margin-bottom:1.5rem;box-shadow:0 4px 24px rgba(0,0,0,.15)}}
    .entry-meta{{display:flex;align-items:center;gap:12px;margin-bottom:.8rem}}
    .entry-mood,.entry-rating{{font-size:1.05rem}}
    .entry-place{{font-size:.78rem;color:{tm};background:{mina};padding:.2rem .7rem;border-radius:20px}}
    .entry-title{{font-size:1.25rem;font-weight:600;color:{tp};font-family:'Noto Serif KR',serif;margin:.5rem 0 1rem;line-height:1.4}}
    .entry-content{{font-size:.9rem;color:{tb};line-height:1.9;white-space:pre-wrap;word-break:keep-all}}
    .entry-photos{{font-size:.78rem;color:{tm};margin-top:1rem;padding-top:.8rem;border-top:1px solid {bdr_s}}}

    .highlight-box{{background:{hlbg};border:1px solid {ac2a};border-left:3px solid {ac2};border-radius:8px;padding:.8rem 1.2rem;margin:1rem 0}}
    .highlight-label{{font-size:.73rem;color:{ac2};font-weight:600;display:block;margin-bottom:.3rem}}
    .highlight-text{{font-size:.9rem;color:{tb}}}

    .next-plan-box{{font-size:.83rem;color:{npcl};background:{npbg};border:1px solid {npbd};border-radius:8px;padding:.6rem 1rem;margin-top:1rem}}

    .form-card{{background:{card};border:1px solid {bdr_s};border-radius:16px;padding:1.5rem;margin-bottom:1.5rem}}

    .stTextInput input,.stTextArea textarea{{background:{inp}!important;border:1px solid {bdr}!important;border-radius:8px!important;color:{tb}!important;font-family:'Noto Sans KR',sans-serif!important}}
    .stTextInput input:focus,.stTextArea textarea:focus{{border-color:{ac}!important;box-shadow:0 0 0 2px {aca}!important}}
    .stTextInput label,.stTextArea label,.stSelectbox label,.stSlider label{{color:{tm}!important;font-size:.8rem!important}}
    [data-testid="stSelectbox"]>div>div{{background:{inp}!important;border:1px solid {bdr}!important;border-radius:8px!important;color:{tb}!important}}
    .stSlider>div>div>div{{background:{ac}!important}}

    .main .stButton button{{background:linear-gradient(135deg,{ac},{ac2})!important;color:#fff!important;border:none!important;border-radius:10px!important;font-weight:600!important;font-size:.86rem!important;transition:all .2s!important;box-shadow:0 2px 12px {aca}!important}}
    .main .stButton button:hover{{transform:translateY(-2px)!important;box-shadow:0 6px 20px {aca}!important;filter:brightness(1.08)!important}}

    .empty-state{{text-align:center;padding:3rem 2rem;color:{td}}}
    .empty-icon{{font-size:2.8rem;margin-bottom:1rem}}
    .empty-text{{font-size:1rem;color:{tm};margin-bottom:1.5rem;font-weight:500}}

    div[data-testid="stVerticalBlock"]:has(> div:first-child .bulletin-board-wrapper) {{
        background-color: #b58d68;
        background-image: radial-gradient(#9c7551 15%, transparent 16%), radial-gradient(#9c7551 15%, transparent 16%);
        background-size: 16px 16px;
        background-position: 0 0, 8px 8px;
        padding: 3.5rem 2rem 2.5rem;
        border-radius: 8px;
        border: 12px solid #6b4c3a;
        box-shadow: inset 0 0 15px rgba(0,0,0,0.5), 0 8px 24px rgba(0,0,0,0.2);
        margin-top: 1rem;
    }}
    div[data-testid="stColumn"]:has(.note-marker),
    div[data-testid="column"]:has(.note-marker) {{
        background: #ffffff !important;
        padding: 2.5rem 1.5rem 1.5rem !important;
        border-radius: 4px !important;
        position: relative !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
        margin-bottom: 2rem !important;
        border: 1px solid #ddd !important;
    }}
    div[data-testid="stColumn"]:has(.note-marker)::before,
    div[data-testid="column"]:has(.note-marker)::before {{
        content: "";
        position: absolute;
        top: -12px;
        left: 50%;
        transform: translateX(-50%) rotate(-1.5deg);
        width: 100px;
        height: 28px;
        background: rgba(249, 235, 172, 0.95) !important;
        box-shadow: 1px 1px 3px rgba(0,0,0,0.15) !important;
        border-left: 2px dashed rgba(0,0,0,0.05) !important;
        border-right: 2px dashed rgba(0,0,0,0.05) !important;
        z-index: 10 !important;
        pointer-events: none !important;
    }}
    div[data-testid="stElementContainer"]:has(.note-menu-btn) + div[data-testid="stElementContainer"] {{
        position: absolute !important;
        top: 5px !important;
        right: 5px !important;
        z-index: 20 !important;
    }}
    div[data-testid="stElementContainer"]:has(.note-menu-btn) + div[data-testid="stElementContainer"] button {{
        background: transparent !important;
        border: none !important;
        color: #999 !important;
        font-size: 1.2rem !important;
        padding: 0 !important;
        width: 24px !important; min-width: 24px !important; height: 24px !important;
        box-shadow: none !important;
    }}
    div[data-testid="stElementContainer"]:has(.note-menu-btn) + div[data-testid="stElementContainer"] button:hover {{
        background: rgba(0,0,0,0.05) !important;
        color: #333 !important;
    }}
    div[data-testid="stVerticalBlock"]:has(.note-action-menu) {{
        background: #f9f9f9;
        border-radius: 4px;
        padding: 10px;
        margin-top: 15px;
        border: 1px solid #eee;
    }}
    div[data-testid="stVerticalBlock"]:has(.note-action-menu) button {{ margin-top: 0 !important; }}

    .note-title {{
        font-size: 1.1rem;
        font-weight: 700;
        text-align: left;
        margin-bottom: 0.5rem;
        color: #333;
        border-bottom: 2px solid #f0f0f0;
        padding-bottom: 0.3rem;
    }}
    .note-meta {{
        display: flex;
        justify-content: flex-start;
        font-size: 0.75rem;
        color: #888;
        margin-bottom: 1rem;
        font-weight: 500;
    }}
    .note-content {{
        font-size: 0.9rem;
        line-height: 1.6;
        color: #444;
        min-height: 50px;
        white-space: pre-wrap;
        word-break: keep-all;
    }}

    .search-result-card{{background:{card};border:1px solid {bdr_s};border-radius:12px;padding:1.1rem 1.4rem;margin-bottom:.5rem}}
    .search-result-meta{{display:flex;align-items:center;gap:10px;margin-bottom:.45rem}}
    .search-type-badge{{font-size:.7rem;background:{sbbg};color:{ac2};padding:.15rem .6rem;border-radius:20px;border:1px solid {ac2a}}}
    .search-date{{font-size:.73rem;color:{td}}}
    .search-result-title{{font-size:.97rem;font-weight:600;color:{tp};margin-bottom:.35rem}}
    .search-result-preview{{font-size:.8rem;color:{tm};line-height:1.55}}
    .stSuccess{{background:{succ_bg}!important;border:1px solid {succ_bd}!important;color:{succ_cl}!important;border-radius:8px!important}}

    ::-webkit-scrollbar{{width:4px;height:4px}}
    ::-webkit-scrollbar-track{{background:{bg}}}
    ::-webkit-scrollbar-thumb{{background:{scth};border-radius:3px}}

    #MainMenu{{visibility:hidden}}footer{{visibility:hidden}}header{{visibility:hidden}}

    /* ═══════════════════════════════════════════
       모바일 전용 요소 (데스크톱에서 숨김)
    ═══════════════════════════════════════════ */
    .mob-date-bar{{display:none}}

    /* ═══════════════════════════════════════════
       모바일 최적화 (@media max-width: 768px)
    ═══════════════════════════════════════════ */
    @media(max-width:768px){{

      /* ── 사이드바 → 슬라이드 드로어 ── */
      section[data-testid="stSidebar"]{{
        position:fixed!important;
        top:0!important; bottom:0!important; left:0!important;
        width:84vw!important; max-width:300px!important;
        height:100dvh!important;
        z-index:9999!important;
        overflow-y:auto!important;
        box-shadow:8px 0 40px rgba(0,0,0,.55)!important;
        border-right:1px solid {bdr_s}!important;
      }}

      /* ── 사이드바 닫기(>>) 버튼 숨김 ── */
      section[data-testid="stSidebar"] > div:first-child > div:first-child button:first-child{{
        display:none!important;
      }}

      /* ── 사이드바 열기 FAB (우하단 동그란 버튼) ── */
      [data-testid="collapsedControl"]{{
        position:fixed!important;
        bottom:22px!important; right:22px!important;
        left:auto!important; top:auto!important;
        width:56px!important; height:56px!important;
        background:linear-gradient(135deg,{ac},{ac2})!important;
        border-radius:50%!important;
        box-shadow:0 4px 20px {aca}!important;
        display:flex!important;
        align-items:center!important;
        justify-content:center!important;
        z-index:9998!important;
        transform:none!important;
      }}
      [data-testid="collapsedControl"] svg{{
        color:#fff!important;
        fill:#fff!important;
        width:22px!important; height:22px!important;
      }}

      /* ── 메인 컨텐츠 풀폭 ── */
      .main .block-container{{
        padding:0.75rem 0.75rem 5rem!important;
        max-width:100%!important;
      }}

      /* ── 날짜 바 표시 ── */
      .mob-date-bar{{
        display:flex!important;
        align-items:center;
        justify-content:space-between;
        padding:0.5rem 0 0.9rem;
        border-bottom:1px solid {bdr_s};
        margin-bottom:1rem;
      }}
      .mob-date-bar .mob-logo{{
        font-size:0.88rem;
        font-weight:800;
        color:{ac};
        letter-spacing:0.3px;
      }}
      .mob-date-bar .mob-chip{{
        font-size:0.7rem;
        color:{tm};
        background:{mina};
        padding:0.2rem 0.65rem;
        border-radius:20px;
        border:1px solid {bdr_s};
      }}

      /* ── 페이지 헤더 ── */
      .page-header{{margin-bottom:0.2rem}}
      .page-title{{font-size:1.02rem!important;gap:8px!important}}
      .page-icon{{font-size:1.1rem!important}}
      .page-subtitle{{font-size:0.7rem!important;padding-left:0!important;margin-top:0.1rem!important}}
      .page-divider{{margin:0.5rem 0 1rem!important}}

      /* ── 일기 카드 ── */
      .entry-card{{
        padding:1rem 1.1rem!important;
        border-radius:12px!important;
        margin-bottom:1rem!important;
      }}
      .entry-title{{font-size:1.05rem!important;margin:0.3rem 0 0.6rem!important}}
      .entry-content{{font-size:0.87rem!important;line-height:1.8!important}}
      .entry-photos{{font-size:0.72rem!important;margin-top:0.7rem!important;padding-top:0.6rem!important}}

      /* ── 폼 카드 ── */
      .form-card{{padding:0.85rem!important;margin-bottom:0.8rem!important}}

      /* ── 입력폼 iOS 줌 방지 (font-size 16px 필수) ── */
      .stTextInput input{{font-size:16px!important}}
      .stTextArea textarea{{font-size:16px!important;line-height:1.65!important}}
      [data-testid="stSelectbox"]>div>div{{font-size:16px!important}}

      /* ── 버튼 터치 타깃 ── */
      .main .stButton button{{
        min-height:44px!important;
        border-radius:10px!important;
        font-size:0.85rem!important;
      }}

      /* ── 모드 탭 ── */
      .mode-tabs{{gap:6px!important;margin-bottom:0.7rem!important}}
      .mode-tab{{padding:0.3rem 0.85rem!important;font-size:0.76rem!important}}

      /* ── 달력 날짜 버튼 ── */
      div[data-testid="stElementContainer"]:has(.cal-btn-marker)+div[data-testid="stElementContainer"] button{{
        width:36px!important;min-width:36px!important;max-width:36px!important;
        height:36px!important;min-height:36px!important;
        font-size:0.8rem!important;
      }}

      /* ── 게시판 패딩 ── */
      div[data-testid="stVerticalBlock"]:has(>div:first-child .bulletin-board-wrapper){{
        padding:2rem 0.5rem 1rem!important;
        border:8px solid #6b4c3a!important;
      }}

      /* ── 검색 결과 ── */
      .search-result-card{{padding:0.8rem 0.9rem!important;border-radius:10px!important}}
      .search-result-title{{font-size:0.9rem!important}}
      .search-result-preview{{font-size:0.75rem!important}}

      /* ── 하이라이트 박스 ── */
      .highlight-box{{padding:0.55rem 0.85rem!important;margin:0.5rem 0!important}}
      .highlight-text{{font-size:0.85rem!important}}

      /* ── 빈 상태 ── */
      .empty-state{{padding:2rem 1rem!important}}
      .empty-icon{{font-size:2.2rem!important}}
      .empty-text{{font-size:0.9rem!important}}

      /* ── 스크롤 ── */
      html{{scroll-behavior:smooth;-webkit-overflow-scrolling:touch}}
    }}
    </style>
    """, unsafe_allow_html=True)


inject_css(st.session_state.theme)


# ═══════════════════════════════════════════════════════════════════════════════
#  사이드바
# ═══════════════════════════════════════════════════════════════════════════════
with st.sidebar:

    is_dark = (st.session_state.theme == "dark")
    tm_color = "#6b5e80" if not is_dark else "#aaaaaa"
    st.markdown('<div style="text-align:center;font-size:1.8rem;font-weight:800;margin-bottom:2rem;color:'+tm_color+';letter-spacing:1px;">📓 DATE LOG</div>', unsafe_allow_html=True)

    bc1, bc2 = st.columns(2)
    with bc1:
        st.markdown('<div class="main-nav-marker"></div>', unsafe_allow_html=True)
        if st.button("📔 일기", key="btn_diary", use_container_width=True):
            st.session_state.mode = "diary"; st.session_state.edit_mode = False; st.rerun()
    with bc2:
        st.markdown('<div class="main-nav-marker"></div>', unsafe_allow_html=True)
        if st.button("📌 공유", key="btn_shared", use_container_width=True):
            st.session_state.mode = "shared"; st.session_state.edit_mode = False; st.rerun()

    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)

    year  = st.session_state.cal_year
    month = st.session_state.cal_month

    nc1, nc2, nc3 = st.columns([1, 5, 1])
    with nc1:
        st.markdown('<div class="cal-header-row-marker"></div>', unsafe_allow_html=True)
        st.markdown('<div class="nav-btn-marker"></div>', unsafe_allow_html=True)
        if st.button("‹", key="prev_month"):
            st.session_state.cal_month = 12 if month == 1 else month - 1
            if month == 1: st.session_state.cal_year = year - 1
            st.rerun()
    with nc2:
        st.markdown(f'<div class="cal-header">{year}년 {month}월</div>', unsafe_allow_html=True)
    with nc3:
        st.markdown('<div class="nav-btn-marker"></div>', unsafe_allow_html=True)
        if st.button("›", key="next_month"):
            st.session_state.cal_month = 1 if month == 12 else month + 1
            if month == 12: st.session_state.cal_year = year + 1
            st.rerun()

    day_names  = ["일", "월", "화", "수", "목", "금", "토"]
    day_colors = ["#ff6b6b","#cccccc","#cccccc","#cccccc","#cccccc","#cccccc","#aaaaaa"] if is_dark else ["#e11d48","#555555","#555555","#555555","#555555","#555555","#8b8b9a"]

    dcols = st.columns(7)
    for i, (d, c) in enumerate(zip(day_names, day_colors)):
        dcols[i].markdown(f'<div class="cal-dayname" style="color:{c}">{d}</div>', unsafe_allow_html=True)

    entry_dates = get_all_entry_dates(st.session_state.diaries, st.session_state.shared_notes)
    cal_weeks   = cal_lib.monthcalendar(year, month)
    today       = datetime.date.today()

    for week in cal_weeks:
        wcols = st.columns(7)
        for i, day in enumerate(week):
            with wcols[i]:
                if day == 0:
                    st.markdown('<div class="cal-empty"></div>', unsafe_allow_html=True)
                    continue

                d           = datetime.date(year, month, day)
                is_selected = (d == st.session_state.selected_date)
                is_today    = (d == today)
                has_entry   = (str(d) in entry_dates)

                marker_class = "cal-btn-marker"
                if is_selected: marker_class += " cal-btn-selected"
                elif is_today:  marker_class += " cal-btn-today"

                if i == 0 and not is_selected: marker_class += " cal-btn-sun"
                elif i == 6 and not is_selected: marker_class += " cal-btn-sat"

                if has_entry: marker_class += " cal-btn-has-entry"

                st.markdown(f'<div class="{marker_class}"></div>', unsafe_allow_html=True)
                if st.button(str(day), key=f"day_{d}"):
                    st.session_state.selected_date = d
                    st.session_state.mode = "diary" if st.session_state.mode == "search" else st.session_state.mode
                    st.session_state.edit_mode = False
                    st.session_state.search_query = ""
                    st.rerun()

    sel_str    = str(st.session_state.selected_date)
    has_diary  = sel_str in st.session_state.diaries
    has_shared = sel_str in st.session_state.shared_notes

    if has_diary or has_shared:
        st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
        if has_diary:
            t = st.session_state.diaries[sel_str].get("title", "개인 일기")
            st.markdown(f'<div class="toc-item">📔 {t[:18]}</div>', unsafe_allow_html=True)
        if has_shared:
            t = st.session_state.shared_notes[sel_str].get("title", "공유 노트")
            st.markdown(f'<div class="toc-item">📌 {t[:18]}</div>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)

    search_input = st.text_input("기록 검색", placeholder="🔍 기록 검색...",
                                 key="search_input_box", label_visibility="collapsed")
    if st.button("검색", key="btn_search", use_container_width=True):
        if search_input.strip():
            st.session_state.search_query   = search_input.strip()
            st.session_state.search_results = search_entries(
                search_input.strip(), st.session_state.diaries, st.session_state.shared_notes)
            st.session_state.mode = "search"; st.session_state.edit_mode = False; st.rerun()

    st.markdown('<div style="flex:1;min-height:20px"></div>', unsafe_allow_html=True)

    # 디버그 상태 표시
    if "_load_debug" in st.session_state:
        st.caption(st.session_state._load_debug)

    st.markdown('<div class="settings-panel">', unsafe_allow_html=True)
    st.markdown('<div class="settings-title">⚙️ 환경 설정</div>', unsafe_allow_html=True)
    lbl = "☀️ 라이트 모드로 전환" if is_dark else "🌙 다크 모드로 전환"
    if st.button(lbl, key="btn_theme", use_container_width=True):
        st.session_state.theme = "light" if is_dark else "dark"; st.rerun()
    cur = "🌙 다크" if is_dark else "☀️ 라이트"
    st.markdown(f'<div style="text-align:center;font-size:.68rem;color:#888;margin-top:4px">현재: {cur} 모드</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
#  메인 콘텐츠
# ═══════════════════════════════════════════════════════════════════════════════

def render_mode_tabs():
    m = st.session_state.mode
    dc = "mode-tab mode-tab-active" if m == "diary"  else "mode-tab mode-tab-inactive"
    sc = "mode-tab mode-tab-active" if m == "shared" else "mode-tab mode-tab-inactive"
    qc = "mode-tab mode-tab-active" if m == "search" else "mode-tab mode-tab-inactive"
    h  = f'<div class="mode-tabs"><span class="{dc}">📔 일기</span><span class="{sc}">📌 공유</span>'
    if m == "search": h += f'<span class="{qc}">🔍 검색</span>'
    h += "</div>"
    st.markdown(h, unsafe_allow_html=True)


def render_diary_page():
    sel     = st.session_state.selected_date
    sel_str = str(sel)
    wn      = ["월","화","수","목","금","토","일"]
    dlbl    = f"{sel.year}년 {sel.month}월 {sel.day}일 ({wn[sel.weekday()]})"

    st.markdown(f'<div class="page-header"><div class="page-title"><span class="page-icon">📔</span><span>{dlbl} 일기</span></div><div class="page-subtitle">나만의 소중한 기록</div></div><div class="page-divider"></div>', unsafe_allow_html=True)

    entry = st.session_state.diaries.get(sel_str, {})

    if st.session_state.edit_mode:
        st.markdown('<div class="form-card">', unsafe_allow_html=True)
        title   = st.text_input("제목", value=entry.get("title",""), placeholder="오늘의 제목을 입력해 주세요 ✨", key="diary_title")
        moods   = ["😍 설레","😊 행복","🥰 사랑스러워","😢 슬퍼","😐 그냥 그래","🌟 최고야"]
        mood    = st.selectbox("오늘의 기분", moods, index=moods.index(entry["mood"]) if entry.get("mood") in moods else 1, key="diary_mood")
        place   = st.text_input("📍 장소", value=entry.get("place",""), placeholder="어디 다녀왔나요?", key="diary_place")
        content = st.text_area("일기 내용", value=entry.get("content",""), placeholder="오늘 하루는 어땠나요? 자유롭게 기록해 보세요 💭", height=280, key="diary_content")
        photos  = st.text_input("📸 사진 메모 (선택)", value=entry.get("photos",""), placeholder="사진 설명이나 메모를 남겨보세요", key="diary_photos")
        st.markdown('</div>', unsafe_allow_html=True)
        cs, cc = st.columns(2)
        with cs:
            if st.button("💾 저장하기", key="save_diary", use_container_width=True):
                st.session_state.diaries[sel_str] = {"title":title,"mood":mood,"place":place,"content":content,"photos":photos,"date":sel_str}
                result = save_diary_entry(sel_str, title, content, mood=mood, place=place, photos=photos)
                st.session_state.edit_mode = False
                st.session_state.save_result = result   # rerun 후 메시지 표시용
                st.rerun()
        # 저장 결과 메시지 (rerun 후 표시)
        if "save_result" in st.session_state:
            result = st.session_state.pop("save_result")
            if result is True:
                st.success("구글 드라이브에 안전하게 기록되었습니다! 💕")
            elif isinstance(result, str) and result.startswith("로컬 저장 완료"):
                st.warning(f"💾 {result}")
            else:
                st.error(f"저장 실패: {result}")
        with cc:
            if st.button("✖ 취소", key="cancel_diary", use_container_width=True):
                st.session_state.edit_mode = False; st.rerun()
    elif not entry:
        st.markdown(f'<div class="empty-state"><div class="empty-icon">📝</div><div class="empty-text">{dlbl}의 일기가 없어요</div></div>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1.5, 1, 1.5])
        with col2:
            if st.button("✨ 추가하기", key="new_diary", use_container_width=True):
                st.session_state.edit_mode = True; st.rerun()
    else:
        ph = f"<span class='entry-place'>📍 {entry['place']}</span>" if entry.get("place") else ""
        fh = f"<div class='entry-photos'>📸 {entry['photos']}</div>" if entry.get("photos") else ""
        st.markdown(f'<div class="entry-card"><div class="entry-meta"><span class="entry-mood">{entry.get("mood","")}</span>{ph}</div><h2 class="entry-title">{entry.get("title","제목 없음")}</h2><div class="entry-content">{entry.get("content","").replace(chr(10),"<br>")}</div>{fh}</div>', unsafe_allow_html=True)
        ce, cd = st.columns([3,1])
        with ce:
            if st.button("✏️ 수정하기", key="edit_diary", use_container_width=True):
                st.session_state.edit_mode = True; st.rerun()
        with cd:
            if st.button("🗑️ 삭제", key="del_diary", use_container_width=True):
                del st.session_state.diaries[sel_str]; st.rerun()


import uuid

def render_shared_page():
    st.markdown(f'<div class="page-header"><div class="page-title"><span class="page-icon">📌</span><span>공유 게시판</span></div><div class="page-subtitle">계속해서 누적되는 우리만의 정보 보드 📝</div></div><div class="page-divider"></div>', unsafe_allow_html=True)

    if st.session_state.edit_mode:
        st.markdown('<div class="form-card">', unsafe_allow_html=True)
        note_id  = st.session_state.get("editing_shared_id", str(uuid.uuid4()))
        existing = st.session_state.shared_notes.get(note_id, {})

        title   = st.text_input("제목", value=existing.get("title",""), placeholder="정보의 제목", key="shared_title")
        dt_val  = datetime.date.fromisoformat(existing.get("date")) if existing.get("date") else datetime.date.today()
        dt      = st.date_input("업로드 날짜", value=dt_val, key="shared_date")
        content = st.text_area("내용", value=existing.get("content",""), placeholder="공유할 내용을 적어보세요", height=220, key="shared_content")
        st.markdown('</div>', unsafe_allow_html=True)
        cs, cc = st.columns(2)
        with cs:
            if st.button("💾 핀 꽂기", key="save_shared", use_container_width=True):
                st.session_state.shared_notes[note_id] = {
                    "id": note_id, "title": title, "date": str(dt), "content": content
                }
                save_shared_entry(note_id, title, str(dt), content)
                st.session_state.edit_mode = False; st.rerun()
        with cc:
            if st.button("✖ 취소", key="cancel_shared", use_container_width=True):
                st.session_state.edit_mode = False; st.rerun()
    else:
        notes = []
        for k, v in st.session_state.shared_notes.items():
            if isinstance(v, dict):
                v_copy = v.copy()
                if "id" not in v_copy: v_copy["id"] = k
                notes.append(v_copy)

        notes.sort(key=lambda x: x.get("date", ""), reverse=True)

        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            if st.button("✨ 새로운 정보 핀 꽂기", use_container_width=True):
                st.session_state.editing_shared_id = str(uuid.uuid4())
                st.session_state.edit_mode = True
                st.rerun()

        if not notes:
            st.markdown(f'<div class="empty-state"><div class="empty-icon">📌</div><div class="empty-text">게시판이 텅 비었어요. 새로운 정보를 꽂아보세요!</div></div>', unsafe_allow_html=True)
            return

        with st.container():
            st.markdown('<div class="bulletin-board-wrapper"></div>', unsafe_allow_html=True)
            grid = st.columns(2)
            for i, n in enumerate(notes):
                col = grid[i % 2]
                with col:
                    st.markdown(f'<div class="note-marker"></div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="note-menu-btn"></div>', unsafe_allow_html=True)
                    if st.button("⋮", key=f"menu_{n['id']}", help="메뉴"):
                        if st.session_state.get("show_menu_for") == n['id']:
                            st.session_state.show_menu_for = None
                        else:
                            st.session_state.show_menu_for = n['id']
                        st.rerun()

                    st.markdown(f"""
                        <h2 class="note-title">{n.get("title","제목 없음")}</h2>
                        <div class="note-meta"><span>📅 {n.get("date","")}</span></div>
                        <div class="note-content">{n.get("content","").replace(chr(10),"<br>")}</div>
                    """, unsafe_allow_html=True)

                    if st.session_state.get("show_menu_for") == n['id']:
                        st.markdown('<div class="note-action-menu"></div>', unsafe_allow_html=True)
                        bc1, bc2 = st.columns(2)
                        with bc1:
                            if st.button("✏️ 수정", key=f"edit_{n['id']}", use_container_width=True):
                                st.session_state.editing_shared_id = n['id']
                                st.session_state.edit_mode = True
                                st.session_state.show_menu_for = None
                                st.rerun()
                        with bc2:
                            if st.button("🗑️ 삭제", key=f"del_{n['id']}", use_container_width=True):
                                delete_shared_entry(n['id'])
                                del st.session_state.shared_notes[n['id']]
                                st.session_state.show_menu_for = None
                                st.rerun()


def render_search_page():
    query   = st.session_state.search_query
    results = st.session_state.search_results
    st.markdown(f'<div class="page-header"><div class="page-title"><span class="page-icon">🔍</span><span>"{query}" 검색 결과</span></div><div class="page-subtitle">총 {len(results)}개의 기록을 찾았어요</div></div><div class="page-divider"></div>', unsafe_allow_html=True)

    if not results:
        st.markdown('<div class="empty-state"><div class="empty-icon">🔍</div><div class="empty-text">검색 결과가 없어요</div><div class="empty-sub">다른 키워드로 검색해 보세요</div></div>', unsafe_allow_html=True)
        return

    for r in results:
        icon  = "📔" if r["type"] == "diary" else "📌"
        label = "개인 일기" if r["type"] == "diary" else "공유 노트"
        d     = datetime.date.fromisoformat(r["date"])
        dlbl  = f"{d.year}년 {d.month}월 {d.day}일"
        st.markdown(f'<div class="search-result-card"><div class="search-result-meta"><span class="search-type-badge">{icon} {label}</span><span class="search-date">{dlbl}</span></div><div class="search-result-title">{r.get("title","제목 없음")}</div><div class="search-result-preview">{r.get("preview","")}</div></div>', unsafe_allow_html=True)
        if st.button(f"📖 보러가기 ({dlbl})", key=f"goto_{r['date']}_{r['type']}"):
            st.session_state.selected_date = d; st.session_state.mode = r["type"]; st.session_state.edit_mode = False; st.rerun()
        st.markdown("<br>", unsafe_allow_html=True)


# ── 라우팅 ────────────────────────────────────────────────────────────────────

# 모바일 날짜 바 (CSS로 데스크톱에서 숨김, 모바일에서만 표시)
_sel = st.session_state.selected_date
_wn  = ["월","화","수","목","금","토","일"]
_dlabel = f"{_sel.month}월 {_sel.day}일 ({_wn[_sel.weekday()]})"
st.markdown(
    f'<div class="mob-date-bar">'
    f'<span class="mob-logo">💕 DATE LOG</span>'
    f'<span class="mob-chip">{_dlabel}</span>'
    f'</div>',
    unsafe_allow_html=True
)

render_mode_tabs()
mode = st.session_state.mode
if   mode == "diary":  render_diary_page()
elif mode == "shared": render_shared_page()
elif mode == "search": render_search_page()
