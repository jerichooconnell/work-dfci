import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import spekpy as sp

def gen_plot(s,lab):
    xx, yy = s.get_spectrum()
    plt.plot(xx, yy/1000000,label=lab)
    plt.xlabel('Energy [keV]')
    plt.ylabel('Fluence $[cm^{-1} keV^{-2}]$')
    plt.title('Effect of Filtration on the Beam')
def gen_plot_norm(s,lab,s1,s2,s2_val,s2_title,info=False):
    xx, yy = s.get_spectrum()
    s1.plot(xx, yy/np.sum(yy),label=lab)
    s1.set_xlabel('Energy [keV]')
    s1.set_ylabel('Fluence $[cm^{-1} keV^{-2}]$')
    s1.set_title('Effect of Filtration on the Beam')
    if info:
        print(f'{lab} \n \t Mean Energy: {s.get_emean()} keV \n \t Fluence {s.get_flu()} photons cm-2')
    s2.semilogy(s.get_emean(),s2_val,'*')
    s2.set_title(f'{s2_title}')

# Could you write a class that stores a spectrum array and information about the spectrum?
# Make a plot function in the class that plots the spectrum, and another that plots the spectrum normalized to 1.
# Make a function that plots the spectra of two objects, and the difference between them.
# Make a function that plots the spectra of two objects, and the ratio between them.
# Make a function that plots the spectra of two objects, and the ratio between them.

class spectrum(object):
    def __init__(self,xx,yy,info):
        self.xx = xx
        self.yy = yy
        self.yy_norm = yy/np.sum(yy)
        self.mean = np.sum(xx*yy)/np.sum(yy) # mean energy
        self.flu = np.sum(yy) # fluence
    def plot(self,ax):
        ax.plot(self.xx,self.yy)
        ax.title('Spectrum')
        ax.set_xlabel('Energy [keV]')
        ax.set_ylabel('Fluence $[cm^{-1} keV^{-2}]$')
    def plot_norm(self,ax):
        ax.plot(self.xx,self.yy_norm)
        ax.title('Normalized Spectrum')
        ax.set_xlabel('Energy [keV]')
        ax.set_ylabel('Normalized Fluence')
    def plot_diff(self,ax,s2):
        ax.plot(self.xx,self.yy-s2.yy)
        self.diff = np.mean(self.yy-s2.yy)
        ax.title('Difference')
        ax.set_xlabel('Energy [keV]')
        ax.set_ylabel('Fluence $[cm^{-1} keV^{-2}]$')
        ax.text(0.5,0.5,f'Mean difference: {self.diff}')
    def plot_ratio(self,ax,s2):
        ax.plot(self.xx,self.yy/s2.yy)
        ax.title('Ratio')
        ax.set_xlabel('Energy [keV]')
        ax.set_ylabel('Ratio')
        self.ratio = np.mean(self.yy/s2.yy)
        ax.text(0.5,0.5,f'Mean ratio: {self.ratio}')

# Could you generate a pandas dataframe that stores multiple spectra and information about them?

# class spectrum_df(object):
#     def __init__(self) -> None:
#         self.df = pd.DataFrame(columns=['xx','yy','yy_norm','mean','flu'])
#     def add_spectrum(self,xx,yy,info):
#         self.df.append({'xx':xx,'yy':yy,'yy_norm':yy/np.sum(yy),'mean':np.sum(xx*yy)/np.sum(yy),'flu':np.sum(yy)},ignore_index=True)


# if __name__ == '__main__':
#     materials = ['Al','Ti','Water','Cesium Iodide','Sn','Si','Cesium Iodide','Si']
#     thicknesses = [1,1,100,0.6,1,0.1,0.8,0.1]

#     s.get_flu()

#     s = sp.Spek(140,th=14)
#     plt.figure(figsize=[10,6])
#     s1 = plt.subplot(121)
#     s2 = plt.subplot(122)
#     for mat, thick in zip(materials, thicknesses):
        
#         s.filter(mat, thick)
#         gen_plot_norm(s,f'After {mat}',s1,s2,s.get_flu(),'Fluence',info='True')
        
#     s1.legend()
