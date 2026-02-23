#!/usr/bin/env python3
import os,sys,random,json,datetime,urllib.request
from pathlib import Path

def load_config():
    cfg_path=Path(__file__).parent/'config.json'
    return json.loads(cfg_path.read_text())

def get_temp():
    try:
        with urllib.request.urlopen('https://wttr.in/Edmonton?format=j1', timeout=6) as r:
            j=json.load(r)
            return int(float(j['current_condition'][0]['temp_C']))
    except Exception:
        return None

# simple generator
FREQ=[3,7,11,18,22,29,33,41,45,49]

def generate(max_num,count,temp=None):
    half=(count+1)//2
    picks=set()
    picks.update(random.sample(FREQ, min(half,len(FREQ))))
    pool=set()
    now=datetime.datetime.now()
    day=now.day
    hour=now.hour
    minute=now.minute
    pool.add((day%max_num) or 1)
    if temp is not None:
        pool.add((abs(temp)%max_num) or 1)
    pool.add((hour%max_num) or 1)
    pool.add((minute%max_num) or 1)
    for _ in range(30):
        pool.add(random.randint(1,max_num))
    while len(picks)<count:
        picks.add(random.choice(list(pool)))
    picks_list=sorted(picks)
    reasons={}
    for n in picks_list:
        r=[]
        if n in FREQ:
            r.append('과거 5회 중 자주 등장한 후보')
        if temp is not None and (n==((abs(temp)%max_num) or 1)):
            r.append(f'오늘 기온 {temp}°C에서 파생')
        if n==((day%max_num) or 1):
            r.append(f'오늘 날짜 {day}에서 파생')
        if n==((hour%max_num) or 1):
            r.append('현재 시간에서 파생')
        if not r:
            r.append('랜덤 추출')
        reasons[n]='; '.join(r)
    return picks_list,reasons


def send_telegram(token,chat_id,text):
    import requests
    url=f'https://api.telegram.org/bot{token}/sendMessage'
    resp=requests.post(url,data={'chat_id':chat_id,'text':text})
    return resp.ok


def append_history(path,lotto,picks,reasons):
    p=Path(path)
    p.parent.mkdir(parents=True,exist_ok=True)
    ts=datetime.datetime.now().isoformat()
    line=[ts,lotto,','.join(map(str,picks)),json.dumps(reasons,ensure_ascii=False)]
    with p.open('a',encoding='utf-8') as f:
        f.write('\t'.join(line)+"\n")

if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser()
    ap.add_argument('--lotto',required=True)
    ap.add_argument('--count',type=int,required=True)
    args=ap.parse_args()
    cfg=load_config()
    temp=get_temp()
    max_num = 50 if 'Max' in args.lotto else 49
    picks,reasons=generate(max_num,args.count,temp)
    lines=[f"{args.lotto} 추천 ({datetime.datetime.now().strftime('%Y-%m-%d %H:%M')})"]
    if temp is not None:
        lines.append(f"(Edmonton 현재 기온: {temp}°C)")
    lines.append('추천번호: '+', '.join(map(str,picks)))
    lines.append('선정 이유:')
    for p in picks:
        lines.append(f"- {p}: {reasons[p]}")
    body='\n'.join(lines)
    # save history
    append_history(cfg.get('history_path','history.csv'),args.lotto,picks,reasons)
    # send if env set
    token=os.environ.get('TELEGRAM_BOT_TOKEN')
    chat_id=os.environ.get('TELEGRAM_CHAT_ID')
    if token and chat_id:
        ok=send_telegram(token,chat_id,body)
        if not ok:
            print('Telegram send failed, printing message:\n')
            print(body)
    else:
        print('No TELEGRAM env set — printing message:\n')
        print(body)
