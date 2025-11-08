import sys, math

EPS = 1e-9

def dist(p1, p2):
  return math.hypot(p1[0]-p2[0], p1[1]-p2[1])

def orient(p, q, r):
  v = (q[1]-p[1])*(r[0]-q[0]) - (q[0]-p[0])*(r[1]-q[1])
  if abs(v)<EPS: return 0
  return 1 if v>0 else 2

def onseg(a,b,c):
  if orient(a,b,c)!=0: return False
  return (min(a[0],c[0])-EPS<=b[0]<=max(a[0],c[0])+EPS) and (min(a[1],c[1])-EPS<=b[1]<=max(a[1],c[1])+EPS)

def inter(p1,q1,p2,q2):
  o1,o2,o3,o4 = orient(p1,q1,p2), orient(p1,q1,q2), orient(p2,q2,p1), orient(p2,q2,q1)
  if o1!=o2 and o3!=o4: return True
  if o1==0 and onseg(p1,p2,q1): return True
  if o2==0 and onseg(p1,q2,q1): return True
  if o3==0 and onseg(p2,p1,q2): return True
  if o4==0 and onseg(p2,q1,q2): return True
  return False

def interpt(p1,q1,p2,q2):
  x1,y1=p1; x2,y2=q1; x3,y3=p2; x4,y4=q2
  d=(x1-x2)*(y3-y4)-(y1-y2)*(x3-x4)
  if abs(d)<EPS: return None
  t=((x1-x3)*(y3-y4)-(y1-y3)*(x3-x4))/d
  u=-((x1-x2)*(y1-y3)-(y1-y2)*(x1-x3))/d
  if -EPS<=t<=1+EPS and -EPS<=u<=1+EPS:
    px=x1+t*(x2-x1); py=y1+t*(y2-y1)
    return (round(px,2), round(py,2))
  return None

def area(p):
  s=0
  n=len(p)
  for i in range(n):
    j=(i+1)%n
    s+=p[i][0]*p[j][1]-p[j][0]*p[i][1]
  return abs(s)/2.0

def main():
  d=sys.stdin.read().strip().split()
  if not d:
    print("Abandoned"); return
  n=int(d[0]); seg=[]; pts=set(); i=1
  for _ in range(n):
    x1,y1,x2,y2=map(int,d[i:i+4]); i+=4
    a,b=(x1,y1),(x2,y2)
    seg.append((a,b))
    pts|={a,b}

  for i1 in range(n):
    for j1 in range(i1+1,n):
      a1,b1=seg[i1]; a2,b2=seg[j1]
      if not inter(a1,b1,a2,b2): continue
      pt=interpt(a1,b1,a2,b2)
      if pt: pts.add(pt)
      elif orient(a1,b1,a2)==0:
        if onseg(a1,a2,b1): pts.add(a2)
        if onseg(a1,b2,b1): pts.add(b2)
        if onseg(a2,a1,b2): pts.add(a1)
        if onseg(a2,b1,b2): pts.add(b1)

  g={p:[] for p in pts}; used=set(); total=0.0
  for a,b in seg:
    spts=[x for x in pts if onseg(a,x,b)]
    if abs(a[0]-b[0])>EPS: spts.sort(key=lambda x:x[0])
    else: spts.sort(key=lambda x:x[1])
    for k in range(len(spts)-1):
      u,v=spts[k],spts[k+1]
      d1=dist(u,v)
      if d1<EPS: continue
      e=tuple(sorted((u,v)))
      if e in used: continue
      used.add(e)
      g[u].append((v,d1)); g[v].append((u,d1))
      total+=d1

  seen=set(); stack=[]; cyc=None

  def dfs(u,p):
    nonlocal cyc
    seen.add(u); stack.append(u)
    for v,_ in g[u]:
      if v==p: continue
      if v in stack:
        c=stack[stack.index(v):]
        if len(c)>=3:
          cyc=c; return True
      if v not in seen and dfs(v,u): return True
    stack.pop(); return False

  for pt in pts:
    if pt not in seen and cyc is None:
      dfs(pt,None)

  if not cyc:
    print("Abandoned"); return
  ar=area(cyc)
  if ar<EPS:
    print("Abandoned"); return

  clen=0
  for i in range(len(cyc)):
    clen+=dist(cyc[i],cyc[(i+1)%len(cyc)])

  rem=total-clen
  if rem<EPS:
    print("Kalyan"); return
  cmpa=(rem/4.0)**2
  print("Kalyan" if ar>cmpa+EPS else "Computer")

if __name__=="__main__":
  main()