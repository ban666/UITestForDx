# -*- coding: utf-8 -*-
__author__ = 'liaoben'

import paramiko


class SSHHandler:

    def __init__(self, host = '10.99.113.80', username = 'root', password = '4qGO2M99Fu.XIM#'):
        self._host = host
        self._username = username
        self._password = password
        self.connect()

    def connect(self):
        try:
            self._ssh_fd = paramiko.SSHClient()
            self._ssh_fd.set_missing_host_key_policy( paramiko.AutoAddPolicy() )
            self._ssh_fd.connect(self._host, username=self._username,password=self._password)
        except Exception, e:
            print( 'ssh %s@%s: %s' % (self._username, self._host, e) )
            exit()

    def sftp_open(self):
        self.sftpd = self._ssh_fd.open_sftp()

    def sftp_put( self, _put_from_path, _put_to_path ):
        return self.sftpd.put( _put_from_path, _put_to_path )

    def sftp_get( self, _get_from_path, _get_to_path ):
        return self.sftpd.get( _get_from_path, _get_to_path )

    def sftp_close( self):
        self.sftpd.close()

    def ssh_close( self):
        self.sftpd.close()


if __name__ == '__main__':
    # sshd = ssh_connect( '192.168.134.220', 'root', '1' )
    # sftpd = sftp_open( sshd )
    # try:
    #     sftp_put( sftpd, '/root/_ssh_sftp.py', '/root/new_ssh_sftp.py' )
    # except Exception, e:
    #     print 'ERROR: sftp_put - %s' % e
    # try:
    #     sftp_get( sftpd, '/root/new_ssh_sftp.py', '/root/new_new_ssh_sftp.py' )
    # except Exception, e:
    #     print 'ERROR: sftp_get - %s' % e
    # sftp_close( sftpd )
    # ssh_close( sshd )
    ssh = SSHHandler()
    ssh.sftp_open()
    ssh.sftp_get('/wwwdata/mcp/resource/tipoff/9792/809572611217690624_1','g:/1/1')
    from common import *
    print get_image_info('g:/1/1','B')