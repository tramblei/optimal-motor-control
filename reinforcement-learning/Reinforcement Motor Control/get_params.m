function params = get_params()

% Arm model parameters
m1   = 1.4;    % segment mass
m2   = 1.1;
l1   = 0.3;    % segment length
l2   = 0.33;
s1   = 0.11;   % segment center of mass
s2   = 0.16;
I1   = 0.025;  % segment moment of inertia
I2   = 0.045;
b11  = 0.5;    % joint friction
b22  = 0.5;  
b12  = 0.1; 
b21  = 0.1;

params.m1   = m1;    % segment mass
params.m2   = m2;
params.l1   = l1;    % segment length
params.l2   = l2;
params.s1   = s1;   % segment center of mass
params.s2   = s2;
params.I1   = I1;  % segment moment of inertia
params.I2   = I2;
params.b11  = b11;    % joint friction
params.b22  = b22;  
params.b12  = b12; 
params.b21  = b21;

% For convenience
params.a1 = I1 + I2 + m2 * l1^2;
params.a2 = m2 * l1 * s2;
params.a3 = I2;

end

