import numpy as np

def sudoku_write(sud_arr):
  print()
  print('-------------------------')
  for i in range(sud_arr.shape[0]):
    if (i == 3) or (i == 6):
      print('|-------+-------+-------|')
    print('| ',end='')
    for j in range(sud_arr.shape[1]):
      if (j == 3) or (j == 6):
        print('| ',end='')
      print(sud_arr[i,j],end=' ')
    print('|')
  print('-------------------------')
  print()

class bound_type(object):
  def __init__(self):
    bound.l = 0
    bound.r = 0
    bound.u = 0
    bound.d = 0

easy = np.array([[9,0,1,0,5,4,0,0,8],
                 [0,7,2,6,0,1,5,0,0],
                 [0,4,0,9,8,0,0,0,0],
                 [0,0,0,0,0,0,4,7,2],
                 [0,2,0,0,0,0,0,5,0],
                 [3,6,5,0,0,0,0,0,0],
                 [0,0,0,0,1,6,0,3,0],
                 [0,0,3,4,0,9,1,2,0],
                 [4,0,0,5,2,0,9,0,6]])

input = easy
print('input echo')
sudoku_write(input)

# initialize and fill a matrix of bools to track if the data is original
original = np.ones((9,9))
for i in range(input.shape[0]):
  for j in range(input.shape[1]):
    if input[i,j] == 0:
      original[i,j] = False
    else:
      original[i,j] = True

bound = bound_type
work = input

# initialize variables for coordintates, forward/back, and iteration count
x = 0
y = 0
direction = 1
itcount = 0
isComplete = False

while not(isComplete):
  itcount += 1
  if itcount >= 1e6:
    print('failed to solve in ONE MILLION iterations!')
    exit(1)
  # this block could be rewritten more efficiently
  if not(original[y,x]):
    if 