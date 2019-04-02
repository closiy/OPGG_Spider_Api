def swap(a,b):
    temp = a
    a = b
    b = temp


def bublleSort(arrs):
    length = len(arrs)

    for i in range(length):
        j = length - i - 1
        while j>i+1:
            if arrs[j]<arrs[j-1]:
                swap(arrs[j],arrs[j-1])
            j -= 1
    return


if __name__ == '__main__':
    a = [1,4,2,6,5]
    b = a
    bublleSort(a)
    print('formal_arrs = {},sorted_arrs = {}'.format(b,a))