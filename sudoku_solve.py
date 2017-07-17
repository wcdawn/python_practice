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
original = np.ones((9,9),dtype=bool)
for i in range(input.shape[0]):
  for j in range(input.shape[1]):
    if input[i,j] == 0:
      original[i,j] = False
    else:
      original[i,j] = True

# initialize variables for coordintates, forward/back, and iteration count
bound = bound_type
work = input
x = 0
y = 0
direction = 1
itcount = 0
isComplete = False

while not(isComplete):
  itcount += 1
  if itcount >= 1e6:
    print('failed to solve in ONE MILLION iterations!')
    sudoku_write(work)
    exit(1)
  # this block could be rewritten more efficiently
  if not(original[y,x]):
    if 0 <= y <= 2:
      bound.l = 0
      bound.r = 2
    elif 3 <= y <= 5:
      bound.l = 3
      bound.r = 5
    elif 6 <= y <= 8:
      bound.l = 6
      bound.r = 8
    if 0 <= x <= 2:
      bound.u = 0
      bound.d = 2
    elif 3 <= x <= 5:
      bound.u = 3
      bound.d = 5
    elif 6 <= x <= 8:
      bound.u = 6
      bound.d = 8
    
    if work[y,x]  == 9:
      work[y,x] = 0
      x += direction
      if x == -1:
        x = 8
        y -= 1
      elif x == 9:
        x = 0
        y += 1
      continue
    
    for guess in range(work[y,x]+1,9+1):
      work[y,x] = guess
      error = False
      
      # row check
      for a in range(9):
        if (work[y,x] == work[y,a]) and (a != x):
          # bad guess
          error = True
          break
      # col check
      for a in range(9):
        if (work[y,x] == work[a,x]) and (a != y):
          # bad guess
          error = True
          break
      # sector check
      for a in range(bound.l,bound.r+1):
        for b in range(bound.u,bound.d+1):
          if (work[y,x] == work[a,b]) and (a != y) and (b != x):
            # bad guess
            error = True
            break
      
      if not(error):
        # good guess
        direction = 1
        break
      if (error) and (guess == 9):
        work[y,x] = 0
        direction = -1
      
  x += direction
  if x == 9:
    x = 0
    y += 1
  elif x == -1:
    x = 8
    y -= 1
  if y == 9:
    print('completed')
    isComplete = True
    break
      
print(itcount,' - iterations')
sudoku_write(work)