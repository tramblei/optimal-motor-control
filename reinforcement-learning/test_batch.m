function net = test_batch(net)

%net = fitnet([2,2]);
for i =  1:1000
    x1 = randi(10);
    if i == 1
        net = train(net, x1, x1^2);
    else
        net = adapt(net, x1, x1^2);
    end
end

end

