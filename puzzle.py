#!/usr/bin/python

import sys

pieces = [
  {
    'shape': [
      [1, 0, 1],
      [1, 1, 1],
      [1, 0, 1]
    ],
    'rotate': 2
  },
  {
    'shape': [
      [1, 0, 0],
      [1, 1, 1],
      [0, 0, 1]
    ],
    'rotate': 2 
  },
  {
    'shape': [
      [0, 1],
      [1, 1],
      [1, 0]
    ],
    'rotate': 2
  },
  {
    'shape': [
      [1, 1],
      [1, 1]
    ],
    'rotate': 1 
  },
  {
    'shape': [
      [1, 0],
      [1, 1],
      [1, 0],
      [1, 0]
    ],
    'rotate': 4 
  },
  {
    'shape': [
      [1, 1, 1, 1],
      [0, 0, 0, 1]
    ],
    'rotate': 4 
  },
  {
    'shape': [
      [1, 1, 1],
      [1, 0, 1]
    ],
    'rotate': 4 
  },
  {
    'shape': [
      [0, 1, 1, 1],
      [1, 1, 0, 0]
    ],
    'rotate': 4 
  },
  {
    'shape': [
      [1, 0],
      [1, 1],
      [1, 0]
    ],
    'rotate': 4 
  },
  {
    'shape': [
      [0, 1, 0],
      [1, 1, 0],
      [0, 1, 1]
    ],
    'rotate': 4 
  },
  {
    'shape': [
      [0, 0, 1],
      [1, 1, 1]
    ],
    'rotate': 4 
  },
  {
    'shape': [
      [1, 1, 1],
      [0, 0, 1],
      [0, 0, 1]
    ],
    'rotate': 4 
  },
  {
    'shape': [
      [1, 1],
      [1, 1],
      [1, 1]
    ],
    'rotate': 2 
  }, 
]

def printPicture(picture): 
  rows = len(picture)
  cols = len(picture[0])
   
  for row in range(rows):    
    row_str = ""
    for col in range(cols):
      act = picture[row][col]
      if  act <= 0:
        row_str += " --"
      else:
        row_str += "{:3}".format(act)
    
    print(row_str)
  print()

def insertShape(board, shape, x, y):
  for shape_row in range(len(shape)):
    for shape_col in range(len(shape[0])):
      if shape[shape_row][shape_col] > 0:
        if board[shape_row + y][shape_col + x] > 0:
          return False
      
  for shape_row in range(len(shape)):
    for shape_col in range(len(shape[0])):
      if shape[shape_row][shape_col] > 0:
        board[shape_row + y][shape_col + x] = shape[shape_row][shape_col]
        
  for shape_row in range(-1, len(shape) + 1):
    for shape_col in range(-1, len(shape[0]) + 1):
      pt_x = x + shape_col
      pt_y = y + shape_row
      if pt_x >= 0 and pt_x <= 7 and pt_y >= 0 and pt_y <= 7 and board[pt_y][pt_x] <= 0:
        if pt_x > 0 and board[pt_y][pt_x - 1] <= 0:
          continue
        if pt_x < 7 and board[pt_y][pt_x + 1] <= 0:
          continue
        if pt_y > 0 and board[pt_y - 1][pt_x] <= 0:
          continue
        if pt_y < 7 and board[pt_y + 1][pt_x] <= 0:
          continue
        removeShape(board, shape, x, y)
        return False
    
  return True

def removeShape(board, shape, x, y):      
  for shape_row in range(len(shape)):
    for shape_col in range(len(shape[0])):
      if shape[shape_row][shape_col] > 0:
        board[shape_row + y][shape_col + x] = -1
  
def rotateShape(shape):
  new_shape = []
  for row in range(len(shape[0])):
    new_row = []
    for col in range(len(shape)):
      new_row.append(shape[len(shape) - col - 1][row])
    new_shape.append(new_row)
  return new_shape
  
def rotatePiece(piece):
  new_piece = { 
    'shape': rotateShape(piece['shape']),
    'corners': piece['corners'][3:4] + piece['corners'][0:3] 
  }
  
  return new_piece
  
