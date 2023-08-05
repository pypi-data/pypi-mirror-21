% objects
network([c1,c2,c3,c4,c5,c6]).
computer(c1).
computer(c2).
computer(c3).
computer(c4).
computer(c5).
computer(c6).

% topology
connected(c1,[c2,c3,c4,c5,c6]).
connected(c2,[c1]).
connected(c3,[c1]).
connected(c4,[c1]).
connected(c5,[c1]).
connected(c6,[c1]).