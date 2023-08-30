# IPython log file
import math
import matplotlib.pyplot as plt
import numpy as np
def neig_ls(idx, w, l):
    cx = idx%l
    cy = idx//l
    nx = list([cx - 1, cx + 1])
    ny = list([cy - 1, cy + 1])
    #nxn = [ele for ele in nx if ele >= 0 and ele < n]
    nxn = nx
    nyn = [ele for ele in ny if ele >= 0]
    out = []
    for i in nxn:
        if i < 0:
            i = i + l
        elif i >= l:
            i = i - l
        ij = i + cy*l
        out.append(ij)
    for j in nyn:
        if j >= w:
            out.append('treat')
        else:
            ij = cx + j*l
            out.append(ij)
    return out

def project(arr, w, l):
    zz = np.zeros((w, l))
    for idx in range(len(arr[0])):
        x = idx%l
        y = idx//l
        zz[y][x] = arr[0][idx]
    return zz

# neighbor list done
w = 100 #200
l = 250 #500
soil_grid = np.random.choice(list(range(5, 11)), size=(1, w*l))
water_grid = np.random.choice(list(range(1, 6)), size=(1, w*l))

first_p = np.random.randint(w*l)
k = 0
while k < 10000: # 2e+9 iterations
    k = k + 1
    first_p = np.random.randint(w*l)
    nn = neig_ls(first_p, w, l)
    if 'treat' in nn:
        soil_grid[0][first_p] = soil_grid[0][first_p] - 1
        water_grid[0][first_p] = water_grid[0][first_p] - 1
        continue
    else:
        ss = soil_grid + water_grid
        tts = [ss[0][ele] for ele in nn]
        cch = ss[0][first_p]*np.ones((1, len(tts)))[0] -  np.array(tts)
        ccp = cch[cch > 0]
        if len(ccp) == 0:
            soil_grid[0][first_p] = soil_grid[0][first_p]
            water_grid[0][first_p] = water_grid[0][first_p]
        else:
            ii = list(cch).index(max(cch))
            si = nn[ii]
            if soil_grid[0][first_p] - soil_grid[0][si] > 1:
                soil_grid[0][first_p]  = soil_grid[0][first_p] - 1
                soil_grid[0][si]  = soil_grid[0][si] + 1
                wtt = int(water_grid[0][first_p] + water_grid[0][si])
                comp = []
                cid = []
                for i in range(wtt+1):
                    #cnt = soil_grid[0][si] + i - soil_grid[0][first_p] - wtt + i
                    cnt =  soil_grid[0][first_p] + wtt - i - soil_grid[0][si] - i
                    if cnt >= 0:
                        comp.append(cnt)
                        cid.append(i) # i is the water flowing to des
                #w2d = cid[comp.index(min(comp))]
                if len(comp) == 0:
                    w2d = 0
                else:
                    w2d = cid[comp.index(min(comp))]
                water_grid[0][first_p] = water_grid[0][first_p] - w2d
                water_grid[0][si] = water_grid[0][si] + w2d
            else: #when the soil diff <= 1
                bb = (water_grid[0][first_p] + water_grid[0][si])/2
                b1 = math.floor(bb)
                b0 = math.ceil(bb)
                water_grid[0][first_p] = b0
                water_grid[0][si] = b1

# Here only show the final state
sw = soil_grid + water_grid
aa = project(sw, w, l)
ab = project(soil_grid, w, l)
ac = project(water_grid, w, l)

print('Standard deviation of total level', np.std(aa))
plt.figure()
plt.title('Soil height after {} iterations'.format(k))
plt.imshow(ab)
plt.colorbar()
plt.show()
