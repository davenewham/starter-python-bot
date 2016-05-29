fp = open('./resources/Jokes.txt', 'r')
tmp_str=fp.readline().strip()
global joke_list
#global sum_p = 0
joke_list = []

while tmp_str and tmp_str=="":
  tmp_str = fp.readline().strip()
while tmp_str:
  tmp_item=[]
  if tmp_str != "":
    tmp_item.append(256) 
    tmp_item.append(tmp_str)
  else:
    break
  tmp_str = fp.readline().strip()
  if tmp_str!= "":
    tmp_item.append(tmp_str)		 	#p value element
    tmp_item.append(tmp_str)
    fp.readline()
  joke_list.append(tmp_item)
  tmp_str = fp.readline().strip()
#sum_p = 100 * len(joke_list)                   	 #because all p values start as 100
