from intelhex import IntelHex
from pyOCD.board import MbedBoard


reg_list = ['pc', 'msp', 'psp', 'control', 'primask', 'xpsr'
,'r0','r1','r2','r3','r4','r5','r6','r7','r8','r9','r10','r11','r12','sp','lr'
]

with MbedBoard.chooseBoard(frequency=10000000) as board:
    memory_map = board.target.getMemoryMap()
    ram_regions = [region for region in memory_map if region.type == 'ram']
    ram_region = ram_regions[0]
    rom_region = memory_map.getBootMemory()
    target_type = board.getTargetType()

    addr = rom_region.start
    size = rom_region.length
    data = board.target.readBlockMemoryUnaligned8(addr, size)
    data = bytearray(data)
    with open("rom.bin", 'wb') as f:
        f.write(data)
    ih = IntelHex()
    ih.puts(addr, data)
    ih.tofile("rom.hex", format='hex')
        
    addr = ram_region.start
    size = ram_region.length
    data = board.target.readBlockMemoryUnaligned8(addr, size)
    data = bytearray(data)
    with open("ram.bin", 'wb') as f:
        f.write(data)
    ih = IntelHex()
    ih.puts(addr, data)
    ih.tofile("ram.hex", format='hex')

    with open("uvision.ini", 'w') as f:
        f.write('load ram.hex\n')
        for reg in reg_list:
            reg_val = board.target.readCoreRegister(reg)
            f.write('%s=0x%x\n' % (reg, reg_val))
