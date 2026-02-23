#!/usr/bin/env python3
import os,sys,datetime,json,requests,re
from pathlib import Path

CONFIG=Path(__file__).parent/'config.json'
if CONFIG.exists():
    cfg=json.loads(CONFIG.read_text())
else:
    cfg={}
HISTORY=cfg.get('history_path',str(Path(__file__).parent/'history.csv'))

# Simple fetcher: tries a list of candidate URLs (can be extended).
# For robustness, if remote fetch fails, the script exits quietly.

def fetch_lotto_results(lotto_name):
    # This function attempts to fetch latest winning numbers for given lotto.
    # It tries some well-known public pages; if none work, returns None.
    try:
        if 'Max' in lotto_name:
            # example source: https://www.lottocanada.ca/lotto-max
            url='https://www.lottocanada.ca/lotto-max/results'
        else:
            url='https://www.lottocanada.ca/lotto-649/results'
        r=requests.get(url, timeout=8)
        txt=r.text
        # naive regex to find sequences of numbers 1..50
        nums=re.findall(r'\b([0-9]{1,2})\b', txt)
        nums=[int(n) for n in nums if 1<=int(n)<=60]
        # best-effort: pick first 7 or 6 unique numbers found
        seen=[]
        for n in nums:
            if n not in seen:
                seen.append(n)
            if len(seen)>=7:
                break
        if not seen:
            return None
        # slice appropriate count
        count=7 if 'Max' in lotto_name else 6
        return seen[:count]
    except Exception:
        return None


def compare_and_notify(lotto_name, winning_numbers):
    # Load history and find last recommendation for same lotto
    path=Path(HISTORY)
    last_rec=None
    if path.exists():
        with path.open('r',encoding='utf-8') as f:
            lines=[l.strip() for l in f if l.strip()]
        # parse last line matching lotto_name
        for line in reversed(lines):
            parts=line.split('\t')
            if len(parts)>=3 and parts[1]==lotto_name:
                # parts: ts, lotto, picks, reasons...
                picks=parts[2].split(',')
                picks=[int(x) for x in picks if x]
                last_rec={'ts':parts[0],'picks':picks}
                break
    matches=[]
    if last_rec and winning_numbers:
        matches=[n for n in last_rec['picks'] if n in winning_numbers]
    # record result
    ts=datetime.datetime.now().isoformat()
    record=[ts, lotto_name, ','.join(map(str,last_rec['picks'])) if last_rec else '', ','.join(map(str,winning_numbers)) if winning_numbers else '', str(len(matches)), ','.join(map(str,matches))]
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('a',encoding='utf-8') as f:
        f.write('\t'.join(record)+"\n")
    # notify via telegram if env set
    token=os.environ.get('TELEGRAM_BOT_TOKEN')
    chat_id=os.environ.get('TELEGRAM_CHAT_ID')
    msg=f"[{lotto_name}] 결과 확인: {','.join(map(str,winning_numbers)) if winning_numbers else '조회 실패'}\n"
    if last_rec:
        msg+=f"추천(마지막): {','.join(map(str,last_rec['picks']))}\n"
        msg+=f"맞춘 개수: {len(matches)}; 일치: {','.join(map(str,matches)) if matches else '없음'}\n"
    if token and chat_id:
        try:
            requests.post(f'https://api.telegram.org/bot{token}/sendMessage', data={'chat_id':chat_id,'text':msg})
        except Exception:
            pass
    else:
        print(msg)

if __name__=='__main__':
    # run for both lotto types by default
    for entry in [{'name':'Lotto Max','count':7},{'name':'Lotto 6/49','count':6}]:
        res=fetch_lotto_results(entry['name'])
        compare_and_notify(entry['name'], res)
