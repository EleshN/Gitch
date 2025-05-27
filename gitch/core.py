import subprocess
from gitch.devlog_poster import post_devlog

def gitch_commit(message: str, include_files=True, include_footer=True):
    subprocess.run(["git", "commit", "-m", message])

    file_list = ""
    if include_files:
        diff = subprocess.check_output(["git", "diff", "--name-only", "HEAD~1", "HEAD"]).decode()
        file_list = "\n\nFiles changed:\n" + diff

    footer = ""
    if include_footer:
        footer = '\n\nThis devlog was automated with [Gitch](https://github.com/YOUR_USERNAME/gitch)'

    full_message = message + file_list + footer
    post_devlog(title=message, body=full_message)
