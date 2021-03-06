# coding: utf-8
"""
[udemy]DataScience
Lect.50-51

データクローニング

Webアクセスログをとり，最も見られたページを特定する
Apacheのアクセスログラインを解析するために，正規表現のセットアップを行う

"""
import re

format_pat = re.compile(
    r"(?P<host>[\d\.]+)\s"
    r"(?P<identity>\S*)\s"
    r"(?P<user>\S*)\s"

    r"\[(?P<time>.*?)\]\s"
    r'"(?P<request>.*?)"\s'
    r"(?P<status>\d+)\s"

    r"(?P<bytes>\S*)\s"
    r'"(?P<regerer>.*?)"\s'
    r'"(?P<user_agent>.*?)"\s*'
)

logPath = "/Users/usui/work/python/DataScience/access_log.txt"

# 各アクセスからURLを取り出すためのコードを用意，dictを用いて各URLの出現回数をカウント
# sort() で表示
URLCounts = {}

with open(logPath, "r") as f:
    for line in (l.rstrip() for l in f):
        match = format_pat.match(line)
        if match:
            access = match.groupdict()
            request = access['request']
            fields = request.split()
            if (len(fields) != 3):
                print(fields)


# 空のフィールドに加えて，不要なデータが含まれている．->チェックコードに改変
URLCounts = {}

with open(logPath, "r") as f:
    for line in (l.rstrip() for l in f):
        match = format_pat.match(line)
        if match:
            access = match.groupdict()
            request = access['request']
            fields = request.split()
            if (len(fields) == 3):
                (action, URL, protocol) = fields
                if (action == 'GET'): # POSTをGETアクションでフィルター
                    if URL in URLCounts: # py3系は，in演算子使う 
                        URLCounts[URL] = URLCounts[URL] + 1
                    else:
                        URLCounts[URL] = 1


results = sorted(URLCounts, key = lambda i: int(URLCounts[i]), reverse = True)

for result in results[:20]:
    print(result + ": " + str(URLCounts[result]))


    
"""
なぜUserAgentが空なのか，ある種の悪意のあるスクレイパー？
どんなUserAgentがいるのか明らかにしてみる.

"""
print()
print()
print("どんなUserAgentがいるのか明らかにしてみる.")
print()
print()

UserAgents = {}

with open(logPath, "r") as f:
    for line in (l.rstrip() for l in f):
        match = format_pat.match(line)
        if match:
            access = match.groupdict()
            agent  = access['user_agent']
            if agent in UserAgents:
                UserAgents[agent] = UserAgents[agent] + 1
            else:
                UserAgents[agent] = 1

results = sorted(UserAgents, key = lambda i: int(UserAgents[i]), reverse = True)

for result in results:
    print(result + ": " + str(UserAgents[result]))

"""
データ汚染防止のため，'-', "bot", "spider"を含むもの(W3 Total Cache)を取り除く
"""
print()
print()
print('"データ汚染防止のため，"-", "bot", "spider"を含むもの(W3 Total Cache)を取り除く"')
print()
print()

URLCounts = {}

with open(logPath, "r") as f:
    for line in (l.rstrip() for l in f):
        match = format_pat.match(line)
        if match:
            access = match.groupdict()
            agent  = access['user_agent']
            if ( not( 'bot' in agent or 'spider' in agent or
                     'Bot' in agent or 'Spider' in agent or
                     'W3 Total Cache' in agent or agent == '-' ) ):

                request = access['request']
                fields = request.split()
                if (len(fields) == 3):
                    (action, URL, protocol) = fields
                    if (action == 'GET'):
                        if URL in URLCounts:
                            URLCounts[URL] = URLCounts[URL] + 1
                        else:
                            URLCounts[URL] = 1
                            
results = sorted(URLCounts, key = lambda i: int(URLCounts[i]), reverse = True)

for result in results:
    print(result + ": " + str(URLCounts[result]))
    



"""
ウェブページでないものをヒットしないように, / で終わらないURLを除く
"""
print()
print()
print("ウェブページでないものをヒットしないように, / で終わらないURLを除く")
print()
print()

URLCounts = {}

with open(logPath, "r") as f:
    for line in (l.rstrip() for l in f):
        match = format_pat.match(line)
        if match:
            access = match.groupdict()
            agent  = access['user_agent']
            if ( not( 'bot' in agent or 'spider' in agent or
                     'Bot' in agent or 'Spider' in agent or
                     'W3 Total Cache' in agent or agent == '-' ) ):

                request = access['request']
                fields = request.split()
                if (len(fields) == 3):
                    (action, URL, protocol) = fields
                    if (URL.endswith("/")): # URLが '/' で終わるものを除く
                        if (action == 'GET'):
                            if URL in URLCounts:
                                URLCounts[URL] = URLCounts[URL] + 1
                            else:
                                URLCounts[URL] = 1
                            
results = sorted(URLCounts, key = lambda i: int(URLCounts[i]), reverse = True)

for result in results:
    print(result + ": " + str(URLCounts[result]))

