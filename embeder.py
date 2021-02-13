# Embeder by tasure
title = r"""
  ______           _              _           
 |  ____|         | |            | |          
 | |__   _ __ ___ | |__   ___  __| | ___ _ __ 
 |  __| | '_ ` _ \| '_ \ / _ \/ _` |/ _ \ '__|
 | |____| | | | | | |_) |  __/ (_| |  __/ |   
 |______|_| |_| |_|_.__/ \___|\__,_|\___|_|   
        V 1.0           by tasuren#5161

"""

print(title)


from json import load,dump,dumps
from discord import Embed
from requests import post


# お手軽Embed
def easy_embed(content,color=Embed.Empty):
	es = ">>"
	spl = content.splitlines()
	title = spl[0][len(es):]
	desc,fields = [],{}
	footer = None if not ';;' in spl[-1] else spl[-1][2:]
	if footer: spl.pop(-1)
	spl.pop(0)
	f = None
	for c in spl:
		if c == "":continue
		if c[0] == '<':
			f = c[1:] if '!'!=c[1] else c[2:]
			fields[f] = {'i':True if '!'!=c[1] else False,'c':[]}
			continue
		if f:
			fields[f]['c'].append(c)
			continue
		desc.append(c)
	e = Embed(
		title=title,
		description='\n'.join(desc),
		color=color
	)
	for f in fields.keys():
		e.add_field(
			name=f,
			value='\n'.join(fields[f]['c']),
			inline=fields[f]['i']
		)
	if footer: e.set_footer(text=footer)
	return e.to_dict()

def write(data):
	with open("data.json","w") as f:
		dump(data,f,indent=2)


# Data load
try:
	with open("data.json","r") as f:
		data = load(f)
except:
	with open("data.json","w") as f:
		f.write('{\n	"first": false,\n	"tokens": []\n}')

help_text = """# Embeder HELP
普通ユーザーからEmbedを好きなチャンネルに送信することができます。
**使用は自己責任です！**

help
    コマンドリストを表示
token set <NAME> <TOKEN>
    TOKENリストにTOKENを追加します。
token del <NAME>
    TOKENリストからTOKENを削除します。
tokens
    TOKENリストを表示します。
send <NAME>
    Embedを送信します。
    <NAME>に`set`で設定したアカウントのTOKENの登録名を入れてください。
Exit
    終了します。
"""
ad = ["set","del"]

get_headers = lambda token:{
    'Content-Type': 'application/json',
    'authorization': token,
}

print("Embederへようこそ。helpでコマンドリストを確認できます。\n注意：Discordの利用規約違反なので使用は自己責任です。")


while True:
	cmd = input(">>>")

	if cmd == "":
		continue
	else:
		cmd = cmd.split()

	# HELP
	if cmd[0] == "help":
		print(help_text)
	# TOKENリスト管理
	if cmd[0] == "token" and len(cmd) > 2:
		if not cmd[1] in ad:continue

		if cmd[1] == "set" and len(cmd) > 3:
			data["tokens"][cmd[2]] = cmd[3]
			write(data)
		if cmd[1] == "del":
			if not cmd[2] in data["tokens"]:
				print("その名前でTOKENは保存されていません。")
				continue
			del data["tokens"][cmd[2]]
			write(data)
	# TOKENリスト表示
	if cmd[0] == "tokens" and len(data["tokens"]) != 0:
		for d in data["tokens"].keys():print(f'{d}\n  {data["tokens"][d]}')
	# 送信
	if cmd[0] == "send" and len(cmd) > 1:
		if not cmd[1] in data["tokens"]:
			print("その名前でTOKENは保存されていません。")
			continue

		channel = input("送信先チャンネルIDを入力：")
		title = input("タイトルを入力：")
		description = input("説明を入力：")
		print("他に登録したい場合はreadmeの例にならって書いてください。\n終わったら!end!と入力してください。")
		etc = ""
		while not "!end!" in etc:etc += "\n"+input(":")
		if "!end!" in etc:etc = etc.replace("!end!","")
		print("")

		print("作成中...")
		send_data = {
			"content": None,
			"tts": False,
			"embed": easy_embed(f">>{title}\n{description}{etc}")
		}

		print("送信中...")
		response = post(
			f'https://discord.com/api/v6/channels/{channel}/messages',
			headers=get_headers(data["tokens"][cmd[1]]),
			data=dumps(send_data)
		)
		st = response.status_code
		if st in [200,201,204,304]:print("送信に成功しました。")
		elif st == 400:print("送信に失敗しました。\n  サーバーまたは、送信したデータにエラーがあります。")
		elif st == 401:print("送信に失敗しました。\n  TOKENがあっているか確認をしてください。")
		elif st == 403:print("送信に失敗しました。\n  TOKENがあっているか確認をしてください。\n  またチャンネルIDがあっているか確認してください。")
		elif st == 404:print("送信に失敗しました。\n  チャンネルIDがあっているか確認してください。")
		elif st == 429:print("送信に失敗しました。\n  送信のしすぎで制限を受けています。")
		else:print(f"なんらかの理由で送信に失敗しました。\n  エラーコード：{st}")
	# 終了
	if cmd[0] == "exit":break