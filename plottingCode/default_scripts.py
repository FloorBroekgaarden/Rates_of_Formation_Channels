# Basic scripts / code for plotting  


import numpy as np
import matplotlib.pyplot as plt
# for e.g., minor ticks 
from matplotlib.ticker import (FormatStrFormatter, AutoMinorLocator)

import matplotlib
import seaborn as sns # only used for sns colors 
import pandas as pd # to read in the csv files 
import matplotlib as mpl

from astropy import units as u
from astropy import constants as const

from matplotlib import rc                                                                                                                                                                                                                    
from matplotlib import rcParams
import string
#Set latex environment for plots/labels
# rc('font', family='serif', weight = 'bold')
# rc('text', usetex=True)
# # matplotlib.rcParams['text.latex.preamble']=[r"\usepackage{amsmath}"]
# # matplotlib.rcParams['text.latex.preamble'] = [r'\boldmath']
# rc('axes', linewidth=2)
# rc('text', usetex=True)


# matplotlib.rcParams['xtick.major.size'] = 12
# matplotlib.rcParams['ytick.major.size'] = 12
# matplotlib.rcParams['xtick.minor.size'] = 8
# matplotlib.rcParams['ytick.minor.size'] = 8
# matplotlib.rcParams['font.weight']= 'bold'
# matplotlib.rcParams.update({'font.weight': 'bold'})

# fs = 24 # fontsize for plots
# rc('axes', linewidth=2)

dictDCOdirectory = {'BHBH':'BH-BH', 'BHNS': 'NS-BH', 'NSNS':'NS-NS'}



mpl.rcParams['hatch.linewidth'] = 0.5   # default is 1.0
mpl.rcParams['hatch.color'] = 'darkslategray'   # optional: set hatch color



rc('font', family='serif', weight = 'bold')
rc('text', usetex=True)
# matplotlib.rcParams['text.latex.preamble']=[r"\usepackage{amsmath}"]
matplotlib.rcParams['text.latex.preamble'] = r'\boldmath'
rc('axes', linewidth=2)

matplotlib.rcParams['xtick.major.size'] = 12
matplotlib.rcParams['ytick.major.size'] = 12
matplotlib.rcParams['xtick.minor.size'] = 8
matplotlib.rcParams['ytick.minor.size'] = 8
matplotlib.rcParams['font.weight']= 'bold'
matplotlib.rcParams.update({'font.weight': 'bold'})

fs = 24 # fontsize for plots
rc('axes', linewidth=2)




def draw_vlines(axe, v_values):
    """ draws vertical grid lines at values in the v_values list """
    
    for v_ in v_values:
        # draw vertical line that looks similar to grid line 
#         axe.plot([v_, v_], [-1E5, 2], lw=2, c='gray', ls='-', zorder=0)
        axe.plot([v_, v_], [-1E5, 2], lw=1.5, c='gray', ls=':', zorder=0)
        
    return 





