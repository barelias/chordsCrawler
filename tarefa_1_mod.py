import numpy as np 
import matplotlib.pyplot as plp 

'''
	Dado uma matriz de distancias m_dist_rand, um numero de dimensoes n_dim,
	um numero de elementos n_cid e um indice de elemento sorteado, retorna um
	vetor de distancias entre a linha sorteada e a outras linhas matriz m_dist_rand
'''
def carrega_cid(m_dist_rand, n_dim, n_cid, sorteio):
	f = np.zeros([dim, cid-1])
	k = np.arange(n_cid)
	for i in range(n_dim):
		f[i,:] = m_dist_rand[k != sorteio, i] - m_dist_rand[sorteio, i]
	return f

'''
	Dado uma matriz matriz_alvo e outra matriz_real, dado o numero de dimensoes dessas
'''
def otimi_grad(matriz_alvo, matriz_real, sorteio, n_cid):
	k = np.arange(n_cid)
	g = (np.sum(matriz_alvo**2,axis=0))**0.5
    h = (g - matriz_real[sorteio, k != sorteio])**2
    J = (np.sum(h))**0.5
    alpha = np.sum((g - matriz_real[sorteio,k != sorteio])*g**-1*matriz_alvo*(-1),axis=1)
    dJ = J**-1*alpha
    return alpha, dJ

def calc_dist_euclid(m_dist_rand):
	#inicializacao dos pontos da cidade
	m = np.zeros([m_dist_rand.shape[0], m_dist_rand.shape[0]])
	for i in range(m_dist_rand.shape[0]):
    	for j in range(m_dist_rand.shape[0]):
        	m[i,j] = ((m_dist_rand[i,0] - m_dist_rand[j,0])**2 + (m_dist_rand[i,1] - m_dist_rand[j,1])**2)**0.5
    return m 


def treinamento_dist(m_d4ist_rand, matriz_real, n_iter, n_cid, n_dim, passo):
	m_dist_aux = m_dist_rand
	for i in range(n_iter):
		sorteio = np.random.randint(n_cid)
		f = carrega_cid(m_dist_aux, n_dim, n_cid, sorteio)
		alpha, dJ = otimi_grad(f, matriz_real, sorteio, n_cid)
		m = calc_dist_euclid(m_dist_aux)
		if  (np.sum(((m-matriz_real)/2)**2) <= 1000):
	        break
		m_dist_aux[sorteio,:] = m_dist_aux[sorteio,:] - alpha*passo 
	return 


#P sera minha matriz_alvo = m _dist_rand
#f = matriz alvo0