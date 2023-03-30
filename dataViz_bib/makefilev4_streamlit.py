import pandas as pd
import geopandas as gpd
import folium
from folium import plugins
import sys
import json
from branca.element import Template, MacroElement
import numpy as np
import sys
import io
from numba import jit, cuda

# # exemple de legende dégradée
# import branca
# colormap = branca.colormap.linear.YlOrRd_09.scale(0, 8500)
# colormap = colormap.to_step(index=[0, 1000, 3000, 5000, 8500])
# colormap.caption = 'Incidents of Crime in Victoria (year ending June 2018)'
# colormap.add_to(m)


def all_vues():
    dico_var={
    'dpe_logtype_baie_mat': {'taxonomie':'materiau','explicative':'1','label':'Baies vitrees - materiaux'}
    ,'dpe_logtype_baie_type_vitrage': {'taxonomie':'materiau','explicative':'1','label':'Baies vitrees - type vitrage'}
    ,'dpe_logtype_baie_u': {'taxonomie':'materiau','explicative':'1','label':'Baies vitrees - conductivite thermique u'}
    , 'dpe_logtype_mur_mat_ext': {'taxonomie':'materiau','explicative':'1','label':'Murs exterieurs - materiaux detail'}
    ,'dpe_logtype_mur_pos_isol_ext': {'taxonomie':'materiau','explicative':'1','label':'Murs exterieurs - type isolation'}
    , 'dpe_logtype_mur_u_ext': {'taxonomie':'materiau','explicative':'1','label':'Murs exterieurs : conductivite thermique u'}
    ,'dpe_logtype_pb_mat': {'taxonomie':'materiau','explicative':'1','label':'Plancher - materiaux detail'}
    , 'dpe_logtype_pb_pos_isol': {'taxonomie':'materiau','explicative':'1','label':'Plancher - type isolation'}
    ,'dpe_logtype_pb_u': {'taxonomie':'materiau','explicative':'1','label':'Plancher : conductivite thermique u'}
    ,'dpe_logtype_prc_s_vitree_ext': {'taxonomie':'materiau','explicative':'1','label':'Baies vitrees - pourcentage surface'}
    ,'dpe_logtype_periode_construction': {'taxonomie':'typologie','explicative':'1','label':'Periode de construction RT - DPE'}
    ,'dpe_logtype_ph_mat': {'taxonomie':'materiau','explicative':'1','label':'Plafond - materiaux detail'}
    ,'dpe_logtype_ph_pos_isol': {'taxonomie':'materiau','explicative':'1','label':'Plafond - type isolation'}
    ,'dpe_logtype_ph_u': {'taxonomie':'materiau','explicative':'1','label':'Plafond : conductivite thermique u'}
    ,'ffo_bat_mat_mur_txt': {'taxonomie':'materiau','explicative':'0','label':'Murs exterieurs - materiaux ffo detail'}
    ,'ffo_bat_mat_toit_txt': {'taxonomie':'materiau','explicative':'1','label':'Toiture - materiaux detail'}
    ,'rnc_ope_periode_construction_max': {'taxonomie':'typologie','explicative':'1','label':'Periode de construction Max'}
    ,'ffo_bat_annee_construction': {'taxonomie':'typologie','explicative':'0','label':'Annee de construction ffo'}
    ,'rnc_ope_l_annee_construction': {'taxonomie':'typologie','explicative':'0','label':'Annee de construction rnc'}
    ,'dpe_logtype_nom_methode_dpe': {'taxonomie':'dpe','explicative':'0','label':'a'}
    ,'dpe_logtype_ch_type_ener_corr': {'taxonomie':'dpe','explicative':'0','label':'Chauffage - energie detail'}
    ,'dpe_logtype_classe_conso_ener': {'taxonomie':'dpe','explicative':'1','label':'DPE - conso'}
    ,'dpe_logtype_classe_estim_ges': {'taxonomie':'dpe','explicative':'1','label':'DPE - ges'}
    , 'dpe_logtype_ecs_type_ener': {'taxonomie':'dpe','explicative':'0','label':'ECS - energie detail'}
    ,'dpe_logtype_inertie': {'taxonomie':'dpe','explicative':'1','label':'DPE - inertie'}
    ,'dpe_conso_ener_std': {'taxonomie':'dpe','explicative':'1','label':'DPE - Conso distribution'}
    ,'dpe_estim_ges_std': {'taxonomie':'dpe','explicative':'1','label':'DPE - GES distribution'}
    ,'dpe_logtype_ch_gen_lib_princ': {'taxonomie':'equipement','explicative':'1','label':'Chauffage - principal detail'}
    ,'dpe_logtype_ch_solaire': {'taxonomie':'equipement','explicative':'1','label':'Chauffage - solaire'}
    ,'dpe_logtype_ch_type_inst': {'taxonomie':'equipement','explicative':'1','label':'Chauffage - type'}
    ,'dpe_logtype_ecs_gen_lib_princ': {'taxonomie':'equipement','explicative':'1','label':'ECS - principal detail'}
    ,'dpe_logtype_ecs_solaire': {'taxonomie':'equipement','explicative':'1','label':'ECS - solaire'}
    ,'dpe_logtype_ecs_type_inst': {'taxonomie':'equipement','explicative':'1','label':'ECS - type'}
    ,'dpe_logtype_presence_balcon': {'taxonomie':'equipement','explicative':'1','label':'balcon - presence'}
    ,'dpe_logtype_presence_climatisation': {'taxonomie':'equipement','explicative':'1','label':'climatisation - presence'}
    ,'dpe_logtype_type_ventilation': {'taxonomie':'equipement','explicative':'1','label':'type de ventilation'}
    ,'dpe_logtype_ratio_ges_conso': {'taxonomie':'dpe','explicative':'-1','label':'a'}
    ,'bdtopo_bat_hauteur_mean': {'taxonomie':'typologie','explicative':'0','label':'Hauteur'}
    ,'hthd_nb_pdl': {'taxonomie':'typologie','explicative':'0','label':'rnc - Nb PDL'}
    ,'rnc_ope_nb_lot_tertiaire': {'taxonomie':'typologie','explicative':'0','label':'rnc - nb lot tertiaire detail'}
    ,'rnc_ope_nb_log': {'taxonomie':'typologie','explicative':'0','label':'rnc - nb logement detail'}
    ,'rnc_ope_nb_lot_tot': {'taxonomie':'typologie','explicative':'0','label':'rnc - nb lots total detail'}
    ,'dle_elec_2020_nb_pdl_res': {'taxonomie':'typologie','explicative':'0','label':'a'}
    ,'dle_gaz_2020_nb_pdl_res': {'taxonomie':'typologie','explicative':'0','label':'a'}
    ,'dle_reseaux_2020_nb_pdl_res': {'taxonomie':'typologie','explicative':'0','label':'a'}
    ,'dle_elec_2020_nb_pdl_pro': {'taxonomie':'typologie','explicative':'0','label':'a'}
    ,'dle_gaz_2020_nb_pdl_pro': {'taxonomie':'typologie','explicative':'0','label':'a'}
    ,'dle_reseaux_2020_nb_pdl_pro': {'taxonomie':'typologie','explicative':'0','label':'a'}
    ,'dle_elec_2020_nb_pdl_tot': {'taxonomie':'typologie','explicative':'0','label':'a'}
    ,'dle_gaz_2020_nb_pdl_tot': {'taxonomie':'typologie','explicative':'0','label':'a'}
    ,'dle_reseaux_2020_nb_pdl_tot': {'taxonomie':'typologie','explicative':'0','label':'a'}
    ,'bpe_l_type_equipement': {'taxonomie':'typologie','explicative':'0','label':'a'}
    ,'bdtopo_bat_l_usage_1': {'taxonomie':'typologie','explicative':'0','label':'a'}
    ,'bdtopo_bat_l_usage_2': {'taxonomie':'typologie','explicative':'0','label':'a'}
    ,'ffo_bat_usage_niveau_1_txt': {'taxonomie':'typologie','explicative':'0','label':'a'}
    ,'rnc_ope_nb_lot_garpark': {'taxonomie':'typologie','explicative':'0','label':'a'}
    ,'hthd_l_type_pdl': {'taxonomie':'typologie','explicative':'0','label':'a'}
    ,'ffo_bat_annee_construction_group': {'taxonomie':'typologie','explicative':'1','label':'Periode de construction - ffo'}
    ,'nb_pdl_res': {'taxonomie':'typologie','explicative':'1','label':'Enedis - nb PDL residentiel'}
    ,'nb_pdl_pro': {'taxonomie':'typologie','explicative':'1','label':'Enedis - nb PDL pro'}
    ,'dle_elec_2020_nb_pdl_tot_group': {'taxonomie':'typologie','explicative':'1','label':'Enedis - nb PDL elec'}
    ,'dle_gaz_2020_nb_pdl_tot_group': {'taxonomie':'typologie','explicative':'1','label':'Enedis - nb PDL gaz'}
    , 'dle_reseaux_2020_nb_pdl_tot_group': {'taxonomie':'typologie','explicative':'1','label':'Enedis - nb PDL reseau de chaleur'}
    ,'bdtopo_bat_usage_1_group': {'taxonomie':'typologie','explicative':'1','label':'Usage 1'}
    ,'bdtopo_bat_usage_2_group': {'taxonomie':'typologie','explicative':'1','label':'Usage 2'}
    ,'bdtopo_bat_hauteur_mean_group': {'taxonomie':'typologie','explicative':'1','label':'Hauteur - classe'}
    ,'hthd_nb_pdl_group': {'taxonomie':'typologie','explicative':'1','label':'hthd - nb PDL total'}
    ,'rnc_ope_nb_lot_tertiaire_group': {'taxonomie':'typologie','explicative':'1','label':'rnc - nb lot tertiaire detail'}
    ,'rnc_ope_nb_log_group': {'taxonomie':'typologie','explicative':'1','label':'rnc - nb logement detail'}
    ,'rnc_ope_nb_lot_tot_group': {'taxonomie':'typologie','explicative':'1','label':'rnc - nb lots total detail'}
    ,'rnc_ope_nb_lot_garpark_group': {'taxonomie':'typologie','explicative':'1','label':'rnc - nb lots stationnement'}
    ,'materiau_mur_ext':{'taxonomie':'materiau','explicative':'1','label':'Murs exterieurs - materiaux'}
    ,'materiau_plafond':{'taxonomie':'materiau','explicative':'1','label':'Plafond - materiaux'}
    ,'materiau_plancher':{'taxonomie':'materiau','explicative':'1','label':'Plancher - materiaux'}
    ,'ecs_type_ener':{'taxonomie':'equipement','explicative':'1','label':'ECS - energie'}
    ,'chauffage_principal':{'taxonomie':'equipement','explicative':'1','label':'Chauffage - principal'}
    ,'materiau_mur':{'taxonomie':'materiau','explicative':'1','label':'Murs exterieurs - materiaux ffo'}
    ,'ecs_principal':{'taxonomie':'equipement','explicative':'1','label':'ECS - principal'}
    ,'chauffage_energie':{'taxonomie':'equipement','explicative':'1','label':'Chauffage - energie'}
    ,'toit_materiau':{'taxonomie':'materiau','explicative':'1','label':'Toiture - materiaux'}
    ,'proportion_pdl_pro': {'taxonomie':'typologie','explicative':'1','label':'Enedis - proportion PDL pro'}
    ,'proportion_lot_tertiaire': {'taxonomie':'typologie','explicative':'1','label':'rnc - proportion lot tertiaire'}
    ,'cluster_12': {'taxonomie':'clustering','explicative':'1','label':'Clustering complet'}
    ,'interpretation_cluster_12': {'taxonomie':'additional','explicative':'1','label':'Clustering interpretation'}
}

    for i in dico_var.items():
        if(i[1]['label']=='a'):
            i[1]['label']=i[0]

    return dico_var