def make_up_axes(axe=None, DCOtype='BHNS',  df_names=['a', 'b'], ordered=None, version='ArXiv'):
    """ creates several things that are axes related"""

    xmin,xmax = -0.1, 1.1
        
    # axes layout and mark up 
    # axe.set_xscale('log')
    DCOname_dict = {'BHNS':'NS-BH', 'BHBH':'BH-BH', 'NSNS':'NS-NS'}
    xlabel = r'$\rm{Fraction } \ \textbf{of} \  \textbf{%s} \ $'%DCOname_dict[DCOtype] + r'$\textbf{mergers} $'
    
    
    bps_names = []
    codes_names = []
   

    v_height=0
    yticks=[]   
    for ind_file, csv_filename in enumerate(df_names):
        
        df = pd.read_csv(csv_filename, header=0, skiprows=[0,1,2,3,4,6,7,8,9,10,11,12,13])
        df = df.iloc[:,1::2]

        rate_max_list = []
        codes_list = []
        
        df_codes = pd.read_csv(csv_filename, header=0, skiprows=[0,1,2,3,4,6,8,9,10,11,12,13])
        df_codes = df_codes.iloc[:,1::2]
        codes = df_codes.columns

        v_height+= -1
        if ordered=='max':
            for ind_n, name in enumerate(df.columns):
                rate = df[name]
                mask_notna = (df[name].notna())
                rate = rate[mask_notna]
                
                rate_max_list.append(np.max(rate))
                
                code = df_codes[name][0]
                codes_list.append(code)
            
            sorted_ind = np.argsort(np.asarray(rate_max_list))
        
            colum_list_sorted = df.columns[sorted_ind]
            codes_list_sorted = np.asarray(codes_list)[sorted_ind]
            
        elif ordered=='year':
            colum_list_sorted = df.columns 
            for ind_n, name in enumerate(df.columns):              
                code = df_codes[name][0]
                codes_list.append(code)
            codes_list_sorted = np.asarray(codes_list)
        
        
        elif ordered=='code':
            for ind_n, name in enumerate(df.columns):
                rate = df[name]
                mask_notna = (df[name].notna())
                rate = rate[mask_notna]
                
                rate_max_list.append(np.max(rate))
                
                code = df_codes[name][0]
                codes_list.append(code)
            
            sorted_ind = np.argsort(np.asarray(codes_list))
        
            colum_list_sorted = df.columns[sorted_ind]
            codes_list_sorted = np.asarray(codes_list)[sorted_ind]     
        
        else:
            colum_list_sorted = df.columns        
            codes_list_sorted = codes 
            

        
        for ind_m, bps_model in enumerate(colum_list_sorted):
            bps_names.append(r'\textbf{%s}'%(bps_model) )
            codes_names.append(r'\textbf{%s}'%(codes_list_sorted[ind_m]) )
            yticks.append(v_height)
            v_height+=-1
        
        # add blank line after each channel 
        v_height+= -1 

    axe.set_yticks([])

    
    axe.set_xlim(xmin, xmax)
    axe.set_ylim(-len(bps_names) -2*len(df_names)+0.5, 0.5)
    
    if version=='ArXiv':
        # add x labels on top
        ax2x = axe.twiny()
        # ax2x.set_xscale('log')   
        ax2x.set_xlim(xmin, xmax)
        ax2x = layoutAxesNoYlabel(ax2x, nameX=xlabel, nameY=r'NA', fontsize=fs+6, setMinor=False, second=True, labelpad=20)
    
    axe = layoutAxesNoYlabel(axe, nameX=xlabel, nameY=r'NA', fontsize=fs+6, setMinor=False, labelpad=4)


    return 
    
     
    




# def plot_using_plotting_style(axe, ps, x_, y_, color):
#     """ uses the plotting style (integer ps between 0 and 30) 
#     to plot the data given the plottingstyle that is given in the csv file 
#     the dictionary is: 

#     1: only upper limit(s) 
#     2: only lower limit(s) 
#     3: interval without center value
#     4: interval with center value   (90% confidence interval or so) 
#     5: interval with range of simulation values 
#     6: interval with range of simulation values last point is upper limit 
#     7: interval with range of simulation values first point is lower limit 
#     8: (two confidence intervals)  range + two center values (weird one) 
#     9: interval with range of simulation values , first one is fiducial 
#     10; interval with range of simulation values use ylim to add lower limit 
#     11; interval with range of simulation values , first two are fiducial 
#     12: single estimate without error bars 
#     13; interval with range of simulation values , first three are fiducial 
#     14; interval with range of simulation values use ylim to add upper limit 
#     15: interval, upper 3 are upper limits 
#     16: two upper limits 
#     17: interval with range of simulation values first point is upper limit 
#     18: interval with range of simulation values first point is upper limit  +   2 upper ones are upper limits
#     19:
#     20: 
    
#     """ 
    
