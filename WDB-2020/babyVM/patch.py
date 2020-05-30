import os
import idaapi
from ida_bytes import get_bytes, patch_bytes

# ('jnz', 'jl', 'jmp', 'jz')
start_addr = 0x14007CA30
end_addr = 0x1400804A0
buf = get_bytes(start_addr, end_addr - start_addr)

pattern = '\xE8\x16\x5B\xFF\xFF' # call get_thread_id, call 0000000140075A41
p = buf.find(pattern)
while p != -1:
	tmp_addr = start_addr + p
	PatchDword(tmp_addr, 0x90909090)
	PatchByte(tmp_addr+4, 0x90)
	print("patched {}.".format(hex(tmp_addr)))

	p = buf.find(pattern, p+4)


print("patch get_thread_id finished.")


start_addr = 0x14007FEF0
end_addr = 0x1400801F8

buf = get_bytes(start_addr, end_addr - start_addr)
pattern = '\xE8\xEE\x58\xFF\xFF' # call time_debug, call 000000014007584D
p = buf.find(pattern)
while p != -1:
	tmp_addr = start_addr + p
	PatchDword(tmp_addr, 0x90909090)
	PatchByte(tmp_addr+4, 0x90)
	print("patched {}.".format(hex(tmp_addr)))

	p = buf.find(pattern, p+4)


print("patch time_debug finished.")	

