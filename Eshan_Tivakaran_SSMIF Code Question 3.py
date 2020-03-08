#!/usr/bin/env python
# coding: utf-8

# ## Question 3

# There is one common theme amongst parts a), b), and c).  It is that if a portion of the list is inside 2 certain numbers (call them starting and ending markers), those numbers (when summed) will be multiplied by their respective number.                                          
# In a), if a portion of the list is inside the numbers 9 and 6, then those numbers (when summed) will be multiplied by 2.
# In b), if a portion of the list is inside the numbers 7 and 4, then those numbers (when summed) will be multiplied by 3.
# In c), if a portion of the list is inside the numbers 4 and 5, then those numbers (when summed) will be multiplied by 0.
# 
# If those 2 markers don't exist, then we must take the sum of the elements in the list (with no caveat).
# This means that we can generalize this process into one simple function.
# 
# The function that does the sum computation is called "total".  The parameters are the list, the starting marker, the ending marker, and the constant.
# 
# First this method checks to see if the starting marker exists in the list and if the ending marker appears after the starting marker.  
# If these two conditions are true, then we need to sum the list in the following manner:
# 
#    The numbers that appear before the starting marker are summed normally and that sum is set to the variable 'a'.
# 
#    The numbers in between the starting and ending marker (inclusive) are summed, then multiplied by their given constant.  This    new sum is set to the variable 'b'.
# 
#    The numbers that appear after the ending marker are summed normally and that sum is set to the variable 'c'.
# 
#    Finally, the total returns the sum of 'a', 'b', and 'c'.
#    
# If either of these conditions aren't true, then the elements in the list are summed regularly.
#  
# This is exhaustive of all of the different possible cases that can happen.  Using the fact that 'list.index(element)' finds only the first instance where 'element' appears in 'list', so we know that if the starting and ending marker appear a second time in the list, it won't be multiplied by the constant (which is what we want).
# 
# Now that we understand how the 'total' function works, let's discuss the 'ssmif_sum' function.  We create a new, empty list called 'outer_list'.  Using a for-loop that traverses the given list, at every iteration, if the index of the inner list is even, it calls the 'total' function with the proper parameters given by the prompt and appends it to 'outer_list'.  If the index of the inner list is odd, it still calls the 'total' function with the proper parameters given by the prompt and appends it to 'outer_list'.
# 
# After iterating over all of the elements in the nested list, we must make sure that condition c) is satisfied and return the final sum.  This can be done by calling 'total' with the proper parameters given by the prompt.  Once the condition is checked, it returns the proper sum.

# In[1]:


def total(l, start_marker, end_marker, multiple):
    if start_marker in l and end_marker in l[l.index(start_marker):]:
        a = sum(l[:l.index(start_marker)])
        b = sum(l[l.index(start_marker) : (l.index(start_marker) + l[l.index(start_marker):].index(end_marker) + 1)]) * multiple
        c = sum(l[l.index(start_marker) + l[l.index(start_marker):].index(end_marker) + 1 :])
        return a + b + c
    else:
        return sum(l)
    
def sum_ssmif(nested_list):
    outer_list = []
    for inner_list in nested_list:
        if nested_list.index(inner_list) % 2 == 0:
            outer_list.append(total(inner_list, 9, 6, 2))
        else:
            outer_list.append(total(inner_list, 7, 4, 3))
    return total(outer_list, 4, 5, 0)