#     # draw upper/lower limit: 
#     if ps in [1,2,6,7, 10, 12, 14, 15 , 16, 17 , 18, 19, 20 ]:
#         msize = 400
#         if ps in [1,6,14]:
#             mstyle = 4 # upper limit 
#             axe.scatter(np.max(x_), np.max(y_), s=msize, c=np.asarray([color]), zorder=1E6, marker=mstyle)
#         if ps in [20]:
#             mstyle =  8 # upper limit but triangle more to the left 
#             axe.scatter(1.05*np.max(x_), np.max(y_), s=msize, c='k', zorder=1E6, marker=mstyle)
#         elif ps in [17, 18]:
#             mstyle=4 # upper limit  (lower limit)
#         # draw upper or lower limit
#             axe.scatter(np.min(x_), np.min(y_), s=msize, c='k', zorder=1E6, marker=mstyle)            
#         elif ps in [2,7]:
#             mstyle=5 # lower limit 
#         # draw upper or lower limit
#             axe.scatter(np.min(x_), np.min(y_), s=msize, c='k', zorder=1E6, marker=mstyle)
#         elif ps in [14]:
#             mstyle=4
#             # 1E4 is upper limit 
#             axe.scatter(0.99*1E5, np.max(y_), s=msize, c='cyan', zorder=1E6, marker=mstyle)
#         elif ps in [15]:
#             mstyle=4
#             # top 3 are upper limit  
#             axe.scatter(x_[-3:], y_[-3:], s=msize, c='k', zorder=1E6, marker=mstyle)
#         elif ps in [18]:
#             mstyle=4
#             # top 2 are upper limit  
#             axe.scatter(x_[-2:], y_[-2:], s=msize, c='k', zorder=1E6, marker=mstyle)
#         elif ps in [16]:
#             mstyle=4
#             # top 3 are upper limit  
#             axe.scatter(x_[-2:], y_[-2:], s=msize, c='k', zorder=1E6, marker=mstyle)
#         elif ps in [10]:
#             mstyle=5
#             # 1E-3 is lower limit y axis 
#             axe.scatter(1E-3, np.max(y_), s=msize, c='cyan', zorder=1E6, marker=mstyle)
#         elif ps in [12]:
#             msize = 125
#             axe.scatter(x_, y_, s=msize, c=np.asarray([color]), zorder=1E2, marker='o') 
#         elif ps in [19]:
#             mstyle=4
#             # 1E-3 is upper lower limit y axis 
#             axe.scatter(1E-3, np.max(y_), s=msize, c='cyan', zorder=1E6, marker=mstyle)



#     # draw error bar 
#     msize = 125
#     if ps in [3,4,5,6, 7, 8,9,10,11,13, 14, 15, 17, 18 ]:
#         axe.errorbar(x=[np.min(x_),np.max(x_)], y=[y_[0], y_[0]], yerr=2*[0.42], color=color, zorder=5, lw=5.5, ecolor=color)
#         axe.errorbar(x=[np.min(x_),np.max(x_)], y=[y_[0], y_[0]], yerr=2*[0.42], fmt='o', zorder=1E5, lw=3.5, ecolor='k', color='k')
#         if ps==4:
#             # plot center values
#             axe.scatter(x_[1], y_[1], s=msize, c='k', zorder=1E2, marker='o')
#         elif ps==3:
#             # don't plot scatter points
#             pass
#         elif ps==15:
#             axe.scatter(x_[0:3], y_[0:3], s=msize, color=[color], zorder=1E2, marker='o') 
#         else:
#             axe.scatter(x_, y_, s=msize, color=[color], zorder=1E2, marker='o') 

 
#     return 




# some functions to make beautiful axes 


