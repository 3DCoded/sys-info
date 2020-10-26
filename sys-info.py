import psutil
import socket
import platform
import ctypes
from datetime import datetime

def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

class OSInfo:
    def __init__(self):
        self._uname = platform.uname()
        self.name = self._uname.system
        self.node = self._uname.node
        self.release = self._uname.release
        self.version = self._uname.version
        self.machine = self._uname.machine
        self.processor = self._uname.processor

    def __str__(self):
        return f'<{self.name} {self.version}>'

    __repr__ = __str__

class BootInfo:
    def __new__(self):
        return datetime.fromtimestamp(psutil.boot_time())

class CPUInfo:
    def __init__(self):
        self.physical_cores = psutil.cpu_count(logical=False)
        self.total_cores = psutil.cpu_count(logical=True)
        self._freq = psutil.cpu_freq()
        self.maxfreq = self._freq.max
        self.minfreq = self._freq.min
        self.currentfreq = self._freq.current

        self.cores = {}
        for x, p in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
            self.cores[x] = p
        self.total_usage = psutil.cpu_percent()

    def __str__(self):
        return f'<CPU {self.physical_cores} physical, {self.total_cores} logical, {self.total_usage}%>'

    __repr__ = __str__

class MemoryInfo:
    def __init__(self):
        self._m = psutil.virtual_memory()
        self.total = self._m.total
        self.available = self._m.available
        self.used = self._m.used
        self.percent = self._m.percent

        self._s = psutil.swap_memory()
        self.s_total = self._s.total
        self.s_free = self._s.free
        self.s_used = self._s.used
        self.s_percent = self._s.percent

    def __str__(self):
        return f'<Memory total={get_size(self.total)} available={get_size(self.available)} used={get_size(self.used)} {self.percent}%>'

    __repr__ = __str__

class DiskPartition:
    def __init__(self, device, mountpoint, fstype):
        self.device = device
        self.mountpoint = mountpoint
        self.fstype = fstype
        self.memory = False

        try:
            self._u = psutil.disk_usage(self.mountpoint)
        except PermissionError:
            self.total = None
            self.used = None
            self.free = None
            self.percent = None
        else:
            self.total = self._u.total
            self.used = self._u.used
            self.free = self._u.free
            self.percent = self._u.percent
            self.memory = True

        buf = ctypes.create_unicode_buffer(1024)
        ctypes.windll.kernel32.GetVolumeInformationW(
            ctypes.c_wchar_p(self.mountpoint),
            buf,
            ctypes.sizeof(buf)
        )
        self.name = buf.value

    def __str__(self):
        return f'<DiskPartition "{self.name}" {self.mountpoint} ({self.fstype}) total={get_size(self.total)} used={get_size(self.used)} free={get_size(self.free)} percent={self.percent}%>'

    __repr__ = __str__

class DiskInfo:
    def __init__(self):
        self._p = psutil.disk_partitions()
        self.partitions = []
        for p in self._p:
            self.partitions.append(DiskPartition(p.device, p.mountpoint, p.fstype))

    def __str__(self):
        return f'<Disk {self.partitions}>'

    __repr__ = __str__

class NetworkAddress:
    def __init__(self, addr, mask, brod, type_):
        self.addr = addr
        self.mask = mask
        self.brod = brod
        self.type_ = type_

    def __str__(self):
        return f'<Address {self.addr} ({self.type_})>'

    __repr__ = __str__

class NetworkInterface:
    def __init__(self, name, addrs):
        self.name = name
        self.addrs = addrs

    def __str__(self):
        return f'<Interface {self.name}>'

    __repr__ = __str__

class NetworkInfo:
    def __init__(self):
        ia = psutil.net_if_addrs()
        self.interfaces = []
        for name, addrs in ia.items():
            a = []
            for addr in addrs:
                a.append(NetworkAddress(addr.address, addr.netmask, addr.broadcast, str(addr.family).split('.')[-1]))
            self.interfaces.append(NetworkInterface(name, a))

    def __str__(self):
        return f'<Network {self.interfaces}>'

    __repr__ = __str__

class BatteryInfo:
    def __init__(self):
        self._b = psutil.sensors_battery()
        self.percent = self._b.percent
        self.secsleft = self._b.secsleft
        self.is_plugged = self._b.power_plugged

    def __str__(self):
        return f'<Battery {self.percent}% secsleft={self.secsleft} is_plugged={self.is_plugged}>'

    __repr__ = __str__

class SysInfo:
    def __init__(self):
        self.os = OSInfo()
        self.boot = BootInfo()
        self.cpu = CPUInfo()
        self.memory = MemoryInfo()
        self.disk = DiskInfo()
        self.network = NetworkInfo()
        self.battery = BatteryInfo()

    def reload(self):
        self.os = OSInfo()
        self.boot = BootInfo()
        self.cpu = CPUInfo()
        self.memory = MemoryInfo()
        self.disk = DiskInfo()
        self.network = NetworkInfo()
        self.battery = BatteryInfo()

    def __str__(self):
         return f'<SysInfo os={self.os} boot={self.boot} cpu={self.cpu} memory={self.memory} disk={self.disk} network={self.network} battery={self.battery}>'

    __repr__ = __str__

s = SysInfo()
