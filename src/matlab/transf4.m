function  x= transf4(s,t)
npt= size(s,1);
A = zeros(npt*2,4);
B = zeros(npt*2,1);

for i=1:npt
    A(2*i - 1, :) =  [s(i,1)  s(i,2)  1 0; ];
    A(2*i, :)      =  [s(i,2)  -s(i,2) 0 1; ];
    B(2*i - 1)    =  t(i,1);
    B(2*i)         =  t(i,2);
end

 x= linsolve(A,B);
       
end