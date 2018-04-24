#!/usr/bin/env python
#---------------------------------------------
from ftplib import FTP
import datetime,time
import os
import sys

def ftpconnect(host, username, password):
    print('ftpconnect start...')
    ftp = FTP()
    ftp.connect(host, 21)
    ftp.login(username, password)
    print('ftpconnect end...')
    return ftp
    
def downloadfile(ftp, remotefile, localfile):
    bufsize = 1024
    fp = open(localfile,'wb')
    ftp.retrbinary('RETR ' + remotefile, fp.write, bufsize)
#    ftp.set_debuglevel(0)
#    fp.close()

def uploadfile(ftp, remotefile, localfile):
    bufsize = 1024
    fp = open(localfile, 'rb')
    ftp.storbinary('STOR '+ remotefile+'.tmp' , fp, bufsize)
    ftp.rename(remotefile+'.tmp',remotefile)
#    ftp.set_debuglevel(0)
#    fp.close() 

#
# set job scheduler: serial, parallel, remote
#
# /g1/mesoium/RMAPS/result/2D_nest/$ECFDATE$HH/unipost/chem
def trans_rafs(srcIp,srcUser,srcPass,srcDir,objIp,objUser,objPass,objDir,IYYYYMMDDHH,FFF):
    try:
        IYYYYMMDD=IYYYYMMDDHH[0:8]
        IHH=IYYYYMMDDHH[8:]
        srcFtp=ftpconnect(srcIp,srcUser,srcPass)
        srcFtp.cwd(srcDir)
        if srcFtp.nlst().index(IYYYYMMDD) < 0:
            return "can't find directory: "+IYYYYMMDD
        else:
            srcFtp.cwd(IYYYYMMDD)
            if srcFtp.nlst().index(IHH) < 0:
                return "can't find directory: "+IHH
            else:
                srcFtp.cwd(IHH)
#        srcFtp.cwd(srcDir+'/'+IYYYYMMDD+'/'+IHH)
        objFtp=ftpconnect(objIp,objUser,objPass)
        objFtp.cwd(objDir)
        exist=0
        if IYYYYMMDDHH in objFtp.nlst():
            exist=1
        if exist == 0:
            objFtp.mkd(IYYYYMMDDHH)
        objFtp.cwd(IYYYYMMDDHH)
        print('trans_rafs start...')
#        for FFF in range(0,4,3):
        itime=datetime.datetime(int(IYYYYMMDDHH[0:4]),int(IYYYYMMDDHH[4:6]),int(IYYYYMMDDHH[6:8]),int(IYYYYMMDDHH[8:10]))
        ctime=itime+datetime.timedelta(hours=int(FFF))
        if len(srcFtp.nlst()) != 0:
            for file in srcFtp.nlst():
                if file.find('pgrb2.0p50.f'+FFF+'.bin') >= 0:
                    size=long(0)
                    realsize=long(1)
                    while size != realsize:
                        size=realsize
                        srcFtp.voidcmd('type i')
                        realsize=long(srcFtp.size(file))
                        print("file size 30 seconds ago: "+str(size))
                        print("file size now: "+str(realsize))
                        if size == realsize:
                            srcFile=file
                            locFile='gfs.t'+IHH+'z.pgrb2.0p50.f'+FFF
                            downloadfile(srcFtp,srcFile,locFile)
                            print('get '+srcFile+' to '+locFile+' complete.')
                            objFile=locFile
                            uploadfile(objFtp,objFile,locFile)
                            print('put '+locFile+' complete.')
#                            os.remove(locFile)
                        else:
                            time.sleep(30)
        srcFtp.close()
        objFtp.close()
    except Exception as e:
        print(e)

if __name__ == "__main__":
#    IYYYYMMDD=(datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y%m%d") 
#    IYYYYMMDDHH=IYYYYMMDD+'12'
    if(len(sys.argv)!=3):
        print("")
        print("**********************************************")
        print("Usage: "+sys.argv[0]+" YYYYMMDDHH FFF")
        print("**********************************************")
        print("")
        os._exit(0)
    IYYYYMMDDHH=sys.argv[1]
    FFF=sys.argv[2]
    srcIp='10.10.72.41'
    srcUser='nwp'
    srcPass='nafp'
    srcDir='/NAFP/NCEP/GFS/0p5'
    objIp='10.10.65.82'
    objUser='cor'
    objPass='smc'
    objDir='/gfs/0p50'
#    IYYYYMMDDHH='2017111412'
    trans_rafs(srcIp,srcUser,srcPass,srcDir,objIp,objUser,objPass,objDir,IYYYYMMDDHH,FFF)
