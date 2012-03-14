# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.upc.lottery_choices import lottery_choices
from scipy.optimize import fmin_l_bfgs_b
from opus_core.logger import logger
from copy import copy
import numexpr as ne

class equilibration_choices(lottery_choices):
    def run(self, 
            probability=None, 
            utilities=None, 
            capacity=None,
            resources=None):
        """
        """

        #resources.check_obligatory_keys(["capacity"])
        self.capacity = resources.get("capacity", capacity)
        ##price of shape (1, nalts)
        self.price = resources.get("price")
        ##price_beta of shape (nagents, 1)
        self.price_beta = resources.get("price_beta")  
        self.U_cached = utilities - np.dot(self.price_beta, self.price.T)
        price0 = copy(self.price)
        results =fmin_l_bfgs_b(self.target_func, price0, fprime=self.fprime, 
                               args=(supply, beta), bounds=bounds0, factr=1e12, 
                               iprint=10)
        price_converged = results[0]
        demand, prob = self.update_demand(price_converged)
        lottery_choices.run(self, probability=prob,
                           resources=resources)
                          )
        
    def update_price(self, price):
        self.price = price

    def update_demand(price):
        self.update_price(price)
        addition = np.dot(self.price_beta, self.price.T)
        U_cached = self.U_cached
        out = ne.evaluate("exp(U_cached + addition)")
        sumV = ne.evaluate("sum(out, axis=1)")[:, np.newaxis]
        ne.evaluate("out / sumV", out=out)
        demand = ne.evaluate("sum(out, axis=0)")
        return demand, out

    def target_func(self, price, supply, beta=None):
        demand, _ = update_demand(price)
        surplus = ne.evaluate("sum((demand - supply)**2)")
        #print surplus
        return surplus

    def fprime(self, price, supply, beta):
        demand, prob = update_demand(price)
        cross = cross_deriv(prob, beta)
        grad = np.sum(2 * (demand - supply) * cross, axis=1)
        return grad

    def own_deriv(self, prob, beta, _prob_beta=None):
        if _prob_beta is None:
            out = ne.evaluate("prob * (1 - prob) * beta")
            #out = prob * (1 - prob) * beta
        else:
            out = ne.evaluate("_prob_beta * (prob - 1)")
            #out = _prob_beta * (prob - 1)
        out = ne.evaluate("sum(out, axis=0)")
        return out

    def cross_deriv(self, prob, beta):
        _prob_beta = ne.evaluate("- prob * beta")
        out = np.dot( prob.T, _prob_beta )
        own = own_deriv(prob, beta, _prob_beta)
        np.fill_diagonal(out, own)
        return out

