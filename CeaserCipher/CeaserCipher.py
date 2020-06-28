list1 = []
list2 = []
list3 = []

def encrypt():
    check = False
    while check is False:
        word = input("Word:->")
        word = word.upper()
        if word.isalpha() or " " in word:
            check = True
        else:
            print("Strings only!!!")

    check = False
    while check is False:
        shift = input("Shift:-> ")
        if shift.isdigit():
            shift = int(shift)
            if shift <= 26:
                check = True
        else:
            print("Integers only!!!")

    for n in word:
        list1.append(ord(n))

    num = 26 - shift
    for i in list1:
        if i + shift >= 90:
            o = i - num
            list2.append(o)
        else:
            i += shift
            list2.append(i)

    for k in list2:
        list3.append(chr(k))
    result = "".join(list3)

    print(result)

def decrypt():
    check = False
    while check is False:
        word = input("Word:->")
        word = word.upper()
        if word.isalpha() or '$' in word:
            check = True
        else:
            print("Strings only!!!")

    check = False
    while check is False:
        shift = input("Shift:-> ")
        if shift.isdigit():
            shift = int(shift)
            if shift <= 26:
                check = True
        else:
            print("Integers only!!!")

    for n in word:
        list1.append(ord(n))

    num = 26 - shift
    for i in list1:
        if i + shift >= 90:
            o = i + num
            list2.append(o)
        else:
            i -= shift
            list2.append(i)

    for k in list2:
        list3.append(chr(k))
    result = "".join(list3)

    print(result)

encrypt()
