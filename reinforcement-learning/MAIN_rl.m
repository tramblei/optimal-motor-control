clear all;

gamma = 0.9;
rand_eps = 0.6;
epsilon = rand_eps;
eps_decay = 0.99;

distance = pi/4;
alpha = pi/4;
initial = [pi/2; pi/2];
target_theta = initial + distance*[cos(alpha); sin(alpha)];
target = [target_theta; 0; 0];

maxepi = 1000; % number of episodes before we stop
maxit = 200; % 1500 iterations per episode
t = 0.5; % get to target in 0.5 seconds
dt = t / maxit;

xpen = 100;
upen = 1;
reward = @(x, u) -(xpen * norm(x(1:2) - target(1:2))^2 + upen * norm(u)^2); % play around with this
num_actions = 5; % higher means that actions are more granular (but slows performance)
actions = linspace(-30, 30, 6); % discrete set of actions to choose from

n = 4;
m = 2;
x = zeros(n, maxit);
x(:, 1) = [pi/2 pi/2 0 0]; % x0
y = zeros(num_actions, maxit);

Q = fitnet([5,5]);
batch_size = 10;
%Q = configure(Q);
Q.trainParam.epochs = 1;
Q.trainFcn = 'trainbr';
Q.trainParam.showWindow = false;

figure;
hold on;

%%% learn Q
learn_size = 10000;
exp_state = zeros(n,learn_size);
exp_rewards = zeros(num_actions,learn_size);
for i = 1:learn_size
    action_idx = randi(num_actions);
    u = actions(action_idx);
   	new_x = runge_kutta4(@arm_dynamics, x(:, i), u, dt);
	exp_state(:, i + 1) = new_x;
    if close_enough(new_x) % within tolerance of target
        bonus = 1000;
    else
        bonus = 0;
    end
    
    
for ep = 1:maxepi
    for i = 1:maxit - 1
        if i > batch_size
            qval = Q(x(:, i));
        else
            qval = zeros(num_actions, 1);
        end
        
        if rand() < epsilon || i <= batch_size % exploration
            action_idx = randi(num_actions);
        else
            [~, action_idx] = max(qval);
        end
        u = actions(action_idx);
        
        new_x = runge_kutta4(@arm_dynamics, x(:, i), u, dt);
        x(:, i + 1) = new_x;
        
        %%% Update Q neural net
        %fprintf('Sum qval: %d\n', sum(qval));
        y(:, i) = qval;
        if close_enough(new_x) % within tolerance of target
            success = true;
            bonus = 100000;
        else
            success = false;
            bonus = 0;
        end
        if i > batch_size
            [maxQ, new_action_idx] = max(Q(new_x));
        else
            [maxQ, new_action_idx] = max(qval);
        end
        %fprintf('Max Q: %d\n', maxQ);
        y(new_action_idx, i) = reward(new_x, u) + gamma * maxQ + bonus;
        if mod(i, batch_size) == 0
            if i <= batch_size && ep == 1
                %Q = train(Q, x(:, i-batch_size+1:i), y(:, i-batch_size+1:i), [], []);
                Q = train(Q, x(:, i-batch_size+1:i), y(:, i-batch_size+1:i));
            else
                Q = adapt(Q, x(:, i-batch_size+1:i), y(:, i-batch_size+1:i));
            end
        end

        if success
            fprintf('Success!\n');
            break;
        end
        
        if epsilon > 0.1
            epsilon = epsilon * eps_decay;
        end
    end
    
    %%% plot theta1 vs theta2
    plot(x(1, end), x(2, end), '.');
    fprintf('Episode: %d\n', ep);
    
    % reset x
    x = zeros(n, maxit);
    y = zeros(num_actions, maxit);
    x(:, 1) = [pi/2 pi/2 0 0]; % x0
    epsilon = rand_eps;
    
end
plot(target(1), target(2), 'o');