def set_couleurs():
    # couleurs=['red','darkgreen','blue',\
    #     'darkorange','darkkhaki','peru','darkcyan','fuchsia','chartreuse','yellow','silver','grey','black', 'lime','orange','khaki','whitesmoke']    
    couleurs=['red','darkgreen','blue',\
        'darkorange','darkkhaki','peru','darkcyan','fuchsia','chartreuse',\
            'gold','silver','darkgrey','black', 'lime','orange','khaki','whitesmoke']    
    return couleurs

def get_highlight(couleur):
    # style={'orange':'red','green':'darkgreen','yellow':'gold','skyblue':'blue','khaki':'darkkhaki',\
        # 'bisque':'darkorange','linen':'peru','darkcyan':'cyan' }
    # style={'red':'red','darkgreen':'lime','blue':'skyblue',\
    #     'darkorange':'bisque','darkkhaki':'khaki','peru':'linen','darkcyan':'cyan','fuchsia':'orchid','chartreuse':'greenyellow','yellow':'gold','silver':'lightgrey','grey':'darkgrey',\
    #          'black':'grey', 'lime':'darkgreen','orange':'red','khaki':'darkkhaki','whitesmoke':'silver'}
    
    style={'red':'red','darkgreen':'darkgreen','blue':'blue',\
        'darkorange':'darkorange','darkkhaki':'darkkhaki','peru':'peru','darkcyan':'darkcyan','fuchsia':'fuchsia','chartreuse':'chartreuse',\
            'gold':'gold','silver':'silver','darkgrey':'darkgrey','black':'grey', 'lime':'darkgreen','orange':'red','khaki':'darkkhaki','whitesmoke':'silver'}
    return style[couleur]


