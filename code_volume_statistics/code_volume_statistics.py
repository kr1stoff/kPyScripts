import requests
from datetime import datetime, timedelta

# 配置
# ! github 仓库中代码不允许提交 token 等密钥相关信息, 改为输入
GITHUB_TOKEN = input("请输入 GitHub Token: ").strip()
USERNAME = 'kr1stoff'
API_URL = 'https://api.github.com'

# 计算本周的起始和结束时间
# * 每周逻辑改成 “六天前到今天”
today = datetime.now()
end_of_week = today
start_of_week = end_of_week - timedelta(days=6)

# 获取所有仓库
headers = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github.v3+json'
}
# * 改为输入指定仓库
# repos_url = f'{API_URL}/users/{USERNAME}/repos'
# repos_response = requests.get(repos_url, headers=headers)
# repos = repos_response.json()

# todo 一些备选仓库
# KML-RNASEQ,KML-LVISA,KML-TCR2,mysite
repo_input = input("请输入仓库名称，多个仓库以逗号(',')分隔：")
repos = [repo.strip() for repo in repo_input.strip(',').split(",")]

# 统计代码行数
total_additions, total_deletions, total_alterations = 0, 0, 0

for repo in repos:
    # repo_name = repo['name']
    repo_name = repo
    commits_url = f'{API_URL}/repos/{USERNAME}/{repo_name}/commits'
    params = {
        'since': start_of_week.isoformat(),
        'until': end_of_week.isoformat(),
        'author': USERNAME
    }
    commits_response = requests.get(commits_url, headers=headers, params=params)
    commits = commits_response.json()

    for commit in commits:
        commit_sha = commit['sha']
        commit_details_url = f'{API_URL}/repos/{USERNAME}/{repo_name}/commits/{commit_sha}'
        commit_details_response = requests.get(commit_details_url, headers=headers)
        commit_details = commit_details_response.json()
        total_alterations += commit_details['stats']['total']
        total_additions += commit_details['stats']['additions']
        total_deletions += commit_details['stats']['deletions']

print(f'本周新增代码行数: {total_additions}')
print(f'本周删除代码行数: {total_deletions}')
print(f'本周总计变动代码行数: {total_alterations}')
