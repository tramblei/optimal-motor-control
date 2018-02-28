function xdot = arm_dynamics(x, u)
% x(1) = theta1
% x(2) = theta2
% x(3) = theta1'
% x(4) = theta2'

xdot = zeros(4,1);

xdot(1) = x(3);
xdot(2) = x(4);

% Recall that M(q)q'' + C(q,q')q' + B(q)q' = u for this arm model
% (No gravity potential term because 2d planar)
% => q'' = inv(M) * [u - B(q)q' - C(q,q')q']
M = inertia_mtx(x(1:2));
C = coriolis_mtx(x(1:2), x(3:4));
B = joint_friction_mtx();
xdot(3:4) = inv(M) * (u - B * x(3:4) - C);

end