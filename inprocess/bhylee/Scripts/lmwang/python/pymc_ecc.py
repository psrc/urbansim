from PyMC.MCMC import *
from numarray import *
from numarray.random_array import randint, seed

N = 7000; n = 500
J = 22

class MultinomialSampler(MetropolisHastings):

    def __init__(self):

        'Initialize superclass'
        MetropolisHastings.__init__(self)

        'Model parameters'
        #self.parameter('beta0',init_val=ones(J)*1.0)
        self.parameter('beta1',init_val=ones(J)*1.0)
        'Nodes'
        self.node('p',(n,J))
        self.node('phi',(n,J))


    def calculate_likelihood(self):
        
        'Initialize likelihood'
        like = 0.0
        
        'Loop over data'
        for i in range(n):

            'Set the first group as a *baseline* -- i.e. coefficients equal to zero'
            #beta0,beta1 = concatenate(([0],self.beta0)),concatenate(([0],self.beta1))
            #beta0,beta1 = self.beta0, self.beta1
            beta1 = self.beta1
            
            #import pdb; pdb.set_trace()
            'Multinomial logit model'
            #self.phi[i] = [exp(beta0[j] + beta1[j]*x[i,j,var['COM_SF']]) for j in range(J)]
            self.phi[i] = [exp(beta1[j]*x1[i,j]) for j in range(J)]
            self.p[i] = [self.phi[i,j]/sum(self.phi[i]) for j in range(J)]
            
            'Multinomial likelihood'
            like += multinomial_like(y[i][:],1,self.p[i][:])

        return like    

if __name__=="__main__":

    import sys
    
    if 'win' in sys.platform:
        csvfile='w:/users/HyungTai/sec10sta_95job_7K.csv'
    elif 'linux' in sys.platform:
        csvfile='/projects/urbansim7/users/HyungTai/sec10sta_95job_7K.csv'
    else:
        csvfile='./sec10sta_95job_7K.csv'
    datafile = open(csvfile)
    var = {}
    var_name = datafile.readline().strip().split(',')
    for i in range(len(var_name)):
        var[var_name[i]] = i
    data = []
    for line in datafile:
        row = line.strip().split(',')
        row = map(float, row)
        data.append(row)
    datafile.close()
    
    data = reshape(data, (N, J, -1))
    y = copy.copy(data[..., var['choice']])
    x1 = copy.copy(data[..., var['COM_SF']] / 1000000)
    del data

    'sample 500 from x, y'
    ind1 = randint(0, N, (n,1))
    ind2 = array(range(J),shape=(1,J))
    y = y[ind1,ind2]
    x1 = x1[ind1,ind2]

    'Instantiate sampler'
    sampler = MultinomialSampler()
    'Run sampler'
    sampler.sample(2000, plot=False)
            