def layoutAxes(ax, nameX='', nameY='', \
               labelSizeMajor = 10, fontsize = 25, second=False, labelpad=None, setMinor=True, labelpad_x=None, labelpad_y=None,\
               noXticks=False, noYticks=False):
    """
    Tiny code to do the layout for axes in matplotlib
    """
    tickLengthMajor = 10
    tickLengthMinor = 5
    tickWidthMajor  = 1.5
    tickWidthMinor  = 1.5


    if labelpad:
        labelpad_x = labelpad
        labelpad_y = labelpad

    
    #rc('axes', linewidth=2)
    #label1 always refers to first axis not the twin 
    if not second:
        for tick in ax.xaxis.get_major_ticks():
            tick.label1.set_fontsize(fontsize)
            #tick.label1.set_fontweight('bold')
        for tick in ax.yaxis.get_major_ticks():
            tick.label1.set_fontsize(fontsize)
            #tick.label1.set_fontweight('bold')
    if second:
        for tick in ax.xaxis.get_major_ticks():
            tick.label2.set_fontsize(fontsize)
            #tick.label1.set_fontweight('bold')
        for tick in ax.yaxis.get_major_ticks():
            tick.label2.set_fontsize(fontsize)
            #tick.label1.set_fontweight('bold')
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(1.2)
    ax.tick_params(length=tickLengthMajor, width=tickWidthMajor, which='major')
    ax.tick_params(length=tickLengthMinor, width=tickWidthMinor, which='minor')


    if labelSizeMajor==10:
        ax.set_xlabel(nameX, fontsize=fontsize,labelpad=labelpad_x)#,fontweight='bold')
        ax.set_ylabel(nameY, fontsize=fontsize,labelpad=labelpad_y)#, fontweight='bold')    
    else:
        ax.set_xlabel(nameX, fontsize=labelSizeMajor,labelpad=labelpad_x)#,fontweight='bold')
        ax.set_ylabel(nameY, fontsize=labelSizeMajor,labelpad=labelpad_y)#, fontweight='bold')  

    if setMinor==True:
        # add minor ticks:
        ax.xaxis.set_minor_locator(AutoMinorLocator())
        ax.yaxis.set_minor_locator(AutoMinorLocator())

    # new do not plot ticks if nameX is none
    if  (noXticks==True):
        ax.set_xticklabels( () )
        ax.set_xticks([])
    if (noYticks==True):
        ax.set_yticks([])
        ax.set_yticklabels( () ) 

    return ax



def layoutAxesNoXandYlabel(ax, nameX='', nameY='', \
               labelSizeMajor = 10, fontsize = 25, second=False, labelpad=None, setMinor=True, labelpad_x=None, labelpad_y=None,\
               noXticks=False, noYticks=False):
    """
    Tiny code to do the layout for axes in matplotlib
    """
    tickLengthMajor = 10
    tickLengthMinor = 5
    tickWidthMajor  = 1.5
    tickWidthMinor  = 1.5
    
    #rc('axes', linewidth=2)
    #label1 always refers to first axis not the twin 
    if not second:
        for tick in ax.xaxis.get_major_ticks():
            tick.label1.set_fontsize(fontsize)
            #tick.label1.set_fontweight('bold')
        for tick in ax.yaxis.get_major_ticks():
            tick.label1.set_fontsize(fontsize)
            #tick.label1.set_fontweight('bold')
    if second:
        for tick in ax.xaxis.get_major_ticks():
            tick.label2.set_fontsize(fontsize)
            #tick.label1.set_fontweight('bold')
        for tick in ax.yaxis.get_major_ticks():
            tick.label2.set_fontsize(fontsize)
            #tick.label1.set_fontweight('bold')
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(1.2)
    ax.tick_params(length=tickLengthMajor, width=tickWidthMajor, which='major')
    ax.tick_params(length=tickLengthMinor, width=tickWidthMinor, which='minor')
    # ax.set_xlabel(nameX, fontsize=fontsize,labelpad=labelpad)#,fontweight='bold')
    # ax.set_ylabel(nameY, fontsize=fontsize,labelpad=labelpad)#, fontweight='bold')    
    
    if setMinor==True:
        # add minor ticks:
        ax.xaxis.set_minor_locator(AutoMinorLocator())
        ax.yaxis.set_minor_locator(AutoMinorLocator())


    # new do not plot ticks if nameX is none
    if  (noXticks==True):
        ax.set_xticklabels( () )
        ax.set_xticks([])
    if (noYticks==True):
        ax.set_yticks([])
        ax.set_yticklabels( () ) 



    return ax


