clear all;

initial = [pi/2; pi/2];     % initial joint configuration
distance = pi/4;            % target distance in radians
directions = 8;             % number of directions
dt = 0.01;                  % time step
n = 50;                     % number of time steps

% form initial state and control
x0 = [initial; zeros(2,1)];
u0 = [0; 0];

