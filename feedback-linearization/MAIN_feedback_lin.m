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

n = size(A, 1);
m = size(B, 2);

% Optimal control parameters
r = 1 * eye(m);
qfs = [200000, 20000, 2000];

figure;
hold on;

directions = 8;
cols = {'black', 'red', 'blue'};

for i = 1:3
    col = cols{i};
    q = qfs(i) * eye(n);
    for d = 1:directions
        alpha = 2*pi*d/directions;
        initial = [pi/2; pi/2];
        distance = pi/4;
        target = initial + distance*[cos(alpha); sin(alpha)];
        theta_star = target;
        x_star = [theta_star; 0; 0]; % zero final velocity

        % Say we want to stabilize the system to x*
        % Find u* such that Ax* + Bu* = 0 (i.e. system is stationary at chosen setpoint)
        % Let x_tilda = x - x*, u_tilda = u - u*
        % We have that x_tilda' = Ax_tilda + Bu_tilda
        % Use lqr framework to find K
        % u_tilda = Kx_tilda
        % => u = K(x-x*) + u*

        % Special case since B'B = I
        u_star = -B' * A * x_star;
        K = -lqr(A,B,q,r);

        % v = K * (x - x_star) + u_star; % optimal feedback policy
        % v = K * x - K * x_star + u_star

        % Need to transform from v back to u using feedback linearization
        % u = M(theta)*v + C(theta, theta_dot) + B*theta_dot

        tic;
        sim sim_feedback_lin
        toc
        
        plot(sim_theta.Data(:,1), sim_theta.Data(:,2), col);
        plot(target(1),target(2),'o');
    end
end

xlabel('\theta_1');
ylabel('\theta_2');
title('Hand reaching task for various endpoints and LQR weights');

% figure;
% plot(sim_theta_dot.Time, sim_theta_dot.Data(:,1));
% hold on;
% plot(sim_theta_dot.Time, sim_theta_dot.Data(:,2));

