# exec(open("scripts/load_data.py").read())	

# from acc.models import Account

# print(os.getcwd())

print("Load data")
with open("notes.txt", "r") as fp:
    for line in fp:
        sa = line.split(' | ')
        print(sa)
    
