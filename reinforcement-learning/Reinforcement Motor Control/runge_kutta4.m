function x2 = runge_kutta4(f, x1, u, dt)
% Calculates ODE using Runge-Kutta 4th order method

k1 = f(x1, u);
k2 = f(x1 + dt / 2 * k1, u);
k3 = f(x1 + dt / 2 * k2, u);
k4 = f(x1 + dt * k3, u);

x2 = x1 + dt/6*(k1 + 2*k2 + 2*k3 + k4);

end