def tooltip_tableau_html(num_classe,interpret):
    
    colorA = ["#19a7bd","#f2f0d3"]
    colorB = ["#19a7bd","#f2f0d3"]
    colorC=[]

    interpret=interpret.replace("é","e")
    interpret=interpret.split("<br>")
    corps=''
    count=0
    for i in interpret :
        v=i.split("->")
        if(len(v)>1) :
            corps=corps+"""<tr>
            <td style="width: 150px;background-color: """+ colorC[0] +""";"><span style="color: #ffffff;">{}</span></td>""".format(v[0])+"""
            <td style="width: 150px;background-color: """+ colorC[1] +""";">{}</td>""".format(v[1])+"""
            </tr>"""
        elif(len(v)==1 and len(v[0])>1) :
            corps=corps+"""<tr>
            <td style="width: 300px;font-weight : bold">{}</td>""".format(v[0])+"""
            </tr>"""
            if(colorC==colorA): colorC=colorB 
            else: colorC=colorA


    
    
    html = """<!DOCTYPE html>
    <html>
    <head>
    <h4 style="margin-bottom:10"; width="200px">{}</h4>""".format(num_classe)+ """
    </head>
    
    <table style="height: 126px; width: 350px;">
    <tbody>
    {} 
    </tbody>""".format(corps)+ """
    </table>

    </html>
    """

    # with open('C:/Users/FilipeAfonso/Documents/dataViz/data/clustering_desciption.html','a') as f:
    #     f.write('<br>*****************************************************************')
    #     f.write(html)
    #     f.write('<br>*****************************************************************')

    
    return html



