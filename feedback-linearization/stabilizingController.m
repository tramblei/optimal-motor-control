function u = stabilizingController(t,z,uStar,xStar,kFit)
%OPTIMALCONTROLLER Summary of this function goes here
%   Detailed explanation goes here

xRef = polyval(xFit,t);
yRef = polyval(yFit,t);
uRef = polyval(uFit,t);
Kx = polyval(kxFit,t);
Ky = polyval(kyFit,t);

u = uRef - Kx.*(x-xRef) - Ky.*(y-yRef);

end

