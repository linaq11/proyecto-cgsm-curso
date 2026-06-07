# -*- coding: utf-8 -*-
import os, win32com.client

pptx = r"C:\LINA\UNAL 2626-1\PROG_SIG\Docker_1\proyecto-cgsm\docs\presentacion\Presentacion_ProgSIG_CGSM.pptx"
outdir = r"C:\LINA\UNAL 2626-1\PROG_SIG\Docker_1\proyecto-cgsm\docs\presentacion\_qa"
os.makedirs(outdir, exist_ok=True)
for f in os.listdir(outdir):
    if f.lower().endswith(".png"):
        os.remove(os.path.join(outdir, f))

ppt = win32com.client.Dispatch("PowerPoint.Application")
pres = ppt.Presentations.Open(pptx, WithWindow=False)
n = pres.Slides.Count
for i in range(1, n + 1):
    pres.Slides(i).Export(os.path.join(outdir, f"slide-{i:02d}.png"), "PNG", 1600, 900)
pres.Close()
ppt.Quit()
print("EXPORTED", n, "slides to", outdir)
