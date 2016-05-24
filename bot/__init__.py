import os.path
fp = open(os.path.dirname(__file__) + '/../resources/jokes.txt', 'r')
tmp_str=fp.readline()
global joke_list = []
while tmp_str and tmp_str!='\n' and tmp_str!= '\r':
  tmp_str = fp.readline()
if(tmp_str):
  while tmp_str:
    tmp_item=[]
    if tmp_str!='\n' and tmp_str!= '\r':
      tmp_item.append(tmp_str)
    else:
      break
    tmp_str = fp.readline()
    if tmp_str!='\n' and tmp_str!= '\r':
      tm_item.append(tmp_str)
    joke_list.append(tmp_item)
    tmp_str = fp.readline()
