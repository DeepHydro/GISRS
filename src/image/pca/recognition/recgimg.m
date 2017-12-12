function [recognized_img]=recgimg(datapath,testimg)
%  datapath: directory of the data images used for training
%  testimg: filename of the image that is to be recgonized
% 
% We reshape all 2D images of the training database
% into 1D column vectors. Then, it puts these 1D column vectors in a row to 
% construct 2D matrix 'X'.
%  
% X- A 2D matrix, containing all 1D image vectors.
%      Suppose all P images in the training database 
%      have the same size of MxN. So the length of 1D 
%      column vectors is MxN and 'X' will be a (MxN)xP 2D matrix.

%%%%%%%%%  finding number of training images in the data path specified as argument  %%%%%%%%%%

D = dir(datapath);  % D is a Lx1 structure with 4 fields as: name,date,byte,isdir of all L files present in the directory 'datapath'
M = 0;
for i=1 : size(D,1)
    if not(strcmp(D(i).name,'.')|strcmp(D(i).name,'..')|strcmp(D(i).name,'Thumbs.db'))
        M = M + 1; % Number of all images in the training database
    end
end

%%%%%%%%% creating the image matrix X  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
for n=1:M
    im = imread(strcat(datapath,'\',num2str(n),'.jpg')); %read image
    im = im2double(rgb2gray(im)); % convert image to gray scale and then to double precision
    [r,c] = size(im); % get number of rows and columns in image
    I(:,n) = im(:); % convert image to vector and store as column in matrix I
end

% calculate mean image
I_mean = mean(I,2);
% subtract mean image from the set of images
I_shifted = I-repmat(I_mean,1,M);

%perform PCA. Matrix I was used as input instead of I_shifted because 
%Matlab documentation states that pca function centers the data
[coeff,score,latent] = pca(I);

%%%% again we use Kaiser's rule here to find how many Principal Components (eigenvectors) to be taken
%%%% if corresponding eigenvalue is greater than 0, then the eigenvector will be chosen for creating eigenface

eig_vec = [];
for i = 1 : size(coeff,2) 
    if( latent(i) > 0 )
        eig_vec = [eig_vec coeff(:,i)];
    end
end

%calculate eigenfaces
eigFaces = I_shifted*eig_vec;

% put eigenface in array and display
ef = [];
for n = 1:size(eig_vec,2)
    temp = reshape(eigFaces(:,n),r,c);
    temp = histeq(temp,255);
    ef = [ef temp];
end
figure;
imshow(ef,'Initialmagnification','fit');
title('Eigenfaces');


projectimg = [ ];  % projected image vector matrix
for i = 1 : size(eigFaces,2)
    temp = eigFaces' * I_shifted(:,i);
    projectimg = [projectimg temp];
end

% load one of the training images to test reconstruction
im = im2double(rgb2gray(imread(testimg))); % convert to gray and then to double
I_test = im(:); % convert image to vector
I_test = I_test-I_mean; % subtract mean images

projtestimg = eigFaces'*I_test; % projection of test image onto the facespace

%%%%% calculating & comparing the euclidian distance of all projected trained images from the projected test image %%%%%

euclide_dist = [ ];
for i=1 : size(eigFaces,2)
    temp = (norm(projtestimg-projectimg(:,i)))^2;
    euclide_dist = [euclide_dist temp];
end
[euclide_dist_min recognized_index] = min(euclide_dist);
recognized_img = strcat(int2str(recognized_index),'.jpg');

end