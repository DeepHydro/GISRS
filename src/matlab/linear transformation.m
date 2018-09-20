 k=1;
 np = 7;
 np2= np*np;
 x=zeros(2,np2);
for i=1:np
    for j=1:np
        x(1,k)=j-1;
        x(2,k)=i-1;
        k=k+1;
    end
end
for i=1:np2
plot(x(1,i),x(2,i),'o-r')
hold on
end
A=[2,0;0,2];
B = [1,-2;3,1];
C  = [2,1;
      1,2];
y = C*x;
hold on
for i=1:np2
plot(y(1,i),y(2,i),'*-b')
hold on
end

hold on
line([0 0],[18 18])