def layoutAxesNoXlabel(ax, nameX='', nameY='', \
               labelSizeMajor = 10, fontsize = 25, second=False, labelpad=None, setMinor=True, rotation=90,\
               noXticks=False, noYticks=False):
    """
    Tiny code to do the layout for axes in matplotlib
    """
    tickLengthMajor = 10
    tickLengthMinor = 5
    tickWidthMajor  = 1.5
    tickWidthMinor  = 1.5
    
    #rc('axes', linewidth=2)
    #label1 always refers to first axis not the twin 
    if not second:
        for tick in ax.xaxis.get_major_ticks():
            tick.label1.set_fontsize(fontsize)
            #tick.label1.set_fontweight('bold')
        for tick in ax.yaxis.get_major_ticks():
            tick.label1.set_fontsize(fontsize)
            #tick.label1.set_fontweight('bold')
    if second:
        for tick in ax.xaxis.get_major_ticks():
            tick.label2.set_fontsize(fontsize)
            #tick.label1.set_fontweight('bold')
        for tick in ax.yaxis.get_major_ticks():
            tick.label2.set_fontsize(fontsize)
            #tick.label1.set_fontweight('bold')
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(1.2)
    ax.tick_params(length=tickLengthMajor, width=tickWidthMajor, which='major')
    ax.tick_params(length=tickLengthMinor, width=tickWidthMinor, which='minor')
    # ax.set_xlabel(nameX, fontsize=fontsize,labelpad=labelpad)#,fontweight='bold')
    if labelSizeMajor==10:
        # ax.set_xlabel(nameX, fontsize=fontsize,labelpad=labelpad)#,fontweight='bold')
        ax.set_ylabel(nameY, fontsize=fontsize,labelpad=labelpad)#, fontweight='bold')    
    else:
        # ax.set_xlabel(nameX, fontsize=labelSizeMajor,labelpad=labelpad)#,fontweight='bold')
        ax.set_ylabel(nameY, fontsize=labelSizeMajor,labelpad=labelpad)#, fontweight='bold')     


    # new do not plot ticks if nameX is none
    if  (noXticks==True):
        ax.set_xticklabels( () )
        ax.set_xticks([])
    if (noYticks==True):
        ax.set_yticks([])
        ax.set_yticklabels( () ) 


    if setMinor==True:
        # add minor ticks:
        ax.xaxis.set_minor_locator(AutoMinorLocator())
        ax.yaxis.set_minor_locator(AutoMinorLocator())

    return ax






def layoutAxesNoYlabel(ax, nameX='', nameY='', \
               labelSizeMajor = 10, fontsize = 25, second=False, labelpad=None, setMinor=True, rotation=0,\
               noXticks=False, noYticks=False):
    """
    Tiny code to do the layout for axes in matplotlib
    """
    tickLengthMajor = 10
    tickLengthMinor = 5
    tickWidthMajor  = 1.5
    tickWidthMinor  = 1.5


    
    #rc('axes', linewidth=2)
    #label1 always refers to first axis not the twin 
    if not second:
        for tick in ax.xaxis.get_major_ticks():
            tick.label1.set_fontsize(fontsize)
            #tick.label1.set_fontweight('bold')
        # for tick in ax.yaxis.get_major_ticks():
        #     tick.label1.set_fontsize(fontsize)
            #tick.label1.set_fontweight('bold')
    if second:
        for tick in ax.xaxis.get_major_ticks():
            tick.label2.set_fontsize(fontsize)
            #tick.label1.set_fontweight('bold')
        # for tick in ax.yaxis.get_major_ticks():
        #     tick.label2.set_fontsize(fontsize)
            #tick.label1.set_fontweight('bold')
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(1.2)
    ax.tick_params(length=tickLengthMajor, width=tickWidthMajor, which='major')
    ax.tick_params(length=tickLengthMinor, width=tickWidthMinor, which='minor')
    ax.set_xlabel(nameX, fontsize=fontsize,labelpad=labelpad, rotation=rotation)#,fontweight='bold')
    # ax.set_ylabel(nameY, fontsize=fontsize,labelpad=labelpad)#, fontweight='bold')    
    
    if setMinor==True:
        # add minor ticks:
        ax.xaxis.set_minor_locator(AutoMinorLocator())
        ax.yaxis.set_minor_locator(AutoMinorLocator())

     # new do not plot ticks if nameX is none
    if  (noXticks==True):
        ax.set_xticklabels( () )
        ax.set_xticks([])
    if (noYticks==True):
        ax.set_yticks([])
        ax.set_yticklabels( () ) 



    return ax



