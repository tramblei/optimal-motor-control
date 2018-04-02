function xdot = arm_dynamics(x, u)
% xdot = f(x,u)

M = inertia_mtx(x(1:2));
C = coriolis_mtx(x(1:2), x(3:4));
invM = inv(M);
J = joint_friction_mtx(); % typically represted using matrix B but B already defined

xdot = zeros(4,1);
xdot(3:4) = invM*(u-J*x(3:4)-C);
xdot(1:2) = x(3:4);

end

