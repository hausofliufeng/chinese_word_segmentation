import sys
import numpy as np
np.random.seed(37)

from fs import fread,fwrite



if __name__ == '__main__':
    path_to_src=sys.argv[1]
    path_to_des=sys.argv[2]
    ratio=float(sys.argv[3])

    data=fread(path_to_src)
    np.random.shuffle(data)

    num=round(len(data)*ratio)
    val=data[:num]

    fwrite(path_to_des,val)