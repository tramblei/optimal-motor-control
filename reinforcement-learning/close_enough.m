function yes = close_enough(x, target)
% returns yes = 1 if x close enough to target

ptol = 0.1;
vtol = 0.1;

if (norm(x(1:2)) < ptol) && (norm(x(3:4)) < vtol)
    yes = 1;
else
    yes = 0;
end

end
