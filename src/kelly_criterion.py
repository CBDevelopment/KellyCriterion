import numpy as np
import matplotlib.pyplot as plt

# https://towardsdatascience.com/python-risk-management-kelly-criterion-526e8fb6d6fd

# Seed for repeatable results
# np.random.seed(2)

def simulate(num_trials, num_experiments, win_prob, payout, starting_money):
    kelly_percent = ((payout * win_prob) - (1 - win_prob)) / payout
    # kelly_percent = win_prob - ((1 - win_prob) / payout)
    experiments = []
    for e in range(num_experiments):
        trials = []
        starting_money = starting_money
        trials.append(starting_money)
        for t in range(1, num_trials):
            # Binomial distribution (number of trials, probability of success, number of experiments)
            # Returns the number of successes
            outcome = np.random.binomial(1, win_prob) # 1 = heads, 0 = tails
            if outcome == 1:
                trials.append(trials[t - 1] * (1 + kelly_percent))
            else:
                trials.append(trials[t - 1] * (1 - kelly_percent))
        experiments.append(trials)
    return experiments, kelly_percent

def plot_simulation(experiments, starting_money, win_rate, payout):
    counter = 0
    # Plot line chart
    for i in range(len(experiments)):
        plt.plot(experiments[i])
        if experiments[i][-1] > starting_money:
            counter += 1
    print(f"Number of experiments with a positive return: {counter}")
    plt.xlabel("Flip Number")
    plt.ylabel("Account Value ($)")
    plt.title(f"Kelly Criterion Simulation for {win_rate * 100}% Win Rate, {payout}-1 Payout, 100 Flips, 50 Trials")
    plt.savefig(f"kelly_criterion_sim_{win_rate * 100}_{payout}.png")
    plt.close()

    # Plot average line chart
    plt.plot(np.mean(experiments, axis=0), linewidth=2, color='black')
    plt.xlabel("Flip Number")
    plt.ylabel("Account Value ($)")
    plt.title(f"Average Payouts for {win_rate * 100}% Win Rate, {payout}-1 Payout, 100 Flips, 50 Trials")
    plt.savefig(f"kelly_criterion_avg_{win_rate * 100}_{payout}.png")
    plt.close()

    # plot a histogram of experiements
    ending_values = [x[-1] for x in experiments]
    plt.hist(ending_values, bins=20)
    plt.xlabel("Account Value ($)")
    plt.ylabel("Frequency")
    plt.title(f"Ending Account Values for {win_rate * 100}% Win Rate, {payout}-1 Payout, 100 Flips, 50 Trials")
    plt.savefig(f"kelly_criterion_hist_{win_rate * 100}_{payout}.png")
    plt.close()


# Kelly Criterion
# Win probability
# W
# Payout
# B
# How much of your capital you should bet to maximize profit
# kelly_percent = (BW - (1-W)) / B

TRIALS = 100
EXPERIMENTS = 50
BANKROLL = 1000
W = .7
B = 2

experiments, kelley_percent = simulate(TRIALS, EXPERIMENTS, W, B, BANKROLL)
print(f"Kelly Percent: {round(kelley_percent, 4)}")

plot_simulation(experiments, BANKROLL, W, B)