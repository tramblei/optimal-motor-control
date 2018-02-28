function C = coriolis_mtx(theta, theta_dot)

params = get_params();

C = [-theta_dot(2) * (2 * theta_dot(1) + theta_dot(2));
     theta_dot(1)];
 
C = C * params.a2 * sin(theta(2));

end

