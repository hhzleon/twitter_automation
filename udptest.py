import socket

def is_udp_port_open(ip, port, timeout=1):
    """
    测试UDP端口是否开放。

    :param ip: 目标IP地址
    :param port: 要测试的UDP端口
    :param timeout: 超时时间，单位是秒
    :return: 如果端口开放返回True，否则返回False
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(timeout)

    try:
        # 尝试通过UDP发送一个数据包
        sock.sendto(b'', (ip, port))
        # 等待接收应答
        sock.recvfrom(1024)
        return True
    except socket.error:
        return False
    finally:
        sock.close()

if __name__ == "__main__":
    ip_address = "123.56.14.156"  # 替换为目标IP地址
    port_number = 30002       # 替换为要测试的端口号
    if is_udp_port_open(ip_address, port_number):
        print(f"UDP端口 {port_number} 在 {ip_address} 上是开放的。")
    else:
        print(f"UDP端口 {port_number} 在 {ip_address} 上不是开放的。")
