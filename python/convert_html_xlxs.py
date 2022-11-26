from bs4 import BeautifulSoup
import os
import pandas as pd
import random

# Fetch the html file
def swapPositions(list, pos1, pos2):
    list[pos1], list[pos2] = list[pos2], list[pos1]
    return list

list = []



for file in os.listdir('.'):
    if file.endswith('.html'):
        with open(file, "r", encoding='utf-8') as f:
            text= f.read()
            soup = BeautifulSoup(text,"html.parser")
            question = soup.title.string
            choice = []
            tags = {tag.name for tag in soup.find_all()}

            answer = soup.find_all('span',class_ = ['to-do-children-checked'])
            choice.append(('1',answer[0].string))
            another_choices = soup.find_all('span',class_ = ['to-do-children-unchecked'])

            for i in range(len(another_choices)):
                choice.append((str(i + 2),another_choices[i].string))
            list.append((question,choice))

excel_file = 'SHCD.xlsx'
df = pd.read_excel(excel_file)
question = []
type = []
ops,true,time,image = [],[],[],[]
for q in list:
    question.append(q[0])
    type.append('Multiple Choice')
    true_q = random.randint(0,3)
    ops.append([q[1][0][1]])
    ops[-1].append(q[1][1][1])
    ops[-1].append(q[1][2][1])
    ops[-1].append(q[1][3][1])
    ops[-1].append('')
    ops[-1] = swapPositions(ops[-1], 0,true_q)
    true.append(true_q + 1)
    time.append(20)
    image.append('')

print(len(question),len(type),len(ops),len(true),len(time),len(image))
df_new = {'Question Text': question,'Question Type': type, 'Option 1': [x[0] for x in ops],'Option 2':[x[1] for x in ops],'Option 3': [x[2] for x in ops],'Option 4': [x[3] for x in ops],'Option 5':[x[4] for x in ops],'Correct Answer': true,'Time in seconds': time, 'Image Link': image}
df_new = pd.DataFrame(df_new)
df_total = pd.concat([df,df_new],ignore_index=True)
df_total.to_excel('SHCD_.xlsx')