import numpy
def calc_move(unstable,uncross,mov_map,pos,mov):
    #####################################################
    # To calculate the moving range of one character:   #
    # unstable=cannot stay at the grid after moving     #
    # uncross=cannot cross over the grid                #
    # mov_map=decay of MOVING ABILITY                   #
    # pos=start at the grid  MOV=initial MOVING ABILITY #
    #####################################################
    #mov_map = numpy.random.randint(1,5,(15, 15))
    #pos = (6, 6)
    #mov = 10
    #unstable=set([(1,2),(5,6)])
    #uncross=set([(4,5),(2,2)])
    wait = {}
    dst = {}
    wait[pos] = mov
    (M,N)=mov_map.shape
    for item in uncross:
        mov_map[item]=255
    while len(wait) > 0:
        (tpos, r) = max(wait.items(), key=lambda x: x[1])
        dst[tpos] = r
        wait.pop(tpos)
        if tpos[0] > 0:
            npos = (tpos[0] - 1, tpos[1])
            if not (npos in dst):
                tr = r - mov_map[npos]
                if (tr >= 0):
                    if npos in wait:
                        r0 = wait[npos]
                        if tr > r0:
                            wait[npos] = tr
                    else:
                        wait[npos] = tr
        if tpos[0] < M-1:
            npos = (tpos[0] + 1, tpos[1])
            if not (npos in dst):
                tr = r - mov_map[npos]
                if tr >= 0:
                    if npos in wait:
                        r0 = wait[npos]
                        if tr > r0:
                            wait[npos] = tr
                    else:
                        wait[npos] = tr
        if tpos[1] > 0:
            npos = (tpos[0], tpos[1] - 1)
            if not (npos in dst):
                tr = r - mov_map[npos]
                if tr >= 0:
                    if npos in wait:
                        r0 = wait[npos]
                        if tr > r0:
                            wait[npos] = tr
                    else:
                        wait[npos] = tr
        if tpos[1] < N-1:
            npos = (tpos[0], tpos[1] + 1)
            if not (npos in dst):
                tr = r - mov_map[npos]
                if tr >= 0:
                    if npos in wait:
                        r0 = wait[npos]
                        if tr > r0:
                            wait[npos] = tr
                    else:
                        wait[npos] = tr
    for item in unstable:
        if item in dst:
            dst.pop(item)
    return dst.keys()