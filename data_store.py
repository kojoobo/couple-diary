import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

_DIR = os.path.dirname(os.path.abspath(__file__))
LOCAL_DATA_FILE    = os.path.join(_DIR, "diary_local.json")
LOCAL_SHARED_FILE  = os.path.join(_DIR, "shared_local.json")

SHEET_NAME        = "couple_diary_data"
SHARED_SHEET_NAME = "couple_diary_share"
HEADERS        = ["날짜", "제목", "기분", "장소", "내용", "사진메모"]
SHARED_HEADERS = ["ID", "제목", "날짜", "내용"]

SAMPLE_DIARY  = {}
SAMPLE_SHARED = {}

# 🔒 서버가 문법 오류를 일으키지 않도록 줄바꿈(\n)을 한 줄로 완벽히 정제한 열쇠 데이터입니다.
GOOGLE_KEY_DATA = {
  "type": "service_account",
  "project_id": "couple-diary-498504",
  "private_key_id": "2bc7227f572d7e2b62f3e62cf5de757638792a39",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDdqPA2/EFmfjNr\na7dFhQsTwLujKYJG3zZPdSPeX7XgiloloqZzOhA0on+iFaN8OKDH7YsiF1pq3bO6\ns21xCvjnLOHv49pWlLRsUdnsnv/MheJRwCTnNuxiZ/pziSaBE3KKnVKwauyWITJa\nqhmVYB0bZPkWvThToO66SmPQJao5O4I3QRnzB3TTjE+bFdHm8ShLwRyB8kxpbxoy\nvhzd1Ef9hPZhY9J9mxDF1K0wh+f79MKum0oeUG3h7vjkD4mgBOW2aj3DeXJdlzMs\nXVm9JieSHH4SkaTG7lqj9y2otE0hnniDBTHAQjkuib/hLbEE7bQXB9klEmFbsao8\n9/8X820TAgMBAAECggEAEhkN8YD1VAl5m37L4KMeuh0/FL2gYFBip+hc2XZMeTAp\nCrA16x8lnWHBJ9PT3KIamohHsMZh89GOYzy5v4ReUzDkCtXUCPd5dB8KVIDQF0i9\nJ3oxNfTTJkVU4RcLHxHRhQWYVhG82sfy5Q0rXpNefQY1aKJiO9qRc06WL+bLXoKM\ngMxxd3+oTXd6JgFJgAnCZVI7Kh6U7qF2c1I7tPp4osvxMqRjlC1jJSF5Ic5KyUhN\nucZCNuNke/mY9PKcAWFgrOLvaoolgNT+v58s6bjg8Xkks++2f7s9RU669F3+EKs7\nHyL3A2Eo8vnTgbqhLjkuDvnCkeZ72CQE12iaZZQFfQKBgQD4g7cUKGsFM1mSqiHw\n699IB9MGjEb2CUXhR1aU5jWxMeQhu9aYNLdujF0t+hDABpvDQXhcSmR7WVfHzZgA\nbkrciccfiL7r2HOQ+qlQdc9pdpF0+/3mvdqe9jOEgKNZWRWog+5s+n3zacufLvAM\nIC2YCiOhqAKFraghP08yCA2CxwKBgQDkViYGKGes5EFICz2IMFR3XfNCGzCcDEY9\nWvWZC+Qwg8A3LcxF/k3yswiTeGGvTkmFNYjkLP6N/BVDutOO6qwFJwx2UW1FswyB\n6gAtALHzd/JUE85o6EZE2udQk45q3+G38COKSa8SetAfQOjxhS1x2SnSDNXdvtYj\njJxC4m/3VQKBgBO09jauAdaWvNqpjSl6uukOXcieJR5rm9QCgTYrj0Ru7WVTbPAC\n9izZCqaTtvJTU9THA1FmQNObQR/CCPS3yk30ywqQIHu5XWi4x+ZugTUexugc94Rt\nt8F1Sp6OSOXT76i+VZDkyEoeMJx972E2yAbPfwXZueF55ORGDfSsuM2PAoGBANBf\nab3O26Xke0qir1l8OWjhPOAD7h1J+kN9oYk0V96KLTxtt+/b/ghQp6/keMjBWciN\nrUoFYZvzAvjXIr9Wmvrswquq7Vxg5DYedGCdNMfpmyRtGr2T0qR9XAClV59ihhsU\ns2o8id8EYq9SzgGyNmGh+08r1XPR9ptkcyl6eREtAoGAa3+tqOvcZ1XDfoTEy/1r\n3E6duXu6DxqbKnYfiyMLDEqtIB8wYGqzj5XYrjrWHFjl6xwbwvh1IoQkZ4f8V8rz\nuee2v8c2fM7BLY1p2mgA7t8HgM1HddK8UVHIxaZC26fO0liy4WxWNHwtr/ltg79z\ns7HCNHQqRE+injR5D60DEOQ=\n-----END PRIVATE KEY-----\n",
  "client_email": "couple-diary@couple-diary-498504.iam.gserviceaccount.com",
  "client_id": "109513363273693200624",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/couple-diary%40couple-diary-498504.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

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
    try:
        scope = ["https://spreadsheets.google.com/feeds",
                 "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(GOOGLE_KEY_DATA, scope)
        return gspread.authorize(creds)
    except Exception as e:
        print(f"Google 인증 에러: {e}")
        return None

def _open_sheet(gc, name, headers):
    try:
        sh = gc.open(name)
    except gspread.SpreadsheetNotFound:
        sh = gc.create(name)
    ws = sh.get_worksheet(0)
    if not ws.row_values(1):
        ws.append_row(headers)
    return ws


# ── 일기 ─────────────────────────────────────────────────────────────────────
def save_diary_entry(date_str, title, content, mood="", place="", photos=""):
    local = _local_load()
    local[str(date_str)] = {
        "title": title, "mood": mood, "place": place,
        "content": content, "photos": photos, "date": str(date_str),
    }
    _local_save(local)

    try:
        gc = _get_gc()
        if gc is None:
            return "google_key.json 인증 실패"
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
    local = _local_load_shared()
    local[note_id] = {"id": note_id, "title": title, "date": date_str, "content": content}
    _local_save_shared(local)

    try:
        gc = _get_gc()
        if gc is None:
            return "google_key.json 인증 실패"
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