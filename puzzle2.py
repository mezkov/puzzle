#!/usr/bin/python

import sys
import copy

pieces = [
  {
    'shape': [
      [1, 0, 1],
      [1, 1, 1],
      [1, 0, 1]
    ],
    'rotate': 2,
    'mirror': 1
  },
  {
    'shape': [
      [1, 0, 0],
      [1, 1, 1],
      [0, 0, 1]
    ],
    'rotate': 2,
    'mirror': 2 
  },
  {
    'shape': [
      [0, 1],
      [1, 1],
      [1, 0]
    ],
    'rotate': 2,
    'mirror': 2
  },
  {
    'shape': [
      [1, 1],
      [1, 1]
    ],
    'rotate': 1 ,
    'mirror': 1
  },
  {
    'shape': [
      [1, 0],
      [1, 1],
      [1, 0],
      [1, 0]
    ],
    'rotate': 4 ,
    'mirror': 2
  },
  {
    'shape': [
      [1, 1, 1, 1],
      [0, 0, 0, 1]
    ],
    'rotate': 4 ,
    'mirror': 2
  },
  {
    'shape': [
      [1, 1, 1],
      [1, 0, 1]
    ],
    'rotate': 4 ,
    'mirror': 1
  },
  {
    'shape': [
      [0, 1, 1, 1],
      [1, 1, 0, 0]
    ],
    'rotate': 4 ,
    'mirror': 2
  },
  {
    'shape': [
      [1, 0],
      [1, 1],
      [1, 0]
    ],
    'rotate': 4 ,
    'mirror': 1
  },
  {
    'shape': [
      [0, 1, 0],
      [1, 1, 0],
      [0, 1, 1]
    ],
    'rotate': 4,
    'mirror': 2
  },
  {
    'shape': [
      [0, 0, 1],
      [1, 1, 1]
    ],
    'rotate': 4 ,
    'mirror': 2
  },
  {
    'shape': [
      [1, 1, 1],
      [0, 0, 1],
      [0, 0, 1]
    ],
    'rotate': 4,
    'mirror': 1
  },
  {
    'shape': [
      [1, 1],
      [1, 1],
      [1, 1]
    ],
    'rotate': 2,
    'mirror': 1
  }, 
]
   
def printObject(obj):
  for y in range(len(obj[0])):
    row_str = ""
    for z in range(len(obj)):
      for x in range(len(obj[0][0])):
        if  obj[z][y][x] <= 0:
          row_str += " --"
        else:
          row_str += "{:3}".format(obj[z][y][x])
      row_str += "   "
    print(row_str)
  print()

def insertShape(board, shape, x, y, z):
  for shape_z in range(len(shape)):
    for shape_y in range(len(shape[0])):
      for shape_x in range(len(shape[0][0])):
        if shape[shape_z][shape_y][shape_x] > 0:
          if board[shape_z + z][shape_y + y][shape_x + x] > 0:
            return False
      
  for shape_z in range(len(shape)):
    for shape_y in range(len(shape[0])):
      for shape_x in range(len(shape[0][0])):
        if shape[shape_z][shape_y][shape_x] > 0:
          board[shape_z + z][shape_y + y][shape_x + x] = shape[shape_z][shape_y][shape_x]
    
  return True

def removeShape(board, shape, x, y, z):      
  for shape_z in range(len(shape)):
    for shape_y in range(len(shape[0])):
      for shape_x in range(len(shape[0][0])):
        if shape[shape_z][shape_y][shape_x] > 0:
          board[shape_z + z][shape_y + y][shape_x + x] = -1
  
def rotateShape(shape):
  new_shape = []
  for row in range(len(shape[0])):
    new_row = []
    for col in range(len(shape)):
      new_row.append(shape[len(shape) - col - 1][row])
    new_shape.append(new_row)
  return new_shape

def mirrorShape(shape):
  new_shape = []
  for row in range(len(shape)):
    new_row = []
    for col in range(len(shape[0])):
      new_row.append(shape[row][len(shape[0]) - col - 1])
    new_shape.append(new_row)
  return new_shape
   