def viz_batiment_simplify(vue,bat,couleur,liste_active,display_clustering):

 

    # geo_j = bat.to_json()
    # geo= folium.GeoJson(data=geo_j,style_function=lambda x: {'fillColor': couleur,'color':couleur})

    # geo= folium.GeoJson(data=bat,style_function=lambda x: {'fillColor': couleur,'color':couleur})
    geo= folium.GeoJson(data=bat)

    return geo


def viz_batiment(vue,bat,couleur,liste_active,display_clustering):

    dico_colonnes=all_vues()
    # dico_colonnes=dict(sorted(dico_colonnes.items(), key=lambda item: item[1]))
            # variables = list(dico_colonnes.keys())
            # labels=(list(dico_colonnes.values()))

    variables = [i[0] for i in dico_colonnes.items() if i[1]['explicative']=='1']
    labels=[i[1]['label'] for i in dico_colonnes.items() if i[1]['explicative']=='1']

    var_tooltip=[variables[labels.index(i)] for i in liste_active]


    
    if(display_clustering):
        # mytooltip=folium.features.GeoJsonTooltip(
        #         fields=['interpretation_cluster_12'],
        #         aliases=['Clustering:'],
        #         style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;")
        #         )
          mytooltip=folium.features.Tooltip(tooltip_tableau_html("Profil du cluster : "+str(bat['cluster_12'].iloc[0]),bat['interpretation_cluster_12'].iloc[0]))
    else: 
        mytooltip=folium.features.GeoJsonTooltip(
                fields=var_tooltip,
                aliases=liste_active,
                style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;")
                )



    geo_j = bat.to_json()
    geo_style_function = lambda x: {'color' :  couleur,'opacity' : 0.50,'weight' : 2,}
    geo_highlight_function = lambda x: {'color': get_highlight(couleur), 'opacity' : 0.9,'weight': 4,'dashArray' : '3, 6'}
    # desc_html='aaaaaa'
    # main display function using the two previous functions

    geo = folium.features.GeoJson(
    data=geo_j,
    name = 'geo',
    control = True,
    style_function = geo_style_function, 
    highlight_function = geo_highlight_function,

    # # the tooltip is where the info display happens
    # # using "folium.features.GeoJsonTooltip" function instead of basic text tooltip
    #         # tooltip=folium.features.GeoJsonTooltip(
    #         #     fields=[
    #         #         'bnb_id',
    #         #         vue, 
    #         #     ],
    #         #     # fields=list(bat.columns)[3:5],
    #         #     aliases=[
    #         #         "Identifiant: ",
    #         #         "Filtre: ",
    #         #     ],
    #         #     style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;")
    #         #     )
             tooltip=mytooltip,
    #         # tooltip=folium.map.Tooltip(
    #         #         text=folium.Html(desc_html, script=True, width=300).render(),
    #         # )
    )

    return geo


