# This class only acts as data structure to capture all stock details for each stock


class Stock:

    def __init__(self):
        self.ticker = ''                         # Ticker name
        self.name = ''                           # Full name of the Stock
        self.market_cap = ''                     # Market capital
        self.forward_pe = 0.0                    # Forward PE
        self.trailing_pe = 0.0                   # Trailing PE
        self.avg_eps_curr_yr = 0.0               # Average EPS for current year
        self.avg_eps_next_yr = 0.0               # Average EPS for next year
        self.avg_eps_prev_yr = 0.0               # Average EPS for previous year
        self.rev_est_curr_yr = 0                 # Revenue estimates for current year
        self.rev_est_next_yr = 0                 # Revenue estimates for next year
        self.rev_est_prev_yr = 0                 # Revenue estimates for previous year
        self.sls_grwth_curr_yr = 0.0             # Sales growth current year
        self.sls_grwth_next_yr = 0.0             # Sales growth next year

    # Calculates EPS change in current year vs previous year
    def avg_eps_chng_curr_yr(self):
        chng = (self.avg_eps_curr_yr - self.avg_eps_prev_yr) * 100 / self.avg_eps_prev_yr
        chng_rnd = round(chng, 2)
        return str(chng_rnd) + '%'

    # Calculates EPS change in next year vs current year
    def avg_eps_chng_next_yr(self):
        chng = (self.avg_eps_next_yr - self.avg_eps_curr_yr) * 100 / self.avg_eps_next_yr
        chng_rnd = round(chng, 2)
        return str(chng_rnd) + '%'



