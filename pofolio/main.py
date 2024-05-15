import random

def main():
    nums_of_play = 10
    current_try = 0
    print('You have {} try to make '.format(current_try))
    res = get_input()
    guess = get_random()
    print(guess)
    while current_try < nums_of_play:
        responds = validate()
        print(responds)

        current_try +=1


def get_random():
    nums = ['1','2','3','4','5','6','7','8','9']
    random.shuffle(nums)
    return nums[:3]

def get_input():
    responds = input('> ')
    try:
        gues = [i for i in responds]
        assert len(gues)==3
        return gues
    except:
        print('Please enter three diget')

def validate():
    new_gues =[]
    res = get_input()
    guess=get_random()
    if res == guess:
        return ('You won')
    for i in range(len(guess)):
        if res[i] in guess:
            new_gues.append('Pico')

        elif res[i] == guess[i]:
            new_gues.append('Firmi')
            return new_gues
    if len(new_gues) ==0:
            return 'Bagels'
    else:
        new_gues.sort()
        return ' '.join(new_gues)



if __name__=='__main__':
    main()