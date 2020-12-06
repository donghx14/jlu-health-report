import requests, json, time, re, argparse
from bs4 import BeautifulSoup

login_url = 'https://ehall.jlu.edu.cn/sso/login'
form_url = 'https://ehall.jlu.edu.cn/infoplus/form/YJSMRDK/start'
start_url = 'https://ehall.jlu.edu.cn/infoplus/interface/start'
render_url = 'https://ehall.jlu.edu.cn/infoplus/interface/render'
action_url = 'https://ehall.jlu.edu.cn/infoplus/interface/doAction'

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36 Edg/87.0.664.47'

def check(username, password):
    for _ in range(10):
        try:
            s = requests.Session()

            headers = {'User-Agent': UA}

            #获取pid
            login_html = s.get(url=login_url, headers=headers)
            soup = BeautifulSoup(login_html.text, 'lxml')
            pid = soup.find(name="input", attrs={"name" :"pid"}).get('value')

            #登录
            data = {'username': username, 'password': password, 'pid': pid, 'source': ''}
            s.post(url=login_url, data=data, headers=headers)

            #获取csrf_token
            form_html = s.get(url=form_url, headers=headers)
            soup = BeautifulSoup(form_html.text, 'lxml')
            csrf_token = soup.find(name="meta", attrs={"itemscope" :"csrfToken"}).get('content')

            #获取打卡地址
            headers = {'User-Agent': UA,'Referer': form_url}
            data = {'idc': 'YJSMRDK', 'csrfToken': csrf_token}
            start_json = s.post(url=start_url, data=data, headers=headers)
            step_id = re.search('(?<=form/)\\d*(?=/render)', start_json.text)[0]

            #获取打卡基础信息
            data = {'stepId': step_id, 'csrfToken': csrf_token}
            render = s.post(url=render_url, data=data, headers=headers)
            render_info = json.loads(render.content)['entities'][0]['data']

            #打卡
            data = {
                'actionId': 1,
                'formData': json.dumps(render_info),
                'nextUsers': '{}',
                'stepId': step_id,
                'timestamp': int(time.time()),
                'csrfToken': csrf_token,
                'lang': 'zh'
            }

            res = s.post(url=action_url, data=data, headers=headers)

            now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            if json.loads(res.content)['ecode'] == 'SUCCEED':
                print(f"[{now_time}] {username} success.")
                return
            else:
                print(f"[{now_time}] {username} failed.")

        except Exception as e:
            print(e)
            print("Retrying...")
            time.sleep(30)
        print("Failed too many times, exiting...")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--user", default=None)
    parser.add_argument("--pwd", default=None)
    args = parser.parse_args()
    
    print(args.user, args.pwd)
    if args.user != None and args.pwd != None:
        check(username=args.user, password=args.pwd)
    else:
        from users import *
        for user in users:
            check(user['username'], user['password'])