def marker_proprietaire(bat_du_proprio,geo):

    for _, r in bat_du_proprio.iterrows(): 
        try:
            html=f"""
            <h5>{bat_du_proprio['proprietaire'].iloc[0]}</h5>
            """

            iframe = folium.IFrame(html=html, width=600, height=100)
            popup = folium.Popup(iframe, max_width=600)           
            folium.Marker((r.noyau.y,r.noyau.x), popup=popup,icon=folium.Icon(color='red')).add_to(geo)
        except:
            continue
        
    return geo


def popup_batiment(bat_actif,clients,geo):
    next=0
    for _, r in clients.iterrows(): 
        # folium.Marker((r.noyau.y,r.noyau.x),icon=folium.Icon(color='green')).add_to(geo)
        #  <h5>{'Identifiant Stonal : ' + r['code']+" : "+eval(r['assetData.ADDRESS'])[0].get('value')}</h5>
        try:
            html=f"""
            <h5>{'Identifiant Stonal : ' + r['code']}</h5>
            <h5>{'Nom : ' + r['name']}</h5>
            <h5>{'Adresse : ' +eval(r['assetData.ADDRESS'])[0].get('value')}</h5>
            """
            if(next<len(bat_actif)): 
                html=html+f"""
                <h5> {"identifiant BNB : "+bat_actif['batiment_groupe_id'].iloc[next]}</h5>
                """

            iframe = folium.IFrame(html=html, width=600, height=100)
            popup = folium.Popup(iframe, max_width=600)
            # popup.add_to(geo)

            #folium.Marker((r.noyau.y,r.noyau.x), popup=clients['code'].iloc[next]+","+eval(clients['assetData.ADDRESS'].iloc[next])[0].get('value')),icon=folium.Icon(color='green')).add_to(geo)
            # folium.Marker((r.noyau.y,r.noyau.x), popup=popup,icon=folium.Icon(color='green')).add_to(geo)
            # stonal_icon = folium.features.CustomIcon('C:/Users/FilipeAfonso/Documents/dataViz/dataViz_bib/icon_building.png', icon_size=(30,30))
            # folium.Marker((r.form_LAT,r.form_LNG), popup=popup,icon=stonal_icon).add_to(geo)
            folium.Marker((r.form_LAT,r.form_LNG), popup=popup,icon=folium.Icon(color='green')).add_to(geo)
        except:
            # sys.exit(0)
            continue
        next=next+1
        
    return geo

