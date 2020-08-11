import os


def bash(command):
    print('\033[92m '+command+"\033[0m")
    os.system(command)


print(" -=GIT commit help=-")

directory = os.path.abspath(os.curdir)
print("Path for Git:", directory)
print("-"*100)
bash('git status')
print("-"*100)
if input("Press Enter for continue 'git add *'  or Any key for exit") != "":
    exit()

bash('git add *')
bash('git status')

print("Committing and Pushing")
msg = input("Enter commit message 'git commit -m' \n")
if msg == "":
    bash(f'git commit')
else:
    bash(f'git commit -m "{msg}"')

bash('git push')
bash('git status')




