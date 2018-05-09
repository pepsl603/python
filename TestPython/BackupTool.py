import  os
import  time

sourceDir = input("请输入待备份的目录：")

running = True
while running:
    if not os.path.exists(sourceDir):
        print("待备份的目录:({})不存在".format(sourceDir))
        sourceDir = input("请输入待备份的目录：")
    else:
        running = False

targetDir = input("请输入保存备份的目录：")
# targetDir + os.sep +
target = time.strftime('%Y%m%d%H%M%S') + '.ZIP'

zip_cmd = 'cd {} && zip -r {} {}'.format(targetDir, target, sourceDir)
print('Zip command is:')
print(zip_cmd)
print('Running:')
if os.system(zip_cmd) == 0:
    print('成功备份到：', targetDir + os.sep + target)
else:
    print('备份失败！！！')
