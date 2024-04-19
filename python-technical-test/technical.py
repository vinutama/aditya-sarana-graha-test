def operate_even_odd_numbers(nums: list):
    result = []
    # loop
    for num in nums:
        # conditions
        if num % 2 == 0:
            # arithmetic
            num *= 2
            result.append(num)
        else:
            num *= 3
            result.append(num)
    return result


print(operate_even_odd_numbers([1, 2, 3, 4, 5, 6, 7, 8]))
