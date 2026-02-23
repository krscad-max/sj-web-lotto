#!/usr/bin/env python3
import requests,re,csv
from pathlib import Path
import time

OUT=Path(__file__).resolve().parent.parent/'web-lotto'/'data'
OUT.mkdir(parents=True,exist_ok=True)

sources={
    '649':{
        'url':'https://www.magayo.com/lotto/canada/lotto-649-results/',
        'want':6,
        'out':'lotto_649.csv'
    },
    'max':{
        'url':'https://www.magayo.com/lotto/canada/lotto-max-results/',
        'want':7,
        'out':'lotto_max.csv'
    }
}

def fetch_with_retry(url, attempts=3, backoff=1.5):
    last_exc=None
    headers={'User-Agent':'Mozilla/5.0 (compatible; Fetcher/1.0)'}
    for i in range(attempts):
        try:
            r=requests.get(url,headers=headers,timeout=10)
            if r.status_code==200 and r.text:
                return r.text
            last_exc=Exception(f'Status {r.status_code}')
        except Exception as e:
            last_exc=e
        time.sleep(backoff*(i+1))
    raise last_exc

def parse_draw_from_text(txt,want):
    # normalize: remove tags and collapse whitespace
    text_only=re.sub(r'<[^>]+>',' ',txt)
    text_only=re.sub(r'<[^>]+>',' ',txt)
    text_only=re.sub(r'\s+',' ',text_only)
    # Try to find the first contiguous run of numbers (6 or 7 numbers close together)
    runs=re.findall(r'((?:\b\d{1,2}\b\D{0,10}){'+str(want)+'})', text_only)
    for run in runs:
        nums=[int(n) for n in re.findall(r"(\d{1,2})", run) if 1<=int(n)<=60]
        # dedupe preserving order
        seen=[]
        for n in nums:
            if n not in seen:
                seen.append(n)
        if len(seen)>=want:
            return seen[:want]
    return None

for key,info in sources.items():
    url=info['url']; want=info['want']; outf=OUT/info['out']
    try:
        txt = fetch_with_retry(url)
        draw = parse_draw_from_text(txt,want)
        if draw:
            # write a timestamped row (ISO)
            row=[time.strftime('%Y-%m-%dT%H:%M:%S'),]+[str(n) for n in draw]
            with outf.open('a',encoding='utf-8') as f:
                f.write(','.join(row)+"\n")
            print('wrote',str(outf),draw)
        else:
            print('parse failed for',key,'- saving sample snapshot for debugging')
            dbg=OUT/('debug_'+key+'.html')
            dbg.write_text(txt,encoding='utf-8')
            try:
                send_telegram_alert(f'web-lotto: parse failed for {key} at {time.strftime("%Y-%m-%dT%H:%M:%S")} (saved debug file)')
            except Exception:
                pass
    except Exception as e:
        print('error fetching',key,':',e)
def send_telegram_alert(text):
    import os
    token=os.environ.get('TELEGRAM_BOT_TOKEN')
    chat=os.environ.get('TELEGRAM_CHAT_ID')
    if not token or not chat:
        return False
    try:
        requests.post(f'https://api.telegram.org/bot{token}/sendMessage', data={'chat_id':chat,'text':text}, timeout=6)
        return True
    except Exception:
        return False
