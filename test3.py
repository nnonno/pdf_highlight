import mechanize
from subprocess import Popen, PIPE

INITIAL_URL = "http://sttm.org/"

br = mechanize.Browser()
br.open(INITIAL_URL)
br.follow_link(text='Bulletins 2015')
print br.title()
pdf_req = br.follow_link(text_regex=r'Sunday,')

ps2ascii = Popen(['ps2ascii'], stdin=PIPE, stdout=PIPE, shell=True)
ps2ascii.stdin.write(pdf_req.read())
ps2ascii.stdin.close()
scheduled = any(text for text in ps2ascii.stdout if "Donald Blom" in text)
ps2ascii.stdout.close()
ps2ascii.wait()
print "Yes" if scheduled else "No"