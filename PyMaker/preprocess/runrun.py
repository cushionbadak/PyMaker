import crawlSO as cso
import time

#for i in range(39, 226):
#    cso.Run1(100 * i + 1, 100 * i + 100, False)
#    ff = open("Done" + str(100 * i + 1) + '_' + str(100 * i + 100) + '.txt', 'w')
#    ff.write("Done.")
#    ff.close()
#    time.sleep(10)

cso.Run2(1, 100, False)
