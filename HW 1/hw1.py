class bfs_node:
  state = 0
  x = 0
  y = 0
  z = 0
  parent = 0
  
  def __init__(self,x,y,z,parent):
    self.x = x
    self.y = y
    self.z = z
    self.parent = parent
    
class ucs_node:
  state = 0
  x = 0
  y = 0
  z = 0
  parent = 0
  cost = 0
  
  def __init__(self,x,y,z,parent,cost):
    self.x = x
    self.y = y
    self.z = z
    self.parent = parent
    self.cost = cost
    
class astar_node:
  state = 0
  x = 0
  y = 0
  z = 0
  parent = 0
  cumul_cost = 0
  cost = 0
  
  def __init__(self,x,y,z,parent,cumul_cost):
    self.x = x
    self.y = y
    self.z = z
    self.parent = parent
    self.cumul_cost = cumul_cost


def check_target(nod,target):
  if((nod.x==target.x)&(nod.y==target.y)):
    return 1
  else:
    return 0

def check_frontier(child,front):
  x_child = child.x
  y_child = child.y
  target_exists_in_front=0
  for i in front:
    if((x_child==i.x)&(y_child==i.y)):
      target_exists_in_front=1
      return target_exists_in_front
  return target_exists_in_front

def get_from_frontier(child,frontier):
  x_child = child.x
  y_child = child.y
  for i in frontier:
    if((x_child==i.x)&(y_child==i.y)):
      return i


def check_closed(child,closed):
  x_child = child.x
  y_child = child.y
  target_exists_in_closed=0
  for i in closed:
    if((x_child==i.x)&(y_child==i.y)):
      target_exists_in_closed=1
      return target_exists_in_closed
  return target_exists_in_closed

def get_from_closed(child,closed):
  x_child = child.x
  y_child = child.y
  for i in closed:
    if((x_child==i.x)&(y_child==i.y)):
      return i

def get_cost(vari):
  return vari.cost

def sort_frontier(frontier):
  frontier.sort(key=get_cost) 
  return frontier

def calculate_path(node_in,land):
  path = []
  flag=0
  while(flag!=1):
    path.append((node_in.x,node_in.y))
    if((node_in.x==land.x)&(node_in.y==land.y)):
      flag = 1
    node_in = node_in.parent
  revpath=[]
  while(len(path)!=0):
    add = path.pop()
    revpath.append(add)
  return revpath


def get_difference(childz,parentz):
  childz = int(childz)
  parentz = int(parentz)
  diff = childz-parentz
  return abs(diff)

def neighbors_bfs(node,z_value,limit,state):
  x = node.x 
  y = node.y 
  z = node.z
  parent = node.state
  parent_cost = 1
  neighbors = [] 
  if(x>=1):
    try:
      neighbors.append(bfs_node(x-1,y,z_value[y][x-1],parent))
    except IndexError:
      pass
    try:
      neighbors.append(bfs_node(x-1,y+1,z_value[y+1][x-1],parent))
    except IndexError:
      pass
  try:
    neighbors.append(bfs_node(x,y+1,z_value[y+1][x],parent))
  except IndexError:
    pass
  try:
    neighbors.append(bfs_node(x+1,y+1,z_value[y+1][x+1],parent))
  except IndexError:
    pass
  try:
    neighbors.append(bfs_node(x+1,y,z_value[y][x+1],parent))
  except IndexError:
    pass
  if(y>=1):
    try:
      neighbors.append(bfs_node(x+1,y-1,z_value[y-1][x+1],parent))
    except IndexError:
      pass
    try:
      neighbors.append(bfs_node(x,y-1,z_value[y-1][x],parent))
    except IndexError:
      pass
  if((x>=1)&(y>=1)):
    try:
      neighbors.append(bfs_node(x-1,y-1,z_value[y-1][x-1],parent))
    except IndexError:
      pass
  
  permissible = []
  for j in neighbors: 
    diff = get_difference(j.z,node.z)
    if(diff<=limit): 
      state+=1
      j.state = state
      permissible.append(j)
  return permissible,state


def bfs(frontier,closed,target,landing,z_value,z_limit):
  target_found = 0
  state = 0
  while(target_found==0):
    if(len(frontier)==0):
      result=0
      return result
    curr_node = frontier.pop(0) 
    closed.append(curr_node)
    flag = check_target(curr_node,target)
    if(flag==1):
        target_found=1
        return calculate_path(curr_node,landing)
    else:
      children,state = neighbors_bfs(curr_node,z_value,z_limit,state)
      for m in children:
        flag2 = check_frontier(m,frontier)
        flag3 = check_closed(m,closed)     
        if((flag2==0)&(flag3==0)):
          m.parent = curr_node
          frontier.append(m)


