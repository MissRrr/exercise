import os
import sys
import paramiko
import subprocess
import time
from paramiko import SSHClient

# ssh-copy-id 下发本机密钥到列表节点上
# ssh.exec_command(f'sshpass -p {info[j][3]} ssh-copy-id "{info[j][2]}@{info[j][0]}"')
# scp 下发文件
# os.system(f"sshpass -p {info[i][3]} scp {path} {info[i][2]}@{info[i][0]}:/root/.ssh/authorized_keys")
path = sys.path[0] + '/tmp_authorized_keys'
remotepath = '/root/.ssh/authorized_keys'


def ssh_connection(node_info) -> SSHClient:
    ssh = paramiko.SSHClient()
    key = paramiko.AutoAddPolicy()
    ssh.set_missing_host_key_policy(key)
    # print(f'connnecting {info[i][2]}@{info[i][0]}...')
    try:
        # 注意 root 用户的 ssh 权限 /etc/ssh/sshd_config PermitRootLogin yes
        ssh.connect(node_info[0], node_info[1], node_info[2], node_info[3], timeout=100)
    except Exception:
        print(f'ssh {node_info[2]}@{node_info[0]} connection failed')
        sys.exit()
    return ssh


def init_node_rsa(ssh) -> (str, SSHClient):
    # 已存在会提示是否覆盖，需要提前判断文件是否存在
    # 初始化节点ssh服务的（输入参数SSHClient连接对象，输出参数SSHClient连接对象）
    rsa_is_exist = bool(ssh.exec_command('[ -f /root/.ssh/id_rsa.pub ] && echo True')[1].read().decode())
    # 执行生成密钥操作
    if not rsa_is_exist:
        ssh.exec_command('ssh-keygen -f /root/.ssh/id_rsa -N ""')
    # 要有停顿时间，不然public_key还未写入
    time.sleep(2)
    # # 注意 /.ssh/config 文件
    config_is_exist = bool(ssh.exec_command('[ -f /root/.ssh/config ] && echo True')[1].read().decode())
    if not config_is_exist:
        ssh.exec_command("echo -e 'StrictHostKeyChecking no\\nUserKnownHostsFile /dev/null' >> ~/.ssh/config ")
    _, stdout, _ = ssh.exec_command('cat /root/.ssh/id_rsa.pub')
    public_key = stdout.read().decode()
    return public_key, ssh


def init_cluster(infos):
    # 前面一个for循环控制集群节点，生成密钥
    ssh_ = []
    for info in infos:
        ssh = ssh_connection(info)
        public_key, ssh = init_node_rsa(ssh)
        # 这里可以保存临时文件在（管理节点/集群节点）执行节点上
        with open(path, 'a') as fp:
            fp.write(public_key)
        time.sleep(1)
        # 将连接对象存放
        ssh_.append(ssh)
    # 下发文件
    for s in ssh_:
        s.open_sftp().put(path, remotepath)
        s.close()


def add_new_node(new_infos, ip_list):
    ssh_ = []
    for new_info in new_infos:
        ssh = ssh_connection(new_info)
        public_key, ssh = init_node_rsa(ssh)
        with open(path, 'a') as fp:
            fp.write(public_key)
        time.sleep(1)
        # 新增节点公钥写入已经初始化好的集群中(或者收集新增的公钥信息再写入[需要处理格式]）
        for ip in ip_list:
            tmp = subprocess.run(f'ssh root@{ip} "echo -e \'{public_key}\n\' >> {remotepath}"', shell=True)
            # print(tmp.returncode)
        ssh_.append(ssh)
    # 给新的节点赋 authorized_keys 文件，覆盖式
    for s in ssh_:
        s.open_sftp().put(path, remotepath)
        s.close()


def remove_node(ip_list):
    for ip in ip_list:
        # p = subprocess.Popen(f'ssh root@{ip} "cat /root/.ssh/id_rsa.pub"', stderr=subprocess.PIPE,
        #                      stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
        p = subprocess.run(f'ssh "root@{ip}" "ls"', shell=True)
        # out, err = p.communicate()

        public_key = p.stdout
        print(p.stderr)
        # print(out.decode())
        # os.system(f'cat {path}')
        # os.system(f'cat /root/.ssh/id_rsa.pub')
        print(public_key)
        # p = os.system(f'ssh root@{ip} "cat /root/.ssh/id_rsa.pub"')
        # print(type(p))
        # print('p：',p)
        for l in open(path, 'rb').readlines():
            print(l)
            # print(l.find(public_key))
        #     print(l.find('AAA'.encode()))


if __name__ == '__main__':
    node_infos = [['10.203.1.195', 22, 'root', 'password'], ['10.203.1.87', 22, 'root', 'password']]
    node_ip_list = ['10.203.1.195', '10.203.1.87']
    new_node_list = [['10.203.1.86', 22, 'root', 'password']]
    # os.getcwd()是指代码在哪一个目录运行的路径 譬如你在 /root 下执行 python3 XXX 它就是 /root
    # path = os.getcwd() + '/tmp_authorized_keys'
    remove_node(['10.203.1.87'])
    # init_cluster(node_infos)
    # add_new_node(new_node_list, node_ip_list)
