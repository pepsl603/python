import random

M = 10
numberList = []

for i in range(M):
    numberList.append(random.randint(1, 20))

print(numberList)

sort_i = len(numberList) - 1
sort_num = 0

while sort_i > 0:

    sort_j = 0
    sort_flag = False
    while sort_j < sort_i:

        if numberList[sort_j] > numberList[sort_j+1]:
            numberList[sort_j], numberList[sort_j+1] = numberList[sort_j+1], numberList[sort_j]
            sort_flag = True
        sort_j += 1
    print(numberList)
    sort_num += 1
    if not sort_flag:
        break
    sort_i -= 1
print('冒泡了%s次' % sort_num)