# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.upc.lottery_choices import lottery_choices
from scipy.optimize import fmin_l_bfgs_b
from opus_core.logger import logger
from opus_core import ndimage
from copy import copy
import numpy as np
try:
    import numexpr as ne
except:
    ne = None

class equilibration_choices(lottery_choices):

    def run(self, 
            probability=None, 
            utilities=None, 
            capacity=None,
            resources=None):
        """
        yet to support sampling of alternatives
        """

        resources.check_obligatory_keys(['price_coef_name'])
        ## assume all agents have the same index, ie no sampling of alts
        assert np.allclose(resources['index'][0, ], resources['index'][1, ])
        self.index = resources['index'][0, ] 
        if utilities is None:
            utilities = resources.get("utilities")
        self.capacity = capacity
        if self.capacity is None:
            self.capacity = resources.get("capacity", None)
        assert self.capacity is not None
        self.capacity = self.capacity[self.index]
        nagents, nalts = utilities.shape
        self.nchoice_set = self.capacity.size
        ##price of shape (1, self.nalts)
        self.price = np.matrix(np.empty(nalts))
        self.price[...] = resources.get("price")[self.index]
        assert self.price.shape == (1, nalts)
        ## agent specific beta for price, of shape (nagents, 1)
        self.beta = resources.get("price_beta")  
        assert self.beta.shape == (nagents, 1)

        self.U_cached = utilities - np.dot(self.beta, self.price)
        price_init = copy(self.price)
        bounds0 = None
        kwargs = {'factr': 1e14, 'iprint':10}
        kwargs.update(resources.get('bfgs_kwargs', {}))
        results = fmin_l_bfgs_b(self.target_func, price_init, 
                                fprime=self.fprime, args=(self.capacity, self.beta), 
                                bounds=bounds0,
                                **kwargs)

        price_converged = results[0]
        resources.merge({'price_converged': price_converged})
        demand, prob = self.update_demand(price_converged)
        return lottery_choices.run(self, probability=prob,
                                   resources=resources)
        
    def update_price(self, price):
        """
        this can be expanded to allow various function form of price
        """
        self.price[...] = price

    def update_demand(self, price):
        self.update_price(price)
        addition = np.dot(self.beta, self.price)
        U_cached = self.U_cached
        out = ne.evaluate("exp(U_cached + addition)")
        sumV = ne.evaluate("sum(out, axis=1)")[:, np.newaxis]
        ne.evaluate("out / sumV", out=out)
        ## when alt set is from sampling
        #demand = ndimage.sum(out.ravel(),
        #                     labels=self.index.ravel(),
        #                     index=np.arange(self.nchoice_set))
        demand = ne.evaluate("sum(out, axis=0)")
        return demand, out

    def target_func(self, price, supply, beta=None):
        demand, _ = self.update_demand(price)
        
        if ne is not None:
            surplus = ne.evaluate("sum((demand - supply)**2)")
        else:
            surplus = np.sum((demand - supply)**2)
        #print surplus
        return surplus

    def fprime(self, price, supply, beta):
        demand, prob = self.update_demand(price)
        cross = self.cross_deriv(prob, beta)
        grad = np.sum(2 * (demand - supply) * cross, axis=1)
        return grad

    def own_deriv(self, prob, beta, _prob_beta=None):
        if ne is not None:
            if _prob_beta is None:
                out = ne.evaluate("prob * (1 - prob) * beta")
            else:
                out = ne.evaluate("_prob_beta * (prob - 1)")
            out = ne.evaluate("sum(out, axis=0)")
        else:
            if _prob_beta is None:
                out = prob * (1 - prob) * beta
            else:
                out = _prob_beta * (prob - 1)
            out = out.sum(axis=0)
        return out

    def cross_deriv(self, prob, beta):
        if ne is not None:
            _prob_beta = ne.evaluate("- prob * beta")
        else:
            _prob_beta = - prob * beta
        out = np.dot( prob.T, _prob_beta )
        own = self.own_deriv(prob, beta, _prob_beta)
        np.fill_diagonal(out, own)
        return out

