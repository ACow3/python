#Biggie Size
def biggie_size(arr):
    for x in range(0, len(arr), 1):
        if arr[x] > 0:
            arr[x] = "big"
    return arr

print(biggie_size([-1, 3, 4, -5]))

#Count Positives
def count_positives(arr):
    count = 0
    for x in range(0, len(arr), 1):
        if(arr[x] > 0):
            count += 1
    arr[len(arr)-1] = count

    return arr

print(count_positives([-1,1,1,1]))


#Sum Total
def sum_total(arr):
    sum = 0
    for x in range(0, len(arr), 1):
        sum+=arr[x]
    print(sum)

sum_total([1,2,3,4])


#Average
def average(arr):
    sum = 0
    for x in range(0, len(arr), 1):
        sum += arr[x]
    avg = sum / len(arr)
    print(avg)

average([1,2,3,4])


#Length
def length(arr):
    print (len(arr))

length([37,2,1,-9])

#Minimum

def minimum(arr):
    for x in range(0, len(arr), 1):
    if arr[x] < :
     = arr[x]

print(min) 
minimum ([37,2,1,-9]])


#Maximum


#Ultimate Analysis



#Reverse List

