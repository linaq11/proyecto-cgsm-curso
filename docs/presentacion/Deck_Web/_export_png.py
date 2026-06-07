# -*- coding: utf-8 -*-
import os, win32com.client

pptx = r"C:\LINA\UNAL 2626-1\AVANCE TESIS\Defensa_Lina_GeoAI_CGSM.pptx"
outdir = r"C:\LINA\UNAL 2626-1\AVANCE TESIS\_qa"
os.makedirs(outdir, exist_ok=True)
for f in os.listdir(outdir):
    if f.lower().endswith(".png"):
        os.remove(os.path.join(outdir, f))

ppt = win32com.client.Dispatch("PowerPoint.Application")
pres = ppt.Presentations.Open(pptx, WithWindow=False)
n = pres.Slides.Count
for i in range(1, n + 1):
    out = os.path.join(outdir, f"slide-{i:02d}.png")
    pres.Slides(i).Export(out, "PNG", 1600, 900)
pres.Close()
ppt.Quit()
print("EXPORTED", n, "slides to", outdir)