def findFirstEmptyPoint(board):
  for z in range(len(board)):
    for y in range(len(board[0])):
      for x in range(len(board[0][0])):
        if board[z][y][x] <= 0:
          return x,y,z
    
def findFirstFilledPoint(obj):
  for z in range(len(obj)):
    for y in range(len(obj[0])):
      for x in range(len(obj[0][0])):
        if obj[z][y][x] > 0:
          return x,y,z
      
def makeObject(shape):
  obj = [[]]
  
  for row in range(len(shape)):
    new_row = []
    for col in range(len(shape[0])):
      new_row.append(shape[row][col])
    obj[0].append(new_row)
  return obj

def rotateObject(obj):
  new_obj = []
  for new_z in range(len(obj[0])):
    new_plane = []
    for new_y in range(len(obj[0][0])):
      new_row = []
      for new_x in range(len(obj)):
        new_row.append(obj[new_x][new_z][new_y])
      new_plane.append(new_row)
    new_obj.append(new_plane)
  return new_obj

def placeShape(board, unused_pieces, setup):
  x, y, z = findFirstEmptyPoint(board)
  
  for piece_idx in unused_pieces:
    setup.append(piece_idx)
    piece = pieces[piece_idx]
    shape = piece['shape']
  
    for mirr in range(piece['mirror']):
      setup.append(mirr)
      if mirr > 0:
        shape = mirrorShape(piece['shape'])

      for rot in range(piece['rotate']):
        setup.append(rot)
        if rot > 0:
          shape = rotateShape(shape)
          
        obj = makeObject(shape)
          
        for orientation in range(3):    
          if orientation > 0:
            obj = rotateObject(obj)
            
          obj_x, obj_y, obj_z = findFirstFilledPoint(obj)
          if x - obj_x + len(obj[0][0]) > 4 or y - obj_y + len(obj[0]) > 4 or z - obj_z + len(obj) > 4 or x < obj_x or y < obj_y or z < obj_z:
            continue
    
          setup.append(orientation)
          if insertShape(board, obj, x - obj_x, y - obj_y, z - obj_z):              
            new_unused_pieces = unused_pieces.copy()
            new_unused_pieces.pop(piece_idx)

            if not new_unused_pieces:
#              print("Heureka!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
              printObject(board)
              print(setup)
              
              with open('results', 'a') as f:
                original_stdout = sys.stdout
                sys.stdout = f 
                printObject(board)
                sys.stdout = original_stdout           
            else:
              placeShape(board, new_unused_pieces, setup)
            
            removeShape(board, obj, x - obj_x, y - obj_y, z - obj_z) 
          setup.pop() 
        setup.pop()
      setup.pop()
    setup.pop()
           
def placeShapeH(board):
  shape = pieces[0]['shape']
  
  unused_pieces = { 1: 1, 2:1, 3:1, 4:1, 5:1, 6:1, 7:1, 8:1, 9:1, 10:1, 11:1, 12:1 }
      
  for z in range(2):
    obj = makeObject(shape)
    insertShape(board, obj, 0, 0, z)
    
    printObject(board)
      
    setup = [z]      
    placeShape(board, unused_pieces, setup)
    removeShape(board, obj, 0, 0, z)
    
for shape_idx in range(len(pieces)):
  piece = pieces[shape_idx]
  shape = piece['shape']
  
  for shape_row in range(len(shape)):
    for shape_col in range(len(shape[0])):
      if shape[shape_row][shape_col] > 0:
        shape[shape_row][shape_col] = shape_idx + 1
        
#  obj = makeObject(shape)
#  for orientation in range(3):    
#    if orientation > 0:
#      obj = rotateObject(obj)
#    printObject(obj)
  
board_line = []
for col in range(4):
  board_line.append(-1)
  
board_plane = []
for col in range(4):
  board_plane.append(board_line.copy())
  
board = []
for row in range(4):
  board.append(copy.deepcopy(board_plane))

#printObject(board)

placeShapeH(board)