##### Formation Channel Fraction specific code 


def obtain_fc_dict():
    """
    Returns a dictionary defining formation channel (fc) specifications.

    Each top-level key corresponds to a grouping of formation channels 
    (e.g., 'CE_simple', 'CE_detailed', or 'total').  
    Each group contains either a list of 'channels' (with properties) 
    or a single entry (for 'total').
    """


    palette = {
        # Neutrals
        "gray_light":  "#e0e0e0",
        "gray_dark":   "#C2C2C2",

        # Non-CE warm family
        "orange_main": "#FFA630",
        "orange_sub":  "#ffc857",
        
        "orange_soft": "#f4a259",
        "red_soft":    "#e45756",
        "rose":        "#d96c75",
        "terracotta":  "#bc4b51",
        "peach":       "#ffb5a7",
        
        # No MT families 
        "violet":      "#7b2cbf",
        "purple":      "#9d4edd",
        "magenta":     "#c77dff",
        "lavender":    "#b8a0ff",
        "burgundy": "#7f1d1d",
        "wine":     "#6d213c",
        "maroon":   "#800020",

        # CE cool family
        "blue_main":   "#00A7E1",
        "blue_light":  "#5dade2",
        "blue_mid":    "#0474BA",
        "blue_dark":   "#004e89",
        "indigo":      "#3a3d98",   # new deep indigo for AIC
        "teal_light":  "#20b2aa",
        "green_blue":  "#58AD8B",
        "aqua":        "#00bfc4",
        "seafoam":     "#8dd3c7",
        "mint":        "#9de0ad",
    }


    fc_dict = {
        # A simplified common-envelope grouping (just two channels).
        "CE_simple": {
            "channels": [
                {"name": "fraction without common envelope", "color":palette["orange_main"], "hatch": None, "label":'without common envelope', "axlabel":"fraction without CE"},
                {"name": "fraction not specified",           "color":palette[ "gray_dark"],  "hatch":None,   "label":'other (CE not specified)'},
                {"name": "fraction with common envelope",    "color":palette["blue_main"],   "hatch": None , "label":'with common envelope', "axlabel":"fraction with CE"}
            ],
            "label_ncols":3
        },

        
        "CE_detailed": {
            "channels": [
                
                # --- Non-CE channels (warm hues, all unique) ---
                {"name": "without CE (no detail specified)", "color":palette["orange_main"], "hatch": None, "label":'without common envelope'},
                {"name": "SMT before and after channel",     "color":palette["orange_main"],    "hatch": '...', "label":'classic SMT (SMT + SMT)'},
                {"name": "SMT+NON",                          "color":palette["rose"],        "hatch": "ooo", "label":'SMT + NON'},
                {"name": "NON+SMT",                          "color":palette["red_soft"], "hatch": "xxx", "label":'NON + SMT'},
                {"name": "channel V intrinsic (z=0) other without CE", "color":palette["peach"], "hatch": "***", "label":'other without CE'},
                
                {"name": "NON + NON",                        "color":palette["magenta"],  "hatch":'\\', "label":'NON + NON'},
                {"name": "CHE",                              "color":palette["lavender"],     "hatch":"///",   "label":'CHE (no MT)'},
                
                
                {"name": "channel V intrinsic (z=0) CE not specified",    "color":palette["gray_dark"],  "hatch": None, "label":'other (CE not specified)'},
                
                # --- CE channels (cool hues, all unique) ---
                {"name": "with CE (no detail specified)",                 "color":palette["blue_main"],  "hatch": None, "label":'with common envelope'},
                
                {"name": "channel I intrinsic (z=0) classic CE (SMT+CE)", "color":palette["blue_main"], "hatch": "//", "label":'classic CE'},
                {"name": "channel III intrinsic (z=0) SCCE",              "color":palette["blue_mid"],   "hatch": "xxx", "label":'single-core CE'},
                {"name": "channel IV intrinsic (z=0) DCCE",               "color":palette["teal_light"], "hatch": "xxx", "label":'double-core CE'},
                
                {"name": "CEE + SMT",                                     "color":palette["green_blue"], "hatch": '\\', "label":'CE + SMT'},
                {"name": "CEE+CEE",                                       "color":palette["aqua"],       "hatch": "\\", "label":'CE + CE'},
                {"name": "NON+CEE",                                       "color":palette["indigo"],    "hatch": '//', "label":'NON + CE'},
                {"name": "CEE+NON",                                       "color":palette["mint"],       "hatch": '//', "label":'CE + NON'},

                {"name": "channel radCEE",  "color":palette["blue_dark"], "hatch": "***", "label":'radiative CE'},
                {"name": "channel convCEE", "color":palette["seafoam"], "hatch": "***", "label":'convective CE'},
                {"name": "channel V intrinsic (z=0) other with CE", "color":palette["seafoam"], "hatch": '...', "label":'other with CE'}
#                 {"name": "channel AIC with CE", "color":palette["indigo"], "hatch": '//', "label":'AIC with CE'},         

            ],
            "label_ncols":5
        },

        # A total merger rate across all intrinsic channels.
        "total": {
            "name": "All intrinsic (z=0) [Gpc^-3 yr^-1]",
            "color": "black",
            "hatch": None,
            "label":r"All intrinsic ($z=0$) \ $[\rm{Gpc}^{-3} \rm{yr}^{-1}$]",
            "label_ncols":1,
            "axlabel":r"Total local merger rate", # % ($z=0$) \ $[\rm{Gpc}^{-3} \rm{yr}^{-1}$]
        },
    }

    
    fc_dict["CE_detailed_subset"] = fc_dict["CE_detailed"].copy()
    
    
    return fc_dict





