def generate():
    max = 1
    while True:
        for a in range(1, max + 1):
            for b in range(1, max + 1):
                for c in range(1, max + 1):
                    for d in range(1, max + 1):
                        for e in range(1, max + 1):
                            for f in range(1, max + 1):
                                for g in range(1, max + 1):
                                    for i in range(1, max + 1):
                                        for j in range(1, max + 1):
                                            magic = a+b+c+d
                                            h = magic-e-f-g
                                            k = magic-f-g-j
                                            l = magic-i-j-k
                                            m = magic-a-e-i
                                            n = magic-b-f-j
                                            o = magic-c-g-k
                                            p = magic-d-h-l
                                            if magic != a+f+k+p:continue
                                            if magic != d+g+j+m:continue
