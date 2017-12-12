close all;
im=imread('lena.jpg');
I = double(imread('lena.jpg'));
X = reshape(I,size(I,1)*size(I,2),3);
[coeff,score, latent]=princomp(X);
Itransformed = X*coeff;
i1 = coeff*X';
contribution = cumsum(latent)./sum(latent);

im1=  reshape(im(:,:,1),size(I,1)*size(I,2),1);
im2=  reshape(im(:,:,2),size(I,1)*size(I,2),1);
Ipc1 = reshape(Itransformed(:,1),size(I,1),size(I,2));
Ipc2 = reshape(Itransformed(:,2),size(I,1),size(I,2));
Ipc3 = reshape(Itransformed(:,3),size(I,1),size(I,2));
figure, imshow(im);
figure, imshow(Ipc1,[]);
figure, imshow(Ipc2,[]);
figure, imshow(Ipc3,[]);

pt_Ipc1 = reshape(Itransformed(:,1),size(I,1)*size(I,2),1);
pt_Ipc2 = reshape(Itransformed(:,2),size(I,1)*size(I,2),1);

% figure, scatter(im1,im2,'o','r');
% hold on
% scatter(pt_Ipc1,pt_Ipc2,'*','b');