# info for Broekgaarden models 

nModels=20 # 
BPSnameslist = list(string.ascii_uppercase)[0:nModels]
modelDirList = ['fiducial', 'massTransferEfficiencyFixed_0_25', 'massTransferEfficiencyFixed_0_5', 'massTransferEfficiencyFixed_0_75', \
               'unstableCaseBB', 'unstableCaseBB','alpha0_1', 'alpha0_5', 'alpha2_0', 'alpha10', 'fiducial', 'rapid', 'maxNSmass2_0', 'maxNSmass3_0', 'noPISN',  'ccSNkick_100km_s', 'ccSNkick_30km_s', 'noBHkick', 'wolf_rayet_multiplier_0_1', 'wolf_rayet_multiplier_5']

alphabetDirDict =  {BPSnameslist[i]: modelDirList[i] for i in range(len(BPSnameslist))}
BPScolors       = sns.color_palette("husl", nModels)
colorDirDict =  {BPSnameslist[i]: BPScolors[i] for i in range(len(BPSnameslist))}


markershapes = ["*", "o", "v",  "p", "H", "^", ">", 'X', "+","<", 'x', "3","d","1", "|", "D", "P", "X", "+", "d"]
dictMarkerShape = {BPSnameslist[i]: markershapes[i] for i in range(len(BPSnameslist))}


metallicities_list = [0.0001, 0.00011, 0.00012, 0.00014, 0.00016, 0.00017,\
   0.00019, 0.00022, 0.00024, 0.00027, 0.0003, 0.00034, \
   0.00037, 0.00042, 0.00047, 0.00052, 0.00058, 0.00065,\
   0.00073, 0.00081, 0.0009, 0.00101, 0.00113, 0.00126,\
   0.0014, 0.00157, 0.00175, 0.00195, 0.00218, 0.00243, \
   0.00272, 0.00303, 0.00339, 0.00378, 0.00422, 0.00471, \
   0.00526, 0.00587, 0.00655, 0.00732, 0.00817, 0.00912, \
   0.01018, 0.01137, 0.01269, 0.01416, 0.01581, 0.01765, 0.01971, 0.022, 0.0244, 0.02705, 0.03]


headerDict_Z_rev = {'classic':'channel I', 'stable B no CEE':'channel II', 'vii':'channel VII',  'immediate CE':'channel III',  r'double-core CE':'channel IV', 'other':'channel V', 'vi':'channel VI'} #['I_classic', 'II_only_stable_MT', 'III_single_core_CE', 'IV_double_core_CE', 'V_other']

