import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

_DIR = os.path.dirname(os.path.abspath(__file__))
GOOGLE_KEY_FILE    = os.path.join(_DIR, "google_key.json")
LOCAL_DATA_FILE    = os.path.join(_DIR, "diary_local.json")
LOCAL_SHARED_FILE  = os.path.join(_DIR, "shared_local.json")

SHEET_NAME        = "couple_diary_data"
SHARED_SHEET_NAME = "couple_diary_share"
HEADERS        = ["날짜", "제목", "기분", "장소", "내용", "사진메모"]
SHARED_HEADERS = ["ID", "제목", "날짜", "내용"]

SAMPLE_DIARY  = {}
SAMPLE_SHARED = {}


# ── 로컬 JSON ────────────────────────────────────────────────────────────────
def _local_load():
    try:
        with open(LOCAL_DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def _local_save(data: dict):
    try:
        with open(LOCAL_DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"일기 로컬 저장 에러: {e}")

def _local_load_shared():
    try:
        with open(LOCAL_SHARED_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def _local_save_shared(data: dict):
    try:
        with open(LOCAL_SHARED_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"공유 로컬 저장 에러: {e}")


# ── Google Sheets 클라이언트 ──────────────────────────────────────────────────
def _get_gc():
    scope = ["https://spreadsheets.google.com/feeds",
             "https://www.googleapis.com/auth/drive"]
    # 1순위: Streamlit Secrets (클라우드 배포)
    try:
        import streamlit as st
        if "gcp_service_account" in st.secrets:
            creds = ServiceAccountCredentials.from_json_keyfile_dict(
                dict(st.secrets["gcp_service_account"]), scope
            )
            return gspread.authorize(creds)
    except Exception:
        pass
    # 2순위: 로컬 google_key.json 파일
    try:
        if os.path.exists(GOOGLE_KEY_FILE):
            creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_KEY_FILE, scope)
            return gspread.authorize(creds)
    except Exception as e:
        print(f"Google 인증 에러: {e}")
    return None

def _open_sheet(gc, name, headers):
    """이름으로 시트를 열고 워크시트를 반환. 없으면 None."""
    try:
        sh = gc.open(name)
    except gspread.SpreadsheetNotFound:
        return None
    ws = sh.get_worksheet(0)
    if not ws.row_values(1):
        ws.append_row(headers)
    return ws


# ── 일기 ─────────────────────────────────────────────────────────────────────
def save_diary_entry(date_str, title, content, mood="", place="", photos=""):
    """로컬 저장 후 Google Sheets 동기화."""
    local = _local_load()
    local[str(date_str)] = {
        "title": title, "mood": mood, "place": place,
        "content": content, "photos": photos, "date": str(date_str),
    }
    _local_save(local)

    try:
        gc = _get_gc()
        if gc is None:
            return "google_key.json 없음"
        ws = _open_sheet(gc, SHEET_NAME, HEADERS)
        if ws is None:
            return "couple_diary_data 시트를 찾을 수 없어요"
        row = [str(date_str), str(title), str(mood), str(place), str(content), str(photos)]
        all_vals = ws.get_all_values()
        for i, r in enumerate(all_vals[1:], start=2):
            if r and r[0] == str(date_str):
                ws.update(f"A{i}:F{i}", [row])
                return True
        ws.append_row(row)
        return True
    except Exception as e:
        return f"로컬 저장 완료 (구글 동기화 실패: {e})"

def load_diary_entries():
    """Google Sheets 우선, 실패 시 로컬."""
    try:
        gc = _get_gc()
        if gc:
            ws = _open_sheet(gc, SHEET_NAME, HEADERS)
            if ws:
                all_vals = ws.get_all_values()
                if len(all_vals) >= 2:
                    header = all_vals[0]
                    def col(r, name):
                        try:
                            return r[header.index(name)] if name in header else ""
                        except (ValueError, IndexError):
                            return ""
                    diaries = {}
                    for r in all_vals[1:]:
                        r = r + [""] * (6 - len(r))
                        ds = r[0].strip()
                        if not ds:
                            continue
                        diaries[ds] = {
                            "title":   col(r, "제목"),
                            "mood":    col(r, "기분"),
                            "place":   col(r, "장소"),
                            "content": col(r, "내용"),
                            "photos":  col(r, "사진메모"),
                            "date":    ds,
                        }
                    if diaries:
                        _local_save(diaries)
                    return diaries
    except Exception as e:
        print(f"일기 구글 로드 에러: {e}")
    return _local_load()


# ── 공유 노트 ────────────────────────────────────────────────────────────────
def save_shared_entry(note_id, title, date_str, content):
    """공유 노트를 로컬 저장 후 Google Sheets 동기화."""
    local = _local_load_shared()
    local[note_id] = {"id": note_id, "title": title, "date": date_str, "content": content}
    _local_save_shared(local)

    try:
        gc = _get_gc()
        if gc is None:
            return "google_key.json 없음"
        ws = _open_sheet(gc, SHARED_SHEET_NAME, SHARED_HEADERS)
        if ws is None:
            return "couple_diary_share 시트를 찾을 수 없어요"
        row = [str(note_id), str(title), str(date_str), str(content)]
        all_vals = ws.get_all_values()
        for i, r in enumerate(all_vals[1:], start=2):
            if r and r[0] == str(note_id):
                ws.update(f"A{i}:D{i}", [row])
                return True
        ws.append_row(row)
        return True
    except Exception as e:
        return f"로컬 저장 완료 (구글 동기화 실패: {e})"

def delete_shared_entry(note_id):
    """공유 노트를 로컬 + Google Sheets에서 삭제."""
    local = _local_load_shared()
    local.pop(note_id, None)
    _local_save_shared(local)

    try:
        gc = _get_gc()
        if gc is None:
            return
        ws = _open_sheet(gc, SHARED_SHEET_NAME, SHARED_HEADERS)
        if ws is None:
            return
        all_vals = ws.get_all_values()
        for i, r in enumerate(all_vals[1:], start=2):
            if r and r[0] == str(note_id):
                ws.delete_rows(i)
                break
    except Exception as e:
        print(f"공유 노트 삭제 에러: {e}")

def load_shared_entries():
    """Google Sheets 우선, 실패 시 로컬."""
    try:
        gc = _get_gc()
        if gc:
            ws = _open_sheet(gc, SHARED_SHEET_NAME, SHARED_HEADERS)
            if ws:
                all_vals = ws.get_all_values()
                if len(all_vals) >= 2:
                    header = all_vals[0]
                    def col(r, name):
                        try:
                            return r[header.index(name)] if name in header else ""
                        except (ValueError, IndexError):
                            return ""
                    shared = {}
                    for r in all_vals[1:]:
                        r = r + [""] * (4 - len(r))
                        nid = r[0].strip()
                        if not nid:
                            continue
                        shared[nid] = {
                            "id":      nid,
                            "title":   col(r, "제목"),
                            "date":    col(r, "날짜"),
                            "content": col(r, "내용"),
                        }
                    if shared:
                        _local_save_shared(shared)
                    return shared
    except Exception as e:
        print(f"공유 노트 구글 로드 에러: {e}")
    return _local_load_shared()


# ── 검색 / 날짜 목록 ──────────────────────────────────────────────────────────
def search_entries(query, diaries=None, shared_notes=None):
    results = []
    q = query.lower()
    if diaries:
        for ds, entry in diaries.items():
            if isinstance(entry, dict):
                if q in entry.get("title","").lower() or q in entry.get("content","").lower():
                    results.append({"type":"diary","date":ds,
                                    "title":entry.get("title",""),
                                    "preview":entry.get("content","")[:100]})
    if shared_notes:
        for nid, note in shared_notes.items():
            if isinstance(note, dict):
                if q in note.get("title","").lower() or q in note.get("content","").lower():
                    results.append({"type":"shared","date":note.get("date",""),
                                    "title":note.get("title",""),
                                    "preview":note.get("content","")[:100]})
    return results

def get_all_entry_dates(diaries=None, shared_notes=None):
    dates = set()
    if diaries:
        dates.update(str(d) for d in diaries.keys())
    if shared_notes:
        for note in shared_notes.values():
            if isinstance(note, dict) and note.get("date"):
                dates.add(str(note["date"]))
    return list(dates)