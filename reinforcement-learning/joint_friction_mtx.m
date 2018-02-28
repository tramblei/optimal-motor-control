function B = joint_friction_mtx()

params = get_params();

B = [params.b11 params.b12;
     params.b21 params.b22];

end

