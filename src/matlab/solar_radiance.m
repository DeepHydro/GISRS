% effective temperature of the sun
T = 5800;
 %Stefan¨CBoltzmann constant. https://en.wikipedia.org/wiki/Stefan%E2%80%93Boltzmann_constant
sbc= 5.67036713*10^-8;
%the diameter of the sun
rsun=6.96 *10^8; 
% emissivity of the sun
es = 0.99;
% distance between the sun and the earth
dis_se = 1.5* 10^11;

%Stefan¨CBoltzmann law
%the sun's total radiant exitance is:
Msun= es * sbc * T^4; 

% Wien's displacement law
% the wavelength of maximum emission is:
wavelength_max = 2897.8 / T * 1000; 

%the total radiant exitance by the total surface area of the sun:
power_sun = 4*pi * rsun^2* Msun;

%the irradiance at the earth (the solar constant):
esun = power_sun / (4*pi * dis_se^2);

%Treating the sun as a disk, the solid angle subtended by the sun as seen from the earth is
sa_sun = pi * rsun^2 / dis_se^2;

%The corresponding radiance observed by a detector with a field of view filled by the sun is then,
L_sun = esun / sa_sun;