def neighbors_ucs(node,z_value,limit,state):
  x = node.x
  y = node.y
  z = node.z
  parent = node.state
  parent_cost = node.cost
  neighbors = []
  st_cost = 10
  diag_cost = 14
  if(x>=1):
    try:
      neighbors.append(ucs_node(x-1,y,z_value[y][x-1],parent,(parent_cost+st_cost)))
    except IndexError:
      pass
    try:
      neighbors.append(ucs_node(x-1,y+1,z_value[y+1][x-1],parent,(parent_cost+diag_cost)))
    except IndexError:
      pass
  try:
    neighbors.append(ucs_node(x,y+1,z_value[y+1][x],parent,(parent_cost+st_cost)))
  except IndexError:
    pass
  try:
    neighbors.append(ucs_node(x+1,y+1,z_value[y+1][x+1],parent,(parent_cost+diag_cost)))
  except IndexError:
    pass
  try:
    neighbors.append(ucs_node(x+1,y,z_value[y][x+1],parent,(parent_cost+st_cost)))
  except IndexError:
    pass
  if(y>=1):
    try:
      neighbors.append(ucs_node(x+1,y-1,z_value[y-1][x+1],parent,(parent_cost+diag_cost)))
    except IndexError:
      pass
    try:
      neighbors.append(ucs_node(x,y-1,z_value[y-1][x],parent,(parent_cost+st_cost)))
    except IndexError:
      pass
  if((x>=1)&(y>=1)):
    try:
      neighbors.append(ucs_node(x-1,y-1,z_value[y-1][x-1],parent,(parent_cost+diag_cost)))
    except IndexError:
      pass
  

  permissible = []
  for j in neighbors:
    diff = get_difference(j.z,node.z)
    if(diff<=limit):
      state+=1
      j.state = state
      permissible.append(j)

  return permissible,state


def uniform_cost(frontier,closed,target,landing_node,z_value,z_limit):
  state = 0 
  target_found = 0 
  while(target_found!=1): 
    if(len(frontier)==0):
      result = 0
      return result
    curr_node = frontier.pop(0) 
    closed.append(curr_node)
    flag = check_target(curr_node,target)
    if(flag==1): 
      final_path = calculate_path(curr_node,landing_node)
      return final_path
   
    else:
      children, state = neighbors_ucs(curr_node,z_value,z_limit,state)
      for c in children:
        flag2 = check_frontier(c,frontier)
        flag3 = check_closed(c,closed)
        if((flag2==0)&(flag3==0)):
          c.parent = curr_node
          frontier.append(c)

      frontier = sort_frontier(frontier)
        

def heuristic(node,target):
  x1 = node.x
  y1 = node.y
  z1 = node.z
  x2 = target.x
  y2 = target.y
  z2 = target.z 
  diff1 = (x1 - x2)**2
  diffy = (y1 - y2)**2
  sum1 = diff1+diffy
  end = sum1**(1/2)
  return (int)(end*10)


def neighbors_astar(node,target,z_value,limit,state):
  x = node.x
  y = node.y
  z1 = node.z
  parent = node.state
  parent_cost = node.cost
  neighbors = []
  st_cost = 10
  diag_cost = 14
  if(x>=1):
    try:
      ct = parent_cost+st_cost+get_difference(z1,z_value[y][x-1])
      neighbors.append(astar_node(x-1,y,z_value[y][x-1],parent,ct))
    except IndexError:
        pass
    try:
      ct = parent_cost+diag_cost+get_difference(z1,z_value[y+1][x-1])
      neighbors.append(astar_node(x-1,y+1,z_value[y+1][x-1],parent,ct))
    except IndexError:
      pass 
  try:  
    ct = parent_cost+st_cost+get_difference(z1,z_value[y+1][x])
    neighbors.append(astar_node(x,y+1,z_value[y+1][x],parent,ct))
  except IndexError:
    pass
  try:
    ct = parent_cost+diag_cost+get_difference(z1,z_value[y+1][x+1])
    neighbors.append(astar_node(x+1,y+1,z_value[y+1][x+1],parent,ct))
  except IndexError:
    pass
  try:
    ct = parent_cost+st_cost+get_difference(z1,z_value[y][x+1])
    neighbors.append(astar_node(x+1,y,z_value[y][x+1],parent,ct))
  except IndexError:
    pass
  if(y>=1):
    try:
      ct = (parent_cost+diag_cost+get_difference(z1,z_value[y-1][x+1]))
      neighbors.append(astar_node(x+1,y-1,z_value[y-1][x+1],parent,ct))
    except IndexError:
      pass
    try:  
      ct = parent_cost+st_cost+get_difference(z1,z_value[y-1][x])
      neighbors.append(astar_node(x,y-1,z_value[y-1][x],parent,ct))
    except IndexError:
      pass
  if((x>=1)&(y>=1)):
    try:
      ct = parent_cost+diag_cost+get_difference(z1,z_value[y-1][x-1])
      neighbors.append(astar_node(x-1,y-1,z_value[y-1][x-1],parent,ct))
    except IndexError:
      pass

  permissible = []
  for j in neighbors:
    diff = get_difference(j.z,z1)
    if(diff<=limit):
      state+=1
      j.state = state
      heur = heuristic(j,target)
      j.cost = j.cumul_cost + heur 
      permissible.append(j)
  return permissible,state

