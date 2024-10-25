nums=[555,901,482,1771]
for num in nums:
    divided_number=num//10
    str_number=str(divided_number)
    odd_count=sum(1 for digit in str_number if digit in "13579")
    if odd_count>0:
        all_odd_count=odd_count
    print(all_odd_count)
