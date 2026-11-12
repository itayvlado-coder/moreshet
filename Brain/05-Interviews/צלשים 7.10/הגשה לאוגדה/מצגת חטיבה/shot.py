import sys, subprocess, pathlib
import build_deck as b
HERE = b.HERE
slides = b.build_slides()
for a in sys.argv[1:]:
    n = int(a)
    f = HERE / "_one.html"
    f.write_text(b.page([slides[n-1]], b.NUM_JS), encoding="utf-8")
    out = HERE / "preview" / f"slide_{n:02d}.png"
    subprocess.run([b.CHROME, "--headless", "--disable-gpu", "--virtual-time-budget=4000", "--hide-scrollbars",
                    "--window-size=1600,900", f"--screenshot={out}", f.as_uri()], capture_output=True)
    print(out)
