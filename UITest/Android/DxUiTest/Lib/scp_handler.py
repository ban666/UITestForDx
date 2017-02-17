# -*- coding: utf-8 -*-
__author__ = 'liaoben'

import paramiko

from scp import SCPClient
import os
from Common import get_image_info
class SCPHandler:

    def __init__(self):
        Host = '10.99.113.80'
        user = "root"
        passwd = "4qGO2M99Fu.XIM#"
        port =22

        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(Host,port,user, passwd)

        self.scpclient = SCPClient(self.ssh.get_transport(), socket_timeout=15.0)

    def get_pic(self,fname,save_name):
        #remotepath='/wwwdata/sjw/resource/img/'+fname
        remotepath=fname
        localpath='g:/test/data/'+save_name
        self.scpclient.get(remotepath, localpath)  #从服务器中获取文件
        return os.path.abspath(localpath)

    def exec_cmd(self,cmd):
        stdin,stdout,stderr=self.ssh.exec_command(cmd)    #一次性的执行命令
        cmd_result=stdout.read(),stderr.read()     #读取命令结果
        return cmd_result

    def close(self):
        self.ssh.close()


if __name__ == '__main__':
    s = SCPHandler()
    pic_list =['/sjw/resource/img/5968/m_7737156199495802881_5248_3936_.jpg','/sjw/resource/img/5968/m_7737154945566679041_3936_5248_.jpg','/sjw/resource/img/5968/m_7737153427060858881_3936_5248_.jpg',
'/sjw/resource/img/5968/m_7737152143561891841_1753_10000_.jpg','/sjw/resource/img/5968/m_7737150402086871041_3936_5248_.jpg','/sjw/resource/img/5968/m_7737148847971409921_3936_3936_.jpg',
'/sjw/resource/img/5968/m_7737147510156206081_8450_3756_.jpg','/sjw/resource/img/5616/m_7737781085863976961_2500_1111_.jpg']
    pic_list = ['/wwwdata'+x for x in pic_list]
    for i in range(len(pic_list)):
        r = s.get_pic(pic_list[i],str(i)+'.jpg')
        print get_image_info(r)
    #s.get_pic()
    # import os
    # localpath='./data/1.jpg'
    # print  os.path.abspath(localpath)
    # r = s.exec_cmd('ls /wwwdata/sjw/resource/img/9776/')
    # print r