def popup_batiment_ancien(bat_actif,clients,geo):
    next=0
    for _, r in bat_actif.iterrows(): 
        #folium.Marker((r.noyau.y,r.noyau.x),icon=folium.Icon(color='green')).add_to(geo)
        try:
            html=f"""
            <h5>{'Identifiant Stonal : ' + clients['code'].iloc[next]+" : "+eval(clients['assetData.ADDRESS'].iloc[next])[0].get('value')}</h5>
            <h5> {"identifiant BNB : "+r['batiment_groupe_id']}</h5>
            """
            iframe = folium.IFrame(html=html, width=600, height=100)
            popup = folium.Popup(iframe, max_width=600)
            # popup.add_to(geo)

            #folium.Marker((r.noyau.y,r.noyau.x), popup=clients['code'].iloc[next]+","+eval(clients['assetData.ADDRESS'].iloc[next])[0].get('value')),icon=folium.Icon(color='green')).add_to(geo)
            # folium.Marker((r.noyau.y,r.noyau.x), popup=popup,icon=folium.Icon(color='green')).add_to(geo)
            folium.Marker((r.form_LAT,r.form_LNG), popup=popup,icon=folium.Icon(color='green')).add_to(geo)
        except:
            # sys.exit(0)
            continue
        next=next+1
        
    return geo


def set_legend(vue,legende):
    
    legende=sorted(legende, key=lambda x: (x is None, x))
    couleurs=set_couleurs()
    legend=f'''<body>
    <div id='maplegend' class='maplegend' 
        style='position: absolute; z-index:9999; border:2px solid grey; background-color:rgba(255, 255, 255, 0.8);
        border-radius:6px; padding: 10px; font-size:14px; right: 20px; bottom: 20px;'>
        
    <div class='legend-title'>{vue}</div>
    <div class='legend-scale'>
        <ul class='legend-labels'>
        '''
    
    i=0
    
    for c in legende:
        legend=legend+f'''<li><span style='background:{couleurs[i]};opacity:0.7;'></span>{c}</li>'''
        i=i+1
        if(i>16): i=0
   
    legend=legend+'''
  

        </ul>
    </div>
    </div>
    </body>
    '''





    deb_macro='''{% macro html(this, kwargs) %}
    '''
    fin_macro='''{% endmacro %}'''

    head = '''
    <head>
        <meta charset='utf-8'>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>jQuery UI Draggable - Default functionality</title>
        <link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">

        <script src="https://code.jquery.com/jquery-1.12.4.js"></script>
        <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
        
        <script>
        $( function() {
        $( "#maplegend" ).draggable({
                        start: function (event, ui) {
                            $(this).css({
                                right: "auto",
                                top: "auto",
                                bottom: "auto"
                            });
                        }
                    });
    });

        </script>
    </head>

    '''



    css_options='''
    <style type='text/css'>
        .maplegend .legend-title {
        text-align: left;
        margin-bottom: 5px;
        font-weight: bold;
        font-size: 90%;
        }
        .maplegend .legend-scale ul {
        margin: 0;
        margin-bottom: 5px;
        padding: 0;
        float: left;
        list-style: none;
        }
        .maplegend .legend-scale ul li {
        font-size: 80%;
        list-style: none;
        margin-left: 0;
        line-height: 18px;
        margin-bottom: 2px;
        }
        .maplegend ul.legend-labels li span {
        display: block;
        float: left;
        height: 16px;
        width: 30px;
        margin-right: 5px;
        margin-left: 0;
        border: 1px solid #999;
        }
        .maplegend .legend-source {
        font-size: 80%;
        color: #777;
        clear: both;
        }
        .maplegend a {
        color: #777;
        }
    </style>
    '''



    template = f"""
    {deb_macro}
    <!doctype html>
    <html lang="fr">
    {head}
    {legend}
    </html>
    {css_options}
    {fin_macro} 

    """

    plot_legend = MacroElement()
    plot_legend._template = Template(template)



    return plot_legend




# nouvelle version V3

def union_geometry(gdf,vue,critere):
    polygons = gdf.loc[gdf[vue] == critere]
    polygons = polygons['geometry'].unary_union
    return polygons

def union_geometry(gdf,vue,critere):
    polygons = gdf.loc[gdf[vue] == critere]
    polygons = polygons['geometry'].unary_union
    return polygons

