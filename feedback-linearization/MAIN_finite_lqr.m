% A under feedback linearization transformation
A = [0 0 1 0;
     0 0 0 1;
     0 0 0 0;
     0 0 0 0];

% B under feedback linearization transformation
B = [0 0;
     0 0;
     1 0;
     0 1];

J = joint_friction_mtx(); % typically represted using matrix B but B already defined

n = size(A, 1);
m = size(B, 2);

tSpan = [0 0.5];
nSoln = 400; % number of timesteps to use
dt = (tSpan(2) - tSpan(1)) / nSoln;
tol = 1e-6;

% LQR weighting
Fs = [200000, 20000, 2000];
Q = 1 * eye(n);
R = eye(m);

directions = 8;
cols = {'black', 'red', 'blue'};
figure;
hold on;
for k = 1:3
    F = eye(n) * Fs(k);
    col = cols{mod(k,3) + 1};
    
    Soln = finite_lqr(tSpan,A,B,Q,R,F,nSoln,tol);
    KK = {Soln.K};
    t = [Soln.t];
    
    for d = 1:directions
        alpha = 2*pi*d/directions;
        initial = [pi/2; pi/2];
        distance = pi/4;
        target = initial + distance*[cos(alpha); sin(alpha)];

        theta_star = target;
        x_star = [theta_star; 0; 0]; % zero final velocity

        x = zeros(n, nSoln);
        x0 = [initial; 0; 0];
        x(:,1) = x0;
        
        % Say we want to stabilize the system to x*
        % Find u* such that Ax* + Bu* = 0 (i.e. system is stationary at chosen setpoint)
        % Let x_tilda = x - x*, u_tilda = u - u*
        % We have that x_tilda' = Ax_tilda + Bu_tilda
        % Use lqr framework to find K
        % u_tilda = Kx_tilda
        % => u = K(x-x*) + u*

        % Special case since B'B = I
        u_star = -B' * A * x_star;

        u = zeros(2,nSoln);
        vs = []
        for i = 1:nSoln - 1
            v = -KK{i} * (x(:,i) - x_star) + u_star;
            vs = [vs,v];
            M = inertia_mtx(x(1:2, i));
            C = coriolis_mtx(x(1:2,i), x(3:4, i));
            invM = inv(M);
            x(3:4, i + 1) = x(3:4, i) + dt * (-invM*(C + J*x(3:4,i)) + v + invM*C + invM*J*x(3:4,i)) .*normrnd([1;1],[2;2]);
            x(1:2, i + 1) = x(1:2, i) + dt * x(3:4, i + 1);
        end

        plot(x(1,:), x(2,:), col);
        plot(target(1),target(2),'o');
    end
end

xlabel('\theta_1');
ylabel('\theta_2');
title('Hand reaching task for various endpoints and LQR weights (finite, no noise)');
