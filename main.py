from ipaddress import ip_address
import pycurl
from io import BytesIO
import cryptocode

urls = ['https://ident.me', # ipv6 and ipv4
        'https://api.ipify.org'] # ipv4 only
length=45
# https://stackoverflow.com/questions/166132/maximum-length-of-the-textual-representation-of-an-ipv6-address

def getip(interface=None):
    for url in urls:
        addr = []
        for ipv in (pycurl.IPRESOLVE_V4,pycurl.IPRESOLVE_V6):
            buffer = BytesIO() # must clear like this
            C = pycurl.Curl()
            if interface:
                C.setopt(pycurl.INTERFACE,interface)
            C.setopt(C.URL, url)
            C.setopt(pycurl.IPRESOLVE, ipv)
            C.setopt(C.WRITEDATA, buffer)
            try:
                C.perform()
                result = buffer.getvalue()
                try: #validate response
                    addr.append(ip_address(result.decode('utf8')))
                except ValueError:
                    pass
            except pycurl.error:
                pass
            finally:
                C.close()

        if len(addr)>1: #IPv4 and IPv6 found
            break

    return addr

if __name__ == '__main__':
    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('-i','--iface',help='network interface to use')
    p = p.parse_args()

    addr = getip(p.iface)

toencrypt = cryptocode.encrypt(str(addr), 'mmlqc')
print(str(toencrypt))