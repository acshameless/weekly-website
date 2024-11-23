import os
import httpx
import re
import urllib.parse

def fetch_ci_time(file_path):
    url = f"https://api.github.com/repos/acshameless/weekly-website/commits?path={file_path}&page=1&per_page=1"
    response = httpx.get(url)
    ci_time = response.json()[0]["commit"]["committer"]["date"].split("T")[0]
    return ci_time

if __name__ == "__main__":
    with open('README.md', 'w') as readme_file, open('RECENT.md', 'w') as recent_file:
        readme_file.write("# Weekly Report\n\n记录工程师 shameless 的 weekly report，不定期发布，欢迎关注，本 repo Fork 自工程师 Tw93 https://github.com/tw93/weekly，特此声明。\n\n")

        for root, dirs, filenames in os.walk('./src/pages/posts'):
            filenames = sorted(filenames, key=lambda x: float(re.findall(r"(\d+)", x)[0]), reverse=True)

        for index, name in enumerate(filenames):
            if name.endswith('.md'):
                file_path = urllib.parse.quote(name)
                old_title = name.split('.md')[0]
                url = f'https://weekly.shameless.top/posts/{old_title}'
                title = f'第 {old_title.split("-")[0]} 周 - {old_title.split("-")[1]}'
                readme_md = f'* [{title}]({url})\n'
                num = int(old_title.split('-')[0])

                if index < 5:
                    modified = fetch_ci_time(f'/src/pages/posts/{file_path}')
                    recent_md = f'* [{title}]({url}) - {modified}\n'
                    recent_file.write(recent_md)

                readme_file.write(readme_md)
