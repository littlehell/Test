import os
import subprocess
import sys

def ReadGrib():
    Product = ['GH', 'U', 'V', 'W']
    PressureLevel = ['10', '20', '50', '70', '100', '150', '200', '250', '300', '400', '500', '600', '700', '800',
                     '850', '900', '925', '950', '1000']
    files = ['pl_2018021500000.grb1']
    os.chdir(r'D:\PythonProject\wgrib')
    Tempfile = []
    for file in files:
        for param in Product:
            for pl in PressureLevel:
                if param == 'GH':
                    OutName = 'tec{0}_{1}_{2}.txt'.format(file[:16], 'H', pl.zfill(4))
                else:
                    OutName = 'tec{0}_{1}_{2}.txt'.format(file[:16], param, pl.zfill(4))
                p = subprocess.call(
                    'wgrib.exe {0} -s |find ":{1}:{2} mb"| wgrib.exe {0} -i -nh -text -o {3}'.format(
                        file, param, pl, OutName), shell=True, stdin=subprocess.PIPE)
                #print(p)
                Tempfile.append(OutName)
    return Tempfile

def Conversion():
    Tempfile = ReadGrib()
    for file in Tempfile:
        f1 = open(file, 'r')
        lines = f1.readlines()
        f1.close()
        handled_lines = []
        for line in lines:
            handled_lines.append(line.strip())
        print(handled_lines)
        f2 = open(file[1:], 'w+')
        for item in handled_lines:
            f2.write(item + '\t')
        f2.close()
        os.remove(file)

if __name__ == '__main__':
    Conversion()
    sys.exit(0)

#a = os.system(r'wgrib.exe pl_2018021412000.grb1 -s |find ":GH:20 mb"|')

#os.system('wgrib.exe pl_2018021412000.grb1 -s | findstr \\X \":U:10\" | wgrib.exe pl_2018021412000.grb1 -i -nh -text -o test.txt')
