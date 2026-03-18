def find_cycle(G, V):
    """DFS-based cycle detection, returns cycle nodes."""
    color={v:0 for v in V}; parent={v:None for v in V}
    def dfs(v):
        color[v]=1
        for u in G.get(v,[]):
            if u not in V: continue
            if color[u]==0:
                parent[u]=v
                c=dfs(u)
                if c: return c
            elif color[u]==1:
                cycle=[u]; cur=v
                while cur!=u: cycle.append(cur); cur=parent[cur]
                return cycle
        color[v]=2; return None
    for v in V:
        if color[v]==0:
            c=dfs(v)
            if c: return c
    return None
 
def kernelise_fvs(G, k):
    """Kernelisation for Feedback Vertex Set: O(k^2) kernel."""
    V=set(G.keys()); fvs=set()
    while k>0:
        # Rule 1: self-loop
        for v in list(V):
            if v in G.get(v,[]): fvs.add(v); V.discard(v); k-=1; break
        # Rule 2: degree ≤ 1 vertices are safe (not in FVS)
        changed=True
        while changed:
            changed=False
            for v in list(V):
                if len([u for u in G.get(v,[]) if u in V])<=1:
                    V.discard(v); changed=True
        # Rule 3: pick high-degree vertex
        if k<=0: break
        cycle=find_cycle(G,V)
        if not cycle: break
        v=max(cycle, key=lambda x: len([u for u in G.get(x,[]) if u in V]))
        fvs.add(v); V.discard(v); k-=1
    return fvs, V
  G={0:[1,2],1:[0,2,3],2:[0,1,3],3:[1,2,4],4:[3]}
fvs,remaining=kernelise_fvs(G,2)
print(f"FVS kernel: {fvs}")
print(f"Remaining acyclic: {remaining}")
print(f"Verify acyclic: {find_cycle(G,remaining) is None}")
