sub  x5, x6, x0
andi x3, x4, 2
or   x3, x4, x5
lh   x6, 0(x9)
sh   x7, 2310(x8)
beq x10, x11, 2310
