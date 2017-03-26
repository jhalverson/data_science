# Jonathan Halverson
# Thursday, March 23, 2017
# Evaulation of the CDF of the multinomial distribution

p_draw = 20 / 3581.0
p_draw = 8 / 1379.0
p_win = 0.5 - 0.5 * p_draw
p_lose = 0.5 - 0.5 * p_draw
pbs = c(p_win, p_lose, p_draw)
sum(pbs)
total = 2487
total = 3264
total = 1379

ct = 0
cdf = 0.0
thres = dmultinom(x=c(1249, 1226, 12), prob=pbs)
thres = dmultinom(x=c(1699, 1545, 20), prob=pbs)
thres = dmultinom(x=c(598, 773, 8), prob=pbs)
#thres = 10
for (i in seq(0, total)) {
  for (k in seq(0, total)) {
    if (i + k <= total) {
      ct = ct + 1
      y = c(i, total - i - k, k)
      prb = dmultinom(x=y, size=total, prob=pbs)
      if (prb <= thres) {
        cdf = cdf + prb
        #print(y)
      }
      else {print(y)}
    }
  }
}
cdf
ct