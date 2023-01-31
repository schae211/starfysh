import numpy as np
import scanpy as sc
import matplotlib.pyplot as plt
import seaborn as sns


# Module import
from .post_analysis import get_z_umap
from .utils import extract_feature


def plot_spatial_feature(adata_sample,
                         map_info,
                         variable,
                         label
                     ):
    all_loc = np.array(map_info.loc[:,['array_col','array_row']])
    fig,axs= plt.subplots(1,1,figsize=(2.5,2),dpi=300)
    g=axs.scatter(all_loc[:,0],
                  -all_loc[:,1],
                  c=variable,
                  cmap='magma',
                  s=1
                 )
    fig.colorbar(g,label=label)
    plt.axis('off')


def plot_spatial_gene(adata_sample,
                         map_info,
                         gene_name,
                         
                     ):
    all_loc = np.array(map_info.loc[:,['array_col','array_row']])
    fig,axs= plt.subplots(1,1,figsize=(2.5,2),dpi=300)
    g=axs.scatter(all_loc[:,0],
                  -all_loc[:,1],
                  c=adata_sample.to_df().loc[:,gene_name],
                  cmap='magma',
                  s=1
                 )
    fig.colorbar(g,label=gene_name)
    plt.axis('off')


def plot_anchor_spots(umap_plot,
                      pure_spots,
                      sig_mean,
                      bbox_x=2,
                     ):
    fig,ax = plt.subplots(1,1,dpi=300,figsize=(3,3))
    ax.scatter(umap_plot['umap1'],
               umap_plot['umap2'],
               s=2,
               alpha=1,
               color='lightgray')
    for i in range(len(pure_spots)):
        ax.scatter(umap_plot['umap1'][pure_spots[i]],
                   umap_plot['umap2'][pure_spots[i]],
                   s=8)
    plt.legend(['all']+[i for i in sig_mean.columns],
               loc='right', 
               bbox_to_anchor=(bbox_x,0.5),)
    ax.grid(False)
    ax.axis('off')


def plot_evs(evs, kmin):
    fig, ax = plt.subplots(1, 1, dpi=300, figsize=(6, 3))
    plt.plot(np.arange(len(evs))+kmin, evs, '.-')
    plt.xlabel('ks')
    plt.ylabel('Explained Variance')
    plt.show()


def pl_spatial_inf_feature(
    adata,
    feature,
    factor=None,
    vmin=0,
    vmax=None,
    s=3,
    cmap='Spectral_r'
):
    """Spatial visualization of Starfysh inference features"""
    if factor is not None:
        assert factor in set(adata.varm['cell_types']), \
            "Invalid Starfysh inference factor (cell type): ".format(factor)

    adata_pl = extract_feature(adata, feature)

    if feature == 'qc_m':
        if isinstance(factor, list):
            title = [f + ' (Inferred proportion - Spatial)' for f in factor]
        else:
            title = factor + ' (Inferred proportion - Spatial)'
        sc.pl.spatial(
            adata_pl,
            color=factor, spot_size=s, color_map=cmap,
            ncols=3, vmin=vmin, vmax=vmax,
            title=title, legend_fontsize=15
        )
    elif feature == 'ql_m':
        title = 'Estimated tissue density'
        sc.pl.spatial(
            adata_pl,
            color='density', spot_size=s, color_map=cmap,
            vmin=vmin, vmax=vmax,
            title=title, legend_fontsize=15
        )
    elif feature == 'qz_m':
        # Visualize deconvolution on UMAP of inferred Z-space
        qz_u = get_z_umap(adata_pl.obs.values, adata.obs.index)
        qc_df = extract_feature(adata, 'qc_m').obs
        if isinstance(factor, list):
            for cell_type in factor:
                title = cell_type + ' (Inferred proportion - UMAP of Z)'
                pl_umap_feature(qz_u, qc_df[cell_type].values, cmap, title,
                                s=s, vmin=vmin, vmax=vmax)
        else:
            title = factor + ' (Inferred proportion - UMAP of Z)'
            pl_umap_feature(qz_u, qc_df[factor].values, cmap, title,
                            s=s, vmin=vmin, vmax=vmax)
    else:
        raise ValueError('Invalid Starfysh inference results `{}`, please choose from `qc_m`, `qz_m` & `ql_m`'.format(feature))

    pass


def pl_umap_feature(qz_u, qc, cmap, title, s=3, vmin=0, vmax=None):
    """Single Z-UMAP visualization of Starfysh deconvolutions"""
    fig, axes = plt.subplots(1, 1, figsize=(4, 3), dpi=200)
    g = axes.scatter(
        qz_u[:, 0], qz_u[:, 1],
        cmap=cmap, c=qc, s=s, vmin=vmin, vmax=vmax,
    )
    axes.set_xticks([])
    axes.set_yticks([])
    axes.axis('off')
    fig.title(title)
    fig.colorbar(g, label='Inferred proportions')

    pass


def pl_spatial_inf_gene(
    adata_sample,
    map_info,
    feature,
    idx,
    plt_title,
    label,
    vmin=None,
    vmax=None,
    s=3,
):
    qvar = feature
    color_idx_list = (qvar[:,idx].astype(float))
    all_loc = np.array(map_info.loc[:,['array_col','array_row']])
    fig,axs= plt.subplots(1,1,figsize=(4,3),dpi=200)
    g=axs.scatter(all_loc[:,0],-all_loc[:,1],cmap='magma',c=color_idx_list,s=s,vmin=vmin,vmax=vmax)

    fig.colorbar(g,label=label)
    plt.title(plt_title)
    axs.set_xticks([])
    axs.set_yticks([])
    plt.axis('off')
    
    pass
