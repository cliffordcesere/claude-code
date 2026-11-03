"""ORA — extrait le logo vectoriel de la fiche de construction (PDF) en SVG.

Usage :
    D=$(mktemp -d)
    for i in 1 3 5; do pdftocairo -svg -f $i -l $i ora/logo/ORA_logo_construction_v3.1.pdf $D/p$i.svg; done
    python3 ora/tools/extract_logo.py $D ora/logo/svg

Sources : p.1 assemblage horizontal (cuivre), p.3 symbole renforcé, p.5 assemblage vertical.
Le symbole seul est découpé dans l'assemblage horizontal. Coordonnées normalisées en unités u
(u = épaisseur du trait ; anneau = 12u). Aucune forme n'est redessinée.
"""
import re,sys,os,json
SRC=sys.argv[1]; OUT=sys.argv[2]
def paths(f):
    s=open(f).read().split('</defs>')[1]
    return [(a,d) for a,d in re.findall(r'<path ([^>]*?)d="([^"]+)"',s)]
def bbox(d):
    n=[float(x) for x in re.findall(r'-?\d+\.?\d*',d)]
    return min(n[0::2]),min(n[1::2]),max(n[0::2]),max(n[1::2])
def norm(d,ox,oy,u):
    toks=re.findall(r'[A-Za-z]|-?\d+\.?\d*',d); out=[];i=0;xy=0
    for t in toks:
        if t.isalpha(): out.append(t); xy=0
        else:
            v=float(t); v=(v-ox)/u if xy==0 else (v-oy)/u
            out.append(f"{v:.4f}".rstrip('0').rstrip('.')); xy^=1
    return ' '.join(out).replace(' Z',' Z')
def subs(d): return ['M'+p for p in d.split('M')[1:]]
p1=paths(f"{SRC}/p1.svg"); horiz=[d for a,d in p1 if '72.158813%' in a and 'evenodd' in a][0]
x0,y0,x1,y1=bbox(horiz); u=(y1-y0)/12
info={"u_pt_p1":u,"w_u":(x1-x0)/u}
for i,s in enumerate(subs(horiz)):
    b=bbox(s); info[f"sub{i}"]=[round((b[0]-x0)/u,3),round((b[1]-y0)/u,3),round((b[2]-x0)/u,3),round((b[3]-y0)/u,3)]
sym=' '.join(s for s in subs(horiz) if (bbox(s)[2]-x0)/u<=12.01)
word=' '.join(s for s in subs(horiz) if (bbox(s)[0]-x0)/u>12.01)
p5=paths(f"{SRC}/p5.svg"); vert=[d for a,d in p5 if 'evenodd' in a and bbox(d)[0]>500][0]
p3=paths(f"{SRC}/p3.svg"); renf=[d for a,d in p3 if 'evenodd' in a and bbox(d)[2]-bbox(d)[0]>80][0]
shapes={}
def add(name,d):
    b=bbox(d); uu=(b[2]-b[0])/12 if name in('vertical','symbole','symbole-renforce') else u
    shapes[name]=(norm(d,b[0],b[1],uu),round((b[2]-b[0])/uu,4),round((b[3]-b[1])/uu,4))
add('horizontal',horiz); add('symbole',sym); add('vertical',vert); add('symbole-renforce',renf)
b=bbox(word); shapes['logotype-ref']=(norm(word,b[0],b[1],u),round((b[2]-b[0])/u,4),round((b[3]-b[1])/u,4))
info.update({k:[v[1],v[2]] for k,v in shapes.items()})
print(json.dumps(info,indent=1))
VER={'cuivre-sur-noir':('#B87333','#0A0A0A'),'blanc-sur-noir':('#FAFAFA','#0A0A0A'),'noir-sur-blanc':('#0A0A0A','#FAFAFA')}
os.makedirs(OUT,exist_ok=True)
for name,(d,w,h) in shapes.items():
    if name=='logotype-ref': continue
    for vn,(fg,bg) in VER.items():
        for withbg in (False,True):
            fn=f"{OUT}/ORA_logo_{name}_{vn}{'_fond' if withbg else ''}.svg"
            if withbg:
                m=h  # zone de securite 1x hauteur symbole = 12u ; on prend 12u
                m=12.0
                vb=f"{-m} {-m} {w+2*m:.4f} {h+2*m:.4f}"; rect=f'<rect x="{-m}" y="{-m}" width="{w+2*m:.4f}" height="{h+2*m:.4f}" fill="{bg}"/>'
            else:
                vb=f"0 0 {w} {h}"; rect=''
            open(fn,'w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}">{rect}<path fill="{fg}" fill-rule="evenodd" d="{d}"/></svg>\n')
