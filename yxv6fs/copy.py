import sys

if(len(sys.argv) != 3):
    print("Usage: python copy.py src dst\n");
    exit()
source = open(sys.argv[1])
destination = open(sys.argv[2])

lines = destination.readlines()
start = -1
end = 0
for idx, line in enumerate(lines):
    if(line.startswith("class WALDisk:")):
        start = idx
    if("crash" in line):
        end = idx
        break

head = lines[:start]
tail = lines[end:]

lines = source.readlines()
start = -1
end = 0
for idx, line in enumerate(lines):
    if(line.startswith("class WALDisk:")):
        start = idx
    if(start != -1 and len(line) > 0 and line[0] != " " and line[0] != "\t"):
        end = idx

result = head + lines[start:end] + tail

destination = open(sys.argv[2], "w")
for line in head:
    destination.write(line)

for line in lines[start:end]:
    destination.write(line)

for line in tail:
    destination.write(line)
destination.close()