def a_star(frontier,closed,target,landing_node,z_value,z_limit):
  state = 0
  target_found = 0 

  while(target_found!=1): 
    if(len(frontier)==0):
      result = 0
      return result
    curr_node = frontier.pop(0)
    closed.append(curr_node)
    flag = check_target(curr_node,target)
    if(flag==1):
      final_path = calculate_path(curr_node,landing_node)
      return final_path
    else:
      children, state = neighbors_astar(curr_node,target,z_value,z_limit,state)
      for c in children:
        flag2 = check_frontier(c,frontier) 
        if(flag2==1): 
          u = get_from_frontier(c,frontier)
          if(c.cost<u.cost):
            frontier.remove(u)
            frontier.append(c)
        flag3 = check_closed(c,frontier)
        if(flag3==1):
          u = get_from_closed(c,frontier)
          if(c.cost<u.cost):
            closed.remove(u)
            frontier.append(c)
        if((flag2==0)&(flag3==0)):
          c.parent = curr_node
          frontier.append(c)
    frontier = sort_frontier(frontier)

def answer(path,l):
  out = open("output.txt","a+")
  if(l!=0):
    out.write("\n")
  if(path==0):
    out.write("FAIL")
  else:
    for t in range(len(path)):
      out.write("%d,%d" %path[t])
      if(t!=(len(path)-1)):
        out.write(" ")

def main():
  f = open("input.txt","r")
  fl = f.readlines()
  algorithm = fl[0]
  num = fl[1].split()
  no_cols = (int)(num[0])
  no_rows = (int)(num[1])
  lan = (fl[2]).split()
  x_land = (int)(lan[0])
  y_land = (int)(lan[1])
  z = int(fl[3])
  no_targets = int(fl[4])
  targets = []
  for i in range(1, no_targets+1):
    tar = (fl[4+i]).split()
    targets.append(tar)
  z_value = []
  c=5+no_targets
  out = open("output.txt","w+")
  for j in range(1,no_rows+1):
    z_value.append((fl[c+j-1]).split())
  if(algorithm.startswith("BFS")|algorithm.startswith("bfs")):
    for l in range(0,no_targets):
      landing_node = bfs_node(x_land,y_land,z_value[y_land][x_land],0)
      landing_node.state = 0
      frontier = [landing_node]
      closed = []
      x_tar = int(targets[l][0])
      y_tar = int(targets[l][1])
      curr_target = bfs_node(x_tar,y_tar,z_value[y_tar][x_tar],0)
      path = bfs(frontier,closed,curr_target,landing_node,z_value,z)
      answer(path,l)
  if(algorithm.startswith("UCS")|algorithm.startswith("ucs")):
    for l in range(0,no_targets):
      landing_node = ucs_node(x_land,y_land,z_value[y_land][x_land],0,0)
      landing_node.state = 0
      frontier = [landing_node]
      closed = []
      x_tar = int(targets[l][0])
      y_tar = int(targets[l][1])
      curr_target = ucs_node(x_tar,y_tar,z_value[y_tar][x_tar],0,0)
      path = uniform_cost(frontier,closed,curr_target,landing_node,z_value,z)
      answer(path,l)
  if(algorithm.startswith("A*")|algorithm.startswith("a*")):
    for l in range(0,no_targets):
      landing_node = astar_node(x_land,y_land,z_value[y_land][x_land],0,0)
      landing_node.state = 0
      frontier = [landing_node]
      closed = []
      x_tar = int(targets[l][0]) 
      y_tar = int(targets[l][1])
      curr_target = astar_node(x_tar,y_tar,z_value[y_tar][x_tar],0,0)
      path = a_star(frontier,closed,curr_target,landing_node,z_value,z)
      answer(path,l)
    
if __name__ == "__main__":
  main()