def process_vue(vue, df_reduit,liste_active,display_clustering,feature_group):
    couleurs=set_couleurs()
    i=0
    print(couleurs)
    print(vue)
    print(df_reduit)
    print(df_reduit[vue])
    print(df_reduit[vue].unique())
    for p in sorted(df_reduit[vue].unique()):
        df_p=df_reduit[df_reduit[vue]==p]
        print('b')
        # polygon_union=union_geometry(df_reduit,vue,p)
        # print('bb')
        # # print(polygon_union)
        # d = [[i, p, polygon_union]]
        # df_p = gpd.GeoDataFrame(data=d, columns=['name',vue,'geometry'])

        geo=viz_batiment(vue,df_p,couleurs[i],liste_active,display_clustering)
        i=i+1
        print('c')
        if(i>16): i=0
        geo.add_to(feature_group)
        # geo.add_to(m)
        # m.add_child(geo)
        print('d')
    
    legende=set_legend(vue,df_reduit[vue].unique())
    # m.get_root().add_child(legende)
    # feature_group.get_root().add_child(legende)
    # legende.add_to(feature_group)

    return

def display_proprietaire(vue,df_batiment,liste_active,bat_actif,clients):

    print(vue)
    print(df_batiment)
    print(liste_active)
    

    display_clustering=False
    for i in liste_active: 
        if(str(i).startswith('Clustering')): 
            display_clustering=True
            liste_active=liste_active+['Clustering interpretation']

    yactif=48.866667
    xactif=2.333333

    print(xactif, yactif)
    m = folium.Map(location=(yactif,xactif),min_zoom=0, max_zoom=18, zoom_start=15, tiles='CartoDB positron')

    #les batiments "clients"c'est soit les bâtiments d'un client actif stonal, on peut rentrer nos données sur ce client sous forme de tableau
    #On note qu'alors des bâtiments ne sont pas forcément retrouvés dans la BDNB
    #ou soit les bâtiments d un propriétaire non client de stonal, dans ce cas on a que les données présentes dans la BDNBO
    #on ne fournit alors que le nom du propriétaire sous forme de string à la base df_batiment




    # df_reduit=df_batiment.drop(['noyau'], axis=1)

    #pour l'accès par proprietaire , on ne supprime pas les vides, mais on les remplaces par une modalités 'manquante'
    # df_reduit=df_reduit[df_reduit[['batiment_groupe_id','geometry',vue]].isnull().any(axis=1)==False]
  
    

    # legende=set_legend(all_vues()[vue]['label'],df_batiment[vue].unique())
    # m.get_root().add_child(legende)

    # if(len(liste_active)==1):
    #     legende=set_legend(all_vues()[vue]['label'],df_batiment[vue].unique())
    # else: 
    #     legende=set_legend(all_vues()['cluster_12']['label'],df_batiment['cluster_12'].unique())

    


    print(df_batiment[vue].unique)
    print('a')

    dico_colonnes=all_vues()

    variables = [i[0] for i in dico_colonnes.items() if i[1]['explicative']=='1']
    labels=[i[1]['label'] for i in dico_colonnes.items() if i[1]['explicative']=='1']

    var_tooltip=[variables[labels.index(i)] for i in liste_active]

    df_reduit=df_batiment[var_tooltip+['geometry']]
    df_reduit.replace([None], 'Manquante', inplace=True)
    print(df_reduit[vue].unique)
    # feature_group = folium.FeatureGroup()

    feature_group=[folium.FeatureGroup(name=v,overlay=True) for v in liste_active]
    i=0
    for vue in liste_active:
        print(vue)
        process_vue(variables[labels.index(vue)], df_reduit,liste_active,display_clustering,feature_group[i])
        # feature_group[i].add_child(set_legend(variables[labels.index(vue)],df_batiment[variables[labels.index(vue)]].unique()))
       
        if(type(clients)==str):
            print(type(clients))
            marker_proprietaire(df_batiment[df_batiment['proprietaire']==clients],feature_group[i])
        else :
            feature_group[i]=popup_batiment(bat_actif,clients,feature_group[i])

        m.add_child(feature_group[i])
        i=i+1



    

    # m.add_child(folium.LayerControl())
    folium.LayerControl().add_to(m)
    plugins.Geocoder().add_to(m)

    # m.save('C:/Users/FilipeAfonso/Documents/ESG/map'+str(dept)+'.html')
    # f = io.BytesIO()
    # m.save(f, close_file=False)

    return m