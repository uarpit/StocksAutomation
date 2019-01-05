
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class Stock:

    def __init__(self):
        self.ticker = ''
        self.name = ''
        self.market_cap = ''
        self.forward_pe = 0.0
        self.trailing_pe = 0.0
        self.avg_eps_curr_yr = 0.0
        self.avg_eps_next_yr = 0.0
        self.avg_eps_prev_yr = 0.0
        self.rev_est_curr_yr = 0
        self.rev_est_next_yr = 0
        self.rev_est_prev_yr = 0
        self.sls_grwth_curr_yr = 0.0
        self.sls_grwth_next_yr = 0.0

    def avg_eps_chng_curr_yr(self):
        chng = (self.avg_eps_curr_yr - self.avg_eps_prev_yr) * 100 / self.avg_eps_prev_yr
        chng_rnd = round(chng, 2)
        return str(chng_rnd) + '%'

    def avg_eps_chng_next_yr(self):
        chng = (self.avg_eps_next_yr - self.avg_eps_curr_yr) * 100 / self.avg_eps_next_yr
        chng_rnd = round(chng, 2)
        return str(chng_rnd) + '%'



