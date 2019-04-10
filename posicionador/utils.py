import matplotlib.pyplot as plt

## Ploting Rotas and Polo

def plot_polo_rotas(rotas_geo, polo_geo, title=''):
    ax = rotas_geo.plot(color='red', alpha=1, edgecolor='k')
    polo_geo.plot(ax=ax, color='green', alpha=0.5)
    plt.title(title)
    plt.show()
        
        
def plot_only_rotas(rotas_geo, title=''):
    rotas_geo.plot(alpha=0.5, edgecolor='k', cmap='tab10')
    plt.title(title)
    plt.show()