def canBePlacedInCorner(shape, corner):
  x = 0
  y = 0
  if corner == 1 or corner == 2:
    x = len(shape[0]) - 1
  if corner == 2 or corner == 3:
    y = len(shape) - 1
    
  if shape[y][x] == 0:
    return False
    
  return True
  
#sdef findFirstEmpty(board):
  
def findFirstEmptyPoint(board):
  for y in range(len(board)):
    for x in range(len(board[0])):
      if board[y][x] <= 0:
        return (x,y)
    
def findFirstFilledPoint(shape):
  for y in range(len(shape)):
    for x in range(len(shape[0])):
      if shape[y][x] > 0:
        return x, y

def placeShape(board, unused_pieces, setup):
  x, y = findFirstEmptyPoint(board)
  
  for piece_idx in unused_pieces:
    setup.append(piece_idx)
    piece = pieces[piece_idx]
    shape = piece['shape']
  
    for rot in range(piece['rotate']):
      if rot > 0:
        shape = rotateShape(shape)
        
      shape_x, shape_y = findFirstFilledPoint(shape)
      if x - shape_x + len(shape[0]) > 8 or y - shape_y + len(shape) > 8 or x < shape_x or y < shape_y:
        continue
    
      setup.append(rot)
      if insertShape(board, shape, x - shape_x, y - shape_y):
        new_unused_pieces = unused_pieces.copy()
        new_unused_pieces.pop(piece_idx)

        if not new_unused_pieces:
#          print("Heureka!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
          printPicture(board)
          print(setup)
          
          with open('solutions', 'a') as f:
            original_stdout = sys.stdout
            sys.stdout = f 
            printPicture(board)
            sys.stdout = original_stdout           
        else:
          placeShape(board, new_unused_pieces, setup)
          
        removeShape(board, shape, x - shape_x, y - shape_y)  
      setup.pop()
    setup.pop()
    
def placeShapeToCorner(board, unused_pieces, corner, setup): 
  for piece_idx in unused_pieces:
    setup.append(piece_idx)
    
    piece = pieces[piece_idx]
    for rotations in range(piece['rotate']):
      setup.append(rotations)
      
      if rotations > 0:
        piece = rotatePiece(piece)
    
      if piece['corners'][corner]:
        shape = piece['shape']
        x = 0
        y = 0
        if corner == 1 or corner == 2:
          x = 8 - len(shape[0])
        if corner == 2 or corner == 3:
          y = 8 - len(shape)
      
        if insertShape(board, shape, x, y):
          new_unused_pieces = unused_pieces.copy()
          new_unused_pieces.pop(piece_idx)
      
          if corner < 3:
            placeShapeToCorner(board, new_unused_pieces, corner + 1, setup)
          else:
#            printPicture(board)
#            print(setup)
            placeShape(board, new_unused_pieces, setup)
          
          removeShape(board, shape, x, y)
              
      setup.pop()
    setup.pop()
    
def placeShapeH(board):
  shape = pieces[0]['shape']
  
  unused_pieces = { 1: 1, 2:1, 3:1, 4:1, 5:1, 6:1, 7:1, 8:1, 9:1, 10:1, 11:1, 12:1 }
      
  for x in range(8 - len(shape[0]) + 1):
    for y in range(1, 3):
      insertShape(board, shape, x, y)
      
      setup = [x, y]      
      placeShapeToCorner(board, unused_pieces, 0, setup)
      removeShape(board, shape, x, y)
    
for shape_idx in range(len(pieces)):
  piece = pieces[shape_idx]
  shape = piece['shape']
  
  for shape_row in range(len(shape)):
    for shape_col in range(len(shape[0])):
      if shape[shape_row][shape_col] > 0:
        shape[shape_row][shape_col] = shape_idx + 1
        
  piece['corners'] = []
  for corner in range(4):
    piece['corners'].append(canBePlacedInCorner(shape, corner))
    
#  piece = pieces[shape_idx]
#  for rotate in range(4):
#    printPicture(piece['shape'])
#    print(piece['corners'])
#    piece = rotatePiece(piece)
    
#  printPicture(shape)
#  print(pieces[shape_idx]['corners'])
  
board_line = []
for col in range(8):
  board_line.append(-1)
  
board = []
for row in range(8):
  board.append(board_line.copy())

#printPicture(board)

placeShapeH(board)

