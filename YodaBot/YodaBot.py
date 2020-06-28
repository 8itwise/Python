import random

print(" _____ _          _____                 ")
print("|_   _| |__ ___  |  ___|__  _ __ ___ ___")
print("| | | '_ \ / _ \ | |_ / _ \| '__/ __/ _ \\")
print("| | | | | |  __/ |  _| (_) | | | (_|  __/")
print("|_| |_| |_|\___| |_|  \___/|_|  \___\___|")

question = ['who', 'what', 'where', 'when', 'why', 'how', 'which', 'wherefore', 'whatever', 'whom', 'whose',  'wherewith', 'whither', 'whence']

contractions = {'aren\'t': 'are not', 'can\'t': 'cannot', 'couldn\'t': 'could not', 'didn\'t': 'did not', 'doesn\'t': 'does not', 'don\'t': 'do not',
                'hadn\'t': 'had not', 'hasn\'t': 'has not', 'haven\'t': 'have not', 'he\'d': 'he had', 'he\'ll':'he shall', 'he\'s': 'he is', 'I\'d': 'I had',
                'I\'ll': 'I shall', 'I\'m': 'I am', 'I\'ve': 'I have', 'isn\'t': 'is not', 'let\'s': 'let us', 'mustn\'t':'must not', 'shan\'t':'shall not',
                'mightn\'t': 'might not', 'she\'ll': 'she shall', 'shouldn\'t': 'should not', 'that\'s': 'that is', 'there\'s': 'there is', 'they\'d':'they had',
                'they\'d':'they had', 'they\'ll': 'they shall', 'they\'re': 'they are', 'they\'ve': 'they have', 'she\'s': 'she is', 'we\'d':'we had', 'we\'re': 'we are',
                'we\'ve': 'we have', 'weren\'t': 'were not', 'what\'s': 'what is', 'what\'ve': 'what have', 'where\'s': 'where is', 'who\'ll':'who will', 'who\'s':'who is',
                'who\'ll': 'who will', 'who\'re': 'who are', 'who\'ve': 'who have', 'won\'t': 'will not', 'wouldn\'t': 'would not', 'you\'d': 'you had', 'you\'ll':'you will',
                'you\'re': 'you are', 'you\'ve': 'you have'}

while True:
    word = str(input("->: "))
    word = word.lower()
    add = word.split()
    if word == 'exit':
        break
    for k, v in contractions.items():
        for n in add:
            if n in contractions and n == k:
                add[add.index(n)] = v
    if add[0] in question:
        add.append('?')
        rand1 = ['Young jedi', '', 'Hmmmm...?']
        random.shuffle(rand1)
        rand_res = random.choice(rand1)
        add.append(rand_res)
        add[0] = add[0].title()
        string_it = " ".join(add)
        print(string_it)
    else:
        add.append(',')
        add = add[:] + add[:2]
        add[:2] = ""
        rand1 = ['..yes...', '', 'Young one']
        random.shuffle(rand1)
        rand_res = random.choice(rand1)
        add.append(rand_res)
        add[0] = add[0].title()
        string_it = " ".join(add)
        print(string_it)