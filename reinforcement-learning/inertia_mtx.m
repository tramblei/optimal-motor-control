function M = inertia_mtx(theta)

params = get_params();

M = [params.a1 + 2 * params.a2 * cos(theta(2)), params.a3 + params.a2 * cos(theta(2))
     params.a3 + params.a2 * cos(theta(2)), params.a3];

end

